import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import json
import tempfile

spec = importlib.util.spec_from_file_location('scraper', Path(__file__).parents[1] / 'scrape-retail.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def product(name, price=10000, unit='kg', multiplier=1, available=True):
    return {'productId':'1', 'productName':name, 'EC_Sección':['CARNICERIA'], 'link':'https://www.carrefour.com.ar/rinon-x-kg/p',
            'items':[{'itemId':'1','measurementUnit':unit,'unitMultiplier':multiplier,
                      'sellers':[{'commertialOffer':{'Price':price,'IsAvailable':available}}]}]}


class PriceMatching(unittest.TestCase):
    def test_new_names_and_accents(self):
        for key, name in [('bife_costilla','Bife de costilla x kg'),('bife_costilla','Bife angosto con hueso x kg'),
                          ('molleja','Mollejas x kg'),('rinon','Riñón x kg'),('lengua','Lengua x kg')]:
            with self.subTest(name=name):
                self.assertEqual(len(m.catalog_matches([product(name)],key,m.AR_ITEMS[key][1])),1)

    def test_wrong_species_prepared_and_ambiguous_units_rejected(self):
        for key, name in [('molleja','Molleja de pollo x kg'),('lengua','Lengua a la vinagreta x kg'),
                          ('bife_costilla','Bife de costilla con lomo x kg'),('bife_costilla','Bife de costilla sin hueso x kg'),
                          ('molleja','Molleja pancreas x kg'),('rinon','Riñón 500 g'),('lengua','Lenguado x kg')]:
            self.assertEqual(m.catalog_matches([product(name)],key,m.AR_ITEMS[key][1]),[])
        for overrides in [{'unit':'un'},{'multiplier':0.5},{'price':0},{'price':float('nan')}]:
            self.assertEqual(m.catalog_matches([product('Riñón x kg',**overrides)],'rinon','rinon'),[])

    def test_alias_dedup_conversion_and_stock(self):
        items=[product('Mollejas x kg'),{**product('Molleja x kg',price=30000,available=False),'productId':'2'}]
        with patch.object(m,'get',return_value=json.dumps(items).encode()), patch.object(m.time,'sleep'):
            row=m.carrefour_prices(1000,['molleja'])['molleja']
        self.assertEqual(row['products'],1)
        self.assertEqual(row['usd_lb'],round(10000/1000/m.LB_PER_KG,2))
        self.assertEqual(row['availability'],'in_stock')
        self.assertEqual(row['listings'][0]['name'],'Mollejas x kg')

    def test_chorizo_stays_separate(self):
        p=product('Bife de chorizo x kg')
        self.assertEqual(len(m.catalog_matches([p],'bife_angosto','bife de chorizo')),1)
        self.assertEqual(m.catalog_matches([p],'bife_costilla','bife de costilla'),[])

    def test_failed_refresh_preserves_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'prices.json'
            original = '{"us": {}, "ar": {"existing": {"usd_lb": 7}}, "fx": {}}'
            output.write_text(original)
            with patch.object(m, 'OUT', output), patch.object(m.sys, 'argv', ['scraper', '--cuts', 'rinon']), patch.object(m, 'get', side_effect=[b'{"data":[["2026-08-31",1500]]}', OSError('HTTP 403')]):
                with self.assertRaises(OSError): m.main()
            self.assertEqual(output.read_text(), original)

    def test_invalid_fx(self):
        for rate in [None,0,-1,float('nan')]:
            with self.assertRaises(ValueError): m.carrefour_prices(rate,['rinon'])

if __name__ == '__main__': unittest.main()
