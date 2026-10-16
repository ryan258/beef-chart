/* A compact account of stored source dates; assembly is not a provider retrieval. */
(function (root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SnapshotSummary = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);

  function period(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}(?:-\d{2})?$/.test(value) || value.startsWith('0000-')) return null;
    const day = value.length === 7 ? `${value}-01` : value;
    const date = new Date(`${day}T00:00:00Z`);
    return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === day ? value : null;
  }

  function dateRange(records, unknown, partlyUnknown) {
    const dates = records.map(record => period(record.period)).filter(Boolean).sort();
    if (!dates.length) return unknown;
    const range = dates[0] === dates[dates.length - 1] ? dates[0] : `${dates[0]}–${dates[dates.length - 1]}`;
    return dates.length === records.length ? range : `${range}; ${partlyUnknown}`;
  }

  function summarize(prices, language = 'en') {
    const es = language === 'es-AR';
    if (!object(prices)) return es ? 'Datos guardados no disponibles.' : 'Snapshot unavailable.';
    const unknown = es ? 'fechas desconocidas' : 'dates unknown';
    const partlyUnknown = es ? 'algunas fechas desconocidas' : 'some dates unknown';
    const parts = [];
    const generated = prices.generated_at;
    const validTimestamp = typeof generated === 'string'
      && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/.test(generated)
      && period(generated.slice(0, 10)) && Number.isFinite(Date.parse(generated));
    parts.push(validTimestamp
      ? `${es ? 'Datos compilados el' : 'Snapshot assembled'} ${new Date(generated).toISOString().slice(0, 10)}`
      : es ? 'Fecha de compilación desconocida' : 'Snapshot assembly date unknown');

    const records = {ar: [], us: []};
    for (const market of ['ar', 'us']) {
      const selected = object(prices[market]) ? prices[market] : {};
      const originals = object(prices.manual_originals) && object(prices.manual_originals[market]) ? prices.manual_originals[market] : {};
      for (const [key, selectedRecord] of Object.entries(selected)) {
        if (!object(selectedRecord)) continue;
        const record = selectedRecord.manual_entry === true ? originals[key] : selectedRecord;
        if (object(record) && record.manual_entry !== true && record.source !== 'Manual entry') records[market].push(record);
      }
    }
    const ipcva = records.ar.filter(record => record.source === 'IPCVA' && record.unit_scale_unverified !== true);
    const indec = records.ar.filter(record => record.source === 'INDEC' && record.unit_scale_unverified !== true);
    const bls = records.us.filter(record => record.source === 'BLS' && record.unit_scale_unverified !== true);
    const usda = records.us.filter(record => record.source === 'USDA ad survey' && record.unit_scale_unverified !== true);
    for (const [rows, label] of [
      [ipcva, es ? 'Encuesta IPCVA de Argentina' : 'Argentina IPCVA survey'],
      [indec, es ? 'Promedios INDEC de Argentina' : 'Argentina INDEC averages'],
      [bls, es ? 'Promedios BLS de EE. UU.' : 'U.S. BLS averages']
    ]) if (rows.length) parts.push(`${label}: ${dateRange(rows, unknown, partlyUnknown)}`);

    if (usda.length) {
      const endingWindows = new Set(), advertisedWindows = new Set();
      const withoutWindow = [];
      for (const record of usda) {
        const start = period(record.effective_start), end = period(record.effective_end);
        if (start && end && start.length === 10 && end.length === 10 && start <= end) {
          const windows = record.interval_basis === 'advertisement_ending_dates_printed_in_pdf' ? endingWindows : advertisedWindows;
          windows.add(start === end ? start : `${start}–${end}`);
        }
        else withoutWindow.push(record);
      }
      if (endingWindows.size) parts.push(`${es ? 'Fechas de finalización de anuncios USDA de EE. UU.' : 'U.S. USDA ad-ending dates'}: ${[...endingWindows].sort().join(', ')}`);
      if (advertisedWindows.size) parts.push(`${es ? 'Períodos anunciados USDA de EE. UU.' : 'U.S. USDA advertised windows'}: ${[...advertisedWindows].sort().join(', ')}`);
      if (withoutWindow.length) parts.push(`${es ? 'Referencias USDA de EE. UU.; períodos de observación' : 'U.S. USDA references; observation periods'}: ${dateRange(withoutWindow, unknown, partlyUnknown)}; ${es ? 'fechas de anuncios desconocidas' : 'advertised dates unknown'}`);
    }

    const carrefour = records.ar.filter(record => record.source === 'Carrefour AR');
    const retained = carrefour.filter(record => record.unit_scale_unverified !== true && /^retained_/.test(record.observation_status || ''));
    const withheld = carrefour.filter(record => record.unit_scale_unverified === true);
    if (retained.length) parts.push(`${es ? 'Referencias conservadas de Carrefour' : 'Retained Carrefour references'}: ${retained.length} (${dateRange(retained, unknown, partlyUnknown)})`);
    if (withheld.length) parts.push(`${es ? 'Precios de Carrefour no publicados' : 'Withheld Carrefour prices'}: ${withheld.length}`);
    if (!ipcva.length && !indec.length && !bls.length && !usda.length && !retained.length && !withheld.length) parts.push(es ? 'Fechas de observación de las fuentes no disponibles' : 'Source observation dates unavailable');
    return `${parts.join('. ')}.`;
  }

  return Object.freeze({summarize});
});
