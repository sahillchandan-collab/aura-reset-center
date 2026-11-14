// Builds a Botany Properties client portfolio report (PDF) from a client's report.json.
// Usage: node build-portfolio-report.js <client-folder>
//   e.g. node build-portfolio-report.js panagiotis-evangelinos
// Writes <client-folder>/out/report.html and <client-folder>/out/<Name>_Portfolio_Report.pdf
// report.json holds personal and financial data and is git-ignored; this script is not.
//
// Report parts:
//   1. Value growth since purchase (title deed price vs estimated value today)
//   2. Current earnings (tenancies, rent under contract, cheques)
//   3. Expenses for the year and the net earnings calculation
//   then legal matters / actions and the basis of all figures.
const fs = require('fs');
const path = require('path');

const dir = path.resolve(__dirname, process.argv[2] || '.');
const data = JSON.parse(fs.readFileSync(path.join(dir, 'report.json'), 'utf8'));
const assets = path.resolve(__dirname, '..', 'botany-letterhead', 'assets');
const b64 = (f) => 'data:image/png;base64,' + fs.readFileSync(path.join(assets, f)).toString('base64');

// ---------- formatting ----------
const round5k = (n) => Math.round(n / 5000) * 5000;
const fmt = (n) => Math.round(n).toLocaleString('en-US');
const fmt2 = (n) => n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
const neg = (n) => (n < 0 ? `(${fmt(-n)})` : fmt(n));
const aedK = (n) => (n >= 1e6 ? `AED ${(n / 1e6).toFixed(2)}M` : `AED ${Math.round(n / 1000)}k`);
const pct = (n, d = 0) => `${n >= 0 ? '+' : '−'}${Math.abs(n * 100).toFixed(d)}%`;
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const dmy = (iso) => {
  if (!iso) return '';
  const p = iso.split('-');
  if (p.length === 2) return new Date(iso + '-01T00:00:00Z').toLocaleDateString('en-GB', { month: 'short', year: 'numeric', timeZone: 'UTC' });
  return `${p[2]}/${p[1]}/${p[0]}`;
};
const monYr = (iso) => new Date(iso.slice(0, 7) + '-01T00:00:00Z').toLocaleDateString('en-GB', { month: 'short', year: 'numeric', timeZone: 'UTC' });
const D = (iso) => new Date(iso + 'T00:00:00Z');
const days = (a, b) => Math.round((D(b) - D(a)) / 864e5) + 1;

// Rent earned inside the period. Each segment is [start, end, annualRent, method]:
// "months" for whole calendar months (annual / 12 per month), "days" for part-months (annual / 365 per day).
function earned(segments) {
  return (segments || []).reduce((s, [a, b, rent, how]) => {
    if (how === 'months') {
      const months = (D(b).getUTCFullYear() - D(a).getUTCFullYear()) * 12 + D(b).getUTCMonth() - D(a).getUTCMonth() + 1;
      return s + rent / 12 * months;
    }
    return s + rent / 365 * days(a, b);
  }, 0);
}

