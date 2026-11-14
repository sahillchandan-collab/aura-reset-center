// Builds a Botany Properties client portfolio report (PDF) from a client's report.json.
// Usage: node build-portfolio-report.js <client-folder>
//   e.g. node build-portfolio-report.js panagiotis-evangelinos
// Writes <client-folder>/out/report.html and <client-folder>/out/<Name>_Portfolio_Report.pdf
// report.json holds personal and financial data and is git-ignored; this script is not.
const fs = require('fs');
const path = require('path');

const dir = path.resolve(__dirname, process.argv[2] || '.');
const data = JSON.parse(fs.readFileSync(path.join(dir, 'report.json'), 'utf8'));
const assets = path.resolve(__dirname, '..', 'botany-letterhead', 'assets');
const b64 = (f) => 'data:image/png;base64,' + fs.readFileSync(path.join(assets, f)).toString('base64');

// ---------- numbers ----------
const round5k = (n) => Math.round(n / 5000) * 5000;
const fmt = (n) => Math.round(n).toLocaleString('en-US');
const aedK = (n) => n >= 1e6 ? `AED ${(n / 1e6).toFixed(2)}M` : `AED ${Math.round(n / 1000)}k`;
const pct = (n) => `${n >= 0 ? '+' : '−'}${Math.abs(n * 100).toFixed(0)}%`;
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const dmy = (iso) => { if (!iso) return ''; const [y, m, d] = iso.split('-'); return `${d}/${m}/${y}`; };
const monYr = (iso) => new Date(iso + 'T00:00:00Z').toLocaleDateString('en-GB', { month: 'short', year: 'numeric', timeZone: 'UTC' });

const props = data.properties.map((p) => {
  const v = p.valuation;
  const mid = v.hold_at_purchase ? p.purchase_price_aed : round5k(p.area_sqft * v.psf_mid);
  const low = round5k(p.area_sqft * v.psf_low);
  const high = round5k(p.area_sqft * v.psf_high);
  return { ...p, est: { low, mid, high }, gain: mid - p.purchase_price_aed, gainPct: mid / p.purchase_price_aed - 1,
    paidPsf: p.purchase_price_aed / p.area_sqft, label: `${p.building} · ${p.unit}` };
}).sort((a, b) => a.purchase_date.localeCompare(b.purchase_date));

const tot = {
  paid: props.reduce((s, p) => s + p.purchase_price_aed, 0),
  mid: props.reduce((s, p) => s + p.est.mid, 0),
  low: props.reduce((s, p) => s + p.est.low, 0),
  high: props.reduce((s, p) => s + p.est.high, 0),
  sqft: props.reduce((s, p) => s + p.area_sqft, 0),
};
tot.gain = tot.mid - tot.paid; tot.gainPct = tot.mid / tot.paid - 1;
const known = props.filter((p) => p.tenancy && p.tenancy.status);
const rented = known.filter((p) => p.tenancy.status === 'Rented');
const vacant = known.filter((p) => p.tenancy.status === 'Vacant');
const annualRent = rented.reduce((s, p) => s + (p.tenancy.annual_rent_aed || 0), 0);
const byId = Object.fromEntries(props.map((p) => [p.id, p]));

