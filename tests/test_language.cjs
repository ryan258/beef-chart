// Focused localization checks: no network, providers, or browser installation.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const translations = fs.readFileSync(path.join(root, 'assets/i18n.js'), 'utf8');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const snapshot = JSON.parse(fs.readFileSync(path.join(root, 'tests/fixtures/prices_legacy_2026_10_07.json'), 'utf8'));
const section = (start, end) => html.slice(html.indexOf(start), html.indexOf(end, html.indexOf(start)));
function setup(search = '', saved = null, blocked = false) {
  const context = vm.createContext({URL, location:{href:'https://example.test/atlas/' + search},
    localStorage:{getItem:() => { if (blocked) throw new Error('Storage blocked'); return saved; }},
    document:{querySelector:() => ({}), querySelectorAll:() => []}, snapshot:structuredClone(snapshot)});
  vm.runInContext(translations + '\n' + section('const $ =', '// 2. COW VISUALIZATIONS')
    + section('function fxLine(', 'let lastFocusedBeforeModal')
    + '\nPRICES = validatePrices(snapshot);', context);
  return code => vm.runInContext(code, context);
}

test('shared language overrides saved choice and works when storage is blocked', () => {
  assert.equal(setup('?lang=es-AR', 'en', true)('language'), 'es-AR');
  assert.equal(setup('?lang=en', 'es-AR')('language'), 'en');
  assert.equal(setup('', 'es-AR')('language'), 'es-AR');
  assert.equal(setup('?lang=invalid', null, true)('language'), 'en');
});

test('all cut descriptions, primal descriptions and relationship qualifications have translations', () => {
  const run = setup('?lang=es-AR');
  assert.equal(run('ALL_CUTS.length'), 24);
  assert.equal(run('ALL_CUTS.every(c => t(c.info) !== c.info && t(c.relationship.type) !== c.relationship.type)'), true);
  assert.equal(run('WHOLESALE_PRIMALS.every(p => t(p.desc) !== p.desc)'), true);
  assert.equal(run('Object.entries(SPANISH).every(([key, value]) => JSON.stringify((key.match(/\\{\\d+\\}/g) || []).sort()) === JSON.stringify((value.match(/\\{\\d+\\}/g) || []).sort()))'), true);
});

test('Spanish preserves withheld prices and evidence, and English restores original wording', () => {
  const run = setup('?lang=es-AR');
  const before = run('JSON.stringify(PRICES)');
  for (const id of ['molleja','rinon','lengua']) {
    assert.equal(run(`validPrice(PRICES.ar.${id})`), false);
    assert.match(run(`priceBlock({arSeries:'${id}'})`), /Precio no publicado.*Solo como evidencia guardada/s);
    assert.doesNotMatch(run(`priceBlock({arSeries:'${id}'})`), /Stored evidence|Historical sample|Publication:/);
  }
  run("language = 'en'");
  assert.match(run("priceBlock({arSeries:'molleja'})"), /Price withheld.*Stored evidence only/s);
  assert.equal(run('JSON.stringify(PRICES)'), before);
});

test('numeric formatting changes without changing currency, units, or stored values', () => {
  const run = setup('?lang=es-AR');
  assert.equal(run('usd(12.5)'), 'US$12,50');
  assert.match(run("monthLabel('2026-10')"), /oct/);
  run("language = 'en'");
  assert.equal(run('usd(12.5)'), '$12.50');
  assert.equal(run("monthLabel('2026-10')"), 'Oct 2026');
});

test('localized templates preserve interpolated text and escape upstream data in dossiers', () => {
  const run = setup('?lang=es-AR');
  assert.equal(run('t`US primal: ${"$& <test>"}`'), 'Región de EE. UU.: $& <test>');
  assert.equal(run("t('constructor')"), 'constructor');
  run('PRICES.ar.lomo.method = "<img src=x onerror=alert(1)>"');
  assert.match(run("priceBlock({arSeries:'lomo'})"), /&lt;img/);
  assert.doesNotMatch(run("priceBlock({arSeries:'lomo'})"), /<img/);
});

test('sampling contract uses canonical values even when display language is Spanish', () => {
  const run = setup('?lang=es-AR');
  run(`PRICES.ar.lomo.products = 1; PRICES.ar.lomo.sampling = {
    per_query_limit:20, eligible_count:1, selected_count:1, unknown_seller_count:0,
    queries:[{query:'lomo',returned_products:1}], coverage:'unknown',
    population:'available_listings', seller_policy:'first_seller_per_sku', seller_ids:['1'], region:null
  }; validatePrices(PRICES);`);
  assert.match(run('samplingContext(PRICES.ar.lomo)'), /Mediana de la muestra.*cobertura sigue siendo desconocida/s);
});
