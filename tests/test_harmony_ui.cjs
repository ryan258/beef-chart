// Exercise actual catalog/search/price/lifecycle functions with bounded DOM doubles.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const section = (start, end) => {
  const a = html.indexOf(start), b = html.indexOf(end, a);
  assert.ok(a >= 0 && b > a, `Missing test boundary ${start}`);
  return html.slice(a, b);
};
function setup() {
  const nodes = new Map(), tables = new Map();
  const context = vm.createContext({URL, location:{href:'https://example.test/?lang=en'},
    snapshot:JSON.parse(fs.readFileSync(path.join(root, 'tests/fixtures/prices_legacy_2026_10_07.json'), 'utf8')),
    document:{querySelector:s => {if (!nodes.has(s)) nodes.set(s, {}); return nodes.get(s);}, querySelectorAll:() => []},
    renderScatter:() => {}, renderTable:(id, caption, headers, rows) => tables.set(id, {caption,headers,rows})});
  vm.runInContext(fs.readFileSync(path.join(root, 'assets/i18n.js'), 'utf8')
    + section('const $ =', '// 2. COW VISUALIZATIONS')
    + section('function fxLine(', 'let lastFocusedBeforeModal')
    + section('const CUT_ALIASES =', 'function cutButton(')
    + section('function safeUsd(', 'function renderTable(')
    + section('function renderPrices(', '\nrenderReferenceTables();'), context);
  return {run:s => vm.runInContext(s, context), nodes, tables, context};
}

test('both display languages find Spanish equivalents, English terms and aliases with identical IDs', () => {
  const {run} = setup();
  for (const [query, expected] of [['cuello',['cogote']], ['garrón delantero',['brazuelo']],
    ['ojo de bife',['bife-ancho']], ['tira de asado',['costillar']], ['achuras',['molleja','rinon','lengua']],
    ['tenderloin',['lomo']], ['NOT A CUT',[]], ['',[]]]) {
    for (const language of ['en','es-AR']) {
      run(`language = ${JSON.stringify(language)}`);
      assert.deepEqual(Array.from(run(`searchCuts(${JSON.stringify(query)}).map(c => c.id)`)), expected);
    }
  }
});

test('supported pecho and cuadrada observations reach their own dossiers without borrowing prices', () => {
  const {run} = setup();
  run('PRICES = validatePrices(snapshot)');
  for (const id of ['pecho','cuadrada']) {
    assert.equal(run(`priceOf(BY_ID.${id}).ar`), null);
    run(`PRICES.ar.${id} = {...PRICES.ar.lomo, label:${JSON.stringify(id)}, ars_kg:30000, usd_lb:9.01}`);
    assert.equal(run(`priceOf(BY_ID.${id}).ar.label`), id);
    assert.match(run(`priceBlock(BY_ID.${id})`), /Argentina.*\$9\.01/s);
  }
});

test('Spanish price table, benchmark, FX and axis labels use locale formatting without changing evidence', () => {
  const {run, tables, nodes} = setup();
  run("PRICES = validatePrices(snapshot); language = 'es-AR'");
  const before = run('JSON.stringify(PRICES)');
  run('renderPrices()');
  const ar = tables.get('price-table').rows.find(row => row[0].includes('Carne picada común'));
  assert.equal(ar[2], '10.613,08 ARS/kg');
  assert.match(ar[4], /1\.498,713132 ARS\/USD/);
  assert.match(nodes.get('#market-change').textContent, /0,6%/);
  assert.equal(run('currencyTick(5.5)'), 'US$5,5');
  assert.equal(run("t('Carrefour Argentina; delivery region unknown')"), 'Carrefour Argentina; región de entrega desconocida');
  assert.equal(run('JSON.stringify(PRICES)'), before);
  assert.equal(tables.get('price-table').rows.filter(row=>row[1]==='Precio no publicado').length, 3);
  run("language = 'en'");
  assert.equal(run('currencyTick(5.5)'), '$5.5');
});

