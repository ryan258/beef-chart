// Focused pure-helper checks. No browser, providers, production data or storage.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ReferenceTools = require('../assets/reference-tools.js');
const {cutUrl, savedCut, rememberCut, butcherNote} = ReferenceTools;
const quote = (overrides = {}) => ({manual:true, market:'ar', amount:18500,
  currency:'ARS', unit:'kg', date:'2026-01-15', ...overrides});

test('cut links retain unrelated parameters, select one cut and language, and clear the old section', () => {
  const url = new URL(cutUrl('http://127.0.0.1:8792/?view=table&cut=pecho&lang=en&view=source#prices', 'bife-costilla', 'es-AR'));
  assert.equal(url.origin, 'http://127.0.0.1:8792');
  assert.deepEqual(url.searchParams.getAll('view'), ['table', 'source']);
  assert.deepEqual(url.searchParams.getAll('cut'), ['bife-costilla']);
  assert.deepEqual(url.searchParams.getAll('lang'), ['es-AR']);
  assert.equal(url.hash, '');
  assert.equal(new URL(cutUrl(url.href, 'lomo', 'en')).searchParams.get('cut'), 'lomo');
});

test('malformed links, cut IDs, languages and executable URL schemes produce no link', () => {
  for (const id of ['', '../lomo', 'Lomo', '<img>', 'lomo x', null, 'a'.repeat(65)]) {
    assert.equal(cutUrl('https://example.test/', id, 'en'), null);
  }
  for (const language of ['', 'es', 'EN', null]) assert.equal(cutUrl('https://example.test/', 'lomo', language), null);
  for (const href of ['not a URL', '/relative', 'javascript:alert(1)', 'data:text/html,lomo', null]) {
    assert.equal(cutUrl(href, 'lomo', 'en'), null);
  }
});

test('saved cuts round-trip only for an existing cut and valid language, without retaining extra data', () => {
  const values = new Map();
  const storage = {getItem:key => values.get(key) ?? null, setItem:(key, value) => values.set(key, value)};
  assert.equal(savedCut(storage, ['lomo']), null);
  assert.equal(rememberCut(storage, 'lomo', 'es-AR'), true);
  assert.deepEqual(savedCut(storage, ['lomo', 'pecho']), {id:'lomo', language:'es-AR'});
  assert.equal(savedCut(storage, ['pecho']), null);
  values.set('beef-chart-last-cut', JSON.stringify({id:'lomo', language:'en', unrelated:'discard'}));
  assert.deepEqual(savedCut(storage, ['lomo']), {id:'lomo', language:'en'});
  assert.equal(rememberCut(storage, '../lomo', 'en'), false);
  assert.equal(rememberCut(storage, 'lomo', 'es'), false);
  assert.equal(values.size, 1);
});

test('corrupt, unavailable and denied storage never blocks lookup or remembering', () => {
  for (const raw of ['{', 'null', '[]', '1', '"lomo"', '{}', '{"id":"lomo"}',
    '{"id":"lomo","language":"es"}', '{"id":"../lomo","language":"en"}']) {
    assert.equal(savedCut({getItem:() => raw}, ['lomo']), null);
  }
  const denied = {getItem:() => {throw new Error('denied');}, setItem:() => {throw new Error('denied');}};
  for (const storage of [denied, null, {}]) {
    assert.equal(savedCut(storage, ['lomo']), null);
    assert.equal(rememberCut(storage, 'lomo', 'en'), false);
  }
  assert.equal(savedCut({getItem:() => '{"id":"lomo","language":"en"}'}, null), null);
});

test('butcher notes preserve bilingual names and literal text without HTML interpretation', () => {
  const malicious = '<img src=x onerror=alert(1)> & "local"';
  const cut = Object.freeze({name:'Vacío', usName:'Abdominal-wall cut', relationship:malicious,
    preparation:'Slice across the grain.'});
  const note = butcherNote(cut, 'en');
  assert.equal(note, `Cut: Vacío\nU.S. reference: Abdominal-wall cut\nRelationship: ${malicious}\nPreparation: Slice across the grain.`);
  assert.match(butcherNote(cut, 'es-AR'), /^Corte: Vacío\nReferencia de EE\. UU\.: Abdominal-wall cut\nRelación: <img/);
  assert.doesNotMatch(note, /Manual quote|unverified|USD|ARS/);
  assert.equal(butcherNote(null, 'en'), '');
  assert.equal(butcherNote({name:'Lomo'}, 'es'), '');
});

test('manual note prices keep native amounts, dates and units in both languages without conversion or mutation', () => {
  const quotes = Object.freeze([Object.freeze(quote()), Object.freeze(quote({market:'us', amount:8.5, currency:'USD', unit:'lb'}))]);
  const cut = Object.freeze({name:'Lomo', usName:'Tenderloin', quotes});
  const before = JSON.stringify(cut);
  const english = butcherNote(cut, 'en'), spanish = butcherNote(cut, 'es-AR');
  assert.match(english, /Manual quote — Argentina: 18,500 ARS\/kg \(2026-01-15\)/);
  assert.match(english, /Manual quote — United States: 8\.50 USD\/lb \(2026-01-15\)/);
  assert.match(english, /Availability and exact product specifications unverified\.$/);
  assert.match(spanish, /Precio manual — Argentina: 18\.500 ARS\/kg \(2026-01-15\)/);
  assert.match(spanish, /Precio manual — Estados Unidos: 8,50 USD\/lb \(2026-01-15\)/);
  assert.match(spanish, /Disponibilidad y especificaciones exactas del producto sin verificar\.$/);
  assert.equal(JSON.stringify(cut), before);
  assert.equal((english.match(/ARS\/kg/g) || []).length, 1);
  assert.equal((english.match(/USD\/lb/g) || []).length, 1);
});

test('incomplete, invalid, withheld and nonmanual quotes never enter butcher notes', () => {
  const invalid = [null, {}, quote({manual:false}), quote({manual:undefined}), quote({withheld:true}),
    quote({unit_scale_unverified:true}), quote({status:'withheld'}), quote({observation_status:'withheld'}),
    quote({market:'AR'}), quote({amount:0}), quote({amount:-1}), quote({amount:'18500'}),
    quote({amount:true}), quote({amount:Infinity}), quote({amount:1e10}), quote({date:null}),
    quote({date:'2026-02-30'}), quote({date:'2026-1-15'}), quote({date:'2999-01-01'}),
    quote({date:'0000-01-01'}), quote({currency:'USD'}), quote({unit:'lb'}), quote({unit:null})];
  assert.equal(butcherNote({name:'Lomo', quotes:invalid}, 'en'), 'Cut: Lomo');
  const mixed = butcherNote({name:'Lomo', quotes:[...invalid, quote()]}, 'en');
  assert.equal((mixed.match(/Manual quote/g) || []).length, 1);
  assert.match(mixed, /18,500 ARS\/kg/);
});

test('the same helper API is available as a browser global without CommonJS', () => {
  const context = vm.createContext({URL, Intl});
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../assets/reference-tools.js'), 'utf8'), context);
  assert.equal(typeof context.ReferenceTools.cutUrl, 'function');
  assert.equal(typeof context.ReferenceTools.savedCut, 'function');
  assert.equal(typeof context.ReferenceTools.rememberCut, 'function');
  assert.equal(context.ReferenceTools.butcherNote({name:'Pecho'}, 'en'), 'Cut: Pecho');
});
