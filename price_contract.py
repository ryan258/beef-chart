"""Minimal v2 snapshot contract: native observations, qualifications, and attempts."""
import copy
import json
import math
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# v2 semantic rules: optional/null legacy evidence stays unknown, never inferred.
ATTEMPT_STATUSES = ('legacy_unverified', 'unknown', 'not_attempted', 'ok', 'no_match', 'partial', 'error', 'partial_error')
EVIDENCE_STATUSES = {
    'provenance_status': ('legacy_unverified', 'parsed_unverified', 'unknown'),
    'observation_status': ('legacy_unverified', 'observed', 'reference_only', 'unverified_layout', 'retained_no_match', 'retained_after_error', 'unknown'),
    'availability': ('unknown', 'in_stock', 'out_of_stock'),
    'fx_provenance': ('unknown', 'recorded', 'inferred_from_legacy_snapshot'),
    'adapter_status': ('unknown', 'unresolved_real_layout'),
    'effective_period_status': ('unknown', 'unverified_report_date'),
}


def safe_integer(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and abs(value) <= 9007199254740991 and int(value) == value


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def valid_period(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}(?:-[0-9]{2})?', value):
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
        if not safe_integer(value) or value < (0 if field == 'unknown_seller_count' else 1):
            raise ValueError('Invalid sampling count')
    if not sample['unknown_seller_count'] <= sample['selected_count'] <= sample['eligible_count'] or not safe_integer(record.get('products')) or record['products'] != sample['selected_count']:
        raise ValueError('Inconsistent sampling counts')
    queries = sample.get('queries')
    if not isinstance(queries, list) or not queries:
        raise ValueError('Missing sampling queries')
    for query in queries:
        if not isinstance(query, dict) or not isinstance(query.get('query'), str) or not query['query'].strip() or not safe_integer(query.get('returned_products')) or query['returned_products'] < 0:
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


def valid_timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]{1,6})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])', value):
        return False
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
        return True
    except (ValueError, OverflowError):
        return False


def timestamp_day(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).date().isoformat()


def validate_json_tree(data):
    """Bound all retained metadata, including extensions; permit shared noncyclic values."""
    ancestors = set()
    nodes = 0

    def visit(value, depth):
        nonlocal nodes
        nodes += 1
        if depth > 12 or nodes > 50000:
            raise ValueError('Evidence metadata limit exceeded')
        if value is None or isinstance(value, bool):
            return
        if isinstance(value, str):
            if len(value) > 16384:
                raise ValueError('Evidence text limit exceeded')
            return
        if isinstance(value, (int, float)):
            if (isinstance(value, int) and abs(value) > 9007199254740991) or not math.isfinite(value) or (value == int(value) and abs(value) > 9007199254740991):
                raise ValueError('Invalid JSON evidence number')
            return
        if not isinstance(value, (dict, list)) or id(value) in ancestors:
            raise ValueError('Invalid or cyclic evidence metadata')
        if len(value) > 1000:
            raise ValueError('Evidence collection limit exceeded')
        ancestors.add(id(value))
        try:
            entries = value.items() if isinstance(value, dict) else enumerate(value)
            for key, child in entries:
                if isinstance(value, dict) and (not isinstance(key, str) or len(key) > 16384):
                    raise ValueError('Invalid evidence key')
                visit(child, depth + 1)
        finally:
            ancestors.remove(id(value))
    visit(data, 0)


def validate_timestamps(obj, fields):
    for field in fields:
        if obj.get(field) is not None and not valid_timestamp(obj[field]):
            raise ValueError(f'Invalid timestamp {field}')


def period_after(left, right):
    # A monthly period establishes no ordering within that month.
    return left[:7] > right[:7] or (len(left) == len(right) == 10 and left > right)


