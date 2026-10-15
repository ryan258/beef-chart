"""Direct BCRA USD quotes: real fixture, coverage and denomination boundaries."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import bcra_fx as bcra

ATTEMPT = '2026-10-15T18:00:00Z'
PERIODS = {'2026-08','2026-09'}
PAYLOAD = json.loads((Path(__file__).parent/'fixtures/bcra_usd_2026_08_09.json').read_text())


class BcraMonthlyFx(unittest.TestCase):
    def test_real_usd_quotes_produce_month_specific_means_and_evidence(self):
        rates,evidence=bcra.parse_quotes(PAYLOAD,PERIODS,ATTEMPT)
        self.assertAlmostEqual(rates['2026-09'][1],1513.7727272727273)
        self.assertAlmostEqual(rates['2026-08'][1],1499.925)
        self.assertEqual(rates['2026-09'][0],'2026-09-01')
        self.assertEqual(evidence['2026-09']['quote_count'],22)
        self.assertEqual(evidence['2026-08']['quote_count'],20)
        self.assertEqual(evidence['2026-09']['last_quote_date'],'2026-09-30')
        self.assertEqual(evidence['2026-09']['basis'],bcra.BASIS)
        self.assertIn('not certified',evidence['2026-09']['coverage'])
        self.assertEqual(len(evidence['2026-09']['receipt']['sha256']),64)

    def test_wrong_currency_bad_quotes_and_duplicate_dates_are_rejected(self):
        mutations=[
            lambda p:p['results'][0]['detalle'][0].update(codigoMoneda='EUR'),
            lambda p:p['results'][0]['detalle'][0].update(tipoCotizacion=True),
            lambda p:p['results'][0]['detalle'][0].update(tipoCotizacion=0),
            lambda p:p['results'][0]['detalle'][0].update(tipoCotizacion=float('nan')),
            lambda p:p['results'][0].update(fecha='2026-09-31'),
            lambda p:p['results'][0].update(fecha='2026-10-01'),
            lambda p:p['results'][0].update(fecha=p['results'][1]['fecha']),
            lambda p:p['results'][0].update(detalle=[]),
        ]
        for mutate in mutations:
            payload=copy.deepcopy(PAYLOAD);mutate(payload)
            with self.assertRaises(ValueError):bcra.parse_quotes(payload,PERIODS,ATTEMPT)

    def test_pagination_mismatch_or_limit_hit_cannot_become_a_monthly_mean(self):
        for fields in [{'count':43},{'offset':1},{'limit':42},{'count':True}]:
            payload=copy.deepcopy(PAYLOAD)
            payload['metadata']['resultset'].update(fields)
            with self.assertRaises(ValueError):bcra.parse_quotes(payload,PERIODS,ATTEMPT)
        for metadata in [None,[],{'resultset':None}]:
            payload=copy.deepcopy(PAYLOAD);payload['metadata']=metadata
            with self.assertRaises(ValueError):bcra.parse_quotes(payload,PERIODS,ATTEMPT)

    def test_missing_or_sparse_month_does_not_borrow_another_month(self):
        payload=copy.deepcopy(PAYLOAD)
        payload['results']=[r for r in payload['results'] if r['fecha'].startswith('2026-08')]
        payload['metadata']['resultset']['count']=len(payload['results'])
        rates,_=bcra.parse_quotes(payload,PERIODS,ATTEMPT)
        self.assertEqual(set(rates),{'2026-08'})
        payload['results']=payload['results'][:2]
        payload['metadata']['resultset']['count']=2
        self.assertEqual(bcra.parse_quotes(payload,PERIODS,ATTEMPT),({},{}))

    def test_no_current_month_future_month_or_unbounded_history_query(self):
        for periods in [set(),{'2026-10'},{'2026-11'},{'2023-01','2026-09'},{'2026-02-31'}]:
            with self.assertRaises(ValueError):bcra.quote_url(periods,ATTEMPT)

    def test_fetch_uses_explicit_complete_month_range_once(self):
        with patch.object(bcra,'get_json',return_value=PAYLOAD) as request:
            rates,_=bcra.fetch_monthly_quotes(PERIODS,ATTEMPT)
        self.assertEqual(request.call_count,1)
        url=request.call_args.args[0]
        self.assertIn('/Cotizaciones/USD?',url)
        self.assertIn('fechadesde=2026-08-01',url)
        self.assertIn('fechahasta=2026-09-30',url)
        self.assertEqual(set(rates),PERIODS)


if __name__ == '__main__':
    unittest.main()
