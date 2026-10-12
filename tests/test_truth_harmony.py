"""Targeted regression cases for the first correction phase; no live providers."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import re
import unittest
from unittest.mock import patch

from price_contract import qualify_snapshot, validate_snapshot, write_snapshot, merge_records
from official_prices import parse_bls, US_SERIES

spec = importlib.util.spec_from_file_location('retail_phase', Path(__file__).parents[1] / 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)


def offer(name, unit='kg', multiplier=1, species='Vacuna'):
    return {'productName':name,'productId':'x','EC_Sección':['CARNICERIA'],'Especie':[species], 'product_form':'raw',
            'items':[{'itemId':'sku','measurementUnit':unit,'unitMultiplier':multiplier,'sellers':[{'commertialOffer':{'Price':10000,'IsAvailable':True}}]}]}


def snapshot():
    return qualify_snapshot({'us':{},'ar':{'rinon':{'label':'Riñón','source':'Carrefour AR','ars_kg':10000,'usd_lb':4.5,'period':'2026-08-01','availability':'in_stock'}},'fx':{},'fetched':'2026-08-01T00:00:00Z'})


class TruthHarmony(unittest.TestCase):
    def test_uniform_unit_contract_for_all_cuts(self):
        for key, (_, words) in retail.AR_ITEMS.items():
            for unit, multiplier in [('un',0.5),('kg',0.5),('kg',True),(None,1)]:
                with self.subTest(key=key,unit=unit,multiplier=multiplier):
                    self.assertEqual(retail.catalog_matches([offer(words+' x kg',unit,multiplier)],key,words),[])
            self.assertTrue(retail.catalog_matches([offer(words+' x kg')],key,words))

    def test_species_and_prepared_products_fail_closed(self):
        for name, species in [('Lomo cocinado x kg','Vacuna'),('Lomo x kg','Porcina'),('Lomo x kg','unknown'),('Lomo de cabra x kg','Vacuna'),('Molleja de conejo x kg','Vacuna')]:
            key='molleja' if name.startswith('Molleja') else 'lomo'
            self.assertEqual(retail.catalog_matches([offer(name,species=species)],key,retail.AR_ITEMS[key][1]),[])

    def test_no_match_retains_original_observation_and_date(self):
        data=snapshot()
        merge_records(data,'ar','Carrefour AR',{},['rinon'],'2026-10-12T00:00:00Z')
        self.assertEqual(data['ar']['rinon']['period'],'2026-08-01')
        self.assertEqual(data['ar']['rinon']['ars_kg'],10000)
        self.assertEqual(data['ar']['rinon']['observation_status'],'retained_no_match')
        self.assertEqual(data['source_status']['Carrefour AR']['coverage']['rinon'],'no_match')

    def test_new_observation_preserves_one_previous_receipt(self):
        data=snapshot(); newer=copy.deepcopy(data['ar']['rinon']);newer['period']='2026-10-12';newer['ars_kg']=12000
        merge_records(data,'ar','Carrefour AR',{'rinon':newer},['rinon'],'2026-10-12T00:00:00Z')
        self.assertEqual(data['ar']['rinon']['previous_observation']['period'],'2026-08-01')

    def test_invalid_data_never_replaces_good_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'prices.json';path.write_text('original')
            for bad in [0,-1,float('nan'),True]:
                data=snapshot();data['ar']['rinon']['ars_kg']=bad
                with self.assertRaises(ValueError):write_snapshot(path,data)
                self.assertEqual(path.read_text(),'original')

    def test_missing_fx_preserves_native_value(self):
        data=snapshot();data['ar']['rinon']['usd_lb']=None
        validate_snapshot(data)
        self.assertEqual(data['ar']['rinon']['ars_kg'],10000)

    def test_invalid_calendar_or_future_fx_rejected(self):
        for change in [{'period':'2026-02-31'},{'fx_date':'2026-08-02'}]:
            data=snapshot();data['ar']['rinon'].update(change)
            with self.assertRaises(ValueError):validate_snapshot(data)

    def test_prior_only_usda_keeps_actual_prior_interval(self):
        text='Fri Oct 02, 2026\nThis Week: 09/26/2026 - 10/02/2026\nPrior Week: 09/19/2026 - 09/25/2026'
        rows=[('Ribeye Steak, Boneless,',[None,None,100,9,None,None])]
        with patch.object(retail,'get',return_value=b'pdf'),patch.object(retail.subprocess,'run') as run,patch.object(retail,'usda_rows',return_value=rows):
            run.return_value.stdout=text
            record=retail.usda_prices()['ribeye_bnls']
        self.assertEqual(record['period'],'2026-09-25')
        self.assertEqual(record['publication_date'],'2026-10-02')
        self.assertEqual(record['fallback_reason'],'not_advertised_current_interval')
        self.assertEqual(record['adapter_status'],'unresolved_real_layout')

    def test_missing_or_overlapping_usda_intervals_not_guessed(self):
        for text in ['Fri Oct 02, 2026','This Week: 10/01/2026 - 10/07/2026\nPrior Week: 10/01/2026 - 10/03/2026']:
            with self.assertRaises(ValueError):retail.usda_intervals(text)

    def test_numeric_column_collision_classified(self):
        text='Item Environment\n'+' '*40+'Stores Wtd Avg Stores Wtd Avg Stores Wtd Avg\n'+'Ribeye Steak, Boneless, Conventional Fresh 1 2'
        with self.assertRaises(ValueError):list(retail.usda_rows(text))

    def test_cut_failures_do_not_block_healthy_cut_or_change_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'prices.json';path.write_text(json.dumps(snapshot()))
            newer={'lengua':{'label':'Lengua','source':'Carrefour AR','period':'2026-10-12','ars_kg':15000,'usd_lb':5,'availability':'in_stock'}}
            with patch.object(retail,'OUT',path),patch.object(retail.sys,'argv',['scraper','--cuts','rinon','lengua']),patch.object(retail,'get',return_value=b'{"data":[["2026-08-31",1500]]}'),patch.object(retail,'carrefour_prices',side_effect=[OSError('blocked'),newer]):
                with self.assertRaises(RuntimeError):retail.main()
            result=json.loads(path.read_text())
            self.assertEqual(result['ar']['rinon']['period'],'2026-08-01')
            self.assertEqual(result['ar']['rinon']['observation_status'],'retained_after_error')
            self.assertEqual(result['ar']['lengua']['ars_kg'],15000)
            self.assertEqual(result['catalog_attempts']['rinon']['status'],'error')
            self.assertEqual(result['catalog_attempts']['lengua']['status'],'ok')

    def test_bundled_observations_are_qualified_without_refresh(self):
        root=Path(__file__).parents[1];data=json.loads((root/'data/prices.json').read_text());validate_snapshot(data)
        self.assertEqual(data['fetched'],'2026-10-07T19:51:30Z')
        self.assertEqual((len(data['us']),len(data['ar'])),(17,19))
        self.assertEqual(data['ar']['rinon']['availability'],'out_of_stock')
        self.assertEqual(data['fx']['latest']['date'],'2026-08-31')
        self.assertTrue(all('fx_provenance' in p for p in data['ar'].values()))

    def test_bls_period_sorting_skips_m13_and_records_actual_previous(self):
        payload={'status':'REQUEST_SUCCEEDED','Results':{'series':[{'seriesID':US_SERIES['ground_beef'][0],'data':[{'year':'2026','period':'M05','value':'5'},{'year':'2026','period':'M13','value':'99'},{'year':'2026','period':'M08','value':'8'},{'year':'2026','period':'M07','value':'-'}]}]}}
        record=parse_bls(payload,'2026-10-12T00:00:00Z')['ground_beef']
        self.assertEqual(record['period'],'2026-08')
        self.assertEqual(record['prev_period'],'2026-05')
        self.assertEqual(record['prev_usd_lb'],5)

    def test_unknown_or_prepared_form_not_assumed_raw(self):
        for form in [None,'cooked','unknown']:
            p=offer('Lomo x kg');p['product_form']=form
            self.assertEqual(retail.catalog_matches([p],'lomo','lomo'),[])

    def test_invalid_qualification_types_rejected(self):
        data=snapshot();data['ar']['rinon']['fx_provenance']=7
        with self.assertRaises(ValueError):validate_snapshot(data)
        data=snapshot();data['source_status']={'Carrefour AR':None}
        with self.assertRaises(ValueError):validate_snapshot(data)