def validate_attempt(state):
    if not isinstance(state, dict) or state.get('status') not in ATTEMPT_STATUSES:
        raise ValueError('Invalid source attempt state')
    validate_timestamps(state, ('attempted_at',))
    for field in ('error_type', 'note'):
        if state.get(field) is not None and not isinstance(state[field], str):
            raise ValueError('Invalid source attempt text')
    if state.get('observation_date') is not None and not valid_period(state['observation_date']):
        raise ValueError('Invalid attempt observation date')
    if 'coverage' in state:
        coverage = state['coverage']
        allowed = ATTEMPT_STATUSES + EVIDENCE_STATUSES['observation_status']
        if not isinstance(coverage, dict) or any(not isinstance(v, str) or v not in allowed for v in coverage.values()):
            raise ValueError('Invalid source coverage')
    if 'native_only' in state:
        keys = state['native_only']
        if not isinstance(keys, list) or any(not isinstance(k, str) or not k.strip() for k in keys) or len(set(keys)) != len(keys):
            raise ValueError('Invalid native-only coverage')


def validate_observation(record, region, today, previous=False):
    if not isinstance(record, dict) or not valid_period(record.get('period')):
        raise ValueError('Invalid observation period')
    for field in ('label', 'source', 'series', 'method', 'market_stage', 'geography', 'fx_basis', 'sampling_note', 'fallback_reason'):
        if record.get(field) is not None and not isinstance(record[field], str):
            raise ValueError(f'Invalid evidence text {field}')
    for field, allowed in EVIDENCE_STATUSES.items():
        if record.get(field) is not None and (not isinstance(record[field], str) or record[field] not in allowed):
            raise ValueError(f'Invalid evidence status {field}')
    validate_timestamps(record, ('retrieved_at', 'last_attempt_at', 'availability_as_of'))
    if 'unit_scale_unverified' in record and not isinstance(record['unit_scale_unverified'], bool):
        raise ValueError('Invalid unit-scale flag')
    validate_sampling(record)
    if record.get('listings') is not None:
        if not isinstance(record['listings'], list):
            raise ValueError('Invalid listing evidence')
        for listing in record['listings']:
            if not isinstance(listing, dict):
                raise ValueError('Invalid listing evidence')
            for field in ('ars_kg', 'unit_multiplier'):
                if listing.get(field) is not None and not positive(listing[field]):
                    raise ValueError('Invalid listing amount')
            if listing.get('available') is not None and not isinstance(listing['available'], bool):
                raise ValueError('Invalid listing availability')
            for field in ('name', 'url', 'measurement_unit', 'species', 'product_form', 'species_evidence', 'form_evidence'):
                if listing.get(field) is not None and not isinstance(listing[field], str):
                    raise ValueError('Invalid listing text')
            for field in ('product_id', 'sku_id', 'seller_id'):
                if listing.get(field) is not None and not isinstance(listing[field], str) and not safe_integer(listing[field]):
                    raise ValueError('Invalid listing identifier')
    for field in ('products', 'stores'):
        if record.get(field) is not None and (not safe_integer(record[field]) or record[field] < 0):
            raise ValueError(f'Invalid count {field}')
    if not positive(record.get('ars_kg' if region == 'ar' else 'usd_lb')):
        raise ValueError('Invalid native observation')
    for field in ('usd_lb', 'prev_usd_lb', 'fx_ars_per_usd'):
        if record.get(field) is not None and not positive(record[field]):
            raise ValueError(f'Invalid price or FX {field}')
    for field in ('fx_date', 'prev_period', 'publication_date', 'effective_start', 'effective_end'):
        value = record.get(field)
        if value is not None and (not valid_period(value) or (field in ('publication_date', 'effective_start', 'effective_end') and len(value) != 10)):
            raise ValueError(f'Invalid date {field}')
    period = record['period']
    start, end, publication = (record.get(k) for k in ('effective_start', 'effective_end', 'publication_date'))
    if start and end and start > end:
        raise ValueError('Reversed effective interval')
    if end and (end if len(period) == 10 else end[:7]) != period:
        raise ValueError('Observation period differs from effective end')
    if start and period_after(start, period):
        raise ValueError('Effective start follows observation period')
    known_by = min(today, timestamp_day(record['retrieved_at'])) if record.get('retrieved_at') else today
    if publication and publication > known_by:
        raise ValueError('Future publication date')
    printed_end_window = record.get('interval_basis') == 'advertisement_ending_dates_printed_in_pdf'
    if printed_end_window:
        if (region != 'us' or record.get('source') != 'USDA ad survey' or not (start and end and publication)
                or not start <= publication <= end
                or (datetime.fromisoformat(end) - datetime.fromisoformat(start)).days > 13):
            raise ValueError('Invalid USDA advertisement ending window')
    if period_after(period, known_by):
        # Printed USDA ad-ending windows can span two weeks; other advertised
        # intervals retain the existing seven-day bound.
        advertised = record.get('source') == 'USDA ad survey' and start and end and publication
        if not advertised or (datetime.fromisoformat(end) - datetime.fromisoformat(start)).days > (13 if printed_end_window else 6) or (datetime.fromisoformat(end) - datetime.fromisoformat(publication)).days > 14:
            raise ValueError('Unsupported future observation period')
    if record.get('prev_period') and period_after(record['prev_period'], period):
        raise ValueError('Previous period follows observation')
    if record.get('fx_date') and (period_after(record['fx_date'], period) or period_after(record['fx_date'], known_by)):
        raise ValueError('Future FX date')
    if region == 'ar':
        rate, converted = record.get('fx_ars_per_usd'), record.get('usd_lb')
        if record.get('source') in ('INDEC', 'IPCVA') and record.get('fx_date') and record['fx_date'][:7] != period[:7]:
            raise ValueError('Monthly FX month differs from observation')
        if record.get('fx_provenance') in ('recorded', 'inferred_from_legacy_snapshot') and (rate is None or not record.get('fx_date')):
            raise ValueError('Incomplete claimed FX lineage')
        if rate is not None and converted is not None:
            expected = record['ars_kg'] / rate / 2.2046226
            tolerance = 0.005 if record.get('source') == 'Carrefour AR' else 1e-9
            if not positive(expected) or abs(converted - expected) > tolerance + 1e-12 * max(abs(converted), abs(expected)):
                raise ValueError('Inconsistent USD conversion')
    if record.get('previous_observation') is not None:
        if previous:
            raise ValueError('Nested previous observation exceeds one level')
        validate_observation(record['previous_observation'], region, today, previous=True)