// ---------- model ----------
const ten = Object.fromEntries((data.tenancies || []).map((t) => [t.property_id, t]));
const sc = data.service_charges?.by_property || {};
const props = data.properties.map((p) => {
  const t = ten[p.id] || null;
  const o = { ...p, t, label: `${p.building}${p.no_deed ? '' : ' · ' + p.unit}` };
  if (!p.no_deed) {
    const v = p.valuation;
    o.est = {
      mid: v.hold_at_purchase ? p.purchase_price_aed : round5k(p.area_sqft * v.psf_mid),
      low: round5k(p.area_sqft * v.psf_low), high: round5k(p.area_sqft * v.psf_high),
    };
    o.gain = o.est.mid - p.purchase_price_aed; o.gainPct = o.est.mid / p.purchase_price_aed - 1;
    o.paidPsf = p.purchase_price_aed / p.area_sqft;
  }
  o.currentRent = t && t.status === 'Rented' ? (t.renewal?.annual_rent || t.annual_rent || 0) : 0;
  o.earned = earned(t?.earned_2026);
  o.sc = sc[p.id] || 0;
  o.maint = (data.maintenance || []).filter((m) => m.property_id === p.id).reduce((s, m) => s + m.cost_aed, 0);
  o.legalCost = (data.legal_costs || []).filter((m) => m.property_id === p.id).reduce((s, m) => s + m.cost_aed, 0);
  o.net = o.earned - o.sc - o.maint - o.legalCost;
  return o;
});
const byId = Object.fromEntries(props.map((p) => [p.id, p]));
const deeded = props.filter((p) => !p.no_deed).sort((a, b) => a.purchase_date.localeCompare(b.purchase_date));
const noDeed = props.filter((p) => p.no_deed);
const sum = (arr, f) => arr.reduce((s, x) => s + f(x), 0);
const tot = {
  paid: sum(deeded, (p) => p.purchase_price_aed), mid: sum(deeded, (p) => p.est.mid),
  low: sum(deeded, (p) => p.est.low), high: sum(deeded, (p) => p.est.high), sqft: sum(deeded, (p) => p.area_sqft),
  rentNow: sum(props, (p) => p.currentRent), rentTarget: sum(props, (p) => p.currentRent || p.t?.target_rent || 0),
  earned: sum(props, (p) => p.earned), sc: sum(props, (p) => p.sc), maint: sum(props, (p) => p.maint),
  legalCost: sum(props, (p) => p.legalCost),
  excluded: sum(data.excluded_costs || [], (c) => c.cost_aed), arrears: sum(data.arrears || [], (a) => a.amount),
  reimburse: sum((data.maintenance || []).filter((m) => m.reimburse), (m) => m.cost_aed),
};
tot.gain = tot.mid - tot.paid; tot.gainPct = tot.mid / tot.paid - 1;
tot.expenses = tot.sc + tot.maint + tot.legalCost; tot.net = tot.earned - tot.expenses;
const rented = props.filter((p) => p.t?.status === 'Rented');
const vacant = props.filter((p) => p.t?.status === 'Vacant');
const year = data.period?.label || '2026';

// ---------- chart: purchase price to estimated value ----------
function growthChart() {
  const W = 680, rowH = 42, top = 26, left = 190, right = 120, H = top + rowH * deeded.length + 34;
  const xMin = 300000, xMax = 800000;
  const x = (v) => left + (v - xMin) / (xMax - xMin) * (W - left - right);
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Purchase price and estimated current value for each apartment">`;
  [300000, 400000, 500000, 600000, 700000, 800000].forEach((t) => {
    s += `<line x1="${x(t)}" x2="${x(t)}" y1="${top - 8}" y2="${H - 30}" stroke="var(--grid)" stroke-width="1"/>`;
    s += `<text x="${x(t)}" y="${H - 14}" class="axis" text-anchor="middle">${t / 1000}k</text>`;
  });
  s += `<text x="${W - right}" y="${H - 1}" class="axis" text-anchor="end">AED</text>`;
  deeded.forEach((p, i) => {
    const cy = top + i * rowH + rowH / 2, same = p.est.mid === p.purchase_price_aed;
    s += `<text x="${left - 14}" y="${cy - 3}" class="rowlab" text-anchor="end">${esc(p.building)}</text>`;
    s += `<text x="${left - 14}" y="${cy + 11}" class="rowsub" text-anchor="end">Unit ${esc(p.unit)} · bought ${monYr(p.purchase_date)}</text>`;
    s += `<rect x="${x(p.est.low)}" y="${cy - 5}" width="${x(p.est.high) - x(p.est.low)}" height="10" rx="5" fill="var(--band)"/>`;
    if (!same) s += `<line x1="${x(p.purchase_price_aed)}" x2="${x(p.est.mid)}" y1="${cy}" y2="${cy}" stroke="var(--ink-3)" stroke-width="2"/>`;
    s += `<circle cx="${x(p.purchase_price_aed)}" cy="${cy}" r="6" fill="var(--surface)" stroke="var(--c-paid)" stroke-width="2.5"/>`;
    s += `<circle cx="${x(p.est.mid)}" cy="${cy}" r="${same ? 3.5 : 6.5}" fill="var(--c-est)" stroke="var(--surface)" stroke-width="2"/>`;
    const lx = Math.max(x(p.est.high), x(p.est.mid)) + 12;
    s += `<text x="${lx}" y="${cy - 2}" class="vlab">${aedK(p.est.mid)}</text>`;
    s += `<text x="${lx}" y="${cy + 12}" class="vsub">${p.valuation.hold_at_purchase ? 'held at cost' : pct(p.gainPct) + ' since purchase'}</text>`;
  });
  return s + '</svg>';
}

