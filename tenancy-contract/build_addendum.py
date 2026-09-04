"""Rebuild the "additional conditions" addendum pages of the Botany tenancy contract.

Usage: python3 build_addendum.py <original_contract.pdf> <output_contract.pdf>

Pages 1-3 (Ejari unified contract) and the final Botany cover page are kept
verbatim from the original; the addendum pages in between are regenerated.
"""
import sys
from pathlib import Path

import pymupdf
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

HERE = Path(__file__).parent
FONTS = HERE / "fonts"

# ---------------------------------------------------------------- deal data
DEAL = {
    "deposit": "AED 3,000",
    "broker_fee": "AED 1,500",
    "annual_rent": "AED 47,000",
    "occupants": ["Abdelatif Aissa"],
    "payments": [
        ("March 18th, 2026", "AED 11,750"),
        ("June 18th, 2026", "AED 11,750"),
        ("September 18th, 2026", "AED 11,750"),
        ("December 18th, 2026", "AED 11,750"),
    ],
}


def register_fonts():
    for name in ["Light", "Regular", "Medium", "Bold", "LightItalic", "BoldItalic"]:
        pdfmetrics.registerFont(TTFont(f"Montserrat-{name}", str(FONTS / f"Montserrat-{name}.ttf")))
    pdfmetrics.registerFontFamily("Montserrat-Light", normal="Montserrat-Light",
                                  bold="Montserrat-Bold", italic="Montserrat-LightItalic",
                                  boldItalic="Montserrat-BoldItalic")


BODY = ParagraphStyle("body", fontName="Montserrat-Light", fontSize=9, leading=13.5,
                      alignment=TA_JUSTIFY, spaceAfter=7)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=22, firstLineIndent=-22)
SUB = ParagraphStyle("sub", parent=BODY, leftIndent=62, firstLineIndent=-30, spaceAfter=3)
NOTE = ParagraphStyle("note", parent=BODY, leftIndent=22)
HEAD = ParagraphStyle("head", fontName="Montserrat-Medium", fontSize=9, leading=13,
                      spaceBefore=10, spaceAfter=6, leftIndent=8, keepWithNext=1)
SIG = ParagraphStyle("sig", fontName="Montserrat-Regular", fontSize=8, leading=11)


class Addendum:
    def __init__(self):
        self.story = []
        self.n = 0
        self._pending_heading = None

    def heading(self, text):
        # glued to the following clause so a heading never ends a page alone
        self._pending_heading = Paragraph(text, HEAD)

    def clause(self, text, subs=None, note=None):
        self.n += 1
        block = []
        if self._pending_heading is not None:
            block.append(self._pending_heading)
            self._pending_heading = None
        block.append(Paragraph(f"{self.n}.&nbsp;&nbsp;{text}", CLAUSE))
        for i, s in enumerate(subs or [], 1):
            block.append(Paragraph(f"{self.n}.{i}&nbsp;&nbsp;&nbsp;{s}", SUB))
        if subs:
            block.append(Spacer(1, 4))
        if note:
            block.append(Paragraph(note, NOTE))
        self.story.append(KeepTogether(block))
        return self.n