// ---------- chart: purchase price to estimated value, one row per apartment ----------
function growthChart() {
  const W = 680, rowH = 46, top = 34, left = 190, right = 120, H = top + rowH * props.length + 34;
  const xMin = 300000, xMax = 800000;
  const x = (v) => left + (v - xMin) / (xMax - xMin) * (W - left - right);
  const ticks = [300000, 400000, 500000, 600000, 700000, 800000];
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Purchase price and estimated current value for each apartment">`;
  ticks.forEach((t) => {
    s += `<line x1="${x(t)}" x2="${x(t)}" y1="${top - 8}" y2="${H - 30}" stroke="var(--grid)" stroke-width="1"/>`;
    s += `<text x="${x(t)}" y="${H - 14}" class="axis" text-anchor="middle">${t / 1000}k</text>`;
  });
  s += `<text x="${W - right}" y="${H - 1}" class="axis" text-anchor="end">AED</text>`;
  props.forEach((p, i) => {
    const cy = top + i * rowH + rowH / 2;
    s += `<text x="${left - 14}" y="${cy - 3}" class="rowlab" text-anchor="end">${esc(p.building)}</text>`;
    s += `<text x="${left - 14}" y="${cy + 11}" class="rowsub" text-anchor="end">Unit ${esc(p.unit)} · bought ${monYr(p.purchase_date)}</text>`;
    s += `<rect x="${x(p.est.low)}" y="${cy - 5}" width="${x(p.est.high) - x(p.est.low)}" height="10" rx="5" fill="var(--band)"/>`;
    if (p.est.mid !== p.purchase_price_aed) s += `<line x1="${x(p.purchase_price_aed)}" x2="${x(p.est.mid)}" y1="${cy}" y2="${cy}" stroke="var(--ink-3)" stroke-width="2"/>`;
    s += `<circle cx="${x(p.purchase_price_aed)}" cy="${cy}" r="6" fill="var(--surface)" stroke="var(--c-paid)" stroke-width="2.5"/>`;
    s += `<circle cx="${x(p.est.mid)}" cy="${cy}" r="${p.est.mid === p.purchase_price_aed ? 3.5 : 6.5}" fill="var(--c-est)" stroke="var(--surface)" stroke-width="2"/>`;
    const lx = Math.max(x(p.est.high), x(p.est.mid)) + 12;
    s += `<text x="${lx}" y="${cy - 2}" class="vlab">${aedK(p.est.mid)}</text>`;
    s += `<text x="${lx}" y="${cy + 12}" class="vsub">${p.valuation.hold_at_purchase ? 'held at cost' : pct(p.gainPct) + ' since purchase'}</text>`;
  });
  return s + '</svg>';
}

// ---------- page pieces ----------
const statusChip = (p) => {
  const st = p.tenancy && p.tenancy.status;
  if (st === 'Rented') return `<span class="chip ok"><i>●</i> Rented</span>`;
  if (st === 'Vacant') return `<span class="chip warn"><i>◐</i> Vacant</span>`;
  return `<span class="chip tbc"><i>○</i> To confirm</span>`;
};
const pending = (what) => `<div class="pending"><b>To be completed by Botany Properties.</b> ${what}</div>`;

function apartmentCard(p) {
  const t = p.tenancy;
  let ten = '';
  if (t && t.status === 'Rented') {
    ten = `<dl class="ten"><dt>Annual rent</dt><dd>AED ${fmt(t.annual_rent_aed || 0)}</dd>
      <dt>Lease</dt><dd>${dmy(t.start)} to ${dmy(t.end)}</dd>
      ${t.cheques ? `<dt>Cheques</dt><dd>${esc(t.cheques)}</dd>` : ''}
      ${t.notes ? `<dt>Notes</dt><dd>${esc(t.notes)}</dd>` : ''}</dl>`;
  } else if (t && t.status === 'Vacant') {
    ten = `<dl class="ten"><dt>Vacant since</dt><dd>${dmy(t.vacant_since) || '—'}</dd>${t.notes ? `<dt>Notes</dt><dd>${esc(t.notes)}</dd>` : ''}</dl>`;
  }
  return `<article class="card">
    <header><div><h3>${esc(p.building)}</h3><div class="sub">Unit ${esc(p.unit)} · Floor ${p.floor} · ${esc(p.community)}</div></div>${statusChip(p)}</header>
    <dl><dt>Size</dt><dd>${fmt(p.area_sqft)} sq ft (${p.area_sqm} m²)</dd>
      <dt>Parking</dt><dd>${esc(p.parking)}</dd>
      <dt>Title deed</dt><dd>${esc(p.deed_no)} · ${esc(p.mortgage)}</dd>
</dl>
    ${ten}
  </article>`;
}

function maintenanceSection() {
  if (!data.maintenance.length) return pending('Maintenance carried out on each apartment: date, work done, cost and who paid.');
  const rows = data.maintenance.map((m) => `<tr><td>${dmy(m.date)}</td><td>${esc(byId[m.property_id]?.label || m.property_id)}</td><td>${esc(m.work)}</td><td class="num">${m.cost_aed != null ? fmt(m.cost_aed) : '—'}</td><td>${esc(m.status || '')}</td></tr>`).join('');
  const total = data.maintenance.reduce((s, m) => s + (m.cost_aed || 0), 0);
  return `<table><thead><tr><th>Date</th><th>Apartment</th><th>Work done</th><th class="num">Cost (AED)</th><th>Status</th></tr></thead><tbody>${rows}</tbody>
    <tfoot><tr><td colspan="3">Total</td><td class="num">${fmt(total)}</td><td></td></tr></tfoot></table>`;
}

