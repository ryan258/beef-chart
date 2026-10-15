// R30–R32: the same corpus against actual inline browser validation, no providers.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const root = path.join(__dirname, '..');
const corpus = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/price_contract_v2.json'), 'utf8'));
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
function section(start, end) {
  const a = html.indexOf(start), b = html.indexOf(end, a);
  assert.ok(a >= 0 && b > a, `Missing validation boundary ${start}`);
  return html.slice(a, b);
}
const source = section('const positiveNumber =', 'const usd =')
  + section('function validPeriod(', 'function recordStatus(');
function validator() {
  const context = vm.createContext({clock:corpus.as_of});
  vm.runInContext(source, context);
  return data => {
    context.candidate = data;
    return vm.runInContext('validatePrices(candidate, clock)', context, {timeout:1000});
  };
}
function candidate(c) {
  const data = structuredClone('root' in c ? c.root : corpus.base);
  for (const [keys, value] of c.set) {
    let parent = data;
    for (const key of keys.slice(0,-1)) parent = parent[key] ??= {};
    parent[keys.at(-1)] = structuredClone(value);
  }
  for (const keys of c.unset) {
    let parent = data;
    for (const key of keys.slice(0,-1)) parent = parent[key];
    delete parent[keys.at(-1)];
  }
  switch (c.build) {
    case 'depth': {
      let node = data.extension = {};
      for (let i=0;i<14;i++) node = node.next = {};
      break;
    }
    case 'nodes': data.extension = Array.from({length:500}, () => Array(100).fill(0)); break;
    case 'collection': data.extension = Array(1001).fill(0); break;
    case 'text': data.extension = 'x'.repeat(16385); break;
    case 'cycle': data.extension = data; break;
    case 'unsafe_number': data.extension = 1e100; break;
  }
  return data;
}

test(`shared v2 corpus: ${corpus.cases.length} compatibility/rejection cases`, () => {
  const validate = validator();
  for (const c of corpus.cases) {
    const data = candidate(c);
    const before = c.build === 'cycle' ? null : JSON.stringify(data);
    if (c.accept) assert.equal(validate(data), data, c.name);
    else assert.throws(() => validate(data), undefined, c.name);
    if (before !== null) assert.equal(JSON.stringify(data), before, c.name);
  }
});

test('bundled bytes, 36 records, legacy unknowns and organ withholding remain intact', () => {
  const file = path.join(root, 'tests/fixtures/prices_legacy_2026_10_07.json');
  const original = fs.readFileSync(file);
  assert.equal(crypto.createHash('sha256').update(original).digest('hex'), corpus.bundled_sha256);
  const data = JSON.parse(original);
  const before = JSON.stringify(data);
  assert.equal(validator()(data), data);
  assert.equal(Object.keys(data.us).length + Object.keys(data.ar).length, 36);
  assert.ok([...Object.values(data.us),...Object.values(data.ar)].every(p => p.retrieved_at === null));
  assert.deepEqual(Object.keys(data.ar).filter(k => data.ar[k].unit_scale_unverified).sort(), ['lengua','molleja','rinon']);
  assert.equal(JSON.stringify(data), before);
  assert.deepEqual(fs.readFileSync(file), original);
});

test('shared noncyclic metadata remains valid', () => {
  const data = structuredClone(corpus.base), evidence = {note:'Shared but not cyclic'};
  data.extension = [evidence,evidence];
  assert.equal(validator()(data), data);
});
