// Execute the actual inline price functions offline; DOM/chart rendering is checked separately.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {test} = require('node:test');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const organs = ['molleja', 'rinon', 'lengua'];
const snapshot = JSON.parse(fs.readFileSync(path.join(root, 'data/prices.json'), 'utf8'));
const section = (start, end) => {
  const from = html.indexOf(start), to = html.indexOf(end, from);
  assert.ok(from >= 0 && to > from, `Inline test boundary missing: ${start}`);
  return html.slice(from, to);
};
const source = section('const $ =', '// 2. COW VISUALIZATIONS')
  + section('function fxLine(', 'let lastFocusedBeforeModal')
  + section('function safeUsd(', 'function renderTable(')
  + section('function renderPrices(', '\nrenderReferenceTables();');
const setup = () => {
  const nodes = new Map();
  const cards = organs.map(key => ({dataset: {ar: key}}));
  const tables = new Map();
  const context = vm.createContext({snapshot: structuredClone(snapshot),
    document: {querySelector: selector => {
      if (!nodes.has(selector)) nodes.set(selector, {});
      return nodes.get(selector);
    }, querySelectorAll: () => cards},
    renderTable: (id, caption, headers, rows) => tables.set(id, {caption, headers, rows}),
    renderScatter: () => {}});
  vm.runInContext(fs.readFileSync(path.join(root, 'assets/i18n.js'), 'utf8'), context);
  vm.runInContext(source + '\nPRICES = validatePrices(snapshot);', context);
  return {run: code => vm.runInContext(code, context), nodes, cards, tables};
};

test('flag blocks comparison prices and native fallback regardless of stock or attempt state', () => {
  const {run} = setup();
  for (const key of organs) {
    assert.equal(run(`validPrice(PRICES.ar.${key})`), false);
    const card = run(`priceLine(PRICES.ar.${key}, null)`);
    assert.match(card, /Price withheld.*Unverified unit scale.*Out-of-stock/s);
    assert.doesNotMatch(card, /\$|ARS\/kg/);
    run(`PRICES.ar.${key}.usd_lb = null; PRICES.ar.${key}.availability = 'in_stock'; PRICES.ar.${key}.observation_status = 'retained_after_error'`);
    assert.doesNotMatch(run(`priceLine(PRICES.ar.${key}, null)`), /\$|ARS\/kg/);
    assert.match(run(`recordStatus(PRICES.ar.${key})`), /Unverified unit scale.*latest attempt failed/);
  }
  assert.equal(run('safeUsd(PRICES.ar.bife_angosto)'), '$7.36');
  assert.match(run('priceLine(null, null)'), /Not available/);
});

test('dossiers keep original numbers as evidence below a withheld-price heading', () => {
  const {run} = setup();
  for (const key of organs) {
    const dossier = run(`priceBlock(BY_ID.${key})`);
    assert.match(dossier, /class="price-value">Price withheld<\/div>/);
    assert.match(dossier, /Stored evidence only:.*recorded as ARS\/kg;.*recorded conversion/);
    assert.match(dossier, /Excluded from price rankings, value comparisons and buying estimates/);
    assert.match(dossier, /2026-10-07/);
    assert.match(dossier, /2026-08-31/);
    assert.match(dossier, /Out-of-stock/);
    assert.ok(dossier.includes(`$${snapshot.ar[key].usd_lb.toFixed(2)}/lb recorded conversion`));
  }
});

test('price table and cards consistently withhold the three prices without mutating evidence', () => {
  const {run, tables, cards, nodes} = setup();
  const before = run('JSON.stringify(PRICES)');
  run('renderPrices()');
  const {rows} = tables.get('price-table');
  assert.equal(rows.length, 36);
  assert.equal(rows.filter(row => row[1] === 'Price withheld').length, 3);
  for (const key of organs) {
    const row = rows.find(row => row[0] === `AR: ${snapshot.ar[key].label}`);
    assert.equal(row[1], 'Price withheld');
    assert.match(row[2], /Stored evidence only:.*recorded conversion/);
    assert.match(row[3], /Unverified unit scale.*Out-of-stock/);
  }
  for (const card of cards) assert.doesNotMatch(card.innerHTML, /\$|ARS\/kg/);
  assert.equal(run('JSON.stringify(PRICES)'), before);
  run('PRICES.us.ground_beef.unit_scale_unverified = true; renderPrices()');
  assert.doesNotMatch(nodes.get('#market-change').textContent, /%/);
});

test('browser contract rejects malformed flags instead of silently enabling prices', () => {
  const {run} = setup();
  for (const value of ['null', '0', '1', '"true"', '"false"', '[]', '{}']) {
    assert.throws(() => run(`PRICES.ar.rinon.unit_scale_unverified = ${value}; validatePrices(PRICES)`), /unit-scale flag/);
  }
  assert.doesNotThrow(() => run('PRICES.ar.rinon.unit_scale_unverified = false; validatePrices(PRICES)'));
});
