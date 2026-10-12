"""Independent BLS/INDEC/monthly-FX attempts; no writes or requests on import."""
import copy
import json
import re
import urllib.request
from http.client import HTTPException

from price_contract import merge_records, positive, qualify_snapshot, valid_period, validate_snapshot

US_SERIES = {
    'ground_beef': ('APU0000703112', 'Ground beef, 100% beef'),
    'ground_chuck': ('APU0000703111', 'Ground chuck, 100% beef'),
    'ground_lean': ('APU0000703113', 'Ground beef, lean & extra lean'),
    'round_roast': ('APU0000703311', 'Round roast, USDA Choice, boneless'),
    'round_steak': ('APU0000703511', 'Round steak, USDA Choice, boneless'),
    'sirloin_steak': ('APU0000703613', 'Sirloin steak, USDA Choice, boneless'),
}
AR_SERIES = {
    'ground_beef': ('105.1_I2CPC_2016_M_27', 'Carne picada común'),
    'asado': ('105.1_I2A_2016_M_14', 'Asado'),
    'cuadril': ('105.1_I2C_2016_M_16', 'Cuadril'),
    'nalga': ('105.1_I2N_2016_M_14', 'Nalga'),
    'paleta': ('105.1_I2P_2016_M_15', 'Paleta'),
}
FX_ID = '92.2_TIPO_CAMBIION_0_0_21_24'
BLS_URL = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
SERIES_URL = 'https://apis.datos.gob.ar/series/api/series/'
INDEC_URL = SERIES_URL + '?ids=' + ','.join(sid for sid, _ in AR_SERIES.values()) + '&last=2&format=json'
MONTHLY_FX_URL = SERIES_URL + f'?ids={FX_ID}&collapse=month&collapse_aggregation=avg&last=12&format=json'
SOURCE_ERRORS = (OSError, ValueError, KeyError, IndexError, TypeError, OverflowError, HTTPException)
MONTHLY_FX_FIELDS = ('series', 'ars_per_usd', 'period', 'source', 'basis')


