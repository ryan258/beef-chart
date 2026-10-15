"""Monthly means of BCRA's published USD quotes, independent of valuation FX."""
import calendar
import hashlib
import json
import statistics
import urllib.parse

from official_prices import get_json
from price_contract import positive, safe_integer, valid_period

USD_URL = 'https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones/USD'
BASIS = 'Monthly arithmetic mean of BCRA published USD quotes'


def quote_url(periods, attempted_at):
    periods = sorted(set(periods))
    if not periods or len(periods) > 24 or any(not valid_period(p) or len(p) != 7 or p >= attempted_at[:7] for p in periods):
        raise ValueError('BCRA FX requires completed observation months')
    first, last = periods[0], periods[-1]
    if (int(last[:4]) - int(first[:4])) * 12 + int(last[5:]) - int(first[5:]) > 23:
        raise ValueError('BCRA FX query exceeds 24 months')
    end = f'{last}-{calendar.monthrange(int(last[:4]), int(last[5:]))[1]:02d}'
    return USD_URL + '?' + urllib.parse.urlencode({
        'fechadesde': first + '-01', 'fechahasta': end, 'limit': 1000, 'offset': 0,
    })


def parse_quotes(payload, periods, attempted_at, url=None):
    url = url or quote_url(periods, attempted_at)
    # Validate the requested range even when an external receipt URL is supplied.
    expected_url = quote_url(periods, attempted_at)
    bounds = urllib.parse.parse_qs(urllib.parse.urlsplit(expected_url).query)
    start, end = bounds['fechadesde'][0], bounds['fechahasta'][0]
    if not isinstance(payload, dict) or payload.get('status') != 200 or not isinstance(payload.get('results'), list):
        raise ValueError('Invalid BCRA USD response')
    metadata = payload.get('metadata')
    if not isinstance(metadata, dict):
        raise ValueError('Missing BCRA pagination metadata')
    resultset = metadata.get('resultset', {})
    if not isinstance(resultset, dict):
        raise ValueError('Missing BCRA pagination metadata')
    count, limit, offset = (resultset.get(k) for k in ('count', 'limit', 'offset'))
    if (not all(safe_integer(v) for v in (count, limit, offset)) or offset != 0 or
            not 1 <= limit <= 1000 or count != len(payload['results']) or not 0 <= count < limit):
        raise ValueError('Incomplete or truncated BCRA USD response')
    days = {}
    for row in payload['results']:
        if not isinstance(row, dict):
            raise ValueError('Invalid BCRA USD row')
        day = row.get('fecha')
        if not valid_period(day) or len(day) != 10 or not start <= day <= end or day in days:
            raise ValueError('Invalid, duplicate or out-of-range BCRA quote date')
        detail = row.get('detalle')
        if (not isinstance(detail, list) or len(detail) != 1 or not isinstance(detail[0], dict)
                or detail[0].get('codigoMoneda') != 'USD' or not positive(detail[0].get('tipoCotizacion'))):
            raise ValueError('Invalid BCRA USD denomination or quote')
        days[day] = detail[0]['tipoCotizacion']
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    receipt = {'url': url, 'sha256': hashlib.sha256(canonical.encode()).hexdigest(),
               'hash_basis': 'Canonical JSON: sorted keys, UTF-8, compact separators'}
    rates, evidence = {}, {}
    for period in sorted(set(periods)):
        quotes = sorted((day, rate) for day, rate in days.items() if day[:7] == period)
        month_end = calendar.monthrange(int(period[:4]), int(period[5:]))[1]
        # Guard against a sparse/interrupted month without inventing a holiday
        # calendar. This is a coverage policy, not certification of every day.
        if len(quotes) < 10 or int(quotes[0][0][-2:]) > 7 or int(quotes[-1][0][-2:]) < month_end - 6:
            continue
        mean = statistics.mean(rate for _, rate in quotes)
        if not positive(mean):
            raise ValueError('Invalid BCRA monthly mean')
        rates[period] = [period + '-01', mean]
        evidence[period] = {
            'source': 'BCRA Estadísticas Cambiarias; USD tipoCotizacion',
            'basis': BASIS, 'period': period, 'ars_per_usd': mean,
            'quote_count': len(quotes), 'first_quote_date': quotes[0][0], 'last_quote_date': quotes[-1][0],
            'query_start': start, 'query_end': end,
            'date_role': 'FX date identifies the monthly period start, not a daily quote',
            'coverage': 'Returned quote days; holiday-calendar completeness not certified',
            'receipt': receipt,
        }
    return rates, evidence


def fetch_monthly_quotes(periods, attempted_at):
    url = quote_url(periods, attempted_at)
    return parse_quotes(get_json(url), periods, attempted_at, url)
