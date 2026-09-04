"""Rebuild the "additional conditions" addendum pages of the Botany tenancy contract.

Usage: python3 build_addendum.py <original_contract.pdf> <output_contract.pdf>

Pages 1-3 (Ejari unified contract) and the final Botany cover page are kept
verbatim from the original; the addendum pages in between are regenerated as a
blank template (deal-specific amounts, dates and names are fill-in lines).
"""
import sys
from pathlib import Path

import pymupdf
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

HERE = Path(__file__).parent
FONTS = HERE / "fonts"

# ------------------------------------------------------------ template knobs
OPTIONS = {
    "occupant_lines": 3,      # blank lines for permitted occupants
    "payment_lines": 4,       # blank cheque / payment lines
    "minor_maintenance_cap": "AED 1,000",   # standard Botany threshold
    "bounce_penalty": "AED 1,000",          # fixed by instruction
}

# fill-in blanks
AMT = "AED&nbsp;__________________"
DATE = "_____&nbsp;/&nbsp;_____&nbsp;/&nbsp;__________"
NUM = "________"
LINE = "______________________________________"


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
                      spaceBefore=10, spaceAfter=6, leftIndent=8)
SIG = ParagraphStyle("sig", fontName="Montserrat-Regular", fontSize=8, leading=11)
FILL = ParagraphStyle("fill", fontName="Montserrat-Regular", fontSize=8.5, leading=16)


def b(s):
    return f"<b>{s}</b>"


class Addendum:
    def __init__(self):
        self.story = []
        self.n = 0
        self._pending_heading = None

    def heading(self, text):
        # glued to the following clause so a heading never ends a page alone
        self._pending_heading = Paragraph(text, HEAD)

    def clause(self, text, subs=None, note=None, keep=True):
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
        # long clauses are allowed to split across pages; the first two
        # flowables (heading + lead-in) always stay together
        self.story.append(KeepTogether(block) if keep else KeepTogether(block[:2]))
        if not keep:
            self.story.extend(block[2:])
        return self.n


def deal_block():
    """Fill-in header identifying the contract this addendum belongs to."""
    rows = [
        [Paragraph("Property (unit / building / community):", FILL), Paragraph(LINE + "________", FILL)],
        [Paragraph("Landlord name:", FILL), Paragraph(LINE + "________", FILL)],
        [Paragraph("Tenant name(s):", FILL), Paragraph(LINE + "________", FILL)],
        [Paragraph("Tenancy period:", FILL),
         Paragraph(f"from&nbsp;{DATE}&nbsp;&nbsp;to&nbsp;{DATE}", FILL)],
        [Paragraph("Annual rent / security deposit:", FILL),
         Paragraph(f"{AMT}&nbsp;&nbsp;/&nbsp;&nbsp;{AMT}", FILL)],
    ]
    t = Table(rows, colWidths=[205, 285])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return [Paragraph("This addendum forms an integral part of the tenancy contract described below.", NOTE),
            t, Spacer(1, 6)]


