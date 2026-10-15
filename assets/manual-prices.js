/* Owner-entered quotes. This module never writes to the scraper-owned snapshot. */
const ManualPrices = (() => {
  const fields = ['date', 'item', 'machine_name', 'price', 'currency', 'unit'];
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  const amount = value => {
    const number = value;
    if (typeof number !== 'number' || !Number.isFinite(number) || number <= 0 || number > 1e9) throw new Error('Price must be a positive number, at most 1000000000');
    return number;
  };
  function parsePrice(value, currency, unit) {
    const price = amount(value);
    if (!['ARS','USD'].includes(currency)) throw new Error('Currency must be ARS or USD');
    if (!['kg','lb'].includes(unit)) throw new Error('Unit must be kg or lb');
    if (currency === 'ARS' && unit === 'kg') return {ars_kg:price, usd_lb:null, native_currency:currency, native_unit:unit};
    if (currency === 'USD' && unit === 'lb') return {ars_kg:null, usd_lb:price, native_currency:currency, native_unit:unit};
    throw new Error('Supported combinations are ARS with kg and USD with lb');
  }
  function apply(snapshot, file, cuts, today = new Date().toISOString().slice(0,10)) {
    if (!object(file) || Object.keys(file).some(key => !['ar','us'].includes(key))) throw new Error('Manual prices must contain only ar and us arrays');
    const prepared = {ar:new Map(), us:new Map()};
    let total = 0;
    for (const country of ['ar','us']) {
      const rows = Object.hasOwn(file,country) ? file[country] : [];
      if (!Array.isArray(rows) || rows.length > 500) throw new Error('Each market must be an array of at most 500 quotes');
      const keys = new Map([['ground_beef','ground_beef']]);
      for (const cut of cuts) {
        const canonical = cut[country === 'ar' ? 'arSeries' : 'usSeries'] || cut.id;
        keys.set(canonical,canonical);
        keys.set(cut.id,canonical);
      }
      rows.forEach((row,index) => {
        try {
          if (!object(row) || Object.keys(row).some(key => !fields.includes(key))) throw new Error('Each quote needs date, item, machine_name, price, currency and unit');
          const blank = value => value == null || (typeof value === 'string' && !value.trim());
          // Drafts never override a source observation. Zero/false are values, not blanks.
          if (blank(row.date) || blank(row.price)) return;
          if (fields.some(key => !Object.hasOwn(row,key))) throw new Error('Each quote needs date, item, machine_name, price, currency and unit');
          if (typeof row.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(row.date) || row.date.startsWith('0000-')) throw new Error('Use an actual observation date in YYYY-MM-DD format');
          const date = new Date(row.date + 'T12:00:00Z');
          if (Number.isNaN(date.getTime()) || date.toISOString().slice(0,10) !== row.date || row.date > today) throw new Error('Observation date must be a real date, no later than today');
          if (typeof row.item !== 'string' || !row.item.trim() || row.item.length > 512) throw new Error('Item must be nonempty text of at most 512 characters');
          if (typeof row.machine_name !== 'string' || !keys.has(row.machine_name)) throw new Error('Unknown machine_name; use the key table in docs/manual-prices.md');
          const key = keys.get(row.machine_name);
          const record = {
            ...parsePrice(row.price, row.currency, row.unit), label:row.item.trim(), period:row.date,
            source:'Manual entry', manual_entry:true, manual_machine_name:key,
            manual_price:row.price, manual_file:'data/manual-prices.json',
            observation_status:'observed', provenance_status:'unknown',
            method:'Manually entered local quote',
            geography:country === 'ar' ? 'Argentina; location unspecified' : 'United States; location unspecified',
            retrieved_at:null, publication_date:null, fx_date:null, fx_ars_per_usd:null,
            fx_provenance:'unknown', availability:'unknown'
          };
          // A later observation wins; a later row revises the same observation date.
          if (!prepared[country].has(key) || record.period >= prepared[country].get(key).period) prepared[country].set(key,record);
          total++;
        } catch (error) {
          error.manualRow = `${country}[${index + 1}]`;
          throw error;
        }
      });
    }
    // Build only after all completed rows pass. Keep automatic selected records and ledgers by reference.
    const prices = {...snapshot, ar:{...snapshot.ar}, us:{...snapshot.us}, manual_originals:{ar:{},us:{}}};
    let selected = 0;
    for (const country of ['ar','us']) for (const [key,record] of prepared[country]) {
      if (Object.hasOwn(snapshot[country],key)) prices.manual_originals[country][key] = snapshot[country][key];
      prices[country][key] = record;
      selected++;
    }
    return {prices, count:selected, entries:total};
  }
  return Object.freeze({parsePrice, apply});
})();
if (typeof module !== 'undefined' && module.exports) module.exports = ManualPrices;
