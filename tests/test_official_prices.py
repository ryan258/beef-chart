"""Offline C06 source-failure and atomic-promotion fixtures; network is forbidden."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import official_prices as official
from price_contract import validate_snapshot

ROOT = Path(__file__).resolve().parents[1]
ATTEMPT = '2026-10-12T20:00:00Z'
spec = importlib.util.spec_from_file_location('retail_official_tests', ROOT / 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)


class OfficialIsolation(unittest.TestCase):
    def setUp(self):
        self.original = json.loads((ROOT / 'data/prices.json').read_text())
        self.payloads = {
            official.BLS_URL: {'status': 'REQUEST_SUCCEEDED', 'Results': {'series': [
                {'seriesID': sid, 'data': [{'year': '2026', 'period': 'M07', 'value': '8.50'},
                                         {'year': '2026', 'period': 'M13', 'value': '99'},
                                         {'year': '2026', 'period': 'M09', 'value': '9.25'}]}
                for sid, _ in official.US_SERIES.values()]}},
            official.INDEC_URL: {'data': [['2026-09-01', 20000, 21000, 22000, 23000, 24000],
                                          ['2026-07-01', 18000, 19000, 20000, 21000, 22000]]},
            official.MONTHLY_FX_URL: {'data': [['2026-09-01', 1500], ['2026-07-01', 1400]]},
        }
        # Fail the test if any missing mock accidentally reaches a provider.
        blocker = patch('urllib.request.urlopen', side_effect=AssertionError('Live network forbidden'))
        blocker.start()
        self.addCleanup(blocker.stop)

    def run_refresh(self, staged=None, all_retail_fail=False):
        requested = []

        def source(url, body=None):
            requested.append(url)
            value = self.payloads[url]
            if isinstance(value, Exception):
                raise value
            return copy.deepcopy(value)

        def catalog(fx, cuts):
            return {'lomo': {'label': 'Lomo fixture', 'source': 'Carrefour AR', 'period': '2026-10-12',
                             'ars_kg': 30000, 'usd_lb': 9.01, 'availability': 'in_stock'}} if 'lomo' in cuts else {}

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.json'
            path.write_text(json.dumps(self.original))
            args = ['scraper', '--official']
            if staged is not None:
                stage_path = Path(directory) / 'official.json'
                stage_path.write_text(staged if isinstance(staged, str) else json.dumps(staged))
                args = ['scraper', '--official-snapshot', str(stage_path)]
            with patch.object(official, 'get_json', side_effect=source), \
                 patch.object(retail, 'OUT', path), patch.object(retail.sys, 'argv', args), \
                 patch.object(retail, 'timestamp', return_value=ATTEMPT), \
                 patch.object(retail, 'get', **({'side_effect': OSError('daily FX failure')} if all_retail_fail else {'return_value': b'{"data":[["2026-08-31",1509.4686]]}'})), \
                 patch.object(retail, 'carrefour_prices', side_effect=catalog) as carrefour, \
                 patch.object(retail, 'usda_prices', **({'side_effect': OSError('USDA failure')} if all_retail_fail else {'return_value': {'ribeye_bnls': {'label': 'Ribeye fixture', 'source': 'USDA ad survey', 'period': '2026-10-09', 'usd_lb': 12}}})) as usda, \
                 patch.object(retail, 'write_snapshot', wraps=retail.write_snapshot) as write, patch('builtins.print'):
                issue = None
                try:
                    retail.main()
                except RuntimeError as error:
                    issue = str(error)
                self.assertEqual(write.call_count, 1)
                self.assertEqual(usda.call_count, 1)
                self.assertEqual(carrefour.call_count, 0 if all_retail_fail else len(retail.AR_ITEMS))
            result = json.loads(path.read_text())
        validate_snapshot(result)
        self.assertEqual(result['fetched'], self.original['fetched'])
        if staged is None:
            self.assertCountEqual(requested, [official.BLS_URL, official.MONTHLY_FX_URL, official.INDEC_URL])
        else:
            self.assertEqual(requested, [])
        for key in ('molleja', 'rinon', 'lengua'):
            self.assertIs(result['ar'][key]['unit_scale_unverified'], True)
        return result, issue

    def assert_retained(self, result, region, key, status):
        old = copy.deepcopy(self.original[region][key])
        actual = copy.deepcopy(result[region][key])
        self.assertEqual(actual.pop('observation_status'), status)
        self.assertEqual(actual.pop('last_attempt_at', ATTEMPT), ATTEMPT)
        old.pop('observation_status', None)
        self.assertEqual(actual, old)

    def test_success_matches_monthly_rates_and_retains_previous_observations(self):
        result, issue = self.run_refresh()
        self.assertIsNone(issue)
        for source in ('BLS', 'INDEC', 'FX monthly'):
            self.assertEqual(result['source_status'][source]['status'], 'ok')
        for region, keys in [('us', official.US_SERIES), ('ar', official.AR_SERIES)]:
            for key in keys:
                p = result[region][key]
                self.assertEqual((p['period'], p['prev_period'], p['retrieved_at']), ('2026-09', '2026-07', ATTEMPT))
                self.assertEqual(p['previous_observation'], self.original[region][key])
        ar = result['ar']['ground_beef']
        self.assertAlmostEqual(ar['usd_lb'], 20000 / 1500 / 2.2046226)
        self.assertAlmostEqual(ar['prev_usd_lb'], 18000 / 1400 / 2.2046226)
        self.assertEqual((ar['fx_date'], ar['fx_ars_per_usd']), ('2026-09-01', 1500))
        self.assertEqual(result['fx']['period'], '2026-09')
        self.assertEqual(result['fx']['monthly_retrieved_at'], ATTEMPT)
        self.assertEqual(result['fx']['latest'], self.original['fx']['latest'])

    def test_bls_failure_allows_indec_catalog_and_usda_to_advance(self):
        self.payloads[official.BLS_URL] = TimeoutError('fixture timeout')
        result, issue = self.run_refresh()
        self.assertIn('BLS', issue)
        self.assertEqual(result['source_status']['BLS']['error_type'], 'TimeoutError')
        for key in official.US_SERIES:
            self.assert_retained(result, 'us', key, 'retained_after_error')
        self.assertEqual(result['ar']['ground_beef']['period'], '2026-09')
        self.assertEqual(result['ar']['lomo']['period'], '2026-10-12')
        self.assertEqual(result['us']['ribeye_bnls']['period'], '2026-10-09')

    def test_indec_failure_allows_bls_to_advance(self):
        self.payloads[official.INDEC_URL] = OSError('fixture failure')
        result, issue = self.run_refresh()
        self.assertIn('INDEC', issue)
        for key in official.AR_SERIES:
            self.assert_retained(result, 'ar', key, 'retained_after_error')
        self.assertEqual(result['us']['ground_beef']['period'], '2026-09')

    def test_missing_failed_and_unmatched_fx_keep_native_indec_without_borrowing_rates(self):
        for payload in [OSError('fixture failure'), {'data': []}, {'data': [['2026-07-01', 1400]]}]:
            with self.subTest(payload=payload):
                self.payloads[official.MONTHLY_FX_URL] = payload
                result, issue = self.run_refresh()
                self.assertIn('INDEC', issue)
                self.assertEqual(result['source_status']['INDEC']['status'], 'partial')
                self.assertCountEqual(result['source_status']['INDEC']['native_only'], official.AR_SERIES)
                for key in official.AR_SERIES:
                    p = result['ar'][key]
                    self.assertEqual(p['period'], '2026-09')
                    self.assertGreater(p['ars_kg'], 0)
                    self.assertIsNone(p['usd_lb'])
                    self.assertIsNone(p['fx_ars_per_usd'])
                    self.assertIsNone(p['fx_date'])
                    self.assertEqual(p['fx_provenance'], 'unknown')
                    self.assertEqual(p['previous_observation'], self.original['ar'][key])
                if isinstance(payload, Exception) or not payload['data']:
                    self.assertEqual(result['fx'], self.original['fx'])

    def test_missing_series_keep_original_evidence_and_partial_coverage(self):
        self.payloads[official.BLS_URL]['Results']['series'].pop(1)
        for row in self.payloads[official.INDEC_URL]['data']:
            row[-1] = None
        result, issue = self.run_refresh()
        self.assertIn('BLS', issue)
        self.assertIn('INDEC', issue)
        for source, region, key in [('BLS', 'us', 'ground_chuck'), ('INDEC', 'ar', 'paleta')]:
            state = result['source_status'][source]
            self.assertEqual(state['status'], 'partial')
            self.assertEqual(state['coverage'][key], 'no_match')
            self.assert_retained(result, region, key, 'retained_no_match')

    def test_empty_success_is_distinct_from_error_and_preserves_observations(self):
        self.payloads = {official.BLS_URL: {'status': 'REQUEST_SUCCEEDED', 'Results': {'series': []}},
                         official.INDEC_URL: {'data': []}, official.MONTHLY_FX_URL: {'data': []}}
        result, issue = self.run_refresh()
        for source, region, series in [('BLS', 'us', official.US_SERIES), ('INDEC', 'ar', official.AR_SERIES)]:
            self.assertIn(source, issue)
            self.assertEqual(result['source_status'][source]['status'], 'no_match')
            for key in series:
                self.assert_retained(result, region, key, 'retained_no_match')
        self.assertEqual(result['source_status']['FX monthly']['status'], 'no_match')
        self.assertEqual(result['fx'], self.original['fx'])

    def test_malformed_source_does_not_contaminate_healthy_sources(self):
        original_payloads = copy.deepcopy(self.payloads)
        cases = [('BLS', official.BLS_URL, {'status': 'REQUEST_NOT_PROCESSED'}),
                 ('BLS', official.BLS_URL, {'status': 'REQUEST_SUCCEEDED', 'Results': {'series': None}}),
                 ('INDEC', official.INDEC_URL, {'data': [['2026-09-01', 123]]}),
                 ('INDEC', official.INDEC_URL, {'data': [['2026-02-31', 1, 2, 3, 4, 5]]}),
                 ('INDEC', official.INDEC_URL, {'data': [['2026-09-01', True, 2, 3, 4, 5]]}),
                 ('FX monthly', official.MONTHLY_FX_URL, {'data': [['2026-09-01', -1]]}),
                 ('FX monthly', official.MONTHLY_FX_URL, {'data': [['2026-09-01', float('nan')]]}),
                 ('FX monthly', official.MONTHLY_FX_URL, {'data': [['2027-01-01', 1500]]}),
                 ('FX monthly', official.MONTHLY_FX_URL, {'data': [['2026-09-01', 1500], ['2026-09-01', 1600]]})]
        for source, url, payload in cases:
            with self.subTest(source=source, payload=payload):
                self.payloads = copy.deepcopy(original_payloads)
                self.payloads[url] = payload
                result, issue = self.run_refresh()
                self.assertIn(source, issue)
                self.assertEqual(result['source_status'][source]['status'], 'error')
                self.assertEqual(result['ar']['lomo']['period'], '2026-10-12')
                if source != 'BLS':
                    self.assertEqual(result['us']['ground_beef']['period'], '2026-09')
                if source == 'BLS':
                    self.assert_retained(result, 'us', 'ground_beef', 'retained_after_error')
                if source == 'INDEC':
                    self.assert_retained(result, 'ar', 'ground_beef', 'retained_after_error')
                if source == 'FX monthly':
                    self.assertEqual(result['ar']['ground_beef']['ars_kg'], 20000)
                    self.assertIsNone(result['ar']['ground_beef']['usd_lb'])

    def test_all_failures_preserve_every_original_value_date_and_unit_flag(self):
        self.payloads = {url: OSError('fixture failure') for url in self.payloads}
        result, issue = self.run_refresh(all_retail_fail=True)
        self.assertIsNotNone(issue)
        self.assertEqual(result['fx'], self.original['fx'])
        for region in ('us', 'ar'):
            for key, original in self.original[region].items():
                actual = copy.deepcopy(result[region][key])
                expected = copy.deepcopy(original)
                for p in (actual, expected):
                    p.pop('observation_status', None)
                    p.pop('last_attempt_at', None)
                self.assertEqual(actual, expected)
        for source in ('BLS', 'INDEC', 'FX monthly', 'FX daily', 'USDA ad survey'):
            self.assertEqual(result['source_status'][source]['status'], 'error')

    def test_staged_file_rejects_bad_source_before_merging_and_continues_retail(self):
        ar = official.parse_indec(self.payloads[official.INDEC_URL], {}, ATTEMPT)
        stage = {'us': {'ground_beef': {'source': 'BLS', 'period': '2026-09', 'usd_lb': -2}}, 'ar': ar, 'fx': {}}
        for staged in [stage, '{invalid json']:
            with self.subTest(staged=staged):
                result, issue = self.run_refresh(staged=staged)
                self.assertIn('BLS', issue)
                self.assert_retained(result, 'us', 'ground_beef', 'retained_after_error')
                self.assertEqual(result['ar']['lomo']['period'], '2026-10-12')
                if isinstance(staged, dict):
                    self.assertEqual(result['ar']['ground_beef']['ars_kg'], 20000)

    def test_official_transport_preserves_request_contract_and_isolates_bad_json(self):
        requests = []

        def transport(request, timeout):
            requests.append(request.full_url)
            self.assertEqual(timeout, 20)
            if request.full_url == official.BLS_URL:
                self.assertEqual(request.get_method(), 'POST')
                body = json.loads(request.data)
                self.assertEqual(body['startyear'], '2025')
                self.assertEqual(body['endyear'], '2026')
                self.assertCountEqual(body['seriesid'], [sid for sid, _ in official.US_SERIES.values()])
                return io.BytesIO(b'{invalid json')
            self.assertEqual(request.get_method(), 'GET')
            return io.BytesIO(json.dumps(self.payloads[request.full_url]).encode())

        with patch('urllib.request.urlopen', side_effect=transport):
            stage = official.fetch_official(ATTEMPT)
        self.assertCountEqual(requests, self.payloads)
        self.assertEqual(stage['source_status']['BLS']['error_type'], 'JSONDecodeError')
        self.assertEqual(stage['source_status']['INDEC']['status'], 'ok')
        self.assertEqual(stage['source_status']['FX monthly']['status'], 'ok')
        self.assertAlmostEqual(stage['ar']['ground_beef']['usd_lb'], 20000 / 1500 / 2.2046226)
