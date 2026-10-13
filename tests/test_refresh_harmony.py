"""Retail transport, malformed-batch and aggregate-health regressions; no providers."""
import copy
from http.client import IncompleteRead
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from price_contract import validate_snapshot

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('retail_harmony', ROOT / 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)
ATTEMPT = '2026-10-13T20:00:00Z'


class RefreshHarmony(unittest.TestCase):
    def setUp(self):
        self.original = json.loads((ROOT / 'data/prices.json').read_text())
        blocker = patch('urllib.request.urlopen', side_effect=AssertionError('Live network forbidden'))
        blocker.start()
        self.addCleanup(blocker.stop)

    def catalog(self, fx, keys):
        key = keys[0]
        return {key: {'source':'Carrefour AR', 'label':retail.AR_ITEMS[key][0],
                      'ars_kg':30000, 'usd_lb':round(30000/fx/retail.LB_PER_KG, 2),
                      'period':'2026-10-13', 'availability':'in_stock'}}

    def refresh(self, catalog=None, cuts=None, daily_error=None, usda=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.json'
            path.write_text(json.dumps(self.original))
            args = ['scraper'] + (['--cuts', *cuts] if cuts else [])
            with patch.object(retail, 'OUT', path), patch.object(retail.sys, 'argv', args), \
                 patch.object(retail, 'timestamp', return_value=ATTEMPT), \
                 patch.object(retail, 'get', **({'side_effect':daily_error} if daily_error else {'return_value':b'{"data":[["2026-10-13",1500]]}'})), \
                 patch.object(retail, 'carrefour_prices', side_effect=catalog or self.catalog), \
                 patch.object(retail, 'usda_prices', **({'side_effect':usda} if isinstance(usda, Exception) else {'return_value':usda if usda is not None else {'ribeye_bnls':{'source':'USDA ad survey', 'period':'2026-10-13', 'usd_lb':12}}})), \
                 patch.object(retail, 'write_snapshot', wraps=retail.write_snapshot) as write, patch('builtins.print'):
                issue = None
                try:
                    retail.main()
                except RuntimeError as error:
                    issue = str(error)
                self.assertEqual(write.call_count, 1)
            result = json.loads(path.read_text())
        validate_snapshot(result)
        return result, issue

    def test_incomplete_catalog_response_saves_other_cuts_and_usda(self):
        def catalog(fx, keys):
            if keys == ['lengua']:
                raise IncompleteRead(b'', 10)
            return self.catalog(fx, keys)
        result, issue = self.refresh(catalog)
        self.assertIn('Carrefour lengua', issue)
        self.assertEqual(result['ar']['lomo']['period'], '2026-10-13')
        self.assertEqual(result['us']['ribeye_bnls']['usd_lb'], 12)
        self.assertEqual(result['catalog_attempts']['lengua']['error_type'], 'IncompleteRead')
        self.assertTrue(result['ar']['lengua']['unit_scale_unverified'])
        self.assertEqual(result['ar']['lengua']['period'], self.original['ar']['lengua']['period'])

    def test_incomplete_daily_fx_does_not_block_usda_or_erase_native_evidence(self):
        result, issue = self.refresh(daily_error=IncompleteRead(b'', 10))
        self.assertIn('FX daily', issue)
        self.assertEqual(result['source_status']['FX daily']['error_type'], 'IncompleteRead')
        self.assertEqual(result['source_status']['Carrefour AR']['status'], 'error')
        self.assertEqual(result['us']['ribeye_bnls']['usd_lb'], 12)
        for key, old in self.original['ar'].items():
            self.assertEqual(result['ar'][key]['ars_kg'], old['ars_kg'])
            self.assertEqual(result['ar'][key]['period'], old['period'])

    def test_incomplete_usda_response_preserves_catalog_updates(self):
        result, issue = self.refresh(usda=IncompleteRead(b'', 10))
        self.assertIn('USDA', issue)
        self.assertEqual(result['source_status']['USDA ad survey']['error_type'], 'IncompleteRead')
        self.assertEqual(result['ar']['lomo']['period'], '2026-10-13')
        self.assertEqual(result['us']['ribeye_bnls']['period'], self.original['us']['ribeye_bnls']['period'])

    def test_malformed_catalog_batch_cannot_block_healthy_updates(self):
        for malformed in [None, {'lengua':None}, {'lengua':{'source':'Carrefour AR','ars_kg':0,'period':'2026-10-13'}},
                          {'unexpected':{'source':'Carrefour AR'}}]:
            with self.subTest(malformed=malformed):
                def catalog(fx, keys):
                    return copy.deepcopy(malformed) if keys == ['lengua'] else self.catalog(fx, keys)
                result, issue = self.refresh(catalog, ['lomo', 'lengua'])
                self.assertIn('Carrefour lengua', issue)
                self.assertEqual(result['ar']['lomo']['period'], '2026-10-13')
                self.assertEqual(result['catalog_attempts']['lengua']['status'], 'error')
                self.assertTrue(result['ar']['lengua']['unit_scale_unverified'])

    def test_malformed_usda_batch_is_rejected_before_final_promotion(self):
        result, issue = self.refresh(usda={'ribeye_bnls':{'source':'USDA ad survey','period':'invalid','usd_lb':12}})
        self.assertIn('USDA', issue)
        self.assertEqual(result['ar']['lomo']['period'], '2026-10-13')
        self.assertEqual(result['us']['ribeye_bnls']['period'], self.original['us']['ribeye_bnls']['period'])

    def test_empty_usda_batch_saves_catalog_and_reports_no_match(self):
        result, issue = self.refresh(usda={})
        self.assertIn('USDA: no match', issue)
        self.assertEqual(result['source_status']['USDA ad survey']['status'], 'no_match')
        self.assertEqual(result['ar']['lomo']['period'], '2026-10-13')
        for key in retail.US_ITEMS:
            record = result['us'][key]
            self.assertEqual(record['observation_status'], 'retained_no_match')
            self.assertEqual(record['usd_lb'], self.original['us'][key]['usd_lb'])
            self.assertEqual(record['period'], self.original['us'][key]['period'])

    def test_derived_fx_validation_rejects_only_the_incompatible_cut(self):
        def catalog(fx, keys):
            records = self.catalog(fx, keys)
            if keys == ['lengua']:
                records['lengua']['period'] = '2026-10-07'
            return records
        result, issue = self.refresh(catalog, ['lomo','lengua'])
        self.assertIn('Carrefour lengua', issue)
        self.assertEqual(result['ar']['lomo']['period'], '2026-10-13')
        self.assertEqual(result['catalog_attempts']['lengua']['error_type'], 'ValueError')
        self.assertEqual(result['ar']['lengua']['period'], self.original['ar']['lengua']['period'])
        self.assertTrue(result['ar']['lengua']['unit_scale_unverified'])

    def test_catalog_health_distinguishes_success_empty_partial_and_errors(self):
        cases = [('ok', ['ok','ok']), ('no_match', ['no_match','no_match']),
                 ('partial', ['ok','no_match']), ('error', ['error','error']),
                 ('partial_error', ['ok','error'])]
        for expected, outcomes in cases:
            with self.subTest(expected=expected):
                states = dict(zip(['lomo','lengua'], outcomes))
                def catalog(fx, keys):
                    state = states[keys[0]]
                    if state == 'error': raise OSError('fixture failure')
                    return {} if state == 'no_match' else self.catalog(fx, keys)
                result, issue = self.refresh(catalog, ['lomo','lengua'])
                self.assertEqual(result['source_status']['Carrefour AR']['status'], expected)
                self.assertEqual(result['source_status']['Carrefour AR']['coverage'], states)
                self.assertEqual(issue is None, expected == 'ok')
                if states['lengua'] == 'no_match':
                    self.assertEqual(result['ar']['lengua']['period'], self.original['ar']['lengua']['period'])
                    self.assertTrue(result['ar']['lengua']['unit_scale_unverified'])

    def test_malformed_nested_catalog_entries_are_classified_value_errors(self):
        product = {'productName':'Lengua vacuna cruda x kg','EC_Sección':['CARNICERIA'],
                   'items':[{'measurementUnit':'kg','unitMultiplier':1,
                             'sellers':[{'commertialOffer':{'Price':30000}}]}]}
        malformed = [None, {**product, 'items':None}, {**product, 'items':[None]}]
        for sellers in [None, [None], [{'commertialOffer':None}]]:
            p = copy.deepcopy(product); p['items'][0]['sellers'] = sellers; malformed.append(p)
        for value in malformed:
            with self.subTest(value=value), self.assertRaises(ValueError):
                retail.catalog_matches([value], 'lengua', 'lengua')

    def test_http_response_closes_when_read_fails(self):
        from unittest.mock import MagicMock
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.side_effect = IncompleteRead(b'', 10)
        with patch('urllib.request.urlopen', return_value=response) as transport:
            with self.assertRaises(IncompleteRead): retail.get(retail.FX_URL)
        self.assertEqual(transport.call_args.kwargs['timeout'], 20)
        response.__exit__.assert_called_once()