function legalSection() {
  if (!data.legal.length) return pending('Open legal or tenancy matters for each apartment: what happened, current status, the action needed and who must act.');
  return data.legal.map((l) => `<article class="legal">
    <header><h3>${esc(byId[l.property_id]?.label || l.property_id)}</h3><span class="chip ${l.priority === 'High' ? 'crit' : 'warn'}"><i>!</i> ${esc(l.priority || 'Open')}</span></header>
    <p><b>Issue.</b> ${esc(l.issue)}</p>
    ${l.status ? `<p><b>Status.</b> ${esc(l.status)}</p>` : ''}
    <p class="action"><b>Action required.</b> ${esc(l.action)}${l.deadline ? ` <span class="muted">By ${dmy(l.deadline)}.</span>` : ''}</p>
  </article>`).join('');
}

const pageHead = (first) => first
  ? `<img class="band" src="${b64('letterhead-header-band.png')}" alt="Botany Properties">`
  : `<div class="minihead"><b>BOTANY PROPERTIES</b><span>Portfolio Report · ${esc(data.client.salutation)}</span></div>`;
const pageFoot = (n, of) => `<footer><span>BOTANY PROPERTIES L.L.C · Dubai, United Arab Emirates</span><span>Page ${n} of ${of}</span></footer>`;
const draft = data.status === 'draft' ? `<div class="draft">Draft · sections marked “to be completed” need Botany Properties’ records</div>` : '';

const occTile = known.length === props.length
  ? `<div class="kpi"><div class="k">Occupancy</div><div class="v">${rented.length} of ${props.length} rented</div><div class="s">${vacant.length ? `${vacant.length} vacant` : 'none vacant'}${annualRent ? ` · AED ${fmt(annualRent)} a year` : ''}</div></div>`
  : `<div class="kpi tbc"><div class="k">Occupancy</div><div class="v">To be confirmed</div><div class="s">Rented and vacant units</div></div>`;

const page1 = `<section class="page">${pageHead(true)}<div class="body">
  ${draft}
  <div class="eyebrow">Portfolio Report · ${esc(data.valuation_date)}</div>
  <h1>Prepared for ${esc(data.client.salutation)}</h1>
  <p class="lede">Your five Dubai apartments under Botany Properties management: what they cost, what they are worth today, and how each one is performing.</p>
  <div class="kpis">
    <div class="kpi"><div class="k">Apartments</div><div class="v">${props.length}</div><div class="s">${fmt(tot.sqft)} sq ft · all mortgage-free</div></div>
    <div class="kpi"><div class="k">Total paid</div><div class="v">${aedK(tot.paid)}</div><div class="s">${monYr(props[0].purchase_date)} to ${monYr(props[props.length - 1].purchase_date)}</div></div>
    <div class="kpi hero"><div class="k">Estimated value today</div><div class="v">${aedK(tot.mid)}</div><div class="s">Range ${aedK(tot.low)}–${aedK(tot.high)}</div></div>
    <div class="kpi"><div class="k">Estimated growth</div><div class="v">+${aedK(tot.gain)}</div><div class="s">${pct(tot.gainPct)} on the price paid</div></div>
    ${occTile}
  </div>
  <h2>Growth since purchase</h2>
  <div class="legend"><span><svg width="16" height="16"><circle cx="8" cy="8" r="5.5" fill="none" stroke="var(--c-paid)" stroke-width="2.5"/></svg>Purchase price</span>
    <span><svg width="16" height="16"><circle cx="8" cy="8" r="6" fill="var(--c-est)"/></svg>Estimated value, ${esc(data.valuation_date)}</span>
    <span><svg width="22" height="16"><rect x="1" y="4" width="20" height="8" rx="4" fill="var(--band)"/></svg>Likely range</span></div>
  ${growthChart()}
  <p class="note">Estimates use 2026 resale prices per square foot in each building, applied to the size on the title deed. Golf Vita is shown at its purchase price because it was bought six months ago. See the last page for the method and sources.</p>
</div>${pageFoot(1, 3)}</section>`;

