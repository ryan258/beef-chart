// Focused manual-price integration checks. Fetch/DOM/D3 are local doubles; no network or browser.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ManualPrices = require('../assets/manual-prices.js');
const root = path.join(__dirname,'..');
const html = fs.readFileSync(path.join(root,'index.html'),'utf8');
const baseline = JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/prices_coverage_2026_10_15.json'),'utf8'));
// Include a source ledger: the selected-view fixture deliberately omits it.
baseline.ar_sources = {
  IPCVA:Object.fromEntries(Object.entries(baseline.ar).filter(([,p])=>p.source==='IPCVA').map(([k,p])=>[k,structuredClone(p)])),
  'Carrefour AR':structuredClone(baseline.carrefour_originals)
};
const section = (start,end) => {
  const a=html.indexOf(start),b=html.indexOf(end,a);
  assert.ok(a>=0 && b>a,start);
  return html.slice(a,b);
};
const quote = (machine_name,price=18500,currency='ARS',unit='kg',date='2026-10-15',item='Local quote') => ({date,item,machine_name,price,currency,unit});
function freeze(value) {
  if(value && typeof value==='object') { Object.values(value).forEach(freeze); Object.freeze(value); }
  return value;
}
function setup(file={ar:[],us:[]}) {
  const snapshot=freeze(structuredClone(baseline));
  const nodes=new Map(),tables=new Map(),cards=['lomo','pecho','molleja'].map(id=>({
    dataset:{},closest:()=>({dataset:{cut:id}})
  }));
  const bodies=new Map([['data/prices.json',JSON.stringify(snapshot)],['data/manual-prices.json',JSON.stringify(file)]]);
  const requests=[];
  const context=vm.createContext({snapshot,file,ManualPrices,URL,AbortController,setTimeout,clearTimeout,
    location:{href:'https://example.test/?lang=en'},
    document:{querySelector:s=>{if(!nodes.has(s))nodes.set(s,{});return nodes.get(s);},querySelectorAll:s=>s==='.cut-card-price'?cards:[]},
    fetch:async(url,options)=>{requests.push({url,options});return {ok:bodies.has(url),text:async()=>bodies.get(url)};},
    renderScatter:()=>{},refreshActiveModal:()=>{},
    renderTable:(id,caption,headers,rows)=>tables.set(id,{caption,headers,rows})});
  vm.runInContext(fs.readFileSync(path.join(root,'assets/i18n.js'),'utf8')
    +section('const $ =','// 2. COW VISUALIZATIONS')
    +section('function fxLine(','let lastFocusedBeforeModal')
    +section('function safeUsd(','function renderTable(')
    +section('function renderPrices(','\nrenderReferenceTables();')
    +section('function acceptPrices(','function updateHeaderOffset('),context);
  const run=code=>vm.runInContext(code,context);
  run('PRICES=validatePrices(snapshot)');
  const apply=()=>run("const result=ManualPrices.apply(snapshot,file,ALL_CUTS,'2026-10-15');PRICES=result.prices;manualPriceCount=result.count;renderPrices()");
  return {run,apply,context,snapshot,nodes,tables,cards,bodies,requests};
}
test('numeric amounts retain explicit currency/unit and reject coercion and unsupported pairs',()=>{
  assert.deepEqual(ManualPrices.parsePrice(18500,'ARS','kg'),{ars_kg:18500,usd_lb:null,native_currency:'ARS',native_unit:'kg'});
  assert.deepEqual(ManualPrices.parsePrice(8.5,'USD','lb'),{ars_kg:null,usd_lb:8.5,native_currency:'USD',native_unit:'lb'});
  for(const value of ['18500','18500 ARS/kilo',true,null,0,-1,NaN,Infinity,1e10]) assert.throws(()=>ManualPrices.parsePrice(value,'ARS','kg'),/positive number/);
  for(const [currency,unit] of [['ARS','lb'],['USD','kg'],['$','lb'],['ars','kg'],['USD','pound'],['USD',null]]) assert.throws(()=>ManualPrices.parsePrice(10,currency,unit));
});
test('overrides preserve complete source records, dates, FX, ledger, original archive and input bytes',()=>{
  const h=setup({ar:[quote('lomo')],us:[quote('tenderloin',8.5,'USD','lb')]});
  const before=JSON.stringify(h.snapshot),fileBefore=JSON.stringify(h.context.file);
  h.apply();
  assert.equal(h.run('PRICES.ar.lomo.ars_kg'),18500);
  assert.equal(h.run('PRICES.ar.lomo.usd_lb'),null);
  assert.equal(h.run('PRICES.ar.lomo.fx_date'),null);
  assert.equal(h.run('PRICES.ar.lomo.fx_ars_per_usd'),null);
  assert.equal(h.run('PRICES.us.tenderloin.usd_lb'),8.5);
  assert.equal(h.run('PRICES.manual_originals.ar.lomo === snapshot.ar.lomo'),true);
  assert.equal(h.run('PRICES.manual_originals.us.tenderloin === snapshot.us.tenderloin'),true);
  assert.equal(h.run('PRICES.ar_sources === snapshot.ar_sources'),true);
  assert.equal(h.run('PRICES.carrefour_originals === snapshot.carrefour_originals'),true);
  assert.equal(h.run('PRICES.fx === snapshot.fx'),true);
  assert.equal(h.run('PRICES.ar.aguja === snapshot.ar.aguja'),true);
  assert.equal(JSON.stringify(h.snapshot),before);
  assert.equal(JSON.stringify(h.context.file),fileBefore);
});
test('English and Spanish cards, tooltips, dossiers and coverage show native amounts and manual labels',()=>{
  const h=setup({ar:[quote('lomo',18500,'ARS','kg','2026-10-14','Friend’s local lomo')],us:[quote('tenderloin',8.5,'USD','lb')]});
  h.apply();
  for(const language of ['en','es-AR']) {
    h.run(`language=${JSON.stringify(language)};renderPrices()`);
    const native=language==='en'?'18,500 ARS/kg':'18.500 ARS/kg';
    const dollars=language==='en'?'$8.50':'US$8,50';
    const label=language==='en'?/Manual quote/:/Precio manual/;
    const card=h.cards[0].innerHTML;
    assert.ok(card.includes(native));assert.ok(card.includes(dollars));assert.match(card,label);
    const tooltip=h.run("priceLine(priceOf(BY_ID.lomo).ar,priceOf(BY_ID.lomo).us,'tooltip')");
    assert.ok(tooltip.includes(native));assert.match(tooltip,label);
    const dossier=h.run('priceBlock(BY_ID.lomo)');
    assert.ok(dossier.includes(native));assert.ok(dossier.includes(dollars));assert.match(dossier,/2026-10-14/);
    assert.match(dossier,/Friend’s local lomo/);
    const row=h.tables.get('coverage-table').rows.find(r=>r[0]==='Lomo');
    assert.ok(row[1].includes(native));assert.match(row[1],label);assert.ok(row[2].includes(dollars));
    assert.match(h.nodes.get('#manual-price-status').textContent,language==='en'?/2 manual quotes selected/:/seleccionaron 2 precios manuales/);
    assert.match(h.nodes.get('#coverage-summary').textContent,language==='en'?/1 manual quotes\./:/1 precios manuales\./);
  }
});
test('overridden automatic observations remain visible with their own original source/date/FX evidence',()=>{
  const h=setup({ar:[quote('lomo')],us:[quote('tenderloin',8.5,'USD','lb')]});h.apply();
  const dossier=h.run('priceBlock(BY_ID.lomo)');
  assert.equal((dossier.match(/Automatic observation beneath manual quote/g)||[]).length,2);
  assert.ok(dossier.includes(h.snapshot.ar.lomo.source));assert.ok(dossier.includes(h.snapshot.ar.lomo.period));
  assert.ok(dossier.includes(h.snapshot.us.tenderloin.source));assert.ok(dossier.includes(h.snapshot.us.tenderloin.period));
  assert.match(dossier,/Original Carrefour observation.*2026-10-07/s);
  assert.ok(dossier.includes(h.snapshot.carrefour_originals.lomo.fx_date));
  const rows=h.tables.get('price-table').rows;
  assert.ok(rows.some(r=>r[0]==='AR: Local quote'&&r[2]==='18,500 ARS/kg'&&r[3].includes('Manual entry')));
  assert.ok(rows.some(r=>r[0]==='US: Local quote'&&r[1]==='$8.50/lb'));
  for(const [country,key] of [['ar','lomo'],['us','tenderloin']]) {
    const original=h.snapshot[country][key];
    assert.ok(rows.some(r=>r[0]===`${country.toUpperCase()}: ${original.label}`&&r[3].includes(original.source)&&r[3].includes(original.period)));
  }
  assert.ok(rows.some(r=>r[0].startsWith('Original Carrefour observation:')&&r[3].includes('2026-10-07')));
});
test('missing connections can be filled and a new organ quote never clears original withholding',()=>{
  const h=setup({ar:[quote('cogote'),quote('pecho'),quote('molleja')],us:[quote('molleja',9.75,'USD','lb')]});h.apply();
  assert.equal(h.run('priceOf(BY_ID.cogote).ar.ars_kg'),18500);
  assert.equal(h.run('priceOf(BY_ID.pecho).ar.ars_kg'),18500);
  assert.match(h.cards[1].innerHTML,/18,500 ARS\/kg/);
  assert.match(h.cards[2].innerHTML,/US \$9\.75\/lb/);
  const dossier=h.run('priceBlock(BY_ID.molleja)');
  assert.match(dossier,/Manual quote/);assert.match(dossier,/Price withheld/);
  assert.equal(h.run('PRICES.carrefour_originals.molleja.unit_scale_unverified'),true);
  assert.equal(h.run('PRICES.manual_originals.ar.molleja.unit_scale_unverified'),true);
  assert.equal(h.run('JSON.stringify(PRICES.carrefour_originals.molleja)'),JSON.stringify(h.snapshot.carrefour_originals.molleja));
});
test('latest date and equal-date row order select by canonical key without altering history rows',()=>{
  const file={ar:[quote('lomo',10000,'ARS','kg','2026-10-12'),quote('lomo',19000),quote('lomo',18000,'ARS','kg','2026-10-13'),quote('lomo',20000)],us:[quote('lomo',10,'USD','lb'),quote('tenderloin',11,'USD','lb')]};
  const h=setup(file);h.apply();
  assert.equal(h.run('manualPriceCount'),2);
  assert.equal(h.run('PRICES.ar.lomo.ars_kg'),20000);
  assert.equal(h.run('PRICES.us.tenderloin.usd_lb'),11);
  assert.equal(file.ar.length,4);assert.equal(file.us.length,2);
});
test('normal file loader displays valid quotes; removing them restores automatic selection',async()=>{
  const h=setup({ar:[quote('lomo')],us:[]});
  await h.run('loadPriceFiles()');
  assert.equal(h.run('PRICES.ar.lomo.manual_entry'),true);
  assert.match(h.cards[0].innerHTML,/18,500 ARS\/kg/);
  assert.ok(h.requests.every(r=>r.options.cache==='no-store'&&r.options.signal instanceof AbortSignal));
  h.bodies.set('data/manual-prices.json',JSON.stringify({ar:[],us:[]}));
  await h.run('loadPriceFiles()');
  assert.equal(h.run('JSON.stringify(PRICES.ar.lomo)'),JSON.stringify(h.snapshot.ar.lomo));
  assert.equal(h.run('manualPriceCount'),0);assert.equal(h.nodes.get('#manual-price-status').textContent,'');
});
test('malformed, unsupported, unknown-key and future quotes reject atomically and retain source evidence',async()=>{
  const badRows=[{...quote('lomo'),price:'18500'},{...quote('lomo'),price:true},{...quote('lomo'),currency:'USD'},quote('typo'),{...quote('lomo'),date:'2026-02-30'},{...quote('lomo'),date:'2999-01-01'},{...quote('lomo'),currency:undefined}];
  for(const bad of badRows) {
    const h=setup({ar:[quote('pecho'),bad],us:[]});
    const before=JSON.stringify(h.snapshot);
    await h.run('loadPriceFiles()');
    assert.equal(h.run('manualPriceCount'),0);
    assert.equal(h.run('JSON.stringify(PRICES.ar)'),JSON.stringify(h.snapshot.ar));
    assert.equal(h.run('JSON.stringify(PRICES.us)'),JSON.stringify(h.snapshot.us));
    assert.match(h.nodes.get('#manual-price-status').textContent,/rejected or unavailable.*ar\[2\]/);
    assert.equal(JSON.stringify(h.snapshot),before);
  }
});
test('unreadable or invalid JSON manual files leave valid automatic prices visible',async()=>{
  const h=setup();
  for(const raw of [null,'{"ar": [']) {
    if(raw===null) h.bodies.delete('data/manual-prices.json'); else h.bodies.set('data/manual-prices.json',raw);
    await h.run('loadPriceFiles()');
    assert.equal(h.run('priceLoadState'),'ready');
    assert.equal(h.run('JSON.stringify(PRICES.ar.lomo)'),JSON.stringify(h.snapshot.ar.lomo));
    assert.match(h.nodes.get('#manual-price-status').textContent,/automatic observations are shown/);
  }
});
test('manual file cannot bypass rejection of an invalid automatic snapshot',async()=>{
  const h=setup({ar:[quote('lomo')],us:[]});
  const bad=structuredClone(baseline);bad.ar.lomo.usd_lb=-1;
  h.bodies.set('data/prices.json',JSON.stringify(bad));
  await h.run('loadPriceFiles()');
  assert.equal(h.run('PRICES'),null);assert.equal(h.run('priceLoadState'),'unavailable');
  assert.match(h.cards[0].textContent,/Price data unavailable/);
});
test('manual item text is escaped in dossier HTML',()=>{
  const h=setup({ar:[quote('lomo',18500,'ARS','kg','2026-10-15','<img src=x onerror=alert(1)>')],us:[]});h.apply();
  const dossier=h.run('priceBlock(BY_ID.lomo)');
  assert.match(dossier,/&lt;img/);assert.doesNotMatch(dossier,/<img/);
});
test('actual chart callbacks mark manual USD points and omit native-only manual ARS points',()=>{
  const h=setup({ar:[quote('lomo')],us:[quote('tenderloin',8.5,'USD','lb'),quote('molleja',9.75,'USD','lb')]});h.apply();
  const marks=[];
  class Selection {
    constructor(data=[],tag='g') {this.dataRows=data;this.tag=tag;this.marks=[];}
    selectAll(){return new Selection();}
    select(){return new Selection();}
    data(rows){this.dataRows=rows;return this;}
    join(tag){this.tag=tag;return this;}
    append(tag){const s=new Selection(this.dataRows,tag);s.marks=this.dataRows.map(d=>({tag,d,attrs:{}}));marks.push(...s.marks);return s;}
    filter(fn){return new Selection(this.dataRows.filter(fn),this.tag);}
    attr(key,value){this.marks.forEach(m=>m.attrs[key]=typeof value==='function'?value(m.d):value);return this;}
    text(value){this.marks.forEach(m=>m.text=typeof value==='function'?value(m.d):value);return this;}
    style(){return this;}
    remove(){return this;}
    on(){return this;}
    call(fn){fn(this);return this;}
  }
  const scale=()=>{const f=x=>x;f.domain=f.range=f.nice=f.padding=()=>f;f.bandwidth=()=>10;return f;};
  const axis=()=>{const f=()=>{};f.ticks=f.tickSize=f.tickFormat=()=>f;return f;};
  h.context.d3={select:()=>new Selection(),scaleLinear:scale,scaleBand:scale,axisBottom:axis,max:(rows,fn)=>Math.max(...rows.map(fn))};
  h.context.d3Available=()=>true;h.context.moveTooltip=h.context.hideTooltip=()=>{};
  vm.runInContext(section('function renderScatter()','const VALUE_MODEL ='),h.context);
  h.run('renderScatter()');
  const manual=marks.filter(m=>m.tag==='circle'&&m.attrs['data-price-state']==='manual');
  assert.equal(manual.length,2);
  assert.ok(manual.every(m=>m.attrs['stroke-dasharray']==='2 2'));
  assert.ok(manual.some(m=>m.d.us?.usd_lb===8.5));assert.ok(manual.some(m=>m.d.us?.usd_lb===9.75));
  assert.ok(marks.some(m=>m.tag==='text'&&m.text==='$8.50 †'));
  assert.equal(marks.some(m=>m.tag==='circle'&&m.d.ar?.manual_entry&&m.attrs.fill==='var(--navy)'),false);
});
test('the full saved snapshot retains every original receipt, FX field and source ledger after loading and language changes',async()=>{
  const pricePath=path.join(root,'data/prices.json'),manualPath=path.join(root,'data/manual-prices.json');
  const priceBytes=fs.readFileSync(pricePath,'utf8'),manualBytes=fs.readFileSync(manualPath,'utf8');
  const actual=JSON.parse(priceBytes);
  const h=setup({ar:[quote('lomo')],us:[quote('tenderloin',8.5,'USD','lb')]});
  h.bodies.set('data/prices.json',priceBytes);
  await h.run('loadPriceFiles()');
  assert.equal(h.run('manualPriceCount'),2);
  for(const language of ['en','es-AR']) {
    h.run(`language=${JSON.stringify(language)};renderPrices();priceBlock(BY_ID.lomo)`);
    for(const key of ['carrefour_originals','ar_sources','fx','source_status']) assert.equal(h.run(`JSON.stringify(PRICES.${key})`),JSON.stringify(actual[key]),key);
    assert.equal(h.run('JSON.stringify(PRICES.manual_originals.ar.lomo)'),JSON.stringify(actual.ar.lomo));
    assert.equal(h.run('JSON.stringify(PRICES.manual_originals.us.tenderloin)'),JSON.stringify(actual.us.tenderloin));
    assert.equal(h.run('JSON.stringify(PRICES.ar.aguja)'),JSON.stringify(actual.ar.aguja));
  }
  assert.equal(fs.readFileSync(pricePath,'utf8'),priceBytes);
  assert.equal(fs.readFileSync(manualPath,'utf8'),manualBytes);
});
const tenCutDrafts=()=>({ar:['cogote','pecho','garron','bife_costilla','molleja','rinon','lengua','aguja','entrana','tapa'].map(key=>quote(key,null,'ARS','kg',null,key)),us:[]});
test('the ten-cut draft worksheet loads without changing any selected source observation',async()=>{
  const active=tenCutDrafts();
  assert.equal(active.ar.length,10);
  assert.deepEqual(active.ar.map(p=>p.machine_name),['cogote','pecho','garron','bife_costilla','molleja','rinon','lengua','aguja','entrana','tapa']);
  assert.ok(active.ar.every(p=>p.date===null&&p.price===null&&p.currency==='ARS'&&p.unit==='kg'));
  const h=setup(active);await h.run('loadPriceFiles()');
  assert.equal(h.run('manualPriceCount'),0);
  assert.equal(h.run('priceLoadState'),'ready');
  assert.equal(h.run('JSON.stringify(PRICES.ar)'),JSON.stringify(h.snapshot.ar));
  assert.equal(h.run('JSON.stringify(PRICES.us)'),JSON.stringify(h.snapshot.us));
  assert.equal(h.run('JSON.stringify(PRICES.carrefour_originals)'),JSON.stringify(h.snapshot.carrefour_originals));
  assert.equal(h.nodes.get('#manual-price-status').textContent,'');
});
test('null, omitted and blank date/price fields skip drafts without masking a completed quote in either market',()=>{
  for(const country of ['ar','us']) {
    const currency=country==='ar'?'ARS':'USD',unit=country==='ar'?'kg':'lb',key=country==='ar'?'lomo':'tenderloin';
    const valid=quote(key,12345,currency,unit,'2026-10-13');
    const drafts=[quote(key,null,currency,unit,null),quote(key,100,currency,unit,null),quote(key,null,currency,unit),
      quote(key,'',currency,unit),quote(key,'   ',currency,unit),quote(key,100,currency,unit,''),quote(key,100,currency,unit,'   '),
      quote(key,100,currency,unit),quote(key,100,currency,unit)];
    delete drafts[7].date;delete drafts[8].price;
    const file={ar:[],us:[]};file[country]=[valid,...drafts];
    const h=setup(file);h.apply();
    assert.equal(h.run('manualPriceCount'),1);
    assert.equal(h.run('result.entries'),1);
    assert.equal(h.run(`PRICES.${country}.${key}.period`),'2026-10-13');
    assert.equal(h.run(`PRICES.${country}.${key}.${country==='ar'?'ars_kg':'usd_lb'}`),12345);
  }
});
test('gradual completion selects only finished cuts and clearing a value restores original evidence',async()=>{
  const active=tenCutDrafts();
  const h=setup(active);
  const row=key=>active.ar.find(p=>p.machine_name===key);
  const reload=async()=>{h.bodies.set('data/manual-prices.json',JSON.stringify(active));await h.run('loadPriceFiles()');};
  row('pecho').date='2026-10-15';await reload();
  assert.equal(h.run('manualPriceCount'),0);assert.equal(h.run('priceOf(BY_ID.pecho).ar'),null);
  row('pecho').price=18500;await reload();
  assert.equal(h.run('manualPriceCount'),1);assert.match(h.cards[1].innerHTML,/18,500 ARS\/kg/);
  row('aguja').date='2026-10-14';row('aguja').price=17000;await reload();
  assert.equal(h.run('manualPriceCount'),2);
  assert.equal(h.run('JSON.stringify(PRICES.manual_originals.ar.aguja)'),JSON.stringify(h.snapshot.ar.aguja));
  row('molleja').price=12000;await reload();assert.equal(h.run('manualPriceCount'),2);
  assert.equal(h.run('PRICES.ar.molleja.unit_scale_unverified'),true);
  row('molleja').date='2026-10-15';await reload();assert.equal(h.run('manualPriceCount'),3);
  assert.equal(h.run('PRICES.ar.molleja.ars_kg'),12000);
  assert.equal(h.run('PRICES.manual_originals.ar.molleja.unit_scale_unverified'),true);
  assert.equal(h.run('PRICES.carrefour_originals.molleja.unit_scale_unverified'),true);
  row('aguja').price=null;await reload();
  assert.equal(h.run('manualPriceCount'),2);
  assert.equal(h.run('JSON.stringify(PRICES.ar.aguja)'),JSON.stringify(h.snapshot.ar.aguja));
  assert.equal(h.run('JSON.stringify(PRICES.ar_sources)'),JSON.stringify(h.snapshot.ar_sources));
  assert.equal(h.run('JSON.stringify(PRICES.carrefour_originals)'),JSON.stringify(h.snapshot.carrefour_originals));
  assert.equal(h.run('JSON.stringify(PRICES.fx)'),JSON.stringify(h.snapshot.fx));
});
test('supplied invalid values remain errors among drafts, with the correct row and atomic source fallback',async()=>{
  for(const bad of [quote('lomo',0),quote('lomo',false),quote('lomo','18500'),quote('lomo',-1),quote('lomo',100,'ARS','kg','2026-02-30')]) {
    const h=setup({ar:[quote('cogote',null,'ARS','kg',null),quote('pecho'),bad],us:[]});
    await h.run('loadPriceFiles()');
    assert.equal(h.run('manualPriceCount'),0);
    assert.match(h.nodes.get('#manual-price-status').textContent,/ar\[3\]/);
    assert.equal(h.run('JSON.stringify(PRICES.ar)'),JSON.stringify(h.snapshot.ar));
  }
});
test('draft skipping does not silently accept invalid structures or unknown field names',async()=>{
  for(const bad of [null,[],{...quote('pecho',null,'ARS','kg',null),currncy:'ARS'}]) {
    const h=setup({ar:[bad],us:[]});await h.run('loadPriceFiles()');
    assert.equal(h.run('manualPriceCount'),0);
    assert.match(h.nodes.get('#manual-price-status').textContent,/rejected or unavailable.*ar\[1\]/);
    assert.equal(h.run('JSON.stringify(PRICES.ar)'),JSON.stringify(h.snapshot.ar));
  }
});