// ---------- pieces ----------
const chip = (st) => st === 'Rented' ? `<span class="chip ok"><i>●</i> Rented</span>`
  : st === 'Vacant' ? `<span class="chip warn"><i>◐</i> Vacant</span>` : `<span class="chip tbc"><i>○</i> To confirm</span>`;
const pageHead = (first) => first
  ? `<img class="band" src="${b64('letterhead-header-band.png')}" alt="Botany Properties">`
  : `<div class="minihead"><b>BOTANY PROPERTIES</b><span>Portfolio Report · ${esc(data.client.salutation)} · ${esc(data.valuation_date)}</span></div>`;
const PAGES = 5;
const pageFoot = (n) => `<footer><span>BOTANY PROPERTIES L.L.C · Dubai, United Arab Emirates</span><span>Page ${n} of ${PAGES}</span></footer>`;
const page = (n, body) => `<section class="page">${pageHead(n === 1)}<div class="body">${body}</div>${pageFoot(n)}</section>`;
const partHead = (n, title, sub) => `<div class="part"><span>Part ${n}</span><h2>${title}</h2>${sub ? `<p>${sub}</p>` : ''}</div>`;

// ---------- page 1: summary + growth chart ----------
const p1 = page(1, `
  <div class="eyebrow">Portfolio Report · ${esc(data.valuation_date)}</div>
  <h1>Prepared for ${esc(data.client.salutation)}</h1>
  <p class="lede">Your ${props.length} Dubai apartments under Botany Properties management: what they cost and are worth today, what they earn, and what they cost to run in ${year}.</p>
  <div class="kpis">
    <div class="kpi"><div class="k">Apartments</div><div class="v">${props.length}</div><div class="s">${rented.length} rented · ${vacant.length} vacant</div></div>
    <div class="kpi"><div class="k">Estimated value</div><div class="v">${aedK(tot.mid)}</div><div class="s">Paid ${aedK(tot.paid)}${noDeed.length ? ` · ${deeded.length} with deeds` : ''}</div></div>
    <div class="kpi"><div class="k">Growth</div><div class="v">+${aedK(tot.gain)}</div><div class="s">${pct(tot.gainPct)} on the price paid</div></div>
    <div class="kpi"><div class="k">Rent under contract</div><div class="v">${aedK(tot.rentNow)}</div><div class="s">a year · ${aedK(tot.rentTarget)} once both vacant flats are let</div></div>
    <div class="kpi hero"><div class="k">Net earnings ${year}</div><div class="v">AED ${fmt(tot.net)}</div><div class="s">after service charges, repairs and legal costs</div></div>
  </div>
  ${partHead(1, 'Growth since purchase', 'Price on the title deed compared with an estimate of today’s value.')}
  <div class="legend"><span><svg width="16" height="16"><circle cx="8" cy="8" r="5.5" fill="none" stroke="var(--c-paid)" stroke-width="2.5"/></svg>Purchase price</span>
    <span><svg width="16" height="16"><circle cx="8" cy="8" r="6" fill="var(--c-est)"/></svg>Estimated value, ${esc(data.valuation_date)}</span>
    <span><svg width="22" height="16"><rect x="1" y="4" width="20" height="8" rx="4" fill="var(--band)"/></svg>Likely range</span></div>
  ${growthChart()}
  ${noDeed.length ? `<p class="note">${noDeed.map((p) => esc(p.building)).join(', ')} is not shown because its title deed has not been provided yet.</p>` : ''}`);

