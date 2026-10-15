"""IPCVA AMBA monthly retail benchmarks from its public HTML export."""
import copy
import hashlib
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser

from official_prices import SOURCE_ERRORS
from bcra_fx import BASIS, fetch_monthly_quotes
from price_contract import (enable_ar_sources, merge_records, positive, qualify_snapshot,
                            select_ar_sources, source_records, valid_period, validate_snapshot)

EXPORT_URL = 'https://ipcva.agrositio.com/estadisticas/vista_precios_consumidor_xls.php'
REPORT_URL = 'https://api.carneargentina.org.ar/web/uploads/globals/1/Informe%20Mensual%20de%20Precios%20SEP26_.pdf'
# These IDs/labels are kg-priced beef rows, checked against report table 3.
# Prepared foods and the frozen-hamburger four-unit price are excluded.
ITEMS = {
    'asado': (10, 'Asado'), 'bife_ancho': (70, 'Bife Ancho'),
    'bife_angosto': (15, 'Bife angosto'), 'bola_lomo': (71, 'Bola de Lomo'),
    'carnaza_comun': (72, 'Carnaza Común'), 'colita': (86, 'Colita de cuadril'),
    'cuadrada': (73, 'Cuadrada'), 'cuadril': (14, 'Cuadril'), 'falda': (74, 'Falda'),
    'lomo': (77, 'Lomo'), 'matambre': (87, 'Matambre'), 'nalga': (13, 'Nalga'),
    'osobuco': (78, 'Osobuco'), 'paleta': (11, 'Paleta'), 'peceto': (79, 'Peceto'),
    'ground_beef': (81, 'Picada Común'), 'ground_beef_special': (82, 'Picada Especial'),
    'roast_beef': (83, 'Roast Beef'), 'tapa_asado': (88, 'Tapa de asado'),
    'tapa_nalga': (84, 'Tapa de Nalga'), 'tortuguita': (89, 'Tortuguita'),
    'vacio': (85, 'Vacío'),
}
MONTHS = {name: index for index, names in enumerate(
    [('ene', 'jan'), ('feb',), ('mar',), ('abr', 'apr'), ('may',), ('jun',),
     ('jul',), ('ago', 'aug'), ('sep',), ('oct',), ('nov',), ('dic', 'dec')], 1)
    for name in names}


class ExportTable(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = self.cell = None
        self.tables = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.tables += 1
        elif tag == 'tr':
            if self.row is not None:
                raise ValueError('Nested IPCVA row')
            self.row = []
        elif tag in ('td', 'th'):
            if self.row is None or self.cell is not None:
                raise ValueError('Invalid IPCVA cell')
            self.cell = []

    def handle_data(self, value):
        if self.cell is not None:
            self.cell.append(value)

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            if self.cell is not None:
                raise ValueError('Unclosed IPCVA cell')
            self.rows.append(self.row)
            self.row = None


def export_url(attempted_at):
    year = int(attempted_at[:4])
    return EXPORT_URL + '?' + urllib.parse.urlencode({
        'productos': ','.join(str(sid) for sid, _ in ITEMS.values()),
        'desde': f'{year - 1}-01-01', 'hasta': attempted_at[:7] + '-01',
    })


def get_export(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'beef-chart price snapshot'})
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read(1_000_001)
    if len(raw) > 1_000_000:
        raise ValueError('IPCVA export exceeds size limit')
    return raw.decode('utf-8-sig')


