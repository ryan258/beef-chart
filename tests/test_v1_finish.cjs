// Actual v1 UI integration with bounded DOM doubles; no D3, network or real clipboard.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const snapshotText = fs.readFileSync(path.join(root, 'data/prices.json'), 'utf8');
const section = (start, end) => {
  const a = html.indexOf(start), b = html.indexOf(end, a);
  assert.ok(a >= 0 && b > a, `Missing test boundary ${start}`);
  return html.slice(a, b);
};

function setup({href = 'https://example.test/?view=table&lang=en#explore', saved = null, deniedStorage = false} = {}) {
  const nodes = new Map(), tables = new Map(), panels = [], values = new Map();
  if (saved !== null) values.set('beef-chart-last-cut', JSON.stringify(saved));
  class Node {
    constructor(id = '') {
      this.id = id; this.hidden = false; this.open = false; this.isConnected = true;
      this.dataset = {}; this.listeners = new Map(); this.children = new Map();
      this.classList = {add() {}, remove() {}}; this.value = ''; this.textContent = '';
      this.scrollTop = 0;
    }
    set innerHTML(value) {
      this.markup = value;
      if (this.id === 'modal-content') {
        for (const panel of panels) {
          panel.isConnected = false;
          for (const child of panel.children.values()) child.isConnected = false;
        }
        if (nodes.has('#cut-modal-card')) nodes.get('#cut-modal-card').scrollTop = 0;
      }
      // Only enumerate authored controls. Values assigned to textarea.value never become markup.
      for (const match of value.matchAll(/<([a-z]+)\b([^>]*\bid="([^"]+)"[^>]*)>/g)) {
        const child = new Node(match[3]); child.hidden = /\bhidden\b/.test(match[2]);
        child.tagName = match[1];
        this.children.set('#' + child.id, child);
      }
    }
    get innerHTML() { return this.markup || ''; }
    querySelector(selector) { return this.children.get(selector); }
    querySelectorAll() {
      return [nodes.get('#modal-close-btn'), ...(panels.at(-1)?.children.values() || [])]
        .filter(node => node?.isConnected && (node.id === 'modal-close-btn' || ['button','textarea'].includes(node.tagName)));
    }
    setAttribute(name, value) { this[name] = value; }
    getAttribute(name) { return this[name] ?? null; }
    addEventListener(name, handler) { this.listeners.set(name, handler); }
    click() { return this.listeners.get('click')?.(); }
    focus() { context.document.activeElement = this; }
    select() { this.selected = true; this.selectionStart = 0; this.selectionEnd = this.value.length; }
    setSelectionRange(start, end) { this.selectionStart = start; this.selectionEnd = end; }
    showModal() { this.open = true; }
    close() { this.open = false; }
    insertAdjacentElement(position, panel) { assert.equal(position, 'afterend'); panels.push(panel); }
  }
  const storage = {getItem:key => values.get(key) ?? null, setItem:(key, value) => values.set(key, value)};
  const context = vm.createContext({URL, snapshot:JSON.parse(snapshotText),
    location:{href}, history:{replaceState:(_state, _title, url) => { context.location.href = String(url); }},
    navigator:{clipboard:{writeText:async () => {}}},
    document:{documentElement:{}, querySelector:selector => {
      const currentPanel = panels.at(-1);
      if (currentPanel?.isConnected && currentPanel.children.has(selector)) return currentPanel.children.get(selector);
      if (!nodes.has(selector)) nodes.set(selector, new Node(selector.slice(1)));
      return nodes.get(selector);
    }, querySelectorAll:() => [], createElement:() => new Node()},
    renderScatter() {}, renderModalRadar() {}, renderDirectories() {}, renderCowMaps() {},
    renderSankey() {}, renderTreemap() {}, renderReferenceTables() {}, hideTooltip() {},
    lastSearch:null,
    renderTable:(id, caption, headers, rows) => tables.set(id, {caption, headers, rows})});
  Object.defineProperty(context, 'localStorage', {get:() => {
    if (deniedStorage) throw new Error('Storage denied');
    return storage;
  }});
  const run = source => vm.runInContext(source, context);
  for (const file of ['assets/i18n.js', 'assets/reference-tools.js', 'assets/snapshot-summary.js', 'assets/manual-prices.js']) {
    run(fs.readFileSync(path.join(root, file), 'utf8'));
  }
  run(section('const $ =', '// 2. COW VISUALIZATIONS')
    + "\nconst modalOverlay = $('#cut-modal-overlay'); const modalContent = $('#modal-content');\n"
    + section('function fxLine(', 'function openReferenceModal(')
    + section('function openCutModal(', 'function renderModalRadar(')
    + section('function safeUsd(', 'function renderTable(')
    + section('function renderPrices(', '\nrenderReferenceTables();')
    + section('function refreshActiveModal(', 'async function readPriceFile(')
    + section('function setLanguage(', "$$('[data-language]')")
    + section('rememberedCut = ReferenceTools.savedCut(', "window.addEventListener('popstate'"));
  return {run, context, nodes, tables, panels, values, storage};
}

