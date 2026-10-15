// A fixed October 15 selected-view fixture drives display checks; no provider calls or browser.
// Fixture retains prices/dates; omits source ledgers and previous_observation history throughout.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const section = (start, end) => {
  const a=html.indexOf(start), b=html.indexOf(end,a);
  assert.ok(a>=0 && b>a, start);
  return html.slice(a,b);
};
function setup() {
  const nodes=new Map(), tables=new Map();
  const snapshot=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/prices_coverage_2026_10_15.json'),'utf8'));
  const context=vm.createContext({snapshot, URL, location:{href:'https://example.test/?lang=en'},
    document:{querySelector:s=>{if(!nodes.has(s))nodes.set(s,{});return nodes.get(s);},querySelectorAll:()=>[]},
    renderScatter:()=>{},renderTable:(id,caption,headers,rows)=>tables.set(id,{caption,headers,rows})});
  vm.runInContext(fs.readFileSync(path.join(root,'assets/i18n.js'),'utf8')
    +section('const $ =','// 2. COW VISUALIZATIONS')
    +section('function fxLine(','let lastFocusedBeforeModal')
    +section('function safeUsd(','function renderTable(')
    +section('function renderPrices(','\nrenderReferenceTables();'),context);
  const run=s=>vm.runInContext(s,context);
  run('PRICES = validatePrices(snapshot)');
  return {run,nodes,tables,context};
}
test('Bola de lomo connects its own IPCVA observation without making round roast an exact match',()=>{
  const {run}=setup();
  assert.equal(run('BY_ID.bola.arSeries'),'bola_lomo');
  assert.equal(run('priceOf(BY_ID.bola).ar === PRICES.ar.bola_lomo'),true);
  assert.match(run('BY_ID.bola.relationship.type'),/generic.*equivalence unverified/);
  const dossier=run('priceBlock(BY_ID.bola)');
  assert.match(dossier,/IPCVA.*2026-09/s);
  assert.match(dossier,/19,332 ARS\/kg/);
});
test('coverage distinguishes dated, retained, withheld, native-only and missing in both languages without changing evidence',()=>{
  const {run,nodes,tables}=setup();
  // Pin a small explicit scenario so later refreshes cannot invalidate status expectations.
  run(`PRICES.ar={lomo:{...PRICES.ar.lomo},aguja:{...PRICES.ar.aguja,observation_status:'retained_after_error'},
    molleja:{...PRICES.ar.molleja,unit_scale_unverified:true},bola_lomo:{...PRICES.ar.bola_lomo,usd_lb:null}};
    PRICES.us={tenderloin:{...PRICES.us.tenderloin}}`);
  const before=run('JSON.stringify(PRICES)');
  for (const language of ['en','es-AR']) {
    run(`language=${JSON.stringify(language)};renderPrices()`);
    const rows=tables.get('coverage-table').rows;
    assert.equal(rows.length,24);
    assert.match(nodes.get('#coverage-summary').textContent,language==='en'?/Argentina: 2 dated observations · 1 retained references · 1 withheld · 20 missing/:/Argentina: 2 observaciones fechadas · 1 referencias conservadas · 1 precios no publicados · 20 faltantes/);
    assert.match(nodes.get('#coverage-summary').textContent,language==='en'?/1 of 24 cuts/:/1 de 24 cortes/);
    assert.match(rows.find(r=>r[0]==='Aguja')[1],language==='en'?/Retained reference.*2026-10-07/s:/Referencia conservada.*2026-10-07/s);
    assert.match(rows.find(r=>r[0]==='Bola de lomo')[1],language==='en'?/Native only · USD unavailable/:/Solo moneda de origen · USD no disponible/);
    assert.doesNotMatch(rows.find(r=>r[0]==='Mollejas')[1],/\$|ARS\/kg/);
    assert.match(rows.find(r=>r[0]==='Cogote')[1],language==='en'?/No connected price series/:/No hay una serie de precios conectada/);
    assert.match(rows.find(r=>r[0]==='Pecho')[1],language==='en'?/No observation in this snapshot/:/Sin observación en estos datos guardados/);
  }
  assert.equal(run('JSON.stringify(PRICES)'),before);
});
test('cards, tooltips and dossiers make retained, withheld and missing sides explicit',()=>{
  const {run}=setup();
  run("PRICES.ar.aguja.observation_status='retained_after_error'");
  for (const layout of ['compact','tooltip']) {
    const value=run(`priceLine(PRICES.ar.aguja,null,${JSON.stringify(layout)})`);
    assert.match(value,/Retained reference.*Carrefour AR/s);
    assert.match(value,/Missing/);
    assert.match(value,/Oct 7, 2026|2026-10-07/);
    const withheld=run(`priceLine(PRICES.ar.molleja,null,${JSON.stringify(layout)})`);
    assert.match(withheld,/Price withheld/);
    assert.doesNotMatch(withheld,/\$|ARS\/kg/);
  }
  assert.match(run('priceBlock(BY_ID.pecho)'),/data-price-state="missing".*No observation in this snapshot/s);
  assert.match(run('priceBlock(BY_ID.cogote)'),/No connected price series/);
  assert.match(run('priceBlock(BY_ID.lomo)'),/Original Carrefour observation.*2026-10-07/s);
});
test('coverage loading and unavailable states are not mistaken for missing source coverage',()=>{
  const {run,nodes,tables}=setup();
  run("PRICES=null;priceLoadState='loading';renderPrices()");
  assert.equal(nodes.get('#coverage-summary').textContent,'Loading stored prices…');
  assert.equal(tables.get('coverage-table').rows.length,1);
  run("priceLoadState='unavailable';language='es-AR';renderPrices()");
  assert.equal(nodes.get('#coverage-summary').textContent,'Datos de precios no disponibles');
  assert.doesNotMatch(nodes.get('#coverage-summary').textContent,/24|faltantes/);
});
test('every connected converted dossier price has a chart row and withheld organs do not enter the chart',()=>{
  const {run}=setup();
  assert.equal(run(`ALL_CUTS.every(c=>{
    const p=priceOf(c);
    return (!validPrice(p.ar)||PRICE_ROWS.some(r=>r.ar===c.arSeries))
      && (!validPrice(p.us)||PRICE_ROWS.some(r=>r.us===c.usSeries));
  })`),true);
  assert.equal(run("PRICE_ROWS.some(r=>['molleja','rinon','lengua'].includes(r.ar))"),false);
});
test('actual scatter callbacks draw retained markers hollow with text and dashed connectors',()=>{
  const {run,context}=setup();
  const attrs=[], texts=[];
  let chartRows=[];
  const selection=new Proxy({}, {get:(_,method)=>(...args)=>{
    if(method==='data') chartRows=args[0];
    if(method==='attr') attrs.push(args);
    if(method==='text') texts.push(args[0]);
    // Axis invocation only styles nested selections, which does not affect these callbacks.
    return selection;
  }});
  const scale=()=>{
    const f=x=>x;
    f.domain=f.nice=f.range=f.padding=()=>f;
    f.bandwidth=()=>10;
    return f;
  };
  const axis=()=>{const a=()=>{};a.ticks=a.tickSize=a.tickFormat=()=>a;return a;};
  context.d3={select:()=>selection,scaleLinear:scale,scaleBand:scale,axisBottom:axis,max:(xs,f)=>Math.max(...xs.map(f))};
  context.d3Available=()=>true;
  context.moveTooltip=context.hideTooltip=()=>{};
  vm.runInContext(section('function renderScatter()','const VALUE_MODEL ='),context);
  run('renderScatter()');
  const ar=chartRows.find(r=>r.ar?.source==='Carrefour AR');
  assert.ok(ar);
  assert.ok(attrs.some(([key,fn])=>key==='stroke-dasharray'&&typeof fn==='function'&&fn(ar)==='5 4'));
  assert.ok(attrs.some(([key,fn])=>key==='fill'&&typeof fn==='function'&&fn(ar)==='var(--bg)'));
  assert.ok(attrs.some(([key,fn])=>key==='data-price-state'&&typeof fn==='function'&&fn(ar)==='retained'));
  assert.ok(texts.some(fn=>typeof fn==='function'&&String(fn(ar)).endsWith(' *')));
  assert.equal(chartRows.some(r=>r.ar?.unit_scale_unverified),false);
});
test('visible illustration and source labels exist for every visual family and translate',()=>{
  const {run}=setup();
  const labels=['Fig. 01 / Editorial illustration','Anatomical illustration','Sourced observations · stored',
    'Illustrative model · fixed inputs','This illustration does not use the stored cut prices.',
    'Cut images are illustrations, not photographs of the surveyed products. Prices retain their source, date and status.',
    'Cut illustration · product specification unverified','Editorial trait illustration','Steak image: illustration.'];
  run("language='es-AR'");
  for(const label of labels) {
    assert.ok(html.includes(label),label);
    assert.notEqual(run(`t(${JSON.stringify(label)})`),label,label);
  }
  assert.match(html,/○ \/ \* Retained reference/);
});
test('fixed October 15 snapshot reports actual coverage and preserves every stored field while rendering',()=>{
  const {run,nodes,tables}=setup();
  const before=run('JSON.stringify(PRICES)');
  for(const language of ['en','es-AR']) {
    run(`language=${JSON.stringify(language)};renderPrices()`);
    assert.equal(tables.get('coverage-table').rows.length,24);
    const summary=nodes.get('#coverage-summary').textContent;
    assert.match(summary,language==='en'?/Argentina: 14 dated observations · 3 retained references · 3 withheld · 4 missing/:/Argentina: 14 observaciones fechadas · 3 referencias conservadas · 3 precios no publicados · 4 faltantes/);
    assert.match(summary,language==='en'?/United States: 14 dated observations · 0 retained references · 0 withheld · 10 missing/:/Estados Unidos: 14 observaciones fechadas · 0 referencias conservadas · 0 precios no publicados · 10 faltantes/);
    assert.match(summary,language==='en'?/13 of 24 cuts/:/13 de 24 cortes/);
  }
  assert.equal(run('JSON.stringify(PRICES)'),before);
});