def validate_snapshot(data, as_of=None):
    validate_json_tree(data)
    if not isinstance(data, dict) or data.get('schema_version') != 2 or not isinstance(data.get('fx'), dict) or not isinstance(data.get('source_status'), dict):
        raise ValueError('Expected v2 snapshot and FX object')
    as_of = timestamp() if as_of is None else as_of
    if not valid_timestamp(as_of):
        raise ValueError('Invalid validation clock')
    today = timestamp_day(as_of)
    validate_timestamps(data, ('fetched', 'generated_at'))
    if data.get('qualification_note') is not None and not isinstance(data['qualification_note'], str):
        raise ValueError('Invalid qualification note')
    if 'sources' in data and (not isinstance(data['sources'], dict) or any(v is not None and not isinstance(v, str) for v in data['sources'].values())):
        raise ValueError('Invalid source descriptions')
    if data['fx'].get('latest') is not None and not isinstance(data['fx']['latest'], dict):
        raise ValueError('Invalid latest FX object')
    for fx, date_field in ((data['fx'], 'period'), (data['fx'].get('latest') or {}, 'date')):
        if fx.get('ars_per_usd') is not None and not positive(fx['ars_per_usd']):
            raise ValueError('Invalid top-level FX rate')
        value = fx.get(date_field)
        if value is not None and (not valid_period(value) or len(value) != (7 if date_field == 'period' else 10) or period_after(value, today)):
            raise ValueError('Invalid top-level FX date')
        validate_timestamps(fx, ('monthly_retrieved_at', 'retrieved_at'))
        for field in ('series', 'source', 'basis'):
            if fx.get(field) is not None and not isinstance(fx[field], str):
                raise ValueError('Invalid FX context')
    for field in ('source_status', 'catalog_attempts'):
        states = data.get(field)
        if states is None and field == 'catalog_attempts':
            continue
        if not isinstance(states, dict):
            raise ValueError('Invalid attempt collection')
        for state in states.values():
            validate_attempt(state)
    for region in ('us', 'ar'):
        if not isinstance(data.get(region), dict):
            raise ValueError(f'Missing {region} observations')
        for key, record in data[region].items():
            try:
                validate_observation(record, region, today)
            except ValueError as error:
                raise ValueError(f'{region}/{key}: {error}') from error
    if not isinstance(data.get('ar_sources', {}), dict):
        raise ValueError('Invalid Argentine source collection')
    for source, records in data.get('ar_sources', {}).items():
        if not isinstance(source, str) or not source or not isinstance(records, dict):
            raise ValueError('Invalid Argentine source collection')
        for record in records.values():
            validate_observation(record, 'ar', today)
            if record.get('source') != source:
                raise ValueError('Argentine source identity mismatch')
    originals = data.get('carrefour_originals', {})
    if not isinstance(originals, dict):
        raise ValueError('Invalid original Carrefour collection')
    for record in originals.values():
        validate_observation(record, 'ar', today)
        if record.get('source') != 'Carrefour AR':
            raise ValueError('Original Carrefour source identity mismatch')
    return data