test('opening, linking and explicitly resuming a dossier preserve the cut and its language', () => {
  const {run, context, nodes, values} = setup();
  run("setLanguage('es-AR'); openCutModal(BY_ID.vacio)");
  const linked = new URL(context.location.href);
  assert.equal(linked.searchParams.get('cut'), 'vacio');
  assert.equal(linked.searchParams.get('lang'), 'es-AR');
  assert.equal(linked.searchParams.get('view'), 'table');
  assert.equal(linked.hash, '');
  assert.equal(nodes.get('#cut-modal-overlay').open, true);
  assert.equal(nodes.get('#resume-cut').hidden, false);
  assert.match(nodes.get('#resume-cut').textContent, /Vacío/);
  const saved = JSON.parse(values.get('beef-chart-last-cut'));
  assert.deepEqual(saved, {id:'vacio', language:'es-AR'});

  const reopened = setup({href:context.location.href});
  reopened.run('syncCutFromLocation()');
  assert.equal(reopened.run('activeCutId'), 'vacio');
  assert.equal(reopened.run('language'), 'es-AR');
  const resumed = setup({saved});
  assert.equal(resumed.nodes.get('#cut-modal-overlay').open, false);
  resumed.nodes.get('#resume-cut').click();
  assert.equal(resumed.run('activeCutId'), 'vacio');
  assert.equal(resumed.run('language'), 'es-AR');
  assert.equal(new URL(resumed.context.location.href).searchParams.get('cut'), 'vacio');
});

test('denied storage and malformed or prototype-like cut links leave reference lookup usable', () => {
  const denied = setup({deniedStorage:true});
  assert.doesNotThrow(() => denied.run('openCutModal(BY_ID.lomo)'));
  assert.equal(denied.run('activeCutId'), 'lomo');
  for (const id of ['constructor', '__proto__', 'toString', '../lomo', '<img src=x>', 'missing-cut']) {
    const {run, context, nodes} = setup({href:`https://example.test/?lang=es-AR&cut=${encodeURIComponent(id)}`});
    assert.doesNotThrow(() => run('syncCutFromLocation()'));
    assert.equal(run('activeCutId'), null);
    assert.equal(nodes.get('#cut-modal-overlay').open, false);
    assert.match(nodes.get('#cut-link-status').textContent, /Ese enlace/);
    assert.doesNotMatch(nodes.get('#cut-link-status').textContent, /<img/);
    context.location.href = 'https://example.test/?lang=en&cut=lomo';
    run('syncCutFromLocation()');
    assert.equal(run('activeCutId'), 'lomo');
  }
  const invalidSaved = setup({saved:{id:'constructor', language:'en'}});
  assert.equal(invalidSaved.nodes.get('#resume-cut').hidden, true);
  const warning = setup({href:'https://example.test/?lang=en&cut=typo'});
  warning.run('syncCutFromLocation()');
  assert.match(warning.nodes.get('#cut-link-status').textContent, /That cut link is unknown/);
  warning.run("setLanguage('es-AR')");
  assert.match(warning.nodes.get('#cut-link-status').textContent, /Ese enlace/);
  warning.run('openCutModal(BY_ID.lomo)');
  assert.equal(warning.nodes.get('#cut-link-status').textContent, '');
});

