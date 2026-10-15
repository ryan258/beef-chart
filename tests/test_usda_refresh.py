"""Real USDA PDF acceptance and transport isolation, without live providers."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from price_contract import qualify_snapshot, validate_snapshot

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('retail_usda_tests',ROOT/'scrape-retail.py')
retail=importlib.util.module_from_spec(spec);spec.loader.exec_module(retail)
PDF=(ROOT/'tests/fixtures/usda_3228_2026_10_09.pdf').read_bytes()
TEXT=(ROOT/'tests/fixtures/usda_3228_2026_10_09.txt').read_text()
BASE=json.loads((ROOT/'tests/fixtures/prices_before_ipcva.json').read_text())
ATTEMPT='2026-10-09T20:00:00Z'


class UsdaRefresh(unittest.TestCase):
    def setUp(self):
        blocker=patch('urllib.request.urlopen',side_effect=AssertionError('Live requests forbidden'))
        blocker.start();self.addCleanup(blocker.stop)

    def parsed(self,text=TEXT):
        with patch.object(retail,'get',return_value=PDF) as request, \
             patch.object(retail.subprocess,'run') as extract:
            extract.return_value.stdout=text
            records=retail.usda_prices()
            self.assertEqual(request.call_args_list, [unittest.mock.call(retail.USDA_PDF)])
        return records

    def test_real_national_rows_have_expected_weights_and_no_regional_contamination(self):
        # Store/price pairs transcribed from national pages 1–4 of the fixture.
        pairs={
            'ribeye_bnls':[(2258,19.27),(18,14.98)],
            'strip_bnls':[(2257,13.73),(1988,12.12)],
            'tenderloin':[(200,18.57)],'brisket_whole':[(470,4.86)],
            'chuck_roast':[(4019,7.64),(127,6.73)],'short_ribs':[(364,9.62),(80,7.76)],
            'skirt':[(151,12.17),(75,9.99)],'flank':[(36,12.10),(15,12.99)],
            'tri_tip':[(737,8.37),(155,7.38),(408,9.60),(182,7.99)],
            'eye_round':[(693,7.01),(74,5.99)],'bottom_round':[(2831,6.66),(154,5.66)],
        }
        records=self.parsed()
        self.assertEqual(set(records),set(retail.US_ITEMS))
        for key,points in pairs.items():
            total=sum(s for s,_ in points)
            self.assertEqual(records[key]['stores'],total,key)
            self.assertEqual(records[key]['usd_lb'],round(sum(s*p for s,p in points)/total,2),key)
            self.assertEqual(records[key]['geography'],'United States')

    def test_printed_ending_window_avoids_release_page_and_does_not_invent_prior_dates(self):
        records=self.parsed()
        for record in records.values():
            self.assertEqual((record['effective_start'],record['effective_end']),('2026-10-03','2026-10-15'))
            self.assertEqual(record['publication_date'],'2026-10-09')
            self.assertEqual(record['interval_basis'],retail.USDA_END_WINDOW)
            self.assertIsNone(record['prev_period'])
            self.assertIsNone(record['prev_usd_lb'])
        # Validate as of publication, when the printed ending window is ahead.
        validate_snapshot(qualify_snapshot({'us':records,'ar':{},'fx':{}}),as_of=ATTEMPT)

    @unittest.skipUnless(shutil.which('pdftotext'),'pdftotext required for PDF extraction')
    def test_actual_pdf_extracts_and_parses_with_one_http_resource(self):
        with patch.object(retail,'get',return_value=PDF) as request:
            records=retail.usda_prices()
        self.assertEqual(request.call_count,1)
        self.assertEqual(records['ribeye_bnls']['usd_lb'],19.24)
        self.assertEqual(len(records),11)

    def test_reversed_pdf_window_fails_without_fetching_metadata(self):
        with self.assertRaisesRegex(ValueError,'Reversed USDA'):
            self.parsed(TEXT.replace('10/3/2026 to 10/15/2026','10/20/2026 to 10/15/2026'))

    def test_missing_national_identity_or_cw_columns_fails_closed(self):
        for text in [TEXT.replace('NATIONAL','MISSING NATIONAL HEADING'),
                     TEXT.replace('CW','PW')]:
            with self.assertRaisesRegex(ValueError,'national CW/PW/PY'):
                self.parsed(text)

    def test_pdf_download_timeout_records_the_step_and_preserves_original_values(self):
        data=qualify_snapshot(BASE)
        with patch.object(retail,'get',side_effect=TimeoutError('read timed out')):
            issues=retail.refresh_usda(data,ATTEMPT)
        self.assertIn('PDF download',issues[0])
        state=data['source_status']['USDA ad survey']
        self.assertEqual((state['error_type'],state['step']),('TimeoutError','PDF download'))
        for key,old in BASE['us'].items():
            self.assertEqual(data['us'][key]['usd_lb'],old['usd_lb'])
            self.assertEqual(data['us'][key]['period'],old['period'])
        self.assertEqual(data['ar'],BASE['ar'])

    def test_legacy_missing_interval_fallback_identifies_release_page_timeout(self):
        data=qualify_snapshot(BASE)
        text=TEXT.replace('ending during the period of 10/3/2026 to 10/15/2026','ending-date window omitted')
        with patch.object(retail,'get',side_effect=[PDF,TimeoutError('read timed out')]), \
             patch.object(retail.subprocess,'run') as extract:
            extract.return_value.stdout=text
            retail.refresh_usda(data,ATTEMPT)
        self.assertEqual(data['source_status']['USDA ad survey']['step'],'Release-date page')
        self.assertEqual(data['source_status']['USDA ad survey']['error_type'],'TimeoutError')

    def test_pdf_extraction_timeout_is_distinct_from_an_http_timeout(self):
        data=qualify_snapshot(BASE)
        with patch.object(retail,'get',return_value=PDF), \
             patch.object(retail.subprocess,'run',side_effect=subprocess.TimeoutExpired('pdftotext',20)):
            retail.refresh_usda(data,ATTEMPT)
        state=data['source_status']['USDA ad survey']
        self.assertEqual(state['step'],'PDF text extraction')
        self.assertEqual(state['error_type'],'TimeoutExpired')

    def test_usda_only_command_preserves_other_sources_and_previous_usda_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prices.json';path.write_text(json.dumps(BASE))
            with patch.object(retail,'OUT',path), patch.object(retail.sys,'argv',['scraper','--usda-only']), \
                 patch.object(retail,'timestamp',return_value=ATTEMPT), \
                 patch.object(retail,'get',return_value=PDF) as request, \
                 patch.object(retail.subprocess,'run') as extract, patch('builtins.print'):
                extract.return_value.stdout=TEXT
                retail.main()
            result=json.loads(path.read_text())
        self.assertEqual(request.call_args_list,[unittest.mock.call(retail.USDA_PDF)])
        self.assertEqual(result['ar'],BASE['ar'])
        self.assertEqual(result['fx'],BASE['fx'])
        self.assertEqual(result['source_status']['USDA ad survey']['status'],'ok')
        for key,old in BASE['us'].items():
            if old['source']=='BLS':self.assertEqual(result['us'][key],old)
            else:
                self.assertEqual(result['us'][key]['period'],'2026-10-15')
                self.assertEqual(result['us'][key]['previous_observation'],{k:v for k,v in old.items() if k!='previous_observation'})
        validate_snapshot(result,as_of=ATTEMPT)


if __name__ == '__main__':
    unittest.main()