def build_story(o):
    a = Addendum()
    a.story += deal_block()
    cap = b(o["minor_maintenance_cap"])
    pen = b(o["bounce_penalty"])

    # ------------------------------------------------------------- deposit
    a.heading("Deposit")
    dep = a.clause(
        f"The tenant shall pay a security deposit of {b(AMT)} to the landlord, or to Botany Properties on the "
        "landlord's behalf, on signing this contract. "
        "The deposit is refundable to the tenant on vacating, subject to:",
        subs=["the premises being returned in a satisfactory condition, allowing for reasonable wear and tear, "
              "and in the repainted and deep-cleaned condition required by this addendum",
              "all keys, remotes and access cards being returned to the landlord",
              "the tenant providing final, settled bills and clearance certificates for DEWA, chiller / "
              "district cooling and any other service provider",
              "all rent, penalties, community fines and other sums due under this contract having been paid."])
    a.clause(
        "The landlord may deduct from the security deposit only the following: (a) the cost of repairing loss "
        "or damage to the property, furniture, fixtures or appliances beyond reasonable wear and tear; (b) the "
        "cost of repainting and deep cleaning where the tenant has not carried these out; (c) unpaid utility, "
        "chiller or service-provider bills; (d) unpaid rent, penalties, legal costs or community fines due under "
        "this contract; and (e) the cost of replacing lost keys, remotes and access cards. The landlord shall "
        "provide the tenant with an itemised statement of any deduction.")
    a.clause(
        "The landlord shall refund the security deposit, less any permitted deductions, within 30 (thirty) days "
        "of the tenant handing back possession and providing the documents listed in clause "
        f"{dep}. The deposit shall not be treated as rent and may not be used by the tenant to offset the "
        "last rent payment.")
    broker = a.clause(
        f"Upon signing this lease, the tenant shall pay Botany Properties a non-refundable broker fee of "
        f"{b(AMT)} inclusive of VAT.")
    a.clause(
        "Should the tenant decide to terminate the tenancy contract prior to the contract start date, the "
        "security deposit and broker fee will be forfeited, and any rental cheques provided will be returned "
        "to the tenant.")
    a.clause(
        "Should the landlord decide to terminate the tenancy contract prior to the contract start date, the "
        "landlord will return the security deposit and all rental cheques to the tenant and will refund the "
        f"tenant the total sum of the broker fee referred to in clause {broker}.")

    # ---------------------------------------------------- use and occupancy
    a.heading("Use of premises &amp; occupancy")
    a.clause(
        "The tenant may use the premises only as a private residence (residential purposes only) and must not "
        "use the premises for any illegal, commercial or immoral purpose, or in any way that causes nuisance "
        "to neighbours or the building.")
    a.clause(
        "The tenant shall not sub-let, assign, share or part with possession of the premises or any part of "
        "them, whether for payment or not, and shall not offer the premises for short-term or holiday letting "
        "(including through Airbnb, Booking.com or any similar platform), without the prior written approval "
        "of the landlord. Any breach entitles the landlord to terminate the tenancy in accordance with the law "
        "and to retain the security deposit in addition to any other remedy.")
    occ = [f"Name:&nbsp;{LINE}&nbsp;&nbsp;&nbsp;ID / passport no.:&nbsp;{LINE[:26]}"
           for _ in range(o["occupant_lines"])]
    a.clause(
        "Only the individual(s) named below (the \"permitted occupants\") are permitted to reside in the "
        "premises for the tenancy period:",
        subs=occ,
        note="Any other person who intends to stay in the premises for longer than 7 (seven) consecutive days "
             "must be notified to Botany Properties in writing, together with a copy of that person's "
             "identification, before the stay begins. Such a stay is permitted only upon the written approval "
             "of the landlord, which may be granted or refused at the landlord's discretion. Any unapproved "
             "occupancy shall be treated as a breach of this contract, and the tenant remains fully liable for "
             "the conduct of, and any damage caused by, all occupants and visitors.")
    a.clause(
        "Where more than one person is named as tenant or permitted occupant, each of them is jointly and "
        "severally liable for all obligations of the tenant under the tenancy contract and this addendum, "
        "and a notice given to any one of them is deemed given to all.")
    a.clause(
        "The tenant will abide by all rules and regulations issued by the developer, the owners' association, "
        "the facility management company and building security, including rules on parking, balconies, "
        "common areas, waste disposal, deliveries, contractors and noise. The tenant shall not store items on "
        "balconies or in common areas, shall not hang laundry or place satellite dishes or signage on the "
        "exterior of the building, and shall not cause noise or disturbance to neighbours, in particular "
        "between 10:00 pm and 8:00 am.")
    a.clause(
        "Any fine, charge or penalty imposed by the developer, owners' association, facility management "
        "company, municipality or any authority as a result of the conduct of the tenant, the permitted "
        "occupants or their visitors shall be paid by the tenant within 7 (seven) days of demand, and may "
        "otherwise be deducted from the security deposit.")
    a.clause(
        "No pets or animals of any kind may be kept in the premises without the prior written approval of the "
        "landlord and, where required, of the developer or owners' association. Smoking (including shisha and "
        "electronic cigarettes) is not permitted inside the premises. Any damage, odour or staining caused by "
        "pets or smoking shall be remedied at the tenant's cost.")

    # -------------------------------------------------------- maintenance
    a.heading("Maintenance")
    a.clause(
        "The tenant agrees to keep the property, including but not limited to all fixtures, fittings, "
        "furniture, appliances and electrical goods, in good and clean condition throughout the term of the "
        "tenancy contract and to report any defect or damage to Botany Properties promptly in writing.")
    a.clause(
        "All maintenance and repair work in the property resulting from misuse, neglect or negligence by the "
        "tenant, the permitted occupants or their visitors is the responsibility of the tenant, irrespective "
        "of the cost.")
    a.clause(
        f"All minor maintenance is the responsibility of the tenant. Maintenance repair works amounting to "
        f"{cap} or below (per incident) are the tenant's responsibility.")
    ac = a.clause(
        f"{b('Air-conditioning / chiller and plumbing:')} the maintenance, servicing and repair of the "
        "air-conditioning and chiller system (including fan-coil units, compressors, thermostats, filters, "
        "ducting and condensate drainage) and of all plumbing (including pipes, taps, mixers, water heaters, "
        "drains, toilets, water pumps and leaks) is the sole responsibility of the tenant for the full duration "
        "of the tenancy, regardless of the cost of the works. The landlord shall not bear or reimburse any "
        "repair, servicing or replacement cost relating to these systems. The tenant shall use licensed "
        "contractors and shall have the air-conditioning system serviced at least twice a year. The parties "
        "agree that this clause is the written agreement referred to in article 8 of the tenancy contract as "
        "regards the AC / chiller and plumbing.")
    a.clause(
        f"Save for the AC / chiller and plumbing set out in clause {ac}, and save for damage caused by the "
        "tenant, major maintenance of the electrical, mechanical and structural elements of the property is "
        f"the responsibility of the landlord. Maintenance repair works amounting to more than {cap} (per "
        "incident) for those elements are the landlord's responsibility.")
    a.clause(
        "The tenant agrees not to make any structural, mechanical, electrical or decorative alterations, and "
        "not to change locks or install additional locks or fixtures, without the prior written permission "
        "of the landlord. No carpets shall be glued to the tiles, nor shall holes be drilled into tiles.")

    # ------------------------------------------- furniture and fixtures
    a.heading("Furniture, fixtures &amp; appliances")
    inv = a.clause(
        "A handover inspection report, with photographs and an inventory of all furniture, fixtures, fittings, "
        "appliances, keys and access cards, shall be prepared and signed by both parties (or their "
        "representatives) at move-in. The same report shall be used for the move-out inspection, and the "
        "difference between the two, beyond reasonable wear and tear, shall determine any deduction from the "
        "security deposit. Failure by the tenant to attend or sign the move-out inspection shall be deemed "
        "acceptance of the landlord's report.")
    a.clause(
        "The tenant shall not remove, replace, dispose of or alter any item of furniture, fixture, fitting or "
        "appliance belonging to the landlord without first submitting a written request to Botany Properties. "
        "Any replacement or change may only be carried out after the landlord's written approval has been "
        "obtained through Botany Properties.")
    a.clause(
        "Any item replaced by the tenant, with approval, must be of equal or higher value, quality and "
        "specification than the existing item of furniture, fixture, fitting or appliance. The replacement "
        "item shall become the property of the landlord and shall remain in the premises on vacating, unless "
        "the landlord agrees otherwise in writing. The original item shall not be disposed of without the "
        "landlord's written approval and, where the landlord so requests, shall be stored safely and returned "
        "on vacating. Any unauthorised replacement, or any replacement of lesser value, entitles the landlord "
        "to recover the full replacement cost from the tenant and/or the security deposit.")
    a.clause(
        "All keys, remotes and access cards listed in the handover report shall be returned on vacating. The "
        "cost of replacing any lost or unreturned key, remote or access card, together with any developer or "
        "facility-management charge for re-issuing it and, where a key is lost, the cost of changing the "
        "relevant lock, shall be paid by the tenant or deducted from the security deposit.")

    # -------------------------------------------------------- vacating
    a.heading("Vacating condition")
    a.clause(
        "Upon vacating the property, the tenant will be responsible for filling any holes in the walls and "
        "restoring any other modification to the surfaces to their original condition. The tenant shall, at "
        "the tenant's own cost and before handing back the keys, (a) repaint all the internal walls and "
        "ceilings of the apartment in the original colour and finish, and (b) professionally deep clean the "
        "whole apartment, especially the bathrooms and kitchen, and return the property in a clean condition, "
        "free of the tenant's belongings and rubbish. Should the tenant fail to do so, the landlord may have "
        "the painting and cleaning carried out and deduct the cost from the security deposit, with any "
        "shortfall payable by the tenant within 7 (seven) days of demand.")

    # ------------------------------------------- fees and rent payments
    a.heading("Additional Fees | Rental Payments / Non-payments")
    a.clause(
        "The landlord is responsible for paying the developer's or owners' association service charges and "
        "major maintenance (sinking fund) fees for the duration of the ownership of the property.")
    a.clause(
        "Water, electricity and sewerage consumption (DEWA or any other service provider), chiller / district "
        "cooling consumption and capacity charges, gas, internet and municipality housing fees are the "
        "responsibility of the tenant. The tenant shall register the DEWA and chiller / district cooling "
        "accounts in the tenant's own name within 7 (seven) days of the start date, shall keep them in the "
        "tenant's name for the whole tenancy, and shall close all accounts and obtain clearance certificates "
        "when the tenancy ends and the tenant vacates the property.")
    a.clause(
        "The tenant shall be responsible for arranging insurance for their personal belongings and will not "
        "have the right to claim from the landlord for compensation for any losses or damages to those "
        "belongings during the tenancy contract.")
    pay_lines = [f"Payment {i}&nbsp;&ndash;&nbsp;on or before&nbsp;{DATE}&nbsp;&nbsp;for the amount of&nbsp;{AMT}"
                 for i in range(1, o["payment_lines"] + 1)]
    a.clause(
        f"The tenant agrees to pay the annual rent of {b(AMT)} by {b(NUM)} post-dated cheque(s) made "
        "payable to the landlord and delivered to Botany Properties, on the following dates (unused lines to "
        "be struck through):",
        subs=pay_lines)
    a.clause(
        "In the event of a rent cheque not being honoured or bouncing, or a rent payment / wire transfer not "
        "being received on or before the date agreed above, the tenant agrees:",
        subs=[
            f"to pay the landlord a penalty of {pen} per bounced cheque or delayed payment, as administration "
            "charges. The penalty must be paid within 24 (twenty-four) hours of the cheque bouncing or the "
            "payment falling due. In addition, the outstanding rent must be cleared in full, by cash or bank "
            "transfer, within 72 (seventy-two) hours of the due date.",
            f"that in addition to the penalty above, a late-payment charge of {b(AMT)} per day shall apply "
            "for each day the rent remains unpaid after the 72-hour period, until the rent is received in "
            "full.",
            "that if the penalty is not paid within the 24-hour period, the landlord holds all rights to open "
            "a case against the tenant before the Rental Dispute Centre and/or any competent court for the "
            "penalty amount, and all legal charges, court fees, lawyer's fees and related expenses incurred by "
            "the landlord in doing so shall be borne and paid by the tenant.",
            "that failure to settle the outstanding rent and the associated penalty within the specified "
            "timeframe will result in a legal 30-day notice being issued to the tenant, as per Article 25 of "
            "Law No. (33) of 2008 under the Dubai Real Estate Legislation.",
            "that if the tenant does not settle the outstanding payment within the 30-day notice period, the "
            "landlord reserves the right to initiate an eviction case before the Rental Dispute Centre against "
            "the tenant, to claim all rent, penalties, charges and legal costs due, and to apply the security "
            "deposit towards those sums in accordance with this addendum.",
            "that a bounced cheque is an offence under UAE law, and the landlord's rights under this clause "
            "are without prejudice to any other rights or remedies available to the landlord.",
        ], keep=False)
    a.clause(
        f"Should Botany Properties renew this tenancy agreement, the tenant agrees to pay Botany Properties a "
        f"renewal fee of {b(AMT)} inclusive of VAT in respect of drafting the renewal agreement, arranging "
        "the signing of the contracts for both parties and the collection and delivery of rental cheques.")
    ej = a.n + 1
    a.clause(
        "It is common practice that the tenant is responsible to register the contract with EJARI. By signing "
        f"this addendum, both the tenant and landlord confirm that this clause {ej} supersedes article 14 of "
        "the tenancy contract and that it is the tenant's responsibility, at the tenant's cost, to register "
        "the contract with EJARI within 14 (fourteen) days of the start date and to cancel the EJARI "
        "registration on termination. The landlord shall provide a copy of the title deed and ID documents "
        "to enable the tenant to do so.")

    # ---------------------------------------------- renewal and increase
    a.heading("Renewal &amp; rent increase")
    a.clause(
        f"On each renewal of this tenancy the annual rent shall increase by a minimum of {b('5% (five percent)')} "
        "over the rent of the expiring year, or by the highest increase permitted under the RERA Rental Index "
        "Calculator of the Dubai Land Department at the time of renewal, whichever is higher. The tenant "
        "acknowledges and agrees that this clause constitutes prior written notice of the rent increase for "
        "every renewal, that no separate notice of increase is required to be served before renewal, and that "
        "the increase shall be deemed accepted by the tenant on renewal. The only exception is where the RERA "
        "Rental Index Calculator / Dubai Land Department does not permit any increase for the property at the "
        "time of renewal, in which case the increase shall be limited to the maximum permitted (if any).")
    a.clause(
        "Renewal of the tenancy is subject to the tenant having paid all rent on time, having no bounced "
        "cheques, and having no outstanding penalties, community fines, utility bills or other sums due under "
        "this contract. Any such sums must be settled before the renewal contract is issued.")

    # ------------------------------------------------------ notices
    a.heading("Vacating / Notices")
    a.clause(
        "The landlord will give the tenant not less than 48 hours' notice (except in the case of an emergency) "
        "to enter the property to inspect, maintain, repair, alter, improve or rebuild.")
    a.clause(
        "In the event that the tenant wishes to vacate or renew the lease at the end of the tenancy, they "
        "should notify Botany Properties in writing 60 (sixty) days prior to the expiry date of the rental "
        "contract.")
    a.clause(
        "The parties agree that there may be instances where the tenant shall need to terminate the lease "
        "early. In this event the tenant will give 3 (three) months' notice in writing through Botany Properties "
        "and will pay an early-termination penalty equal to 2 (two) months' rent; the landlord agrees to "
        "refund any rent paid for the period after the termination date, less that penalty and any other "
        "sums due. The broker fee is not refundable on early termination.")
    a.clause(
        "In the event that the landlord wishes to sell the property, the tenant agrees to allow access to the "
        "property for viewings, if reasonable notice (48 hours) is given. If the property is sold during the "
        "term of the contract, the tenant has the right to remain in the property for the duration of this "
        "contract at the same rental rate, and the new owner takes over the landlord's rights and obligations "
        "under this contract. The rights of the tenant in the event of a sale shall be governed by RERA, "
        "unless otherwise agreed between the tenant and the landlord.")
    a.clause(
        "If the landlord wishes to evict the tenant on expiry of the tenancy for a reason permitted by law, "
        "the landlord will give the tenant 12 (twelve) months' written notice. The parties agree that such "
        "notice may be given by email sent by Botany Properties, on behalf of the landlord, to the tenant's "
        "email address stated in the tenancy contract, and that the tenant accepts such email as formal and "
        "legal notice of eviction, without any requirement for notary public attestation, registered mail or "
        "any other form of service. The notice is deemed received on the date the email is sent. This is in "
        "line with article 7 of the tenancy contract, under which the parties have confirmed their email "
        "addresses as the addresses for all formal and legal notifications. This is without prejudice to the "
        "landlord's right to terminate the tenancy during its term for non-payment or other breach in "
        "accordance with the law and this addendum.")

    # ------------------------------------------------------ other terms
    a.heading("Other Terms &amp; Conditions")
    a.clause(
        "The landlord confirms that the previous occupants have settled and closed all DEWA, chiller and other "
        "service provider accounts prior to the start date of the lease, and that the property is free of any "
        "outstanding utility or service-provider liability at handover.")
    a.clause(
        "This lease agreement shall be subject to the laws of Dubai and the United Arab Emirates, and any "
        "dispute shall be referred to the Rental Dispute Centre. This addendum is prepared in English only; "
        "if an Arabic translation of this addendum is produced, the English text of the addendum shall "
        "prevail as between the parties.")
    a.clause(
        "This property is let and managed by Botany Properties on behalf of the landlord. For the whole "
        "tenancy period, all communication, notices, requests, approvals, complaints and maintenance reports "
        "from the tenant shall be made only through Botany Properties, and not directly to the landlord. Any "
        "notice which this contract or the law requires the tenant to give to the landlord is validly given "
        "when delivered in writing (including by email) to Botany Properties, and any notice given by Botany "
        "Properties on behalf of the landlord is valid as if given by the landlord. Where required, and with "
        "the landlord's approval, Botany Properties may collect rent cheques, cash and any other sums due "
        "under this contract on behalf of the landlord and shall issue a receipt for each amount collected; "
        "payment to Botany Properties in this way discharges the tenant's obligation to the landlord for that "
        "amount. Botany Properties acts as the landlord's agent only and does not assume the landlord's "
        "obligations under this contract.")
    a.clause(
        "Botany Properties has used its best endeavours to ascertain the DEWA premises number and chiller "
        "account details but will not be held liable for any inaccuracies.")
    a.clause(
        "The property will be handed over with all keys and access cards to the tenant, and the handover "
        "inspection report in clause "
        f"{inv} signed, upon realisation of the first rental payment, the security deposit and the broker "
        "fee, and not before the tenancy start date.")
    a.clause(
        "This addendum forms an integral part of the tenancy contract. In case of any inconsistency between "
        "the printed terms of the unified tenancy contract and this addendum, this addendum shall prevail to "
        "the extent permitted by law. Each page of this addendum shall be initialled by the landlord and the "
        "tenant, and any amendment must be in writing and signed by both parties.")

    # ----------------------------------------------------- signature block
    line = "_" * 44
    sig = Table([
        [Paragraph("Broker signature &amp; date", SIG), Paragraph("Sales Manager signature &amp; date", SIG)],
        [Paragraph(line, SIG), Paragraph(line, SIG)],
        ["", ""],
        [Paragraph("Tenant 1 signature &amp; date", SIG), Paragraph("Landlord 1 signature &amp; date", SIG)],
        [Paragraph(line, SIG), Paragraph(line, SIG)],
        ["", ""],
        [Paragraph("Tenant 2 signature &amp; date (if any)", SIG),
         Paragraph("Landlord 2 signature &amp; date (if any)", SIG)],
        [Paragraph(line, SIG), Paragraph(line, SIG)],
    ], colWidths=[220, 220], rowHeights=[14, 22, 28, 14, 22, 28, 14, 22])
    sig.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    a.story.append(KeepTogether([
        Spacer(1, 10),
        Paragraph("I confirm that I have read, agree to and accept all the additional conditions above.", NOTE),
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
        canvas.drawString(52, 30, "Landlord initials: ____________        Tenant initials: ____________")

    frame = Frame(52, 60, W - 104, H - 60 - 120, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(str(out_path), pagesize=A4, title="Tenancy contract - additional conditions",
                          author="Botany Properties")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(build_story(OPTIONS))


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