def build_story(d):
    a = Addendum()
    b = lambda s: f"<b>{s}</b>"  # noqa: E731

    a.heading("Deposit")
    a.clause(
        f"The tenant shall pay {b(d['deposit'])} security deposit to the landlord. This will be "
        "refunded to the tenant when vacating, subject to:",
        subs=["the premise is left in a satisfactory condition, allowing for reasonable wear and tear",
              "all keys, remotes and/or access cards are returned to the landlord",
              "the tenant provides the receipt of the final payment for all utility charges"],
        note="The security deposit will be used by the landlord in case of any loss or damage to the "
             "property during the period of tenancy, and only for the value of damage incurred.")
    broker = a.clause(
        f"Upon signing this lease, the tenant shall pay a non-refundable broker fee of {b(d['broker_fee'])} "
        "inclusive of VAT.")
    a.clause(
        "Should the tenant decide to terminate the tenancy contract prior to the contract start date, the "
        "deposit and broker fee will be forfeited, and any rental cheques provided will be returned to the tenant.")
    a.clause(
        "If the landlord decides to terminate the contract prior to the contract start date, the landlord will "
        "return the security deposit and annual rent cheques to the tenant, as well as refunding the tenant the "
        f"total sum of the broker fee mentioned in addendum number {broker}.")

    a.heading("Use of premise &amp; occupancy")
    a.clause(
        "The tenant may use the premises only as a property of residence (residential purposes only) and must "
        "not use the premises for any illegal purpose.")
    a.clause("No sub-leasing or transferring under any circumstances unless agreed by the landlord in writing.")
    a.clause(
        "The tenant will abide by the rules and regulations given by the security, facility management company "
        "and developer of the community.")
    occ = "; ".join(f"({i}) {b(n)}" for i, n in enumerate(d["occupants"], 1))
    a.clause(
        "Only the individual(s) named below are permitted to reside in the premises for the tenancy period: "
        f"{occ}. Any other person who intends to stay in the premises for longer than 7 (seven) consecutive days "
        "must be notified to Botany Properties in writing, together with a copy of that person's identification, "
        "prior to their stay. Such a stay is permitted only upon the written approval of the landlord, which may "
        "be granted or refused at the landlord's discretion. Any unapproved occupancy shall be treated as a "
        "breach of this contract and the tenant shall remain fully liable for the conduct of, and any damage "
        "caused by, all occupants and visitors.")

    a.heading("Maintenance")
    a.clause(
        "The tenant agrees to keep the property, including but not limited to any fixtures, fittings, "
        "furniture, appliances and electrical goods, in good condition throughout the term of the tenancy contract.")
    a.clause(
        "All general maintenance work in the property resulting from misuse or negligence by the tenant is the "
        "responsibility of the tenant, irrespective of the cost.")
    a.clause(
        "All minor maintenance is the responsibility of the tenant. Maintenance repair works amounting to "
        f"{b('AED 1,000')} and below are the tenant's responsibility.")
    a.clause(
        f"{b('Air-conditioning / chiller and plumbing:')} the maintenance, servicing and repair of the "
        "air-conditioning and chiller system (including FCUs, thermostats, filters, ducting and drainage) and of "
        "all plumbing (including pipes, taps, mixers, water heaters, drains, toilets and leaks) is the sole "
        "responsibility of the tenant for the full duration of the tenancy, regardless of the cost of the works. "
        "The landlord shall not bear or reimburse any repair, servicing or replacement cost relating to these "
        "systems. The tenant shall use a licensed contractor and shall keep the AC system regularly serviced. "
        "This clause supersedes any other clause in this addendum and article 8 of the tenancy contract as regards "
        "the AC / chiller and plumbing.")
    a.clause(
        "Save for the AC / chiller and plumbing set out above, major maintenance of the electrical, mechanical "
        "and structural elements of the property is the responsibility of the landlord. Maintenance repair works "
        f"amounting to more than {b('AED 1,000')} for those elements are the landlord's responsibility, provided "
        "the fault did not result from misuse or negligence by the tenant.")
    a.clause(
        "The tenant agrees not to make any structural, mechanical or electrical alterations without written "
        "permission from the landlord. No carpets shall be glued to the tiles, nor shall holes be drilled into tiles.")

    a.heading("Furniture, fixtures &amp; appliances")
    a.clause(
        "Where the property is let furnished, or contains fixtures, fittings or appliances belonging to the "
        "landlord, an inventory / handover report shall be signed by both parties at handover. The tenant shall "
        "not remove, replace, dispose of or alter any item of furniture, fixture, fitting or appliance without "
        "first submitting a written request to Botany Properties. Any replacement or change may only be carried "
        "out after the landlord's written approval has been obtained through Botany Properties.")
    a.clause(
        "Any item replaced by the tenant, with approval, must be of equal or higher value, quality and "
        "specification than the existing item of furniture, fixture, fitting or appliance. The replacement item "
        "shall become the property of the landlord and shall remain in the premises on vacating, unless the "
        "landlord agrees otherwise in writing. The original item shall not be disposed of without the landlord's "
        "written approval and, where the landlord so requests, shall be stored safely and returned on vacating. "
        "Any unauthorised replacement, or any replacement of lesser value, entitles the landlord to recover the "
        "full replacement cost from the tenant and/or the security deposit.")

    a.heading("Vacating condition")
    a.clause(
        "Upon vacating the property, the tenant will be responsible for filling any holes in the walls and "
        "restoring any other modification to the surfaces to their original condition. The tenant shall, at the "
        "tenant's own cost and before handing back the keys, (a) repaint all the internal walls and ceilings of "
        "the apartment in the original colour and finish, and (b) professionally deep clean the whole apartment, "
        "especially the bathrooms and kitchen, and return the property in a clean condition, free of the tenant's "
        "belongings and rubbish. Should the tenant fail to do so, the landlord may have the painting and cleaning "
        "carried out and deduct the cost from the security deposit, with any shortfall payable by the tenant.")

    a.heading("Additional Fees | Rental Payments / Non-payments")
    a.clause(
        "The landlord is responsible for paying any developer's management fees, including service charges and "
        "major maintenance fees, for the duration of the ownership of the property.")
    a.clause(
        "Water, electricity, sewerage consumption (DEWA, or any other service providers), cooling / chiller "
        "consumption charges and municipality taxes are the responsibility of the tenant, and all accounts should "
        "be closed when the tenancy expires and the tenant vacates the property.")
    a.clause(
        "The tenant shall be responsible for arranging insurance for their personal belongings and will not have "
        "the right to claim from the landlord for compensation for any losses or damages during the tenancy contract.")
    pay = d["payments"]
    a.clause(
        f"The tenant agrees to make {b(str(len(pay)) + ' payments')} by cheque towards the annual rent of "
        f"{b(d['annual_rent'])} on the following dates:",
        subs=[f"{b(f'Payment {i} &ndash; on or before {date} for the amount of {amt}')}"
              for i, (date, amt) in enumerate(pay, 1)])
    a.clause(
        "In the event of a rent cheque not being honoured or bouncing, or a rent payment / wire transfer not "
        "being received on or before the date agreed above, the tenant agrees:",
        subs=[
            f"to pay the landlord a penalty of {b('AED 1,000/-')} per bounced cheque or delayed payment. The "
            "penalty must be paid within 24 (twenty-four) hours of the cheque bouncing or the payment falling "
            "due. In addition, the outstanding rent must be cleared in full within 72 (seventy-two) hours.",
            "that if the penalty is not paid within the 24-hour period, the landlord holds all rights to open a "
            "case against the tenant before the Rental Dispute Centre and/or any competent court for the penalty "
            "amount, and all legal charges, court fees, lawyer's fees and related expenses incurred by the "
            "landlord in doing so shall be borne and paid by the tenant.",
            "that failure to settle the outstanding rent and the associated penalty within the specified "
            "timeframe will result in a legal 30-day notice being issued to the tenant, as per Article 25 of Law "
            "No. (33) of 2008 under the Dubai Real Estate Legislation.",
            "that if the tenant does not settle the outstanding payment within the 30-day notice period, the "
            "landlord reserves the right to initiate an eviction case with RERA / the Rental Dispute Centre "
            f"against the tenant. The landlord is at liberty to retain the security deposit of {b(d['deposit'])} "
            "in full from the tenant to guarantee and/or cover the condition of the premises at the end of the "
            "tenancy contract, provided the landlord undertakes to refund the security deposit, or any part "
            "thereof, after deduction for any works / repairs or any unpaid utility bills within a reasonable "
            "period upon returning possession to the landlord.",
            "that a bounced cheque is a criminal offence under UAE law, and the landlord's rights under this clause "
            "are without prejudice to any other rights or remedies available to the landlord.",
        ])
    a.clause(
        f"Should Botany renew this tenancy agreement, the tenant agrees to pay the broker a fee of {b(d['broker_fee'])} "
        "inclusive of VAT in respect of drafting a new agreement, arranging the signing of the contracts for both "
        "parties and for the collection and delivery of rental cheques.")
    ej = a.n + 1
    a.clause(
        "It is common practice that the tenant is responsible to register the contract with EJARI. By signing this "
        f"addendum, both the tenant and landlord are confirming that addendum (no. {ej}) supersedes article 14 of the "
        "tenancy contract and that it will be the tenant's responsibility to register the contract with EJARI upon "
        "commencement of the lease, as well as cancelling the EJARI upon termination.")

    a.heading("Renewal &amp; rent increase")
    a.clause(
        f"On each renewal of this tenancy the annual rent shall increase by a minimum of {b('5% (five percent)')} "
        "over the rent of the expiring year, or by the highest increase permitted under the RERA Rental Index "
        "Calculator of the Dubai Land Department at the time of renewal, whichever is higher. The tenant "
        "acknowledges and agrees that this clause constitutes prior written notice of the rent increase for every "
        "renewal, that no separate notice of increase is required to be served before renewal, and that the "
        "increase shall be deemed accepted by the tenant on renewal. The only exception is where the RERA Rental "
        "Index Calculator / Dubai Land Department does not permit any increase for the property at the time of "
        "renewal, in which case the increase shall be limited to the maximum permitted (if any).")

    a.heading("Vacating / Notices")
    a.clause(
        "The landlord will give the tenant not less than 48 hours' notice (except in the case of an emergency) "
        "to enter the property to inspect, maintain, repair, alter, improve or rebuild.")
    a.clause(
        "In the event that the tenant wishes to vacate or renew the lease at the end of the tenancy, they should "
        "notify the landlord in writing 60 days prior to the expiry date of the rental contract.")
    a.clause(
        "Any change to the terms and conditions of the tenancy contract on renewal, other than the rent increase "
        "provided for above, shall be notified by the landlord to the tenant in writing 90 days prior to the end "
        "of the contract.")
    a.clause(
        "The parties agree that there may be instances where the tenant shall need to terminate the lease early. "
        "In this event, and in accordance with current guidelines, the tenant will provide the landlord with 3 "
        "months' notice in writing and incur a two-month rent penalty; the landlord agrees to refund any "
        "outstanding rental amount.")
    a.clause(
        "In the event that the landlord wishes to sell the property, the tenant agrees to allow access to the "
        "property for viewings, if reasonable notice (48 hours) is given. If the property is sold during the term "
        "of the contract, the tenant has the right to remain in the property for the duration of this contract at "
        "the same rental rate. The rights of the tenant in the event of a sale shall be governed by RERA, unless "
        "otherwise agreed between the tenant and the landlord.")
    a.clause(
        "If the landlord wishes to evict the tenant, then the landlord must issue 12 months' written notice to the "
        "tenant, attested by the notary public and sent by recorded delivery. The conditions for the eviction must "
        "be compliant with current RERA law and regulations.")

    a.heading("Other Terms &amp; Conditions")
    a.clause(
        "The landlord confirms that the previous tenants have settled and closed all DEWA, or any other service "
        "providers' accounts prior to the start date of the lease.")
    a.clause(
        "This lease agreement shall be subject to the Laws of Dubai, the United Arab Emirates, and any dispute "
        "shall be referred to the Rental Dispute Centre. It is prepared in English, and if there is any ambiguity "
        "between the English text and any Arabic translation, the English shall prevail.")
    a.clause(
        "This property is LET ONLY by Botany, and Botany act as a letting agent and do not manage the property, "
        "hold any monies on account, or have responsibility / liability for the landlord. Once the tenant is in "
        "occupation all communication is to be made directly between landlord and tenant, save for the approvals "
        "which this addendum requires to be requested through Botany Properties.")
    a.clause(
        "Botany have used their best endeavours to ascertain the DEWA premise number but will not be held liable "
        "for any inaccuracies.")
    a.clause(
        "The landlord understands that a copy of their title deed and ID documents will be provided to the tenant "
        "to enable the tenant to complete the EJARI registration.")
    a.clause(
        "The property will be handed over with all keys and access cards to the tenant upon realisation of the "
        "first rental payment and security deposit to the landlord, and tenancy start date.")

    # signature block
    line = "_" * 44
    sig = Table([
        [Paragraph("Broker signature &amp; date", SIG), Paragraph("Sales Manager signature &amp; date", SIG)],
        [Paragraph(line, SIG), Paragraph(line, SIG)],
        ["", ""],
        [Paragraph("Tenant 1 signature &amp; date", SIG), Paragraph("Landlord 1 signature &amp; date", SIG)],
        [Paragraph(line, SIG), Paragraph(line, SIG)],
    ], colWidths=[220, 220], rowHeights=[14, 22, 28, 14, 22])
    sig.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    a.story.append(KeepTogether([
        Spacer(1, 10),
        Paragraph("I confirm that I agree to and accept all the additional conditions above.", NOTE),
        Spacer(1, 26),
        sig,
    ]))
    return a.story