// ---------- page 2: value table + apartment register ----------
const growthRows = deeded.map((p) => `<tr><td><b>${esc(p.building)}</b><br><span class="muted">Unit ${esc(p.unit)} · ${fmt(p.area_sqft)} sq ft</span></td><td>${dmy(p.purchase_date)}</td>
  <td class="num">${fmt(p.purchase_price_aed)}</td><td class="num">${fmt(p.paidPsf)}</td><td class="num">${fmt(p.est.mid)}<br><span class="muted">${aedK(p.est.low)}–${aedK(p.est.high)}</span></td>
  <td class="num"><b>${p.valuation.hold_at_purchase ? '—' : (p.gain >= 0 ? '+' : '−') + fmt(Math.abs(p.gain))}</b><br><span class="muted">${p.valuation.hold_at_purchase ? 'held at cost' : pct(p.gainPct)}</span></td></tr>`).join('');
const deedRows = deeded.map((p) => `<tr><td><b>${esc(p.building)}</b> · ${esc(p.unit)}</td><td>${p.floor}</td><td>${esc(p.parking)}</td><td>${esc(p.deed_no)}</td><td>${esc(p.mortgage)}</td></tr>`).join('');
const p2 = page(2, `
  <h2 class="first">Value by apartment</h2>
  <table><thead><tr><th>Apartment</th><th>Purchased</th><th class="num">Price paid (AED)</th><th class="num">AED per sq ft paid</th><th class="num">Estimated value (AED)</th><th class="num">Change (AED)</th></tr></thead>
  <tbody>${growthRows}</tbody>
  <tfoot><tr><td colspan="2">Portfolio (${deeded.length} apartments)</td><td class="num">${fmt(tot.paid)}</td><td class="num">${fmt(tot.paid / tot.sqft)}</td><td class="num">${fmt(tot.mid)}</td><td class="num">+${fmt(tot.gain)}<br><span class="muted">${pct(tot.gainPct)}</span></td></tr></tfoot></table>
  <h3 class="tight">How the values were estimated</h3>
  <div class="method">${deeded.map((p) => `<p><b>${esc(p.building)}, unit ${esc(p.unit)}.</b> ${esc(p.valuation.evidence)}</p>`).join('')}
  <p class="muted">These are desktop estimates from published resale prices applied to the size on each title deed, not formal valuations. Sources are listed on the last page.</p></div>
  <h2>Title deed register</h2>
  <table class="compact"><thead><tr><th>Apartment</th><th>Floor</th><th>Parking</th><th>Title deed no.</th><th>Mortgage</th></tr></thead><tbody>${deedRows}
  ${noDeed.map((p) => `<tr><td><b>${esc(p.building)}</b> · ${esc(p.unit)}</td><td colspan="4" class="muted">Title deed not yet provided</td></tr>`).join('')}</tbody></table>
  <p class="note">All apartments are registered with the Dubai Land Department in the sole name of ${esc(data.owner?.name || data.client.name)} (owner no. ${esc(data.client.dld_owner_no)}).</p>`);

