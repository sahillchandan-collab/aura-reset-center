import sys
out = sys.argv[1]
def copy(label):
    rows = "".join(f"<tr><td class=n>{i}</td><td></td><td></td><td></td><td></td></tr>" for i in range(1, 6))
    pk = lambda name, desc, price: f'<div class=pk><span class=box></span><b>{name}</b><span class=d>{desc}</span><span class=p>AED {price} / month</span></div>'
    return f"""
<section class=page>
 <header>
  <div class=brand><img src="logo-black.svg" alt="Yontro"></div>
  <div class=title>
   <div class=copy>{label}</div>
   <h1>INVOICE</h1>
   <table class=meta><tr><td>Invoice no.</td><td class=line>YON-</td></tr><tr><td>Invoice date</td><td class=line></td></tr><tr><td>Payment due</td><td class=line><span class=hint>in advance, before the service month starts</span></td></tr></table>
  </div>
 </header>
 <div class=from>Yontro - F.Z.E &middot; Ajman Free Zone licence 57169 &middot; Office 214, Clover Bay Tower, Business Bay, Dubai &middot; TRN: ____________________ &middot; +971 52 432 1112 &middot; admin@yontro.ae &middot; yontro.ae</div>
 <div class=grid2>
  <div class=card><h3>Bill to</h3>
   <div class=f><span>Business name</span><i></i></div><div class=f><span>Contact person</span><i></i></div>
   <div class=f><span>Address</span><i></i></div><div class=f2><div class=f><span>Trade licence</span><i></i></div><div class=f><span>TRN</span><i></i></div></div>
   <div class=f2><div class=f><span>Phone</span><i></i></div><div class=f><span>Email</span><i></i></div></div></div>
  <div class=card><h3>Service</h3>
   {pk("Launch", "5 videos + 5 posts", "5,000")}{pk("Growth", "10 videos + 10 posts", "7,500")}{pk("Scale", "15 videos + 15 posts", "10,000")}
   <div class=pk><span class=box></span><b style="width:auto;margin-right:2mm">Add-ons / other</b><span class=d>itemised below</span></div>
   <div class=f><span>Service period: from</span><i></i><span>to</span><i></i></div><div class=pk style="margin-top:2mm"><b style="width:13mm">Term</b><span class=box></span>3 months<span class=box style="margin-left:4mm"></span>2<span class=box style="margin-left:4mm"></span>1</div><div class=f><span>This invoice covers month</span><i class=short></i><span>of</span><i class=short></i></div></div>
 </div>
 <table class=items><thead><tr><th class=n>#</th><th>Description</th><th class=q>Qty</th><th class=r>Rate (AED)</th><th class=a>Amount (AED)</th></tr></thead><tbody>{rows}</tbody></table>
 <div class=grid2b>
  <div>
   <div class=card><h3>Payment method</h3>
    <div class=pay><span><span class=box></span>Cash</span><span><span class=box></span>Card</span><span><span class=box></span>Cheque</span></div>
    <div class=f2><div class=f><span>Cheque no.</span><i></i></div><div class=f><span>Bank</span><i></i></div></div>
    <div class=f2><div class=f><span>Cheque date</span><i></i></div><div class=f><span>Card receipt / ref.</span><i></i></div></div>
    <div class=f2><div class=f><span>Amount received (AED)</span><i></i></div><div class=f><span>Balance due (AED)</span><i></i></div></div>
   </div>
   <div class=words><span>Amount in words</span><i></i><i></i></div>
  </div>
  <table class=totals>
   <tr><td>Subtotal</td><td></td></tr>
   <tr><td>Discount <small>(referral / promo code: ________)</small></td><td></td></tr>
   <tr><td>VAT 5% <small>(only if TRN shown)</small></td><td></td></tr>
   <tr class=grand><td>TOTAL DUE (AED)</td><td></td></tr>
  </table>
 </div>
 <div class=sign>
  <div><i></i><span>Client name and signature</span></div><div><i></i><span>Date</span></div>
  <div><i></i><span>For Yontro: name and signature</span></div><div class=stampbox><img src="yontro-stamp-blue.png" alt="Company stamp"></div>
 </div>
 <div class=terms><h4>Terms and conditions</h4><ol>
  <li>Fees are payable in advance: the first month on signing, then each month before it starts. All amounts are in UAE dirhams (AED).</li>
  <li>Work starts, and continues, once the month's payment is received (cheques once cleared). Fees paid are non-refundable; any videos Yontro misses are delivered the next month or credited.</li>
  <li>Issued under the Yontro Service Agreement signed by the client. Standard commitment: 3 months; a 1- or 2-month term applies only if agreed in that agreement. Afterwards month to month with 30 days' written notice.</li>
  <li>Ad spend for paid campaigns is paid by the client directly to the ad platforms and is not included in this invoice.</li>
  <li>Cheques are payable to &ldquo;Yontro - F.Z.E&rdquo;. A returned cheque must be replaced within 3 working days; bank charges for returned cheques are paid by the client.</li>
  <li>Cash payments are valid only against this invoice signed and stamped by Yontro. Card payments require the terminal receipt.</li>
  <li>Yontro may pause work, including posting, while a payment is overdue.</li>
  <li>The client owns the final videos, designs and website on full payment. Yontro keeps raw footage, methods and templates.</li>
  <li>VAT is charged at 5% only if Yontro is VAT-registered and its TRN is shown above.</li>
  <li>Governed by the laws of the UAE; disputes go to the competent UAE courts. Not valid without an authorised signature and company stamp. E&amp;OE.</li>
 </ol></div>
 <footer><span>Thank you for choosing Yontro.</span><span class=tag>Social media that brings customers.</span></footer>
</section>"""
css = """
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font:9.2pt 'Sora',Arial,sans-serif;color:#0B0B0B}
.page{width:210mm;height:297mm;padding:10mm 12mm 12mm;position:relative;page-break-after:always;border-left:5mm solid #FF5A1F;overflow:hidden}
h1,h3,h4,.copy{font-family:'Michroma',Arial,sans-serif;font-weight:400;margin:0}
header{display:flex;justify-content:space-between;align-items:flex-start}
.brand img{height:19mm;margin:-3mm 0 0 -3mm}
.title{text-align:right}.title h1{font-size:22pt;letter-spacing:.06em;margin:1mm 0 1mm}
.copy{display:inline-block;background:#0B0B0B;color:#fff;font-size:7pt;letter-spacing:.18em;padding:1.2mm 3mm;border-radius:10mm}
.meta{margin-left:auto;border-collapse:collapse;font-size:8.5pt}.meta td{padding:1mm 0 1mm 3mm}.meta td:first-child{color:#555;text-align:right}
.meta .line{border-bottom:.3mm solid #0B0B0B;width:44mm;text-align:left;font-weight:600}.hint{color:#999;font-size:7pt;font-weight:400}
.from{font-size:7.4pt;color:#444;border-top:.6mm solid #0B0B0B;border-bottom:.2mm solid #ccc;padding:2mm 0;margin:2mm 0 3mm}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.grid2b{display:grid;grid-template-columns:1.25fr 1fr;gap:4mm;align-items:start}
.card{border:.3mm solid #d4d0c8;border-radius:2.5mm;padding:2.5mm 3.5mm}
h3{font-size:7.5pt;letter-spacing:.16em;color:#E0420C;margin-bottom:2mm;text-transform:uppercase}
.f{display:flex;align-items:flex-end;gap:2mm;margin:1.8mm 0;font-size:8pt;color:#555;flex:1}.f span{white-space:nowrap}.f i{flex:1;border-bottom:.25mm solid #888;height:4mm}.f i.short{flex:0 0 12mm}.f em{font-style:normal;font-size:7pt;color:#999}
.f2{display:flex;gap:4mm}
.box{display:inline-block;width:3.6mm;height:3.6mm;border:.35mm solid #0B0B0B;border-radius:.6mm;vertical-align:middle;margin-right:2mm;flex:0 0 auto}
.pk{display:flex;align-items:center;font-size:8.3pt;margin:1.6mm 0}.pk b{width:15mm}.pk .d{color:#555;flex:1;font-size:7.4pt}.pk .p{font-weight:600}
.items{width:100%;border-collapse:collapse;margin:3mm 0}.items th{background:#0B0B0B;color:#fff;font-weight:600;font-size:7.8pt;text-align:left;padding:2mm}
.items td{border-bottom:.25mm solid #d4d0c8;height:6.4mm;padding:0 2mm}.items .n{width:8mm;color:#999;text-align:center}.items .q{width:14mm}.items .r{width:26mm}.items .a{width:30mm}
.items td:nth-child(n+3){border-left:.25mm solid #eee}
.pay{display:flex;gap:9mm;font-size:10pt;font-weight:600;margin:1mm 0 2.5mm}.pay .box{width:4.6mm;height:4.6mm}
.words{display:flex;flex-direction:column;font-size:8pt;color:#555;margin-top:3mm}.words i{border-bottom:.25mm solid #888;height:5mm}
.totals{width:100%;border-collapse:collapse;font-size:8.6pt}.totals td{padding:2.3mm 2mm;border-bottom:.25mm solid #d4d0c8}.totals td:last-child{width:32mm;border-left:.25mm solid #eee}
.totals small{color:#888;font-size:6.8pt}.grand td{background:#FF5A1F;color:#0B0B0B;font-weight:700;font-size:10pt;border:none}
.sign{display:grid;grid-template-columns:1.4fr .7fr 1.4fr .9fr;gap:5mm;align-items:end;margin:3mm 0 2mm}.sign div{display:flex;flex-direction:column;font-size:7.4pt;color:#555}.sign i{border-bottom:.3mm solid #0B0B0B;height:8mm;margin-bottom:1mm}
.stampbox{height:22mm;display:flex;align-items:center;justify-content:center}.stampbox img{width:24mm;transform:rotate(-9deg);opacity:.9;mix-blend-mode:multiply}.stamp{border:.3mm dashed #aaa;border-radius:50%;height:16mm;align-items:center;justify-content:center;color:#bbb!important}
.terms{border-top:.6mm solid #0B0B0B;padding-top:2mm}.terms h4{font-size:7pt;letter-spacing:.16em;margin-bottom:1mm}
.terms ol{columns:2;column-gap:7mm;margin:0;padding-left:4mm;font-size:6.3pt;line-height:1.33;color:#333}.terms li{break-inside:avoid;margin-bottom:.6mm}
footer{position:absolute;left:12mm;right:12mm;bottom:5mm;display:flex;justify-content:space-between;font-size:7pt;color:#777}.tag{font-family:'Michroma',Arial;color:#E0420C;font-size:6.5pt;letter-spacing:.1em}
"""
html = f"""<!doctype html><html><head><meta charset=utf-8><title>Yontro Invoice</title>
<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Michroma&family=Sora:wght@300;400;600;700&display=swap"><style>{css}</style></head>
<body>{copy("CUSTOMER COPY")}{copy("OFFICE COPY")}</body></html>"""
open(out, "w").write(html)