def render_addendum(out_path, header_png):
    W, H = A4

    def on_page(canvas, doc):
        # header image placed exactly where the original template had it
        canvas.drawImage(str(header_png), 43.9, H - 86.3, width=454.7, height=41.3, mask="auto")
        canvas.setFont("Montserrat-Regular", 7)
        canvas.setFillGray(0.45)
        canvas.drawRightString(W - 44, 30, f"Additional conditions - page {doc.page}")

    frame = Frame(52, 60, W - 104, H - 60 - 120, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(str(out_path), pagesize=A4, title="Tenancy contract - additional conditions",
                          author="Botany Properties")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(build_story(DEAL))


def main(src, dst):
    register_fonts()
    src_doc = pymupdf.open(src)
    header_png = HERE / "header.png"
    # render the header ("additional conditions" wordmark) straight from the
    # original page so its transparency / anti-aliasing is preserved
    page = src_doc[3]
    rect = page.get_image_rects(page.get_images()[0][0])[0]
    page.get_pixmap(clip=rect, dpi=400).save(str(header_png))

    addendum_pdf = HERE / "addendum_only.pdf"
    render_addendum(addendum_pdf, header_png)

    out = pymupdf.open()
    out.insert_pdf(src_doc, from_page=0, to_page=2)          # Ejari contract pages 1-3
    out.insert_pdf(pymupdf.open(str(addendum_pdf)))          # new addendum pages
    out.insert_pdf(src_doc, from_page=len(src_doc) - 1)      # Botany back cover
    out.save(dst, garbage=3, deflate=True)
    print(f"wrote {dst}: {len(out)} pages ({len(pymupdf.open(str(addendum_pdf)))} addendum pages)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