// ---------- page 3: current earnings ----------
const contract = (t) => {
  if (!t) return '';
  if (t.status === 'Vacant') return `<span class="muted">${t.target_rent ? `Target AED ${fmt(t.target_rent)} a year` : ''}</span>`;
  if (t.renewal) return `${dmy(t.renewal.start)} – ${dmy(t.renewal.end)}<br><span class="muted">renewal</span>`;
  return t.start ? `${dmy(t.start)} – ${dmy(t.end)}` : '<span class="muted">Ongoing</span>';
};
const earnRows = props.map((p) => {
  const t = p.t, yieldTxt = p.currentRent && !p.no_deed ? pct(p.currentRent / p.purchase_price_aed, 1).replace('+', '') : '—';
  return `<tr><td><b>${esc(p.building)}</b><br><span class="muted">${p.no_deed ? esc(p.unit) : 'Unit ' + esc(p.unit)}</span></td>
    <td>${chip(t?.status)}<br><span class="muted">${esc(t?.tenant || '')}</span></td><td>${contract(t)}</td>
    <td class="num">${p.currentRent ? fmt(p.currentRent) : '—'}</td><td class="num">${yieldTxt}</td></tr>`;
}).join('');
const chequeRows = props.filter((p) => p.t && (p.t.cheques || p.t.notes || p.t.renewal)).map((p) => `<div class="cq"><h4>${esc(p.label)}</h4>
  ${p.t.renewal ? `<p><b>Renewal.</b> ${esc(p.t.renewal.cheques)}. ${esc(p.t.renewal.status)}.</p>` : ''}
  ${p.t.cheques ? `<p><b>Cheques.</b> ${esc(p.t.cheques)}</p>` : ''}
  ${p.t.notes ? `<p class="muted">${esc(p.t.notes)}</p>` : ''}</div>`).join('');
const p3 = page(3, `
  ${partHead(2, 'Current earnings', `Who is renting each apartment, on what terms, and the rent under contract today.`)}
  <table class="earn"><colgroup><col style="width:27%"><col style="width:23%"><col style="width:23%"><col style="width:13%"><col style="width:14%"></colgroup><thead><tr><th>Apartment</th><th>Status / tenant</th><th>Contract</th><th class="num">Annual rent (AED)</th><th class="num">Yield on price paid</th></tr></thead>
  <tbody>${earnRows}</tbody>
  <tfoot><tr><td colspan="3">Rent under contract now</td><td class="num">${fmt(tot.rentNow)}</td><td></td></tr>
  <tr class="sub"><td colspan="3">Once ${vacant.map((p) => esc(p.building)).join(' and ')} ${vacant.length > 1 ? 'are' : 'is'} let at target rent</td><td class="num">${fmt(tot.rentTarget)}</td><td></td></tr></tfoot></table>
  <h2>Cheques and collections</h2>
  <div class="cqs">${chequeRows}</div>`);

