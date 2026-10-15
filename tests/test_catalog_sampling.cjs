// C14 runs the actual inline validators/renderers against synthetic records, offline.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {test} = require('node:test');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const snapshot = JSON.parse(fs.readFileSync(path.join(root, 'tests/fixtures/prices_legacy_2026_10_07.json'), 'utf8'));
const section = (start, end) => {
  const from = html.indexOf(start), to = html.indexOf(end, from);
  assert.ok(from >= 0 && to > from);
  return html.slice(from, to);
};
const source = section('const $ =', '// 2. COW VISUALIZATIONS')
  + section('function fxLine(', 'let lastFocusedBeforeModal')
  + section('function safeUsd(', 'function renderTable(')
  + section('function renderPrices(', '\nrenderReferenceTables();');
const sample = {
  queries: [{query: 'lengua', returned_products: 20}], per_query_limit: 20,
  eligible_count: 3, selected_count: 2, population: 'available_listings',
  seller_policy: 'first_seller_per_sku', seller_ids: ['seller-1'], unknown_seller_count: 1,
  region: null, coverage: 'possibly_truncated'
};
const setup = () => {
  const tables = new Map();
  const context = vm.createContext({snapshot: structuredClone(snapshot), sample: structuredClone(sample),
    document: {querySelector: () => ({}), querySelectorAll: () => []},
    renderTable: (id, caption, headers, rows) => tables.set(id, rows), renderScatter: () => {}});
  vm.runInContext(fs.readFileSync(path.join(root, 'assets/i18n.js'), 'utf8'), context);
  vm.runInContext(source + '\nPRICES = validatePrices(snapshot);', context);
  return {run: code => vm.runInContext(code, context), tables};
};

test('legacy dossiers and table share unknown coverage without changing evidence or organ suppression', () => {
  const {run, tables} = setup();
  const before = run('JSON.stringify(PRICES)');
  run('renderPrices()');
  for (const [key, p] of Object.entries(snapshot.ar).filter(([,p]) => p.source === 'Carrefour AR')) {
    const note = run(`samplingContext(PRICES.ar[${JSON.stringify(key)}])`);
    assert.match(note, /Historical sample:.*original query counts, limit hits and seller\/region coverage unknown/);
    assert.ok(run(`priceBlock({arSeries:${JSON.stringify(key)}})`).includes(note));
    assert.ok(tables.get('price-table').find(row => row[0] === 'AR: ' + p.label)[3].includes(note));
  }
  assert.equal(tables.get('price-table').filter(row => row[1] === 'Price withheld').length, 3);
  assert.equal(run('samplingContext(PRICES.us.ground_beef)'), '');
  assert.equal(run('JSON.stringify(PRICES)'), before);
});

test('new sample explains median, query limit, first seller, missing IDs and region consistently', () => {
  const {run, tables} = setup();
  run('PRICES.ar.lengua.sampling = sample; PRICES.ar.lengua.products = 2; validatePrices(PRICES); renderPrices()');
  const note = run('samplingContext(PRICES.ar.lengua)');
  assert.match(note, /2 listings available at observation, from 3 eligible listings/);
  assert.match(note, /lengua: 20/);
  assert.match(note, /First seller per SKU; selected seller IDs: seller-1; 1 selected listings lack a seller ID/);
  assert.match(note, /Delivery region: unknown.*Query limit reached; possibly truncated/);
  assert.ok(run('priceBlock({arSeries:"lengua"})').includes(note));
  assert.ok(tables.get('price-table').find(row => row[0] === 'AR: Lengua')[3].includes(note));
  run('sample.population = "out_of_stock_references"; sample.queries[0].returned_products = 3; sample.coverage = "unknown"; validatePrices(PRICES)');
  assert.match(run('samplingContext(PRICES.ar.lengua)'), /2 out-of-stock references only.*Query limit not reached; coverage still unknown/);
  run('sample.queries[0].query = "<img src=x onerror=alert(1)>"; sample.seller_ids[0] = "<script>"');
  const dossier = run('priceBlock({arSeries:"lengua"})');
  assert.doesNotMatch(dossier, /<img|<script>/);
  assert.match(dossier, /&lt;img/);
});

test('browser rejects malformed or contradictory sampling metadata', () => {
  const {run} = setup();
  const bad = [null, [], 'sample', {...sample, selected_count: true}, {...sample, selected_count: 4},
    {...sample, per_query_limit: 0}, {...sample, queries: []},
    {...sample, queries: [{query: 'lengua', returned_products: -1}]}, {...sample, coverage: 'complete'},
    {...sample, coverage: 'unknown'}, {...sample, population: 'all_products'}, {...sample, seller_policy: 'all_sellers'},
    {...sample, seller_ids: [3]}, {...sample, seller_ids: []}, {...sample, unknown_seller_count: 3}, {...sample, region: []}];
  run('PRICES.ar.lengua.products = 2');
  for (const value of bad) assert.throws(() => run(`PRICES.ar.lengua.sampling = ${JSON.stringify(value)}; validatePrices(PRICES)`), /sampling/);
});