def get_json(url, body=None):
    request = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                     headers={'User-Agent': 'beef-chart price snapshot', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def monthly_rows(payload, columns, attempted_at):
    if not isinstance(payload, dict) or not isinstance(payload.get('data'), list):
        raise ValueError('Missing monthly data rows')
    rows = {}
    for row in payload['data']:
        if not isinstance(row, list) or len(row) != columns + 1 or not valid_period(row[0]):
            raise ValueError('Invalid monthly row shape/date')
        period = row[0][:7]
        if period > attempted_at[:7] or row[0] > attempted_at[:10] or period in rows:
            raise ValueError('Future or duplicate monthly period')
        if any(value is not None and not positive(value) for value in row[1:]):
            raise ValueError('Invalid monthly value')
        rows[period] = row
    return rows


def parse_bls(payload, attempted_at):
    if not isinstance(payload, dict) or payload.get('status') != 'REQUEST_SUCCEEDED':
        raise ValueError('BLS did not report success')
    series = payload['Results']['series']
    if not isinstance(series, list):
        raise ValueError('Invalid BLS series list')
    by_id = {}
    for item in series:
        if not isinstance(item, dict) or not isinstance(item.get('seriesID'), str) or not isinstance(item.get('data'), list):
            raise ValueError('Invalid BLS series')
        if item['seriesID'] in by_id:
            raise ValueError('Duplicate BLS series')
        by_id[item['seriesID']] = item['data']
    records = {}
    for key, (sid, label) in US_SERIES.items():
        values = {}
        for row in by_id.get(sid, []):
            if not isinstance(row, dict):
                raise ValueError('Invalid BLS row')
            if row.get('period') == 'M13':  # Annual observations are not monthly prices.
                continue
            if not isinstance(row.get('period'), str) or not re.fullmatch(r'M(0[1-9]|1[0-2])', row['period']):
                raise ValueError('Invalid BLS month')
            period = f"{row.get('year')}-{row['period'][1:]}"
            if not valid_period(period) or period > attempted_at[:7] or period in values:
                raise ValueError('Invalid/future/duplicate BLS period')
            value = row.get('value')
            if value is None or value == '-':
                continue
            value = float(value) if isinstance(value, str) else value
            if not positive(value):
                raise ValueError('Invalid BLS price')
            values[period] = value
        periods = sorted(values, reverse=True)
        if periods:
            current, previous = periods[0], periods[1] if len(periods) > 1 else None
            records[key] = {'label': label, 'series': sid, 'source': 'BLS', 'period': current,
                            'usd_lb': values[current], 'prev_period': previous,
                            'prev_usd_lb': values[previous] if previous else None}
    return records


def parse_monthly_fx(payload, attempted_at):
    return {period: row for period, row in monthly_rows(payload, 1, attempted_at).items() if row[1] is not None}


def parse_indec(payload, rates, attempted_at):
    rows = monthly_rows(payload, len(AR_SERIES), attempted_at)
    records = {}
    for column, (key, (sid, label)) in enumerate(AR_SERIES.items(), start=1):
        periods = sorted((period for period, row in rows.items() if row[column] is not None), reverse=True)
        if not periods:
            continue
        current, previous = periods[0], periods[1] if len(periods) > 1 else None
        fx_date, rate = rates.get(current, (None, None))
        previous_rate = rates.get(previous, (None, None))[1]
        records[key] = {'label': label, 'series': sid, 'source': 'INDEC', 'period': current,
                        'ars_kg': rows[current][column],
                        'usd_lb': rows[current][column] / rate / 2.2046226 if rate else None,
                        'prev_period': previous,
                        'prev_usd_lb': rows[previous][column] / previous_rate / 2.2046226 if previous_rate else None,
                        'fx_ars_per_usd': rate, 'fx_date': fx_date, 'fx_basis': 'BCRA monthly average',
                        'fx_provenance': 'recorded' if rate else 'unknown'}
    return records


def fetch_official(attempted_at):
    """Stage every source independently; absent FX cannot prevent native INDEC parsing."""
    stage = {'us': {}, 'ar': {}, 'fx': {}, 'source_status': {}}
    rates = {}
    year = int(attempted_at[:4])
    body = {'seriesid': [sid for sid, _ in US_SERIES.values()], 'startyear': str(year - 1), 'endyear': str(year)}
    for source, url, request_body in [('BLS', BLS_URL, body), ('FX monthly', MONTHLY_FX_URL, None), ('INDEC', INDEC_URL, None)]:
        state = {'attempted_at': attempted_at}
        try:
            payload = get_json(url, request_body)
            if source == 'BLS':
                result = stage['us'] = parse_bls(payload, attempted_at)
            elif source == 'FX monthly':
                result = rates = parse_monthly_fx(payload, attempted_at)
                if rates:
                    latest = max(rates)
                    stage['fx'] = {'series': FX_ID, 'ars_per_usd': rates[latest][1], 'period': latest,
                                   'source': 'BCRA via datos.gob.ar (monthly average)',
                                   'basis': 'INDEC conversions use the monthly average matched to each observation month.'}
            else:
                result = stage['ar'] = parse_indec(payload, rates, attempted_at)
            state['status'] = 'ok' if result else 'no_match'
        except SOURCE_ERRORS as error:
            state.update(status='error', error_type=type(error).__name__)
        stage['source_status'][source] = state
    return stage


def merge_official(data, stage, attempted_at):
    """Validate each staged source before mutating the snapshot; return non-success sources."""
    issues = []
    for source, region, series in [('BLS', 'us', US_SERIES), ('INDEC', 'ar', AR_SERIES), ('FX monthly', 'fx', None)]:
        state = {'status': 'error', 'attempted_at': attempted_at}
        try:
            # Missing states support the previous internal --official-snapshot format.
            incoming = stage.get('source_status', {}).get(source, {'status': 'ok'})
            if incoming.get('status') not in ('ok', 'no_match', 'error'):
                raise ValueError('Invalid official source state')
            state.update(incoming, attempted_at=attempted_at)
            if state['status'] == 'error':
                raise ValueError('Official source attempt failed')
            records = copy.deepcopy(stage[region])
            if not isinstance(records, dict):
                raise ValueError('Invalid staged source object')
            if state['status'] == 'no_match' and records:
                raise ValueError('No-match state contains observations')
            if series is None:
                if records:
                    if set(records) - set(MONTHLY_FX_FIELDS) or records.get('series') != FX_ID:
                        raise ValueError('Unexpected monthly FX fields/series')
                    if not positive(records.get('ars_per_usd')) or not valid_period(records.get('period')) or len(records['period']) != 7 or records['period'] > attempted_at[:7]:
                        raise ValueError('Invalid monthly FX observation')
                    if any(not isinstance(records.get(key), str) for key in ('source', 'basis')):
                        raise ValueError('Invalid monthly FX context')
                    data['fx'].update(records, monthly_retrieved_at=attempted_at)
                state['status'] = 'ok' if records else 'no_match'
            else:
                if set(records) - set(series) or any(not isinstance(p, dict) or p.get('source') != source for p in records.values()):
                    raise ValueError('Unexpected official series/source')
                candidate = {'us': {}, 'ar': {}, 'fx': {}}
                candidate[region] = records
                validate_snapshot(qualify_snapshot(candidate))
                if any(p['period'] > attempted_at[:7] for p in records.values()):
                    raise ValueError('Future official observation')
                merge_records(data, region, source, records, list(series), attempted_at)
                state['coverage'] = data['source_status'][source]['coverage']
                missing_fx = [key for key, p in records.items() if region == 'ar' and p.get('usd_lb') is None]
                state['status'] = 'no_match' if not records else 'partial' if len(records) < len(series) or missing_fx else 'ok'
                if missing_fx:
                    state['native_only'] = missing_fx
        except (AttributeError, *SOURCE_ERRORS) as error:
            state.update(status='error', error_type=state.get('error_type', type(error).__name__))
            if series is not None:
                state['coverage'] = {key: 'error' for key in series}
                for key in series:
                    old = data[region].get(key)
                    if old and old.get('source') == source:
                        old.update(observation_status='retained_after_error', last_attempt_at=attempted_at)
        data['source_status'][source] = state
        if state['status'] != 'ok':
            issues.append(source)
    return issues
