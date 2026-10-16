/* Small reference helpers. Returned notes are plain text, never HTML. */
(function (root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ReferenceTools = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const storageKey = 'beef-chart-last-cut';
  const validLanguage = language => language === 'en' || language === 'es-AR';
  const validId = id => typeof id === 'string' && /^[a-z][a-z0-9_-]{0,63}$/.test(id);
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  const text = value => typeof value === 'string' && value.trim() ? value : '';

  function cutUrl(href, id, language) {
    if (typeof href !== 'string' || !validId(id) || !validLanguage(language)) return null;
    try {
      const url = new URL(href);
      if (!['http:', 'https:'].includes(url.protocol)) return null;
      url.searchParams.set('cut', id);
      url.searchParams.set('lang', language);
      url.hash = '';
      return url.href;
    } catch (_) {
      return null;
    }
  }

  function savedCut(storage, ids) {
    try {
      const saved = JSON.parse(storage.getItem(storageKey));
      if (!object(saved) || !validId(saved.id) || !validLanguage(saved.language)
          || !Array.isArray(ids) || !ids.includes(saved.id)) return null;
      return {id: saved.id, language: saved.language};
    } catch (_) {
      return null;
    }
  }

  function rememberCut(storage, id, language) {
    if (!validId(id) || !validLanguage(language)) return false;
    try {
      storage.setItem(storageKey, JSON.stringify({id, language}));
      return true;
    } catch (_) {
      return false;
    }
  }

  function validQuote(quote) {
    if (!object(quote) || quote.manual !== true || quote.withheld === true
        || quote.unit_scale_unverified === true || quote.status === 'withheld'
        || quote.observation_status === 'withheld' || !['ar', 'us'].includes(quote.market)
        || typeof quote.amount !== 'number' || !Number.isFinite(quote.amount)
        || quote.amount <= 0 || quote.amount > 1e9
        || !((quote.currency === 'ARS' && quote.unit === 'kg')
          || (quote.currency === 'USD' && quote.unit === 'lb'))
        || typeof quote.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(quote.date)
        || quote.date.startsWith('0000-')) return false;
    const date = new Date(quote.date + 'T12:00:00Z');
    return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === quote.date
      && quote.date <= new Date().toISOString().slice(0, 10);
  }

  function butcherNote(cut, language) {
    if (!object(cut) || !text(cut.name) || !validLanguage(language)) return '';
    const labels = language === 'es-AR' ? {
      cut: 'Corte', usName: 'Referencia de EE. UU.', relationship: 'Relación',
      preparation: 'Preparación', quote: 'Precio manual', ar: 'Argentina', us: 'Estados Unidos',
      unverified: 'Disponibilidad y especificaciones exactas del producto sin verificar.'
    } : {
      cut: 'Cut', usName: 'U.S. reference', relationship: 'Relationship',
      preparation: 'Preparation', quote: 'Manual quote', ar: 'Argentina', us: 'United States',
      unverified: 'Availability and exact product specifications unverified.'
    };
    const lines = [`${labels.cut}: ${cut.name}`];
    for (const field of ['usName', 'relationship', 'preparation']) {
      if (text(cut[field])) lines.push(`${labels[field]}: ${cut[field]}`);
    }
    const quotes = Array.isArray(cut.quotes) ? cut.quotes.filter(validQuote) : [];
    for (const quote of quotes) {
      const amount = new Intl.NumberFormat(language, {
        minimumFractionDigits: quote.currency === 'USD' ? 2 : 0, maximumFractionDigits: 6
      }).format(quote.amount);
      lines.push(`${labels.quote} — ${labels[quote.market]}: ${amount} ${quote.currency}/${quote.unit} (${quote.date})`);
    }
    if (quotes.length) lines.push(labels.unverified);
    return lines.join('\n');
  }

  return Object.freeze({cutUrl, savedCut, rememberCut, butcherNote});
});
