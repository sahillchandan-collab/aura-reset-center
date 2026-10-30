emps = [
 ("Lianna Gozmao", "Account Manager & Content Strategist", (1500, 1800, 700), "One thousand seven hundred and thirty-three dirhams and thirty-three fils"),
 ("Azeem Shafi", "Videographer & Video Editor", (1500, 2000, 800), "One thousand eight hundred and sixty-three dirhams and thirty-three fils"),
 ("Usama Rehman", "Sales Agent", (1500, 1500, 700), "One thousand six hundred and three dirhams and thirty-three fils"),
]
def pr(x): return round(x/30*13, 2)
def page(name, role, comp, words):
    b, h, t = comp; tot_m = b+h+t; total = pr(tot_m)
    pb, ph = pr(b), pr(h); pt = round(total-pb-ph, 2)
    f = lambda x: f"{x:,.2f}"
    return f"""<section class=page>
<header><img src="logo-black.svg"><div class=ttl><h1>SALARY PAYOUT</h1><div class=sub>CASH PAYMENT CONSENT &amp; RECEIPT</div><div class=meta>Ref. <b>YPAY-2026-10-</b></div></div></header>
<div class=from>Yontro - F.Z.E &middot; Licence 57169 (Ajman Free Zone) &middot; Office 214, Clover Bay Tower, Business Bay, Dubai &middot; admin@yontro.ae</div>
<h2>1. Employee</h2>
<table class=kv><tr><td>Full name</td><td><b>{name}</b></td><td>Position</td><td><b>{role}</b></td></tr>
<tr><td>Passport / Emirates ID no.</td><td class=line></td><td>Mobile</td><td class=line></td></tr></table>
<h2>2. Pay period and calculation</h2>
<table class=kv><tr><td>Pay period</td><td><b>19 October 2026 – 31 October 2026</b></td><td>Days paid</td><td><b>13 calendar days</b> (12 working days + 1 rest day)</td></tr>
<tr><td>Basis</td><td colspan=3>Monthly salary &divide; 30 &times; 13 days, as per the offer of employment, section 4</td></tr></table>
<table class=calc><thead><tr><th>Component</th><th>Monthly (AED)</th><th>Pro-rata, 13 days (AED)</th></tr></thead><tbody>
<tr><td>Basic salary</td><td>{f(b)}</td><td>{f(pb)}</td></tr>
<tr><td>Housing allowance</td><td>{f(h)}</td><td>{f(ph)}</td></tr>
<tr><td>Transport allowance</td><td>{f(t)}</td><td>{f(pt)}</td></tr>
<tr><td>Deductions (absence / penalties, if any)</td><td>—</td><td class=blank>&minus; ____________</td></tr>
<tr class=tot><td>NET AMOUNT PAID IN CASH</td><td></td><td>AED {f(total)}</td></tr></tbody></table>
<div class=words><span>Amount in words</span><b>{words} only</b></div>
<h2>3. Consent to cash payment</h2>
<ol class=decl>
<li>I agree to receive my salary for the pay period above <b>in cash</b>, instead of through the Wage Protection System (WPS), at my own request and with the Company's agreement. This consent applies only to the pay period stated on this form.</li>
<li>I confirm I have counted the cash in the presence of the Company's representative and received the <b>full net amount</b> shown above, which matches the calculation in section 2.</li>
<li>I understand that commission, retention or upsell payments are not part of this payout. They are calculated and paid separately under the schemes in my offer of employment.</li>
<li>This form does not change my employment terms or any right I have under UAE Labour Law, including end-of-service benefits, which are calculated on my basic salary.</li>
<li>Any discrepancy must be raised in writing before signing. Once signed, this form is the receipt for this payment.</li></ol>
<h2>4. Signatures</h2>
<div class=sig>
 <div class=card><h3>Employee</h3><div class=f><span>Signature</span><i class=tall></i></div><div class=f><span>Date</span><i></i></div><div class=f><span>Place</span><i></i></div></div>
 <div class="card co"><h3>For Yontro - F.Z.E</h3><div class=stamp>Company stamp</div><div class=f><span>Name</span><i></i></div><div class=f><span>Signature</span><i class=tall></i></div><div class=f><span>Date</span><i></i></div></div>
 <div class=card><h3>Witness</h3><div class=f><span>Name</span><i></i></div><div class=f><span>Signature</span><i class=tall></i></div><div class=f><span>Date</span><i></i></div></div>
</div>
<footer><span>Original: Company file &middot; Copy: Employee</span><span>Yontro - F.Z.E &middot; Private and confidential</span></footer>
</section>"""
css = """@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font:9pt/1.45 'Sora',Arial,sans-serif;color:#0B0B0B}
.page{width:210mm;height:297mm;padding:11mm 13mm 14mm;position:relative;page-break-after:always;border-left:5mm solid #FF5A1F;overflow:hidden}
h1,h2,h3{font-family:'Michroma',Arial,sans-serif;font-weight:400;margin:0}
header{display:flex;justify-content:space-between;align-items:flex-start}header img{height:18mm;margin:-3mm 0 0 -3mm}
.ttl{text-align:right}.ttl h1{font-size:19pt;letter-spacing:.05em}.sub{font-family:'Michroma';font-size:7.5pt;letter-spacing:.14em;color:#E0420C;margin-top:1mm}
.meta{font-size:8pt;color:#555;margin-top:2mm}.meta b{display:inline-block;border-bottom:.3mm solid #0B0B0B;min-width:30mm;color:#0B0B0B}
.from{font-size:7.4pt;color:#444;border-top:.6mm solid #0B0B0B;border-bottom:.2mm solid #ccc;padding:2mm 0;margin:3mm 0 1mm}
h2{font-size:7.8pt;letter-spacing:.14em;color:#E0420C;text-transform:uppercase;margin:4.5mm 0 2mm}
table{width:100%;border-collapse:collapse}table.kv td{padding:2mm 2mm;border-bottom:.25mm solid #e2ded6;font-size:8.6pt}table.kv td:nth-child(odd){color:#666;width:22%}
td.line{border-bottom:.3mm solid #888!important}
table.calc th{background:#0B0B0B;color:#fff;text-align:left;font-weight:600;font-size:8pt;padding:2.2mm}table.calc td{padding:2.4mm;border-bottom:.25mm solid #e2ded6}
table.calc td:not(:first-child),table.calc th:not(:first-child){text-align:right}td.blank{color:#999}
tr.tot td{background:#FF5A1F;font-weight:700;font-size:10pt;border:none}
.words{display:flex;gap:4mm;align-items:baseline;border-bottom:.3mm solid #888;padding:3mm 0 1.5mm;font-size:8.6pt}.words span{color:#666;white-space:nowrap}
ol.decl{margin:0;padding-left:5mm;font-size:8.2pt;line-height:1.5}ol.decl li{margin-bottom:1.6mm}
.sig{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:4mm}.card{border:.3mm solid #d4d0c8;border-radius:2.5mm;padding:3mm 3.5mm;position:relative}.card h3{font-size:7.5pt;letter-spacing:.12em;margin-bottom:1mm}
.f{display:flex;align-items:flex-end;gap:2mm;margin:2.6mm 0;font-size:7.8pt;color:#555}.f i{flex:1;border-bottom:.25mm solid #888;height:4mm}.f i.tall{height:11mm}
.card.co{padding-right:25mm}.stamp{position:absolute;right:3mm;top:50%;margin-top:-9.5mm;width:19mm;height:19mm;border:.3mm dashed #aaa;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#bbb;font-size:5.8pt;text-align:center}
footer{position:absolute;left:13mm;right:13mm;bottom:6mm;display:flex;justify-content:space-between;font-size:7pt;color:#777;border-top:.25mm solid #d4d0c8;padding-top:1.6mm}"""
html = f"""<!doctype html><html><head><meta charset=utf-8><title>Yontro Salary Payout Forms</title>
<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Michroma&family=Sora:wght@300;400;600;700&display=swap"><style>{css}</style></head><body>""" + "".join(page(*e) for e in emps) + "</body></html>"
open("payout.html","w").write(html)
