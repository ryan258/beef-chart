const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {summarize} = require('../assets/snapshot-summary.js');
const ManualPrices = require('../assets/manual-prices.js');
const snapshot = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/prices.json'), 'utf8'));

test('the bundled snapshot distinguishes assembly, survey periods, ad-ending dates and retained prices', () => {
  const text = summarize(snapshot);
  assert.match(text, /^Snapshot assembled 2026-10-15\./);
  assert.match(text, /Argentina IPCVA survey: 2026-09\./);
  assert.match(text, /U\.S\. BLS averages: 2026-09\./);
  assert.match(text, /U\.S\. USDA ad-ending dates: 2026-10-03–2026-10-15\./);
  assert.match(text, /Retained Carrefour references: 3 \(2026-10-07\)\./);
  assert.match(text, /Withheld Carrefour prices: 3\./);
  assert.doesNotMatch(text, /assembled 2026-10-07|retrieved|live/i);
  const spanish = summarize(snapshot, 'es-AR');
  assert.match(spanish, /^Datos compilados el 2026-10-15\./);
  assert.match(spanish, /Encuesta IPCVA de Argentina: 2026-09\./);
  assert.match(spanish, /Referencias conservadas de Carrefour: 3 \(2026-10-07\)\./);
  assert.match(spanish, /Precios de Carrefour no publicados: 3\./);
});

test('manual overrides retain the original source dates without promoting manual dates to survey dates', () => {
  const cuts = [
    {id:'lomo', arSeries:'lomo', usSeries:'tenderloin'},
    {id:'aguja', arSeries:'aguja', usSeries:'chuck_roast'},
    {id:'molleja', arSeries:'molleja'},
    {id:'new-cut'}
  ];
  const quote = (machine_name, currency, unit) => ({date:'2026-10-16', item:'Owner quote', machine_name, price:50, currency, unit});
  const overlay = ManualPrices.apply(snapshot, {
    ar:[quote('lomo','ARS','kg'), quote('aguja','ARS','kg'), quote('molleja','ARS','kg'), quote('new-cut','ARS','kg')],
    us:[quote('tenderloin','USD','lb')]
  }, cuts, '2026-10-16').prices;
  assert.equal(summarize(overlay), summarize(snapshot));
  assert.equal(summarize(overlay,'es-AR'), summarize(snapshot,'es-AR'));
  assert.doesNotMatch(summarize(overlay), /2026-10-16/);
});

test('unavailable, legacy, malformed and partly unknown evidence stay explicitly unknown', () => {
  assert.equal(summarize(null), 'Snapshot unavailable.');
  assert.equal(summarize(undefined,'es-AR'), 'Datos guardados no disponibles.');
  assert.equal(summarize({fetched:'2026-10-01T00:00:00Z'}), 'Snapshot assembly date unknown. Source observation dates unavailable.');
  const input = {generated_at:'2026-02-31T00:00:00Z', ar:{a:{source:'IPCVA',period:'2026-08'}, b:{source:'IPCVA',period:null}, c:null}, us:{a:{source:'BLS',period:'2026-13'}, b:{source:'BLS',period:'2026-02-30'}}};
  const text = summarize(input);
  assert.match(text, /^Snapshot assembly date unknown\./);
  assert.match(text, /Argentina IPCVA survey: 2026-08; some dates unknown\./);
  assert.match(text, /U\.S\. BLS averages: dates unknown\./);
  assert.doesNotMatch(text, /2026-13|2026-02-30|2026-02-31/);
  assert.match(summarize(input,'es-AR'), /2026-08; algunas fechas desconocidas/);
  assert.doesNotThrow(() => summarize({ar:[],us:null,manual_originals:[]}));
});