test('loading and unavailable prices have distinct localized states and preserve reference access', () => {
  const {run, nodes} = setup();
  run("language = 'es-AR'; renderPrices()");
  assert.match(nodes.get('#market-price').textContent, /Cargando/);
  assert.match(run('priceBlock(BY_ID.lomo)'), /Cargando/);
  run("priceLoadState = 'unavailable'; renderPrices()");
  assert.match(nodes.get('#data-note').textContent, /No se pudieron cargar/);
  assert.match(run('priceBlock(BY_ID.lomo)'), /No se pudieron validar o cargar.*recargá/s);
  assert.doesNotMatch(run('priceBlock(BY_ID.lomo)'), /No hay un precio verificado/);
  run('PRICES = validatePrices(snapshot)');
  assert.match(run('priceBlock(BY_ID.cogote)'), /No hay un precio verificado/);
  assert.equal(run("searchCuts('ojo de bife')[0].id"), 'bife-ancho');
});

test('native price precision agrees across table, dossier, fallback and withheld evidence in both languages', () => {
  const {run, tables} = setup();
  run('PRICES = validatePrices(snapshot); PRICES.ar.lomo.ars_kg = 12345.678901; PRICES.ar.lomo.usd_lb = null');
  const before = run('JSON.stringify(PRICES)');
  for (const [language, number] of [['en','12,345.678901'], ['es-AR','12.345,678901']]) {
    run(`language = ${JSON.stringify(language)}; renderPrices()`);
    const row = tables.get('price-table').rows.find(row => row[0] === 'AR: Lomo');
    assert.equal(row[2], number + ' ARS/kg');
    assert.ok(run('priceBlock(BY_ID.lomo)').includes(number + ' ARS/kg'));
    assert.ok(run('priceLine(PRICES.ar.lomo, null)').includes(number + ' ARS/kg'));
    assert.ok(run('retainedPriceEvidence(PRICES.ar.lomo)').includes(number));
  }
  assert.equal(run('JSON.stringify(PRICES)'), before);
});

test('the treemap Other dialog rerenders from canonical copy when Spanish switches back to English', () => {
  const {run, context} = setup();
  let click;
  const selection = new Proxy({}, {get:(_, method) => (...args) => {
    if (method === 'on' && args[0] === 'click') click = args[1];
    return selection;
  }});
  const layout = () => {};
  layout.size = layout.padding = layout.round = () => layout;
  context.d3 = {select:()=>selection, hierarchy:()=>({sum:()=>({leaves:()=>[]})}), treemap:()=>layout};
  context.d3Available = () => true;
  context.moveTooltip = context.hideTooltip = () => {};
  context.focusModal = () => {};
  context.modalContent = {innerHTML:''};
  context.activeModal = null;
  vm.runInContext(section('const VALUE_MODEL =', '// 6. FLOATING TOOLTIP')
    + section('function openReferenceModal(', 'function openPrimalModal('), context);
  run("language = 'es-AR'; renderTreemap()");
  click({}, {data:{name:'Other', key:'shank'}});
  assert.match(context.modalContent.innerHTML, /Otros valores ilustrativos/);
  run("language = 'en'; activeModal()");
  assert.match(context.modalContent.innerHTML, /Other illustrative value.*This fixed 2%/s);
  assert.doesNotMatch(context.modalContent.innerHTML, /Otros valores/);
});

test('completed loading updates the open dossier while restoring recreated link focus and reading position', () => {
  const {run, nodes, context} = setup();
  let focusedOptions = null;
  const oldLink = {id:'', dataset:{}, getAttribute:()=>'https://example.test/recipe'};
  const close = {id:'modal-close-btn', dataset:{}, getAttribute:()=>null};
  const newLink = {...oldLink, focus:options=>{focusedOptions=options;context.document.activeElement=newLink;}};
  const modal = {open:true, querySelectorAll:()=>controls};
  let controls = [close, oldLink];
  let dossier = '';
  context.document.activeElement = oldLink;
  context.modalOverlay = modal;
  nodes.set('#cut-modal-card', {scrollTop:240});
  context.activeModal = () => {
    dossier = run('priceBlock(BY_ID.lomo)'); controls=[close,newLink];
    nodes.get('#cut-modal-card').scrollTop=0;context.document.activeElement=close;
  };
  vm.runInContext(section('function refreshActiveModal(', 'function updateHeaderOffset('), context);
  run('acceptPrices(validatePrices(snapshot))');
  assert.match(dossier, /\$8\.38/);
  assert.equal(context.document.activeElement, newLink);
  assert.equal(focusedOptions.preventScroll, true);
  assert.equal(nodes.get('#cut-modal-card').scrollTop, 240);
  assert.equal(run('priceLoadState'), 'ready');
});