// ---------- page 4: expenses + net earnings ----------
const otherRows = [
  ...(data.maintenance || []).map((m) => ({ ...m, kind: 'Repair', what: m.work })),
  ...(data.legal_costs || []).map((m) => ({ ...m, kind: 'Legal', what: m.item })),
].sort((a, b) => a.date.localeCompare(b.date)).map((m) => `<tr><td>${dmy(m.date)}</td><td>${esc(byId[m.property_id]?.label || '')}</td><td>${esc(m.what)}${m.paid_by ? `<br><span class="muted">Paid by ${esc(m.paid_by)}${m.reimburse ? ', to be reimbursed' : ''}</span>` : ''}</td><td class="num">${fmt(m.cost_aed)}</td></tr>`).join('');
const netRows = props.map((p) => `<tr><td><b>${esc(p.building)}</b></td><td class="num">${fmt(p.earned)}</td><td class="num">${neg(-p.sc)}</td><td class="num">${p.maint + p.legalCost ? neg(-(p.maint + p.legalCost)) : '—'}</td><td class="num"><b>${neg(p.net)}</b></td></tr>`).join('');
const p4 = page(4, `
  ${partHead(3, `Expenses and net earnings for ${year}`, `Service charges for ${esc(data.service_charges.period)}, plus repairs and legal costs paid during ${year}.`)}
  <h3 class="tight">Repairs and legal costs</h3>
  <table class="compact"><thead><tr><th>Date</th><th>Apartment</th><th>Item</th><th class="num">AED</th></tr></thead><tbody>${otherRows}</tbody>
  <tfoot><tr><td colspan="3">Total repairs and legal</td><td class="num">${fmt(tot.maint + tot.legalCost)}</td></tr></tfoot></table>
  <h3 class="tight">Net earnings by apartment, ${year}</h3>
  <table class="compact"><thead><tr><th>Apartment</th><th class="num">Rent earned</th><th class="num">Service charge</th><th class="num">Repairs / legal</th><th class="num">Net (AED)</th></tr></thead>
  <tbody>${netRows}</tbody>
  <tfoot><tr><td>Portfolio</td><td class="num">${fmt(tot.earned)}</td><td class="num">${neg(-tot.sc)}</td><td class="num">${neg(-(tot.maint + tot.legalCost))}</td><td class="num">${fmt(tot.net)}</td></tr></tfoot></table>
  <div class="statement">
    <div class="row"><span>Rent earned in ${year}</span><span>${fmt(tot.earned)}</span></div>
    <div class="row"><span>Less service charges</span><span>(${fmt(tot.sc)})</span></div>
    <div class="row"><span>Less repairs</span><span>(${fmt(tot.maint)})</span></div>
    <div class="row"><span>Less legal costs</span><span>(${fmt(tot.legalCost)})</span></div>
    <div class="row total"><span>Net earnings ${year}</span><span>AED ${fmt(tot.net)}</span></div>
    ${tot.arrears ? `<div class="row foot"><span>Of which still to be collected from the former La Fontana tenant</span><span>${fmt(tot.arrears)}</span></div>
    <div class="row foot"><span>Net earnings already collected</span><span>AED ${fmt(tot.net - tot.arrears)}</span></div>` : ''}
  </div>
  <div class="aside"><b>Not included in net earnings.</b> ${(data.excluded_costs || []).map((c) => `${esc(c.item)}: AED ${fmt(c.cost_aed)}`).join('; ')}. Total AED ${fmt(tot.excluded)}.
  ${tot.reimburse ? `<br><b>Due to Botany Properties.</b> AED ${fmt(tot.reimburse)} for the two AC repairs paid on your behalf.` : ''}</div>`);

// ---------- page 5: legal + actions + basis ----------
const legalBlocks = (data.legal || []).map((l) => `<article class="legal ${l.priority === 'High' ? 'hi' : ''}">
  <header><h4>${esc(byId[l.property_id]?.label || l.property_id)}</h4><span class="chip ${l.priority === 'High' ? 'crit' : l.priority === 'Low' ? 'tbc' : 'warn'}"><i>!</i> ${esc(l.priority)} priority</span></header>
  <p>${esc(l.issue)}</p>${l.status ? `<p class="muted">${esc(l.status)}</p>` : ''}
  <p class="action"><b>Action.</b> ${esc(l.action)}</p></article>`).join('');
const basis = [
  `Rent earned is the part of each contract that falls in ${year}: whole months at one-twelfth of the annual rent, part months by the day.`,
  ...props.filter((p) => p.t?.prior_same_rent).map((p) => `${esc(p.building)}: the tenant was in the flat before the current contract started, so January to July is counted at the current rent.`),
  ...props.filter((p) => p.t?.dates_inferred).map((p) => `${esc(p.building)}: contract taken as ${dmy(p.t.start)} to ${dmy(p.t.end)}, based on the last cheque dated 20/02/2027 and four quarterly cheques.`),
  ...props.filter((p) => p.t?.status === 'Vacant' && !(p.t.earned_2026 || []).length).map((p) => `${esc(p.building)}: no rent in ${year}.`),
  ...props.filter((p) => p.t?.no_prior_rent).map((p) => `${esc(p.building)}: no rent is counted before the current contract started on ${dmy(p.t.start)}.`),
  `Service charges are the amounts billed for ${esc(data.service_charges.period)}. Botany Properties’ management fees are not included.`,
];
const p5 = page(5, `
  <h2 class="first">Legal matters and actions required</h2>
  ${legalBlocks}
  <h2>Basis of the figures</h2>
  <ul class="basis">${basis.map((b) => `<li>${b}</li>`).join('')}</ul>
  <div class="method"><p class="muted src"><b>Sources for the value estimates.</b> ${data.sources.map(([t, u]) => `${esc(t)} (${esc(u.replace(/^https?:\/\/(www\.)?/, ''))})`).join('; ')}.</p></div>`);

