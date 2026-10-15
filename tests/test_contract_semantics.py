"""R30–R32: shared offline compatibility/rejection corpus and atomic promotion."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from price_contract import qualify_snapshot, validate_snapshot, write_snapshot

ROOT = Path(__file__).resolve().parents[1]
CORPUS = json.loads((ROOT / 'tests/fixtures/price_contract_v2.json').read_text())


def candidate(case):
    data = copy.deepcopy(case.get('root', CORPUS['base'])) if 'root' in case else copy.deepcopy(CORPUS['base'])
    for path, value in case['set']:
        parent = data
        for key in path[:-1]:
            parent = parent.setdefault(key, {})
        parent[path[-1]] = copy.deepcopy(value)
    for path in case['unset']:
        parent = data
        for key in path[:-1]:
            parent = parent[key]
        parent.pop(path[-1], None)
    kind = case.get('build')
    if kind == 'depth':
        data['extension'] = {}
        node = data['extension']
        for _ in range(14):
            node['next'] = {}
            node = node['next']
    elif kind == 'nodes':
        data['extension'] = [[0] * 100 for _ in range(500)]
    elif kind == 'collection':
        data['extension'] = [0] * 1001
    elif kind == 'text':
        data['extension'] = 'x' * 16385
    elif kind == 'cycle':
        data['extension'] = data
    elif kind == 'unsafe_number':
        data['extension'] = 1e100
    return data


class ContractSemantics(unittest.TestCase):
    def test_shared_semantic_corpus(self):
        for case in CORPUS['cases']:
            with self.subTest(case=case['name']):
                data = candidate(case)
                before = json.dumps(data) if case.get('build') != 'cycle' else None
                if case['accept']:
                    self.assertIs(validate_snapshot(data, as_of=CORPUS['as_of']), data)
                else:
                    with self.assertRaises(ValueError):
                        validate_snapshot(data, as_of=CORPUS['as_of'])
                if before is not None:
                    self.assertEqual(json.dumps(data), before)

    def test_bundled_snapshot_bytes_unknowns_and_flags_unchanged(self):
        path = ROOT / 'tests/fixtures/prices_legacy_2026_10_07.json'
        original = path.read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), CORPUS['bundled_sha256'])
        data = json.loads(original)
        before = copy.deepcopy(data)
        self.assertIs(validate_snapshot(data, as_of=CORPUS['as_of']), data)
        self.assertEqual(data, before)
        self.assertEqual(qualify_snapshot(data), before)
        self.assertTrue(all(p['retrieved_at'] is None for group in ('us', 'ar') for p in data[group].values()))
        self.assertEqual({k for k, p in data['ar'].items() if p.get('unit_scale_unverified')}, {'molleja', 'rinon', 'lengua'})
        self.assertEqual(path.read_bytes(), original)

    def test_invalid_semantics_cannot_replace_last_good_file(self):
        names = {'arbitrary_conversion_rejected', 'reversed_interval', 'previous_bad_native', 'bad_status', 'bad_timestamp_yesterday'}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.json'
            original = (ROOT / 'data/prices.json').read_bytes()
            path.write_bytes(original)
            for case in CORPUS['cases']:
                if case['name'] in names:
                    with self.subTest(case=case['name']), self.assertRaises(ValueError):
                        write_snapshot(path, candidate(case))
                    self.assertEqual(path.read_bytes(), original)
                    self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_metadata_aliases_are_not_mistaken_for_cycles(self):
        data = copy.deepcopy(CORPUS['base'])
        evidence = {'note': 'Shared but not cyclic'}
        data['extension'] = [evidence, evidence]
        validate_snapshot(data, as_of=CORPUS['as_of'])


if __name__ == '__main__':
    unittest.main()