test('every dossier note uses its selected manual native quote and leaves automatic evidence untouched in both languages', () => {
  const {run} = setup();
  const before = run('JSON.stringify(snapshot)');
  assert.equal(run('ALL_CUTS.length'), 24);
  for (const language of ['en', 'es-AR']) {
    run(`language = ${JSON.stringify(language)}; PRICES = validatePrices(snapshot, '2026-10-16T12:00:00Z')`);
    for (const note of run('ALL_CUTS.map(butcherNoteFor)')) {
      assert.doesNotMatch(note, /Manual quote|Precio manual|ARS\/kg|USD\/lb/);
    }
    run(`const quotes${language === 'en' ? 'En' : 'Es'} = {
      ar:ALL_CUTS.map((cut, i) => ({date:'2026-01-15', item:'AR local quote', machine_name:cut.id, price:1000 + i, currency:'ARS', unit:'kg'})),
      us:ALL_CUTS.map((cut, i) => ({date:'2026-01-14', item:'US local quote', machine_name:cut.id, price:3.5 + i, currency:'USD', unit:'lb'}))
    }; PRICES = ManualPrices.apply(snapshot, quotes${language === 'en' ? 'En' : 'Es'}, ALL_CUTS, '2026-01-15').prices`);
    const cuts = run('ALL_CUTS');
    for (let index = 0; index < cuts.length; index++) {
      const cut = cuts[index];
      const note = run(`butcherNoteFor(BY_ID[${JSON.stringify(cut.id)}])`);
      const amount = new Intl.NumberFormat(language, {maximumFractionDigits:6}).format(1000 + index);
      const usd = new Intl.NumberFormat(language, {minimumFractionDigits:2, maximumFractionDigits:6}).format(3.5 + index);
      assert.ok(note.includes(cut.n), cut.id);
      assert.ok(note.includes(cut.eq), cut.id);
      assert.ok(note.includes(run(`t(BY_ID[${JSON.stringify(cut.id)}].relationship.type)`)), cut.id);
      assert.ok(note.includes(run(`t(BY_ID[${JSON.stringify(cut.id)}].info)`)), cut.id);
      assert.ok(note.includes(`${amount} ARS/kg (2026-01-15)`), cut.id);
      assert.ok(note.includes(`${usd} USD/lb (2026-01-14)`), cut.id);
      assert.equal((note.match(/ARS\/kg/g) || []).length, 1);
      assert.equal((note.match(/USD\/lb/g) || []).length, 1);
      assert.doesNotMatch(note, /IPCVA|BLS|Carrefour|2026-09|2026-10-07/);
    }
    run('PRICES.ar.lomo.unit_scale_unverified = true');
    assert.doesNotMatch(run('butcherNoteFor(BY_ID.lomo)'), /ARS\/kg/);
    assert.match(run('butcherNoteFor(BY_ID.lomo)'), /USD\/lb/);
    assert.equal(run('JSON.stringify(snapshot)'), before);
    run('PRICES = snapshot');
    assert.doesNotMatch(run('butcherNoteFor(BY_ID.lomo)'), /ARS\/kg|USD\/lb/);
  }
});

test('actual copy handlers write plain text or select the complete note/link on clipboard rejection', async () => {
  const {run, context, panels} = setup();
  const copied = [];
  context.navigator.clipboard.writeText = async value => { copied.push(value); };
  for (const language of ['en', 'es-AR']) {
    run(`language = ${JSON.stringify(language)}; renderCutTools({...BY_ID.lomo,
      n:'<img src=x onerror=alert(1)>', eq:'<b>literal</b>', info:'<script>literal</script>'})`);
    const panel = panels.at(-1), note = panel.querySelector('#butcher-note');
    assert.match(note.value, /<img src=x onerror=alert\(1\)>/);
    assert.match(note.value, /<script>literal<\/script>/);
    assert.doesNotMatch(panel.innerHTML, /<img src=x|<script>literal/);
    await panel.querySelector('#copy-butcher-note').click();
    assert.equal(copied.at(-1), note.value);
    assert.equal(panel.querySelector('#cut-copy-status').textContent, run("t('Note copied.')"));
    context.navigator.clipboard.writeText = async () => { throw new Error('Permission denied'); };
    await panel.querySelector('#copy-butcher-note').click();
    assert.equal(note.selected, true);
    assert.equal(context.document.activeElement, note);
    assert.equal(panel.querySelector('#cut-copy-status').textContent,
      run("t('Clipboard unavailable. Text selected; use your usual copy command.')"));
    panel.querySelector('#copy-cut-link').click();
    await new Promise(resolve => setImmediate(resolve));
    const link = panel.querySelector('#cut-link-fallback');
    assert.equal(link.hidden, false);
    assert.equal(panel.querySelector('#cut-link-fallback-label').hidden, false);
    assert.equal(link.selected, true);
    assert.equal(new URL(link.value).searchParams.get('cut'), 'lomo');
    assert.equal(new URL(link.value).searchParams.get('lang'), language);
    context.navigator.clipboard.writeText = async value => { copied.push(value); };
    panel.querySelector('#copy-cut-link').click();
    await new Promise(resolve => setImmediate(resolve));
    assert.equal(copied.at(-1), link.value);
    assert.equal(panel.querySelector('#cut-copy-status').textContent, run("t('Cut link copied.')"));
  }
});