const css = `
:root{--green:#283718;--sage:#5A6B4A;--ink:#1D2416;--ink-2:#4A5442;--ink-3:#858D7D;--rule:#DCE2D4;--grid:#ECEFE7;
 --surface:#FCFCFB;--tint:#F3F6EF;--band:#E1EAD5;--c-paid:#8AAE5F;--c-est:#3E6E2A;--ok:#2F7A3E;--warn:#A86A00;--crit:#B3261E}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);font:10.2pt/1.42 Carlito,Calibri,'Liberation Sans',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;background:var(--surface)}
.band{display:block;width:100%;height:auto}
.minihead{display:flex;align-items:center;gap:12px;background:var(--green);color:#E9EEE3;padding:10px .85in;font-size:8.6pt;letter-spacing:.06em;text-transform:uppercase}
.minihead b{letter-spacing:.22em;color:#fff;padding-right:12px;border-right:1px solid #5A6B4A}
.body{padding:.28in .85in 0}
footer{position:absolute;left:.85in;right:.85in;bottom:.38in;border-top:1px solid var(--green);padding-top:6px;display:flex;justify-content:space-between;font-size:8pt;color:var(--sage);letter-spacing:.08em}
footer::after{content:"";position:absolute;left:-.85in;right:-.85in;bottom:-.38in;height:6px;background:var(--green)}
.eyebrow{font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:var(--sage);font-weight:700}
h1{font-size:20pt;line-height:1.15;margin:3px 0 5px;color:var(--green)}
h2{font-size:12.5pt;color:var(--green);margin:16px 0 7px;padding-bottom:4px;border-bottom:1px solid var(--rule)} h2.first{margin-top:4px}
h3{font-size:10.5pt;color:var(--green);margin:12px 0 5px} h3.tight{margin:10px 0 4px}
h4{font-size:10pt;margin:0;color:var(--ink)}
.part{margin:16px 0 6px;border-bottom:1.5px solid var(--green);padding-bottom:5px}
.part span{font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--sage);font-weight:700}
.part h2{border:0;margin:1px 0 0;padding:0;font-size:14pt} .part p{margin:1px 0 0;color:var(--ink-2);font-size:9.4pt}
.lede{color:var(--ink-2);margin:0 0 12px;max-width:6.4in}
.kpis{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px}
.kpi{background:var(--tint);border-radius:6px;padding:8px 9px}
.kpi .k{font-size:7.6pt;text-transform:uppercase;letter-spacing:.07em;color:var(--sage);font-weight:700}
.kpi .v{font-size:14pt;font-weight:700;color:var(--ink);margin-top:2px;font-variant-numeric:tabular-nums;white-space:nowrap}
.kpi .s{font-size:8.2pt;color:var(--ink-2);line-height:1.3}
.kpi.hero{background:var(--green)} .kpi.hero .k,.kpi.hero .s{color:#C9D4BD} .kpi.hero .v{color:#fff}
.legend{display:flex;gap:18px;font-size:9pt;color:var(--ink-2);margin:4px 0 0} .legend span{display:flex;align-items:center;gap:5px}
svg .axis{font-size:9px;fill:var(--ink-3)} svg .rowlab{font-size:11px;font-weight:700;fill:var(--ink)} svg .rowsub{font-size:9.5px;fill:var(--ink-2)}
svg .vlab{font-size:11px;font-weight:700;fill:var(--ink)} svg .vsub{font-size:9.5px;fill:var(--ink-2)}
.note{font-size:8.8pt;color:var(--ink-2);margin:5px 0 0}
table{width:100%;border-collapse:collapse;font-size:9.2pt;font-variant-numeric:tabular-nums}
th{text-align:left;font-size:7.8pt;text-transform:uppercase;letter-spacing:.05em;color:var(--sage);border-bottom:1.5px solid var(--green);padding:5px 6px;vertical-align:bottom}
td{padding:5px 6px;border-bottom:1px solid var(--rule);vertical-align:top}
table.compact td{padding:3px 6px}
tfoot td{font-weight:700;border-top:1.5px solid var(--green);border-bottom:none;background:var(--tint)}
tfoot tr.sub td{font-weight:400;border-top:0;background:none;color:var(--ink-2)}
.num{text-align:right;white-space:nowrap} table.earn{table-layout:fixed} th.num{white-space:normal} table.earn td:nth-child(3){white-space:nowrap} .muted{color:var(--ink-3);font-weight:400;font-size:8.5pt}
.chip{white-space:nowrap;font-size:7.8pt;font-weight:700;border-radius:999px;padding:1px 7px;border:1px solid;display:inline-block} .chip i{font-style:normal}
.chip.ok{color:var(--ok);border-color:#BFD9C3;background:#EEF7F0} .chip.warn{color:var(--warn);border-color:#EBD3A8;background:#FFF7E8}
.chip.crit{color:var(--crit);border-color:#EDC0BC;background:#FDF1F0} .chip.tbc{color:var(--ink-2);border-color:var(--rule);background:#fff;font-weight:400}
.cqs{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:7px 12px}
.cq{border-left:3px solid var(--band);padding:1px 0 1px 9px} .cq p{margin:2px 0;font-size:8.9pt}
.statement{margin:12px 0 0 auto;width:4.4in;font-variant-numeric:tabular-nums;font-size:9.6pt}
.statement .row{display:flex;justify-content:space-between;padding:3px 8px;border-bottom:1px solid var(--rule)}
.statement .total{background:var(--green);color:#fff;font-weight:700;font-size:11pt;border:0;padding:6px 8px;border-radius:4px;margin-top:3px}
.statement .foot{color:var(--ink-2);font-size:8.9pt;border:0}
.aside{margin-top:10px;font-size:8.7pt;color:var(--ink-2);background:var(--tint);border-radius:6px;padding:7px 10px}
.legal{border-left:3px solid var(--warn);padding:2px 0 2px 11px;margin-bottom:8px} .legal.hi{border-left-color:var(--crit)}
.legal header{display:flex;justify-content:space-between;align-items:center} .legal p{margin:2px 0;font-size:9.1pt}
.basis{margin:0;padding-left:16px;font-size:8.8pt;color:var(--ink-2)} .basis li{margin-bottom:2px}
.method p{margin:0 0 3px;font-size:8.4pt;line-height:1.35} .src{font-size:7.5pt;line-height:1.35}
`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Portfolio Report · ${esc(data.client.name)}</title><style>${css}</style></head>
<body>${p1}${p2}${p3}${p4}${p5}</body></html>`;

const out = path.join(dir, 'out');
fs.mkdirSync(out, { recursive: true });
const htmlPath = path.join(out, 'report.html');
fs.writeFileSync(htmlPath, html);
const pdfPath = path.join(out, `${data.client.name.replace(/\s+/g, '_')}_Portfolio_Report.pdf`);
fs.writeFileSync(path.join(out, 'figures.json'), JSON.stringify({ tot, props: props.map((p) => ({ id: p.id, earned: p.earned, sc: p.sc, maint: p.maint, legal: p.legalCost, net: p.net, rent: p.currentRent, est: p.est })) }, null, 1));

(async () => {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const pg = await browser.newPage();
  await pg.goto('file://' + htmlPath);
  // Fail loudly if any page's content runs into its footer.
  const overflow = await pg.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
    const body = p.querySelector('.body'), foot = p.querySelector('footer');
    return body.getBoundingClientRect().bottom > foot.getBoundingClientRect().top - 6 ? i + 1 : null;
  }).filter(Boolean));
  await pg.pdf({ path: pdfPath, width: '8.5in', height: '11in', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  console.log('written', pdfPath, overflow.length ? `OVERFLOW on page(s) ${overflow.join(', ')}` : 'no overflow');
})();