const growthRows = props.map((p) => `<tr><td><b>${esc(p.building)}</b><br><span class="muted">Unit ${esc(p.unit)}</span></td><td>${dmy(p.purchase_date)}</td>
  <td class="num">${fmt(p.purchase_price_aed)}</td><td class="num">${fmt(p.paidPsf)}</td><td class="num">${fmt(p.est.mid)}<br><span class="muted">${aedK(p.est.low)}–${aedK(p.est.high)}</span></td>
  <td class="num"><b>${p.valuation.hold_at_purchase ? '—' : (p.gain >= 0 ? '+' : '−') + fmt(Math.abs(p.gain))}</b><br><span class="muted">${p.valuation.hold_at_purchase ? 'held at cost' : pct(p.gainPct)}</span></td></tr>`).join('');

const page2 = `<section class="page">${pageHead(false)}<div class="body">
  <h2>Value by apartment</h2>
  <table><thead><tr><th>Apartment</th><th>Purchased</th><th class="num">Price paid (AED)</th><th class="num">AED per sq ft paid</th><th class="num">Estimated value (AED)</th><th class="num">Change (AED)</th></tr></thead>
  <tbody>${growthRows}</tbody>
  <tfoot><tr><td colspan="2">Portfolio</td><td class="num">${fmt(tot.paid)}</td><td class="num">${fmt(tot.paid / tot.sqft)}</td><td class="num">${fmt(tot.mid)}</td><td class="num">+${fmt(tot.gain)}<br><span class="muted">${pct(tot.gainPct)}</span></td></tr></tfoot></table>
  <h2>Your apartments</h2>
  <div class="cards">${props.map(apartmentCard).join('')}</div>
  ${known.length < props.length ? pending('Rented or vacant status for each apartment, with the annual rent and lease dates for rented units.') : ''}
</div>${pageFoot(2, 3)}</section>`;

