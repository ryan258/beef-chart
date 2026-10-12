"""Minimal v2 snapshot contract: native observations, qualifications, and attempts."""
import copy
import json
import math
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def valid_period(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?', value):
        return False
    try:
        datetime.strptime(value, '%Y-%m-%d' if len(value) == 10 else '%Y-%m')
        return True
    except ValueError:
        return False


def qualify_snapshot(data):
    """Add honest legacy qualifiers; never infer a new retrieval or effective date."""
    data = copy.deepcopy(data)
    data['schema_version'] = 2
    data.setdefault('source_status', {})
    data.setdefault('sources', {})
    data.setdefault('fx', {})
    for region in ('us', 'ar'):
        if not isinstance(data.get(region), dict):
            raise ValueError(f'Missing {region} observation object')
        for record in data[region].values():
            if not isinstance(record, dict):
                raise ValueError('Observation must be an object')
            source = record.get('source', 'Unknown')
            record.setdefault('retrieved_at', None)
            record.setdefault('publication_date', None)
            record.setdefault('prev_period', None)
            record.setdefault('provenance_status', 'legacy_unverified')
            record.setdefault('observation_status', 'reference_only' if record.get('availability') == 'out_of_stock' else 'legacy_unverified')
            record.setdefault('market_stage', 'retail')
            record.setdefault('geography', 'Greater Buenos Aires' if source == 'INDEC' else ('United States' if region == 'us' else 'Carrefour Argentina; delivery region unknown'))
            record.setdefault('method', {'BLS':'Monthly consumer-price average', 'INDEC':'Monthly selected-item average', 'USDA ad survey':'Store-weighted advertised features', 'Carrefour AR':'Sampled catalog median'}.get(source, 'Unknown'))
            if source == 'Carrefour AR':
                record.setdefault('availability', 'unknown')
            if region == 'ar':
                record.setdefault('fx_ars_per_usd', None)
                record.setdefault('fx_date', None)
                record.setdefault('fx_basis', 'Unknown')
                record.setdefault('fx_provenance', 'unknown')
    return data


def validate_sampling(record):
    """Optional observation-owned sample evidence; absence never proves coverage."""
    if 'sampling' not in record:
        return
    sample = record['sampling']
    if not isinstance(sample, dict):
        raise ValueError('Invalid sampling object')
    for field in ('per_query_limit', 'eligible_count', 'selected_count', 'unknown_seller_count'):
        value = sample.get(field)
        if type(value) is not int or value < (0 if field == 'unknown_seller_count' else 1):
            raise ValueError('Invalid sampling count')
    if not sample['unknown_seller_count'] <= sample['selected_count'] <= sample['eligible_count'] or type(record.get('products')) is not int or record['products'] != sample['selected_count']:
        raise ValueError('Inconsistent sampling counts')
    queries = sample.get('queries')
    if not isinstance(queries, list) or not queries:
        raise ValueError('Missing sampling queries')
    for query in queries:
        if not isinstance(query, dict) or not isinstance(query.get('query'), str) or not query['query'].strip() or type(query.get('returned_products')) is not int or query['returned_products'] < 0:
            raise ValueError('Invalid sampling query')
    expected = 'possibly_truncated' if any(q['returned_products'] >= sample['per_query_limit'] for q in queries) else 'unknown'
    if sample.get('coverage') != expected:
        raise ValueError('Invalid sampling coverage')
    if sample.get('population') not in ('available_listings', 'out_of_stock_references') or sample.get('seller_policy') != 'first_seller_per_sku':
        raise ValueError('Invalid sampling population or seller policy')
    ids = sample.get('seller_ids')
    if not isinstance(ids, list) or any(not isinstance(s, str) or not s.strip() for s in ids) or len(set(ids)) != len(ids):
        raise ValueError('Invalid sampling seller IDs')
    known = sample['selected_count'] - sample['unknown_seller_count']
    if len(ids) > known or bool(ids) != bool(known):
        raise ValueError('Inconsistent sampling sellers')
    if 'region' not in sample or (sample['region'] is not None and (not isinstance(sample['region'], str) or not sample['region'].strip())):
        raise ValueError('Invalid sampling region')


def validate_snapshot(data):
    if data.get('schema_version') != 2 or not isinstance(data.get('fx'), dict) or not isinstance(data.get('source_status'), dict):
        raise ValueError('Expected v2 snapshot and FX object')
    if data['fx'].get('latest') is not None and not isinstance(data['fx']['latest'], dict):
        raise ValueError('Invalid latest FX object')
    for rate in (data['fx'].get('ars_per_usd'), (data['fx'].get('latest') or {}).get('ars_per_usd')):
        if rate is not None and not positive(rate):
            raise ValueError('Invalid top-level FX rate')
    for state in data['source_status'].values():
        if not isinstance(state, dict) or not isinstance(state.get('status'), str):
            raise ValueError('Invalid source attempt state')
    for region in ('us', 'ar'):
        if not isinstance(data.get(region), dict):
            raise ValueError(f'Missing {region} observations')
        for key, record in data[region].items():
            if not isinstance(record, dict) or not valid_period(record.get('period')):
                raise ValueError(f'{region}/{key}: invalid observation period')
            for field in ('label', 'source', 'method', 'geography', 'provenance_status', 'observation_status', 'availability', 'fx_basis', 'fx_provenance', 'retrieved_at'):
                if record.get(field) is not None and not isinstance(record[field], str):
                    raise ValueError(f'{region}/{key}: invalid text field {field}')
            if 'unit_scale_unverified' in record and not isinstance(record['unit_scale_unverified'], bool):
                raise ValueError(f'{region}/{key}: invalid unit-scale flag')
            validate_sampling(record)
            native = 'ars_kg' if region == 'ar' else 'usd_lb'
            if not positive(record.get(native)):
                raise ValueError(f'{region}/{key}: invalid native price')
            for field in ('usd_lb', 'prev_usd_lb', 'fx_ars_per_usd'):
                if record.get(field) is not None and not positive(record[field]):
                    raise ValueError(f'{region}/{key}: invalid {field}')
            for field in ('fx_date', 'prev_period', 'publication_date'):
                if record.get(field) is not None and not valid_period(record[field]):
                    raise ValueError(f'{region}/{key}: invalid {field}')
            if record.get('fx_date') and (record['fx_date'][:7] > record['period'][:7] or (len(record['period']) == 10 and record['fx_date'] > record['period'])):
                raise ValueError(f'{region}/{key}: future FX date')
    return data


def merge_records(data, region, source, new, keys, attempted_at):
    outcomes = {}
    for key in keys:
        old = data[region].get(key)
        if key in new:
            record = new[key]
            record['retrieved_at'] = attempted_at
            record.setdefault('provenance_status', 'parsed_unverified')
            record.setdefault('observation_status', 'reference_only' if record.get('availability') == 'out_of_stock' else 'observed')
            if old and old != record:
                record['previous_observation'] = {k:v for k,v in old.items() if k != 'previous_observation'}
            data[region][key] = record
            outcomes[key] = record['observation_status']
        else:
            outcomes[key] = 'no_match'
            if old and old.get('source') == source:
                old['observation_status'] = 'retained_no_match'
                old['last_attempt_at'] = attempted_at
    data['source_status'][source] = {'status':'ok' if new else 'no_match', 'attempted_at':attempted_at, 'coverage':outcomes}


def write_snapshot(path, data):
    data = qualify_snapshot(data)
    data['generated_at'] = timestamp()
    validate_snapshot(data)
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, indent=1, ensure_ascii=False, allow_nan=False)
            handle.write('\n')
        temporary.replace(path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
