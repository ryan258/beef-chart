"""Focused organ-price qualification regressions; fixtures never call providers."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from price_contract import merge_records, qualify_snapshot, validate_snapshot, write_snapshot

ROOT = Path(__file__).resolve().parents[1]
ORGANS = ('molleja', 'rinon', 'lengua')
spec = importlib.util.spec_from_file_location('retail_organs', ROOT / 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)


class OrganUnitScale(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'tests/fixtures/prices_legacy_2026_10_07.json').read_text())

    def test_bundled_flags_preserve_original_values_dates_and_listings(self):
        validate_snapshot(self.data)
        flagged = {key for key, p in self.data['ar'].items() if p.get('unit_scale_unverified')}
        self.assertEqual(flagged, set(ORGANS))
        expected = {'molleja': (1830, .55, [1830]), 'rinon': (279.9, .08, [279.9]),
                    'lengua': (1680, .50, [655, 1680, 10900])}
        for key, (native, converted, listings) in expected.items():
            p = self.data['ar'][key]
            self.assertEqual((p['ars_kg'], p['usd_lb']), (native, converted))
            self.assertEqual(p['period'], '2026-10-07')
            self.assertEqual((p['fx_ars_per_usd'], p['fx_date']), (1509.4686, '2026-08-31'))
            self.assertEqual(p['availability'], 'out_of_stock')
            self.assertIsNone(p['retrieved_at'])
            self.assertEqual([r['ars_kg'] for r in p['listings']], listings)
            self.assertTrue(all(not r['available'] and r['sku_id'] and r['url'] for r in p['listings']))
        self.assertEqual(self.data['fetched'], '2026-10-07T19:51:30Z')
        self.assertEqual(qualify_snapshot(self.data), self.data)

    def test_malformed_flag_never_replaces_valid_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.json'
            path.write_text('original')
            for value in [None, 0, 1, 'true', 'false', [], {}]:
                with self.subTest(value=value):
                    data = copy.deepcopy(self.data)
                    data['ar']['rinon']['unit_scale_unverified'] = value
                    with self.assertRaisesRegex(ValueError, 'unit-scale flag'):
                        write_snapshot(path, data)
                    self.assertEqual(path.read_text(), 'original')
            data['ar']['rinon']['unit_scale_unverified'] = False
            validate_snapshot(data)  # Absence/false is not a verification claim.

    def test_empty_and_failed_attempts_keep_unit_flag_and_original_evidence(self):
        for failed in (False, True):
            with self.subTest(failed=failed), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'prices.json'
                path.write_text(json.dumps(self.data))
                with patch.object(retail, 'OUT', path), patch.object(retail.sys, 'argv', ['scraper', '--cuts', *ORGANS]), \
                     patch.object(retail, 'get', return_value=b'{"data":[["2026-08-31",1509.4686]]}'), \
                     patch.object(retail, 'carrefour_prices', **({'side_effect': OSError('fixture failure')} if failed else {'return_value': {}})), \
                     patch('builtins.print'):
                    # Empty matches and failed attempts both save evidence, then exit nonzero.
                    with self.assertRaises(RuntimeError):
                        retail.main()
                result = json.loads(path.read_text())
                for key in ORGANS:
                    expected = copy.deepcopy(self.data['ar'][key])
                    actual = result['ar'][key]
                    self.assertEqual(actual['observation_status'], 'retained_after_error' if failed else 'retained_no_match')
                    actual.pop('last_attempt_at', None)
                    actual.pop('observation_status')
                    expected.pop('observation_status')
                    self.assertEqual(actual, expected)

    def test_new_observation_preserves_flag_on_previous_evidence(self):
        original = copy.deepcopy(self.data['ar']['rinon'])
        newer = {'label': 'Riñón', 'source': 'Carrefour AR', 'period': '2026-10-12',
                 'ars_kg': 10000, 'usd_lb': None, 'availability': 'in_stock'}
        merge_records(self.data, 'ar', 'Carrefour AR', {'rinon': newer}, ['rinon'], '2026-10-12T00:00:00Z')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.json'
            write_snapshot(path, self.data)
            stored = json.loads(path.read_text())['ar']['rinon']
        self.assertEqual(stored['previous_observation'], original)
        self.assertNotIn('unit_scale_unverified', stored)  # Flag is observation-specific.