def enable_ar_sources(data):
    """Capture originals once, then keep current observations independently by source."""
    sources = data.setdefault('ar_sources', {})
    originals = data.setdefault('carrefour_originals', {})
    for key, record in data['ar'].items():
        source = record.get('source', 'Unknown')
        sources.setdefault(source, {}).setdefault(key, copy.deepcopy(record))
        if source == 'Carrefour AR':
            originals.setdefault(key, copy.deepcopy(record))


def source_records(data, region, source):
    if region == 'ar' and 'ar_sources' in data:
        return data['ar_sources'].setdefault(source, {})
    return data[region]


def select_ar_sources(data):
    """IPCVA is the primary monthly benchmark; source priority is not date ordering."""
    if 'ar_sources' not in data:
        return
    selected = {}
    priority = ('IPCVA', 'INDEC', 'Carrefour AR')
    order = list(priority) + sorted(set(data['ar_sources']) - set(priority))
    for source in order:
        for key, record in data['ar_sources'].get(source, {}).items():
            selected.setdefault(key, copy.deepcopy(record))
    data['ar'] = selected


def merge_records(data, region, source, new, keys, attempted_at):
    outcomes = {}
    stale_observations = {}
    destination = source_records(data, region, source)
    for key in keys:
        old = destination.get(key)
        if key in new:
            record = new[key]
            old_period = old.get('period') if old and old.get('source') == source else None
            new_period = record.get('period')
            if old_period and (period_after(old_period, new_period) or
                               (len(old_period) == 10 and len(new_period) == 7 and old_period[:7] == new_period)):
                # Keep the latest known observation when a valid replay/backfill
                # arrives. A monthly value cannot displace a more precise date
                # from the same month; same-period revisions remain promotable.
                old['last_attempt_at'] = attempted_at
                outcomes[key] = 'unknown'
                stale_observations[key] = {
                    'received_period': new_period,
                    'retained_period': old_period,
                }
                continue
            record['retrieved_at'] = attempted_at
            record.setdefault('provenance_status', 'parsed_unverified')
            record.setdefault('observation_status', 'reference_only' if record.get('availability') == 'out_of_stock' else 'observed')
            if old and old != record:
                record['previous_observation'] = {k:v for k,v in old.items() if k != 'previous_observation'}
            destination[key] = record
            outcomes[key] = record['observation_status']
        else:
            outcomes[key] = 'no_match'
            if old and old.get('source') == source:
                old['observation_status'] = 'retained_no_match'
                old['last_attempt_at'] = attempted_at
    state = {
        'status': 'partial' if stale_observations else 'ok' if new else 'no_match',
        'attempted_at': attempted_at,
        'coverage': outcomes,
    }
    if stale_observations:
        state['stale_observations'] = stale_observations
    data['source_status'][source] = state
    if region == 'ar':
        select_ar_sources(data)


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