test('price arrival preserves a revealed clipboard fallback, focus, selection and reading position', async () => {
  const {run, context, nodes, panels} = setup();
  context.navigator.clipboard.writeText = async () => { throw new Error('Permission denied'); };
  run('openCutModal(BY_ID.vacio)');
  panels.at(-1).querySelector('#copy-cut-link').click();
  await new Promise(resolve => setImmediate(resolve));
  const initial = panels.at(-1).querySelector('#cut-link-fallback');
  assert.equal(initial.hidden, false);
  assert.equal(context.document.activeElement, initial);
  assert.equal(initial.selectionStart, 0);
  assert.equal(initial.selectionEnd, initial.value.length);
  run("$('#cut-modal-card').scrollTop = 240; acceptPrices(validatePrices(snapshot, '2026-10-16T12:00:00Z'))");
  const replacement = panels.at(-1).querySelector('#cut-link-fallback');
  assert.notEqual(replacement, initial);
  assert.equal(replacement.hidden, false);
  assert.equal(panels.at(-1).querySelector('#cut-link-fallback-label').hidden, false);
  assert.equal(replacement.value, initial.value);
  assert.equal(context.document.activeElement, replacement);
  assert.equal(replacement.selectionStart, 0);
  assert.equal(replacement.selectionEnd, replacement.value.length);
  assert.equal(nodes.get('#cut-modal-card').scrollTop, 240);
  assert.equal(panels.at(-1).querySelector('#cut-copy-status').textContent,
    run("t('Clipboard unavailable. Text selected; use your usual copy command.')"));
});

test('navigation reaches the comparison/value evidence and the rendered summary follows source dates in both languages', () => {
  assert.match(html, /<a\b[^>]*href="#data-scatter"[^>]*data-i18n>Compare<\/a>/);
  assert.match(html, /id="data-scatter"/);
  assert.match(html, /id="read-value-shares"[^>]*href="#value-data"[^>]*data-i18n>Read Value Shares →<\/a>/);
  assert.match(html, /<script src="assets\/reference-tools\.js"><\/script>/);
  assert.match(html, /<script src="assets\/snapshot-summary\.js"><\/script>/);
  const {run, context, nodes} = setup();
  nodes.get('#read-value-shares').click();
  assert.equal(nodes.get('#value-data').open, true);
  context.fixture = {generated_at:'2026-08-11T12:00:00Z', fx:{}, source_status:{},
    ar:{lomo:{label:'Lomo', source:'IPCVA', period:'2026-06', ars_kg:1234},
      retained:{label:'Retained', source:'Carrefour AR', period:'2026-05-09', ars_kg:2000, observation_status:'retained_no_match'}},
    us:{ground_beef:{label:'Ground beef', source:'BLS', period:'2026-07', usd_lb:7},
      tenderloin:{label:'Tenderloin', source:'USDA ad survey', period:'2026-08-08', usd_lb:8,
        effective_start:'2026-08-02', effective_end:'2026-08-08'}}};
  for (const language of ['en', 'es-AR']) {
    run(`language = ${JSON.stringify(language)}; PRICES = fixture; renderPrices()`);
    const summary = nodes.get('#snapshot-summary').textContent;
    assert.match(summary, /2026-08-11/);
    assert.match(summary, /IPCVA.*2026-06/);
    assert.match(summary, /BLS.*2026-07/);
    assert.match(summary, /USDA.*2026-08-02–2026-08-08/);
    assert.match(summary, /Carrefour.*1 \(2026-05-09\)/);
    assert.equal(summary, run('SnapshotSummary.summarize(PRICES, language)'));
    assert.match(nodes.get('#data-note').textContent, language === 'en'
      ? /IPCVA is primary for the Argentine cuts it covers/ : /IPCVA es la fuente principal/);
    run("fixture.ar.lomo.period = '2026-04'; renderPrices()");
    assert.match(nodes.get('#snapshot-summary').textContent, /IPCVA.*2026-04/);
    context.fixture.ar.lomo.period = '2026-06';
    assert.equal(run("t('Compare')"), language === 'en' ? 'Compare' : 'Compará');
    assert.equal(run("t('Read Value Shares →')"), language === 'en' ? 'Read Value Shares →' : 'Leé las proporciones de valor →');
  }
});