test('source periods span actual observations and USDA ending dates differ from ordinary advertised windows', () => {
  const input = {generated_at:'2026-10-16T00:15:00+02:00', ar:{a:{source:'IPCVA',period:'2026-08'}, b:{source:'IPCVA',period:'2026-09'}}, us:{
    a:{source:'BLS',period:'2026-07'}, b:{source:'BLS',period:'2026-09'},
    c:{source:'USDA ad survey',period:'2026-12-31',effective_start:'2026-10-03',effective_end:'2026-10-15',interval_basis:'advertisement_ending_dates_printed_in_pdf'},
    d:{source:'USDA ad survey',period:'2026-12-31',effective_start:'2026-10-10',effective_end:'2026-10-17',interval_basis:'advertisement_ending_dates_printed_in_pdf'},
    e:{source:'USDA ad survey',period:'2026-05-09'},
    f:{source:'USDA ad survey',period:null,effective_start:'2026-10-20',effective_end:'2026-10-10'},
    g:{source:'USDA ad survey',period:'2026-12-31',effective_start:'2026-10-17',effective_end:'2026-10-23'}
  }};
  const text = summarize(input);
  assert.match(text, /^Snapshot assembled 2026-10-15\./); // UTC assembly day, independent of the host timezone.
  assert.match(text, /Argentina IPCVA survey: 2026-08–2026-09/);
  assert.match(text, /U\.S\. BLS averages: 2026-07–2026-09/);
  assert.match(text, /ad-ending dates: 2026-10-03–2026-10-15, 2026-10-10–2026-10-17\./);
  assert.match(text, /advertised windows: 2026-10-17–2026-10-23\./);
  assert.doesNotMatch(text, /ad-ending dates: [^.]*2026-10-23/);
  assert.match(text, /observation periods: 2026-05-09; some dates unknown; advertised dates unknown\./);
  assert.doesNotMatch(text, /2026-12-31|2026-10-20/);
  const spanish = summarize(input,'es-AR');
  assert.match(spanish, /Fechas de finalización de anuncios USDA de EE\. UU\.: 2026-10-03–2026-10-15, 2026-10-10–2026-10-17\./);
  assert.match(spanish, /Períodos anunciados USDA de EE\. UU\.: 2026-10-17–2026-10-23\./);
});

test('selected INDEC fallback periods survive manual overlays and do not borrow source-ledger dates', () => {
  const input = {ar:{a:{source:'INDEC',period:'2026-05'},b:{source:'INDEC',period:'2026-06'}},us:{},
    ar_sources:{INDEC:{a:{source:'INDEC',period:'2026-12'}},IPCVA:{a:{source:'IPCVA',period:'2026-11'}}}};
  const text = summarize(input);
  assert.match(text, /Argentina INDEC averages: 2026-05–2026-06\./);
  assert.doesNotMatch(text, /IPCVA|2026-11|2026-12|Source observation dates unavailable/);
  assert.match(summarize(input,'es-AR'), /Promedios INDEC de Argentina: 2026-05–2026-06\./);
  const overlay = {...input,ar:{...input.ar,a:{source:'Manual entry',manual_entry:true,period:'2026-10-16'}},manual_originals:{ar:{a:input.ar.a}}};
  assert.equal(summarize(overlay), text);
});

test('withheld Carrefour evidence never enters the retained count or date range', () => {
  const input = {ar:{
    a:{source:'Carrefour AR',period:'2026-08-01',observation_status:'retained_no_match'},
    b:{source:'Carrefour AR',period:'2026-09-01',observation_status:'retained_after_error'},
    c:{source:'Carrefour AR',period:'2026-10-16',observation_status:'retained_after_error',unit_scale_unverified:true},
    d:{source:'Carrefour AR',period:'2026-10-15',observation_status:'observed'}
  }};
  const text = summarize(input);
  assert.match(text, /Retained Carrefour references: 2 \(2026-08-01–2026-09-01\)/);
  assert.match(text, /Withheld Carrefour prices: 1/);
  assert.doesNotMatch(text, /2026-10-15|2026-10-16/);
});

test('summaries do not mutate data and the browser global exposes the same API', () => {
  const before = JSON.stringify(snapshot);
  summarize(snapshot);
  summarize(snapshot,'es-AR');
  assert.equal(JSON.stringify(snapshot), before);
  const context = vm.createContext({});
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../assets/snapshot-summary.js'), 'utf8'), context);
  assert.equal(typeof context.SnapshotSummary.summarize, 'function');
  assert.equal(context.SnapshotSummary.summarize(snapshot), summarize(snapshot));
});