def parse_export(html, rates, attempted_at, url=None, fx_evidence=None):
    """Fail closed on changed headers, malformed amounts, duplicates or future months."""
    if not isinstance(html, str) or len(html) > 1_000_000:
        raise ValueError('Invalid IPCVA export')
    table = ExportTable()
    table.feed(html)
    table.close()
    if table.tables != 1 or table.row is not None or len(table.rows) < 2:
        raise ValueError('Missing IPCVA export table')
    if table.rows[0] != ['Precios al Consumidor en Moneda Corriente']:
        raise ValueError('Unexpected IPCVA export title')
    headers = table.rows[1]
    expected = {label for _, label in ITEMS.values()}
    if not headers or headers[0] != 'Período' or len(headers) != len(expected) + 1 or set(headers[1:]) != expected:
        raise ValueError('Unexpected IPCVA product headers')
    rows = {}
    for row in table.rows[2:]:
        if len(row) != len(headers):
            raise ValueError('IPCVA column count changed')
        match = re.fullmatch(r'([A-Za-z]{3})-(\d{2}|\d{4})', row[0])
        if not match or match[1].lower() not in MONTHS:
            raise ValueError('Invalid IPCVA month')
        year = int(match[2]) + (2000 if len(match[2]) == 2 else 0)
        period = f'{year:04d}-{MONTHS[match[1].lower()]:02d}'
        if not valid_period(period) or period >= attempted_at[:7] or period in rows:
            raise ValueError('Future, incomplete or duplicate IPCVA month')
        values = {}
        for label, value in zip(headers[1:], row[1:]):
            if value == 'S/D':
                values[label] = None
                continue
            if not re.fullmatch(r'\$\s*(?:\d{1,3}(?:\.\d{3})+|\d+),\d{2}', value):
                raise ValueError('Invalid IPCVA currency amount')
            number = float(value.replace('$', '').replace('.', '').replace(',', '.').strip())
            if not positive(number):
                raise ValueError('Invalid IPCVA price')
            values[label] = number
        rows[period] = values
    records = {}
    # Only use the newest returned month. A missing current cut is not filled
    # with an older row and mislabeled as fresh source coverage.
    if not rows:
        return records
    current = max(rows)
    receipt = {'url': url or export_url(attempted_at),
               'sha256': hashlib.sha256(html.encode('utf-8')).hexdigest()}
    for key, (sid, label) in ITEMS.items():
        value = rows[current][label]
        if value is None:
            continue
        prior = sorted((p for p in rows if p < current and rows[p][label] is not None), reverse=True)
        previous = prior[0] if prior else None
        fx_date, rate = rates.get(current, (None, None))
        previous_rate = rates.get(previous, (None, None))[1]
        records[key] = {
            'label': 'Asado de tira' if key == 'asado' else label,
            'series': str(sid), 'source': 'IPCVA', 'period': current, 'ars_kg': value,
            'usd_lb': value / rate / 2.2046226 if rate else None,
            'prev_period': previous, 'prev_ars_kg': rows[previous][label] if previous else None,
            'prev_usd_lb': rows[previous][label] / previous_rate / 2.2046226 if previous_rate else None,
            'fx_ars_per_usd': rate, 'fx_date': fx_date, 'fx_basis': 'BCRA monthly average',
            'fx_provenance': 'recorded' if rate else 'unknown',
            'geography': 'AMBA (Buenos Aires metropolitan area)', 'market_stage': 'retail',
            'method': 'Monthly survey of butcher shops and supermarkets',
            'publication_date': None, 'source_receipt': copy.deepcopy(receipt),
            'methodology_reference': REPORT_URL,
            'unit_basis': 'ARS/kg; product IDs checked against September 2026 report table 3',
        }
        if fx_evidence is not None:
            records[key]['fx_basis'] = BASIS
            records[key]['fx_evidence'] = copy.deepcopy(fx_evidence.get(current))
            records[key]['previous_fx_evidence'] = copy.deepcopy(fx_evidence.get(previous))
    return records


def refresh_ipcva(data, attempted_at, rates=None):
    """Save IPCVA with a distinct direct-BCRA quote mean; preserve other FX bases."""
    enable_ar_sources(data)
    issues = []
    try:
        html = get_export(export_url(attempted_at))
        records = parse_export(html, {}, attempted_at)
        # Parsing first makes the FX query follow the actual observed months.
        # `rates` remains an internal injection seam for offline callers.
        if rates is None and records:
            periods = {p['period'] for p in records.values()} | {p['prev_period'] for p in records.values() if p['prev_period']}
            fx_state = {'attempted_at': attempted_at}
            rates, evidence = {}, {}
            try:
                rates, evidence = fetch_monthly_quotes(periods, attempted_at)
                fx_state.update(status='ok' if set(rates) == periods else 'partial' if rates else 'no_match',
                                coverage={p: 'ok' if p in rates else 'no_match' for p in sorted(periods)},
                                monthly_rates=evidence)
            except (AttributeError, *SOURCE_ERRORS) as error:
                fx_state.update(status='error', error_type=type(error).__name__,
                                note='Direct BCRA USD quotes unavailable; native IPCVA prices retained')
            data['source_status']['IPCVA FX'] = fx_state
            if fx_state['status'] != 'ok':
                issues.append('IPCVA FX')
            records = parse_export(html, rates, attempted_at, fx_evidence=evidence)
        elif rates is not None:
            records = parse_export(html, rates, attempted_at)
        validate_snapshot(qualify_snapshot({'us': {}, 'ar': records, 'fx': {}}), as_of=attempted_at)
        merge_records(data, 'ar', 'IPCVA', records, list(ITEMS), attempted_at)
        state = data['source_status']['IPCVA']
        native_only = [key for key, record in records.items() if record['usd_lb'] is None]
        lagged = bool(records) and max(p['period'] for p in records.values()) < (
            f'{int(attempted_at[:4]) - 1}-12' if attempted_at[5:7] == '01' else f'{attempted_at[:4]}-{int(attempted_at[5:7]) - 1:02d}')
        if records and (len(records) != len(ITEMS) or native_only or lagged):
            state['status'] = 'partial'
        if native_only:
            state['native_only'] = native_only
            state['note'] = 'Matching monthly FX unavailable for ' + ', '.join(sorted({records[key]['period'] for key in native_only})) + '; native ARS/kg saved'
        if lagged:
            state['note'] = (state.get('note', '') + '; Latest returned IPCVA observation predates the previous calendar month').lstrip('; ')
    except (UnicodeError, *SOURCE_ERRORS) as error:
        state = {'status': 'error', 'attempted_at': attempted_at, 'error_type': type(error).__name__,
                 'coverage': {key: 'error' for key in ITEMS}}
        for record in source_records(data, 'ar', 'IPCVA').values():
            record.update(observation_status='retained_after_error', last_attempt_at=attempted_at)
        data['source_status']['IPCVA'] = state
    select_ar_sources(data)
    data['sources']['ar_monthly'] = 'IPCVA AMBA monthly retail survey; primary where covered'
    if state['status'] != 'ok':
        issues.append('IPCVA')
    return issues