const page3 = `<section class="page">${pageHead(false)}<div class="body">
  <h2>Maintenance carried out</h2>
  ${maintenanceSection()}
  <h2>Legal matters and actions required</h2>
  ${legalSection()}
  <h2>How the values were estimated</h2>
  <div class="method">${props.map((p) => `<p><b>${esc(p.building)}, unit ${esc(p.unit)}.</b> ${esc(p.valuation.evidence)} Applied at AED ${fmt(p.valuation.psf_low)}–${fmt(p.valuation.psf_high)} per sq ft${p.valuation.psf_mid ? `, central AED ${fmt(p.valuation.psf_mid)}` : ''}.</p>`).join('')}
  <p class="muted">These are desktop estimates from published resale data, not formal valuations. Actual sale prices depend on view, floor, condition, furnishing and the market at the time of sale. A RERA-certified valuation can be arranged on request.</p>
  <p class="muted src"><b>Sources.</b> ${data.sources.map(([t, u]) => `${esc(t)} (${esc(u.replace(/^https?:\/\//, ''))})`).join('; ')}.</p></div>
</div>${pageFoot(3, 3)}</section>`;

const css = `
:root{--green:#283718;--sage:#5A6B4A;--ink:#1D2416;--ink-2:#4A5442;--ink-3:#8A9282;--rule:#DCE2D4;--grid:#ECEFE7;
 --surface:#FCFCFB;--tint:#F3F6EF;--band:#E1EAD5;--c-paid:#8AAE5F;--c-est:#3E6E2A;--ok:#2F7A3E;--warn:#A86A00;--crit:#B3261E}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);font:10.5pt/1.45 Carlito,Calibri,'Liberation Sans',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;background:var(--surface)}
.band{display:block;width:100%;height:auto}
.minihead{display:flex;align-items:center;gap:12px;background:var(--green);color:#E9EEE3;padding:10px .9in;font-size:9pt;letter-spacing:.06em;text-transform:uppercase}
.minihead b{letter-spacing:.22em;color:#fff;padding-right:12px;border-right:1px solid #5A6B4A}
.body{padding:.32in .9in 0}
footer{position:absolute;left:.9in;right:.9in;bottom:.38in;border-top:1px solid var(--green);padding-top:6px;display:flex;justify-content:space-between;font-size:8pt;color:var(--sage);letter-spacing:.08em}
footer::after{content:"";position:absolute;left:-.9in;right:-.9in;bottom:-.38in;height:6px;background:var(--green)}
.draft{display:inline-block;background:#FFF4DC;color:#7A4E00;border:1px solid #F0D9A6;border-radius:4px;padding:3px 10px;font-size:8.5pt;margin-bottom:10px}
.eyebrow{font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:var(--sage);font-weight:700}
h1{font-size:21pt;line-height:1.15;margin:4px 0 6px;color:var(--green);font-weight:700}
h2{font-size:13pt;color:var(--green);margin:20px 0 8px;padding-bottom:4px;border-bottom:1px solid var(--rule)}
h3{font-size:11pt;margin:0;color:var(--ink)}
.lede{color:var(--ink-2);margin:0 0 14px;max-width:6in}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
.kpi{background:var(--tint);border-radius:6px;padding:9px 10px}
.kpi .k{font-size:8pt;text-transform:uppercase;letter-spacing:.07em;color:var(--sage);font-weight:700}
.kpi .v{font-size:15pt;font-weight:700;color:var(--ink);margin-top:2px;font-variant-numeric:tabular-nums}
.kpi .s{font-size:8.5pt;color:var(--ink-2)}
.kpi.hero{background:var(--green)} .kpi.hero .k,.kpi.hero .s{color:#C9D4BD} .kpi.hero .v{color:#fff}
.kpi.tbc{background:none;border:1px dashed var(--ink-3)} .kpi.tbc .v{font-size:11.5pt;color:var(--ink-2)}
.legend{display:flex;gap:18px;font-size:9pt;color:var(--ink-2);margin:2px 0 2px} .legend span{display:flex;align-items:center;gap:5px}
svg .axis{font-size:9px;fill:var(--ink-3)} svg .rowlab{font-size:11px;font-weight:700;fill:var(--ink)} svg .rowsub{font-size:9.5px;fill:var(--ink-2)}
svg .vlab{font-size:11px;font-weight:700;fill:var(--ink)} svg .vsub{font-size:9.5px;fill:var(--ink-2)}
.note{font-size:8.8pt;color:var(--ink-2);margin-top:4px}
table{width:100%;border-collapse:collapse;font-size:9.3pt;font-variant-numeric:tabular-nums}
th{text-align:left;font-size:8pt;text-transform:uppercase;letter-spacing:.05em;color:var(--sage);border-bottom:1.5px solid var(--green);padding:5px 6px}
td{padding:6px;border-bottom:1px solid var(--rule);vertical-align:top}
tfoot td{font-weight:700;border-top:1.5px solid var(--green);border-bottom:none;background:var(--tint)}
.num{text-align:right} .muted{color:var(--ink-3);font-weight:400;font-size:8.6pt}
.cards{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:9px}
.card{border:1px solid var(--rule);border-radius:7px;padding:9px 11px;break-inside:avoid}
.card header{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:5px}
.card .sub{font-size:8.6pt;color:var(--ink-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
dl{display:grid;grid-template-columns:auto 1fr;gap:1px 10px;margin:0;font-size:8.9pt} dt{color:var(--ink-3)} dd{margin:0}
dl.ten{margin-top:6px;padding-top:6px;border-top:1px dashed var(--rule)}
.chip{white-space:nowrap;font-size:8pt;font-weight:700;border-radius:999px;padding:2px 8px;border:1px solid} .chip i{font-style:normal}
.chip.ok{color:var(--ok);border-color:#BFD9C3;background:#EEF7F0} .chip.warn{color:var(--warn);border-color:#EBD3A8;background:#FFF7E8}
.chip.crit{color:var(--crit);border-color:#EDC0BC;background:#FDF1F0} .chip.tbc{color:var(--ink-2);border-color:var(--rule);background:#fff;font-weight:400}
.pending{border:1px dashed var(--ink-3);border-radius:6px;padding:10px 12px;color:var(--ink-2);font-size:9.5pt;margin-top:9px;background:#fff}
.legal{border-left:3px solid var(--warn);padding:4px 0 4px 12px;margin-bottom:10px} .legal header{display:flex;justify-content:space-between}
.legal p{margin:3px 0} .legal .action{color:var(--ink)}
.method p{margin:0 0 6px;font-size:9.2pt} .src{font-size:7.8pt;line-height:1.35}
`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Portfolio Report · ${esc(data.client.name)}</title><style>${css}</style></head>
<body>${page1}${page2}${page3}</body></html>`;

const out = path.join(dir, 'out');
fs.mkdirSync(out, { recursive: true });
const htmlPath = path.join(out, 'report.html');
fs.writeFileSync(htmlPath, html);
const pdfPath = path.join(out, `${data.client.name.replace(/\s+/g, '_')}_Portfolio_Report.pdf`);

(async () => {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath);
  await page.pdf({ path: pdfPath, width: '8.5in', height: '11in', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  console.log('written', pdfPath);
})();
