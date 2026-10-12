"""C14 offline sampling evidence regressions; no provider requests permitted."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from price_contract import merge_records, qualify_snapshot, validate_snapshot, write_snapshot
from test_retail_prices import m, product

ROOT = Path(__file__).resolve().parents[1]


class CatalogSampling(unittest.TestCase):
    def setUp(self):
        self.network = patch('urllib.request.urlopen', side_effect=AssertionError('Live request forbidden'))
        self.network.start()
        self.addCleanup(self.network.stop)
        self.data = json.loads((ROOT / 'data/prices.json').read_text())

    def fetch(self, responses, key='molleja'):
        with patch.object(m, 'get', side_effect=[json.dumps(p).encode() for p in responses]), patch.object(m.time, 'sleep'):
            return m.carrefour_prices(1000, [key])[key]

    def test_counts_describe_alias_dedup_and_available_population(self):
        available = product('Mollejas x kg')
        available['items'][0]['sellers'][0]['sellerId'] = 'seller-1'
        unavailable = {**product('Molleja x kg', price=30000, available=False), 'productId': '2'}
        rejected = product('Molleja de pollo x kg')
        response = [available, unavailable, rejected]
        row = self.fetch([response, response])
        sample = row['sampling']
        self.assertEqual(sample['queries'], [{'query': 'molleja', 'returned_products': 3}, {'query': 'mollejas', 'returned_products': 3}])
        self.assertEqual((sample['eligible_count'], sample['selected_count'], row['products']), (2, 1, 1))
        self.assertEqual(sample['population'], 'available_listings')
        self.assertEqual(sample['seller_ids'], ['seller-1'])
        self.assertEqual(sample['unknown_seller_count'], 0)
        self.assertEqual(sample['coverage'], 'unknown')
        self.assertIsNone(sample['region'])
        self.assertEqual(row['ars_kg'], 10000)
        self.assertEqual(row['usd_lb'], round(10000 / 1000 / m.LB_PER_KG, 2))
        self.data['ar']['molleja'] = row
        validate_snapshot(self.data)

    def test_limit_hit_is_possible_truncation_and_short_page_is_unknown(self):
        for size in (19, 20, 21):
            with self.subTest(size=size):
                items = [{**product('Lengua x kg'), 'productId': str(i)} for i in range(size)]
                # First seller remains the selection rule; the second offer must not enter the median.
                items[0]['items'][0]['sellers'].append({'sellerId': 'not-sampled', 'commertialOffer': {'Price': 1, 'IsAvailable': True}})
                row = self.fetch([items], 'lengua')
                s = row['sampling']
                self.assertEqual(s['coverage'], 'possibly_truncated' if size >= 20 else 'unknown')
                self.assertEqual(s['per_query_limit'], 20)
                self.assertEqual(s['selected_count'], size)
                self.assertEqual(s['unknown_seller_count'], size)
                self.assertEqual(s['seller_ids'], [])
                self.assertEqual(s['seller_policy'], 'first_seller_per_sku')
                self.assertEqual(row['ars_kg'], 10000)

    def test_empty_alias_and_out_of_stock_only_median(self):
        items = [{**product('Mollejas x kg', price=price, available=False), 'productId': str(i)} for i, price in enumerate((10000, 20000))]
        items[0]['items'][0]['sellers'][0]['sellerId'] = 'known'
        row = self.fetch([[], items])
        self.assertEqual(row['sampling']['queries'][0]['returned_products'], 0)
        self.assertEqual(row['sampling']['population'], 'out_of_stock_references')
        self.assertEqual(row['sampling']['selected_count'], 2)
        self.assertEqual(row['sampling']['seller_ids'], ['known'])
        self.assertEqual(row['sampling']['unknown_seller_count'], 1)
        self.assertEqual(row['availability'], 'out_of_stock')
        self.assertEqual(row['ars_kg'], 15000)

    def test_malformed_sampling_cannot_replace_file(self):
        row = self.fetch([[product('Lengua x kg')]], 'lengua')
        cases = [('selected_count', True), ('eligible_count', 0), ('selected_count', 2), ('per_query_limit', 0),
                 ('queries', []), ('queries', [{'query': 'lengua', 'returned_products': -1}]),
                 ('coverage', 'complete'), ('coverage', 'possibly_truncated'), ('population', 'all_products'),
                 ('seller_policy', 'all_sellers'), ('seller_ids', ['invented']), ('region', []), ('unknown_seller_count', 2)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.json'
            path.write_text('original')
            for field, value in cases:
                with self.subTest(field=field, value=value):
                    bad = copy.deepcopy(row)
                    bad['sampling'][field] = value
                    self.data['ar']['lengua'] = bad
                    with self.assertRaisesRegex(ValueError, 'sampling'):
                        write_snapshot(path, self.data)
                    self.assertEqual(path.read_text(), 'original')
            for value in (None, [], 'sample'):
                self.data['ar']['lengua'] = {**row, 'sampling': value}
                with self.assertRaisesRegex(ValueError, 'sampling'):
                    validate_snapshot(self.data)

    def test_failed_empty_and_replacement_preserve_observation_owned_evidence(self):
        row = self.fetch([[product('Lengua x kg', available=False)]], 'lengua')
        row['unit_scale_unverified'] = True
        self.data['ar']['lengua'] = row
        original = qualify_snapshot(self.data)['ar']['lengua']
        for failed in (False, True):
            with self.subTest(failed=failed), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'prices.json'
                path.write_text(json.dumps(self.data))
                with patch.object(m, 'OUT', path), patch.object(m.sys, 'argv', ['scraper', '--cuts', 'lengua']), \
                     patch.object(m, 'get', side_effect=[b'{"data":[["2026-08-31",1500]]}', OSError('fixture') if failed else b'[]']), \
                     patch.object(m.time, 'sleep'), patch('builtins.print'):
                    if failed:
                        with self.assertRaises(RuntimeError):
                            m.main()
                    else:
                        m.main()
                retained = json.loads(path.read_text())['ar']['lengua']
                expected = {**original, 'observation_status': 'retained_after_error' if failed else 'retained_no_match'}
                retained.pop('last_attempt_at', None)
                self.assertEqual(retained, expected)
        data = qualify_snapshot(self.data)
        newer = self.fetch([[product('Lengua x kg', price=25000)]], 'lengua')
        merge_records(data, 'ar', 'Carrefour AR', {'lengua': newer}, ['lengua'], '2026-10-12T00:00:00Z')
        self.assertEqual(data['ar']['lengua']['previous_observation'], original)
        validate_snapshot(data)

    def test_legacy_records_remain_unchanged_without_invented_sampling(self):
        before = copy.deepcopy(self.data)
        validate_snapshot(self.data)
        self.assertEqual(qualify_snapshot(self.data), before)
        self.assertEqual(self.data, before)
        self.assertTrue(all('sampling' not in p for p in self.data['ar'].values()))


if __name__ == '__main__':
    unittest.main()
