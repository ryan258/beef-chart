"""Real IPCVA export fixture, source precedence and preservation regressions; offline."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ipcva_prices as ipcva
import official_prices as official
import bcra_fx as bcra
from price_contract import (enable_ar_sources, merge_records, qualify_snapshot,
                            select_ar_sources, validate_snapshot)

ROOT = Path(__file__).resolve().parents[1]
ATTEMPT = '2026-10-15T18:00:00Z'
HTML = (ROOT / 'tests/fixtures/ipcva_export_2026_09.html').read_text()
BASE = json.loads((ROOT / 'tests/fixtures/prices_before_ipcva.json').read_text())
BCRA = json.loads((ROOT / 'tests/fixtures/bcra_usd_2026_08_09.json').read_text())
spec = importlib.util.spec_from_file_location('ipcva_retail_tests', ROOT / 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)


class IpcvaIntegration(unittest.TestCase):
    def setUp(self):
        self.data = qualify_snapshot(BASE)
        blocker = patch('urllib.request.urlopen', side_effect=AssertionError('Live network forbidden'))
        blocker.start()
        self.addCleanup(blocker.stop)

    def refresh(self, html=HTML, rates=None):
        with patch.object(ipcva, 'get_export', return_value=html):
            return ipcva.refresh_ipcva(self.data, ATTEMPT, rates={} if rates is None else rates)

    def test_real_export_matches_captured_report_and_omits_unsupported_cuts(self):
        records = ipcva.parse_export(HTML, {'2026-09': ['2026-09-01', 1500],
                                           '2026-08': ['2026-08-01', 1400]}, ATTEMPT)
        evidence = json.loads((ROOT / 'research_notes/ipcva-2026-10-15/extracted-prices.json').read_text())
        for key, (_, label) in ipcva.ITEMS.items():
            self.assertEqual(records[key]['ars_kg'], evidence['periods']['2026-09'][label])
        self.assertEqual(len(records), 22)
        self.assertEqual(records['asado']['label'], 'Asado de tira')
        for key in ('molleja','rinon','lengua','entrana','tapa','pecho','aguja','bife_costilla'):
            self.assertNotIn(key, records)
        p = records['lomo']
        self.assertEqual((p['period'], p['prev_period']), ('2026-09','2026-08'))
        self.assertAlmostEqual(p['usd_lb'], 28017 / 1500 / 2.2046226)
        self.assertAlmostEqual(p['prev_usd_lb'], 28712 / 1400 / 2.2046226)
        self.assertIsNone(p['publication_date'])

    def test_priority_preserves_every_carrefour_original_across_revisions_and_failures(self):
        originals = {k: copy.deepcopy(v) for k,v in self.data['ar'].items() if v['source'] == 'Carrefour AR'}
        issues = self.refresh()
        self.assertIn('IPCVA', issues)  # Native-only is a partial refresh.
        self.assertEqual(self.data['ar']['lomo']['source'], 'IPCVA')
        self.assertEqual(self.data['ar']['lomo']['period'], '2026-09')
        self.assertEqual(self.data['carrefour_originals'], originals)
        self.assertEqual(self.data['ar_sources']['Carrefour AR'], originals)
        self.assertEqual(self.data['ar']['entrana'], BASE['ar']['entrana'])
        self.assertEqual(self.data['ar']['molleja']['unit_scale_unverified'], True)
        # Both a newer retailer observation and later monthly revisions leave
        # the immutable original unchanged, while updating their own source.
        retail_record = {k:v for k,v in originals['lomo'].items() if k != 'previous_observation'}
        retail_record.update(period='2026-10-15', ars_kg=30000, usd_lb=None,
                             fx_ars_per_usd=None, fx_date=None, fx_provenance='unknown')
        merge_records(self.data, 'ar', 'Carrefour AR', {'lomo':retail_record}, ['lomo'], ATTEMPT)
        self.assertEqual(self.data['ar']['lomo']['source'], 'IPCVA')
        for value in ('$ 28.018,00', '$ 28.019,00'):
            self.refresh(HTML.replace('$ 28.017,00', value))
        with patch.object(ipcva,'get_export',side_effect=OSError('unavailable')):
            ipcva.refresh_ipcva(self.data, ATTEMPT, rates={})
        self.assertEqual(self.data['ar']['lomo']['ars_kg'], 28019)
        self.assertEqual(self.data['ar']['lomo']['observation_status'], 'retained_after_error')
        self.assertEqual(self.data['carrefour_originals'], originals)
        validate_snapshot(self.data, as_of=ATTEMPT)

    def test_no_match_and_old_response_retain_latest_ipcva_month(self):
        self.refresh()
        old = copy.deepcopy(self.data['ar']['lomo'])
        self.refresh(HTML.replace('$ 28.017,00','S/D'))
        self.assertEqual(self.data['ar']['lomo']['ars_kg'], old['ars_kg'])
        self.assertEqual(self.data['ar']['lomo']['observation_status'], 'retained_no_match')
        records = ipcva.parse_export(HTML, {}, ATTEMPT)
        records['lomo']['period'] = '2026-08'
        records['lomo']['prev_period'] = None
        merge_records(self.data,'ar','IPCVA',{'lomo':records['lomo']},['lomo'],ATTEMPT)
        self.assertEqual(self.data['ar']['lomo']['period'],'2026-09')
        self.assertEqual(self.data['source_status']['IPCVA']['status'],'partial')

    def test_changed_headers_bad_amount_duplicate_and_incomplete_month_fail_closed(self):
        for html in [HTML.replace('Bife Ancho','Unexpected cut'),
                     HTML.replace('$ 28.017,00','$ 28,017.00'),
                     HTML.replace('Sep-26','Oct-26'),
                     HTML.replace('Sep-26','Ago-26'), HTML.replace('</td>','',1), '<html>Unavailable</html>']:
            with self.subTest(html=html[:50]):
                with self.assertRaises(ValueError):
                    ipcva.parse_export(html,{},ATTEMPT)

    def test_failed_monthly_fx_keeps_native_price_without_borrowing_saved_fx(self):
        original_fx = copy.deepcopy(self.data['fx'])
        with patch.object(bcra,'get_json',side_effect=OSError('FX unavailable')), \
             patch.object(ipcva,'get_export',return_value=HTML):
            issues = ipcva.refresh_ipcva(self.data,ATTEMPT)
        self.assertCountEqual(issues,['IPCVA FX','IPCVA'])
        self.assertEqual(self.data['fx'],original_fx)
        self.assertEqual(self.data['ar']['lomo']['ars_kg'],28017)
        self.assertIsNone(self.data['ar']['lomo']['usd_lb'])
        self.assertIsNone(self.data['ar']['lomo']['fx_date'])

    def test_archived_evidence_is_validated_and_monthly_fx_must_match(self):
        self.refresh(rates={'2026-09':['2026-09-01',1500]})
        for field in ('ar_sources','carrefour_originals'):
            bad = copy.deepcopy(self.data)
            record = bad[field]['Carrefour AR']['lomo'] if field == 'ar_sources' else bad[field]['lomo']
            record['period']='2026-02-31'
            with self.assertRaises(ValueError): validate_snapshot(bad,as_of=ATTEMPT)
        self.data['ar']['lomo']['fx_date']='2026-08-01'
        with self.assertRaisesRegex(ValueError,'Monthly FX month'):
            validate_snapshot(self.data,as_of=ATTEMPT)

    def test_ipcva_only_command_writes_once_and_does_not_request_retail(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prices.json'
            path.write_text(json.dumps(BASE))
            with patch.object(retail,'OUT',path), patch.object(retail.sys,'argv',['scraper','--ipcva-only']), \
                 patch.object(retail,'timestamp',return_value=ATTEMPT), \
                 patch.object(ipcva,'get_export',return_value=HTML), \
                 patch.object(bcra,'get_json',return_value=BCRA), \
                 patch.object(retail,'carrefour_prices',side_effect=AssertionError('No retailer request')), \
                 patch.object(retail,'usda_prices',side_effect=AssertionError('No USDA request')), \
                 patch.object(retail,'write_snapshot',wraps=retail.write_snapshot) as write, patch('builtins.print'):
                retail.main()
                self.assertEqual(write.call_count,1)
            result=json.loads(path.read_text())
        self.assertEqual(result['us'],BASE['us'])
        self.assertEqual(result['ar']['lomo']['source'],'IPCVA')
        self.assertEqual(result['source_status']['IPCVA']['status'],'ok')
        self.assertEqual(result['source_status']['IPCVA FX']['status'],'ok')
        self.assertEqual(result['ar']['lomo']['fx_basis'],bcra.BASIS)
        self.assertEqual(result['ar']['lomo']['fx_evidence']['quote_count'],22)
        self.assertEqual(result['fx'],BASE['fx'])
        self.assertEqual(result['carrefour_originals']['lomo'],BASE['ar']['lomo'])
        validate_snapshot(result)

    def test_official_failure_changes_only_its_source_records(self):
        self.refresh()
        ipcva_lomo=copy.deepcopy(self.data['ar']['lomo'])
        issues=official.merge_official(self.data,None,ATTEMPT)
        self.assertIn('INDEC',issues)
        self.assertEqual(self.data['ar']['lomo'],ipcva_lomo)
        self.assertEqual(self.data['ar_sources']['INDEC']['ground_beef']['observation_status'],'retained_after_error')
        self.assertEqual(self.data['ar']['ground_beef']['source'],'IPCVA')

    def test_ipcva_only_partial_exit_explains_native_only_and_saves_prices(self):
        august = copy.deepcopy(BCRA)
        august['results'] = [r for r in august['results'] if r['fecha'].startswith('2026-08')]
        august['metadata']['resultset']['count'] = len(august['results'])
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prices.json'
            path.write_text(json.dumps(BASE))
            with patch.object(retail,'OUT',path), patch.object(retail.sys,'argv',['scraper','--ipcva-only']), \
                 patch.object(retail,'timestamp',return_value=ATTEMPT), \
                 patch.object(ipcva,'get_export',return_value=HTML), \
                 patch.object(bcra,'get_json',return_value=august), \
                 patch('builtins.print') as output:
                with self.assertRaisesRegex(SystemExit,'Partial refresh: IPCVA FX, IPCVA'):
                    retail.main()
                self.assertTrue(any('native ARS/kg saved' in str(call) for call in output.call_args_list))
            result=json.loads(path.read_text())
        self.assertEqual(result['ar']['lomo']['ars_kg'],28017)
        self.assertIsNone(result['ar']['lomo']['usd_lb'])

    def test_full_refresh_catalog_errors_do_not_mark_primary_ipcva_failed(self):
        payloads = {
            official.BLS_URL: {'status':'REQUEST_SUCCEEDED','Results':{'series':[]}},
            official.MONTHLY_FX_URL: {'data':[['2026-09-01',1500],['2026-08-01',1400]]},
            official.INDEC_URL: {'data':[['2026-09-01',20000,21000,22000,23000,24000]]},
        }
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prices.json'
            path.write_text(json.dumps(BASE))
            with patch.object(retail,'OUT',path), patch.object(retail.sys,'argv',['scraper','--official']), \
                 patch.object(retail,'timestamp',return_value=ATTEMPT), \
                 patch.object(official,'get_json',side_effect=lambda url,body=None:copy.deepcopy(payloads[url])), \
                 patch.object(bcra,'get_json',return_value=BCRA), \
                 patch.object(ipcva,'get_export',return_value=HTML), \
                 patch.object(retail,'get',return_value=b'{"data":[["2026-10-15",1500]]}'), \
                 patch.object(retail,'carrefour_prices',side_effect=OSError('blocked')), \
                 patch.object(retail,'usda_prices',return_value={}), patch('builtins.print'):
                with self.assertRaises(RuntimeError): retail.main()
            result=json.loads(path.read_text())
        self.assertEqual(result['source_status']['IPCVA']['status'],'ok')
        self.assertEqual(result['source_status']['Carrefour AR']['status'],'error')
        self.assertEqual(result['ar']['lomo']['observation_status'],'observed')
        self.assertEqual(result['ar_sources']['Carrefour AR']['lomo']['observation_status'],'retained_after_error')
        self.assertEqual(result['carrefour_originals']['lomo'],BASE['ar']['lomo'])
        self.assertEqual(result['ar']['ground_beef']['source'],'IPCVA')
        validate_snapshot(result)


if __name__ == '__main__':
    unittest.main()
