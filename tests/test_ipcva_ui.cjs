// Targeted validator and presentation checks; no browser or network.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const baseline = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/prices_before_ipcva.json'), 'utf8'));
const section = (start, end) => {
  const a = html.indexOf(start), b = html.indexOf(end, a);
  assert.ok(a >= 0 && b > a);
  return html.slice(a, b);
};
function setup() {
  const snapshot = structuredClone(baseline);
  snapshot.ar_sources = {'Carrefour AR':{lomo:structuredClone(snapshot.ar.lomo)}, IPCVA:{}};
  snapshot.carrefour_originals = {lomo:structuredClone(snapshot.ar.lomo), molleja:structuredClone(snapshot.ar.molleja)};
  snapshot.ar.lomo = {label:'Lomo',source:'IPCVA',period:'2026-09',ars_kg:28017,usd_lb:null,
    retrieved_at:'2026-10-15T18:00:00Z',geography:'AMBA (Buenos Aires metropolitan area)',
    method:'Monthly survey of butcher shops and supermarkets',publication_date:null,
    fx_date:null,fx_ars_per_usd:null,fx_provenance:'unknown',provenance_status:'parsed_unverified'};
  snapshot.ar_sources.IPCVA.lomo = structuredClone(snapshot.ar.lomo);
  const tables = new Map(), nodes = new Map();
  const context = vm.createContext({URL,location:{href:'https://example.test/?lang=en'},snapshot,
    document:{querySelector:s=>{if(!nodes.has(s))nodes.set(s,{});return nodes.get(s);},querySelectorAll:()=>[]},
    renderScatter:()=>{},renderTable:(id,caption,headers,rows)=>tables.set(id,{caption,headers,rows})});
  vm.runInContext(fs.readFileSync(path.join(root,'assets/i18n.js'),'utf8')
    +section('const $ =','// 2. COW VISUALIZATIONS')
    +section('function fxLine(','let lastFocusedBeforeModal')
    +section('function safeUsd(','function renderTable(')
    +section('function renderPrices(','\nrenderReferenceTables();'),context);
  const run=s=>vm.runInContext(s,context);
  run('PRICES = validatePrices(snapshot)');
  return {run,tables};
}
test('IPCVA native monthly price and original dated Carrefour evidence appear together in both languages',()=>{
  const {run,tables}=setup();
  for(const language of ['en','es-AR']) {
    run(`language = ${JSON.stringify(language)}; renderPrices()`);
    const dossier=run('priceBlock(BY_ID.lomo)');
    assert.match(dossier,/IPCVA.*2026-09/s);
    assert.match(dossier,/<details.*Carrefour.*2026-10-07/s);
    assert.match(dossier,language==='en'?/28,017 ARS\/kg/:/28\.017 ARS\/kg/);
    assert.ok(tables.get('price-table').rows.some(r=>r[0].includes('Carrefour')&&r[3].includes('2026-10-07')));
    const organ=tables.get('price-table').rows.find(r=>r[0].includes('Carrefour')&&r[0].includes('Molleja'));
    assert.equal(organ[1],language==='en'?'Price withheld':'Precio no publicado');
  }
  assert.equal(run('JSON.stringify(PRICES.carrefour_originals.lomo)'),JSON.stringify(baseline.ar.lomo));
});
test('malformed archived records and mismatched monthly FX fail browser validation',()=>{
  const {run}=setup();
  run('const clean = JSON.stringify(snapshot)');
  for(const mutation of [
    "snapshot.ar_sources.IPCVA.lomo.period = '2026-02-31'",
    "snapshot.carrefour_originals.lomo.period = '2026-02-31'",
    "snapshot.ar_sources.IPCVA.lomo.source = 'Carrefour AR'",
    "snapshot.ar.lomo.fx_date = '2026-08-01'",
    'snapshot.ar_sources = []',
    'snapshot.carrefour_originals = []'
  ]) {
    run(`snapshot = JSON.parse(clean); ${mutation}`);
    assert.throws(()=>run('validatePrices(snapshot)'));
  }
});

test('USDA printed ending window is qualified in English and Spanish',()=>{
  const {run}=setup();
  run(`PRICES.us.ribeye_bnls = {...PRICES.us.ribeye_bnls,
    period:'2026-10-15', effective_start:'2026-10-03', effective_end:'2026-10-15',
    publication_date:'2026-10-09', retrieved_at:'2026-10-09T20:00:00Z',
    interval_basis:'advertisement_ending_dates_printed_in_pdf',
    method:'Store-count-weighted national advertised features'};
    validatePrices(PRICES, '2026-10-09T20:00:00Z')`);
  assert.match(run('recordContext(PRICES.us.ribeye_bnls)'),/Advertisement ending dates 2026-10-03–2026-10-15; individual offer dates vary/);
  run("language = 'es-AR'");
  assert.match(run('recordContext(PRICES.us.ribeye_bnls)'),/Fechas de finalización de las promociones 2026-10-03–2026-10-15; las fechas de cada oferta varían/);
});
