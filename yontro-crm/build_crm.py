import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.comments import Comment

OUT = "/home/user/aura-reset-center/yontro-crm/Yontro_CRM.xlsx"
N = 500  # working rows per tab
LAST = N + 1

INK, ORANGE, BONE, GREY = "0B0B0B", "FF5A1F", "F4F2EE", "4A4744"
F = "Arial"
hdr_font = Font(name=F, bold=True, color="FFFFFF", size=10)
hdr_fill = PatternFill("solid", fgColor=INK)
fhdr_fill = PatternFill("solid", fgColor=GREY)
calc_fill = PatternFill("solid", fgColor=BONE)
body = Font(name=F, size=10)
bold = Font(name=F, size=10, bold=True)
thin = Side(style="thin", color="D9D6D0")
box = Border(bottom=thin)

def fill(c):
    return PatternFill("solid", fgColor=c)

wb = Workbook()

# ---------------------------------------------------------------- Settings
st = wb.active
st.title = "Settings"
lists = {
    "A": ("Lead stages", ["New", "Contacted", "Replied", "Meeting booked", "Meeting held",
                          "Proposal sent", "Contract signed + paid", "Closed – No response", "Lost"]),
    "B": ("Inbound sources", ["Website form", "WhatsApp", "Instagram DM", "Referral", "Walk-in", "Phone call", "Other"]),
    "C": ("Outbound sources", ["Apollo", "LinkedIn", "Google Maps", "Instagram research", "Event / networking", "Other"]),
    "D": ("Industries", ["Hospitality / F&B", "Retail", "Real estate", "Entertainment", "Fitness / wellness",
                         "Beauty / salon", "Clinic / healthcare", "Education", "Automotive", "Other"]),
    "E": ("Team", ["Usama", "Lianna", "Azeem", "Owner"]),
    "I": ("Payment methods", ["Bank transfer", "Card", "Cheque", "Cash", "Payment link"]),
    "J": ("Client decision", ["Pending", "Approved", "Backed out"]),
    "K": ("Back-out reasons", ["Video style", "Price", "Timing", "Changed mind", "Business issue", "Other"]),
    "L": ("Refund status", ["Requested", "Approved", "Paid"]),
    "M": ("Shoot types", ["Free video", "Plan shoot", "Add-on", "Event coverage"]),
    "N": ("Shoot status", ["Scheduled", "Shot", "Editing", "Sent for approval", "Delivered", "Posted"]),
    "O": ("Lost / closed reasons", ["No response (4 follow-ups)", "Price", "Not ready", "Went with competitor",
                                   "In-house team", "Not a fit", "Other"]),
    "P": ("Wants more of", ["Walk-in customers", "Enquiries and bookings", "Online sales",
                            "Followers and reach", "A better-looking brand"]),
}
rng = {}
for col, (title, items) in lists.items():
    st[f"{col}1"] = title
    for i, v in enumerate(items, start=2):
        st[f"{col}{i}"] = v
    rng[title] = f"Settings!${col}$2:${col}${len(items)+1}"
# packages table
st["F1"], st["G1"], st["H1"] = "Package", "Monthly fee (AED, ex VAT)", "Videos / month"
for i, (p, fee, v) in enumerate([("Launch", 5000, 10), ("Growth", 7500, 15), ("Scale", 10000, 20)], start=2):
    st[f"F{i}"], st[f"G{i}"], st[f"H{i}"] = p, fee, v
    st[f"G{i}"].number_format = "#,##0"
    st[f"G{i}"].font = Font(name=F, size=10, color="0000FF")
    st[f"H{i}"].font = Font(name=F, size=10, color="0000FF")
st["F6"] = "Source: yontro.ae Packages section. Prices exclude 5% VAT."
rng["Packages"] = "Settings!$F$2:$F$4"
# rules
st["R1"], st["S1"] = "Rule", "Value"
rules = [
    ("Follow-up gap (days)", 3, "Your rule: follow up every 3 days after a lead goes quiet."),
    ("Max follow-ups before closing", 4, "Your rule: 4 follow-ups, each with new value, then stop outreach."),
    ("Decision window after free video (working days)", 3,
     "NOT DECIDED YET - placeholder of 3 working days. Change this one cell and every deadline updates."),
    ("Free video delivery promise (working days)", 5, "From the website: delivered within five working days."),
    ("Minimum term (months)", 3, "From the website: three-month minimum, then month to month."),
    ("Max revision rounds per video", 2, "From the website FAQ: two rounds of changes included."),
]
for i, (k, v, note) in enumerate(rules, start=2):
    st[f"R{i}"], st[f"S{i}"], st[f"T{i}"] = k, v, note
    st[f"S{i}"].font = Font(name=F, size=10, color="0000FF", bold=True)
st["S4"].fill = fill("FFFF00")
st["S4"].comment = Comment("Placeholder - the decision window has not been agreed yet.", "Yontro CRM")
GAP, MAXF, WIN, DELIV, TERM, REV = ("Settings!$S$2", "Settings!$S$3", "Settings!$S$4",
                                    "Settings!$S$5", "Settings!$S$6", "Settings!$S$7")
for c in st[1]:
    if c.value:
        c.font, c.fill = hdr_font, hdr_fill
for row in st.iter_rows(min_row=2):
    for c in row:
        if c.font == Font():
            c.font = body
        elif c.font.name != F:
            c.font = Font(name=F, size=10, bold=c.font.bold, color=c.font.color)
for col in "ABCDEFGHIJKLMNOP":
    st.column_dimensions[col].width = 22
st.column_dimensions["R"].width = 44
st.column_dimensions["S"].width = 8
st.column_dimensions["T"].width = 80
st.freeze_panes = "A2"

# ---------------------------------------------------------------- helpers
def build_table(ws, cols, widths=None):
    """cols: list of (header, kind, extra) kind in input|calc; returns {header: letter}"""
    L = {}
    for i, (h, kind, *_) in enumerate(cols, start=1):
        L[h] = get_column_letter(i)
        c = ws.cell(row=1, column=i, value=h)
        c.font = hdr_font
        c.fill = fhdr_fill if kind == "calc" else hdr_fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[L[h]].width = (widths or {}).get(h, 16)
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "E2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{LAST}"
    return L

def style_rows(ws, cols, L, fmts):
    for r in range(2, LAST + 1):
        for h, kind, *_ in cols:
            c = ws[f"{L[h]}{r}"]
            c.font = body
            c.border = box
            if kind == "calc":
                c.fill = calc_fill
            if h in fmts:
                c.number_format = fmts[h]

def dv(ws, col, source, prompt=None):
    v = DataValidation(type="list", formula1=source, allow_blank=True)
    v.error = "Pick a value from the list (edit lists on the Settings tab)."
    v.errorTitle = "Not on the list"
    ws.add_data_validation(v)
    v.add(f"{col}2:{col}{LAST}")

def int_dv(ws, col, lo, hi):
    v = DataValidation(type="whole", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True)
    v.error = f"Enter a whole number from {lo} to {hi}."
    ws.add_data_validation(v)
    v.add(f"{col}2:{col}{LAST}")

def cf(ws, ref, formula, color=None, font_color=None, bold_=False):
    ws.conditional_formatting.add(ref, FormulaRule(
        formula=[formula],
        fill=fill(color) if color else None,
        font=Font(name=F, color=font_color, bold=bold_) if (font_color or bold_) else None))

CLOSED = '"Contract signed + paid","Closed – No response","Lost"'

# ---------------------------------------------------------------- lead tabs
def lead_tab(name, inbound):
    ws = wb.create_sheet(name)
    cols = [("Lead ID", "input"),
            ("Date received" if inbound else "Date added", "input"),
            ("Source", "input"), ("Business name", "input"), ("Industry", "input"),
            ("Contact name", "input"), ("Role", "input"), ("Phone / WhatsApp", "input"),
            ("Email", "input"), ("Instagram", "input")]
    if not inbound:
        cols += [("LinkedIn", "input")]
    cols += [("Area", "input")]
    if inbound:
        cols += [("Wants more of", "input"), ("First response", "input"), ("Response time (hrs)", "calc")]
    else:
        cols += [("Apollo list / campaign", "input")]
    cols += [("Owner", "input"), ("Stage", "input"), ("Last contact date", "input"),
             ("Follow-ups sent (0-4)", "input"), ("Next follow-up due", "calc"),
             ("Meeting date", "input"), ("Package discussed", "input"),
             ("Lost / closed reason", "input"), ("Notes", "input"),
             ("Days open", "calc"), ("Action flag", "calc")]
    widths = {"Business name": 24, "Email": 24, "Notes": 34, "Action flag": 30, "Stage": 22,
              "Apollo list / campaign": 22, "Lost / closed reason": 22, "Wants more of": 20,
              "Lead ID": 10, "Industry": 18, "Source": 15}
    L = build_table(ws, cols, widths)
    d0 = "Date received" if inbound else "Date added"
    fmts = {d0: "dd-mmm-yy hh:mm" if inbound else "dd-mmm-yy", "Last contact date": "dd-mmm-yy",
            "Next follow-up due": "dd-mmm-yy", "Meeting date": "dd-mmm-yy hh:mm",
            "Days open": "0", "Phone / WhatsApp": "@"}
    if inbound:
        fmts["First response"] = "dd-mmm-yy hh:mm"
        fmts["Response time (hrs)"] = "0.0"
    style_rows(ws, cols, L, fmts)

    for r in range(2, LAST + 1):
        b, stg, last, fu = (f"{L['Business name']}{r}", f"{L['Stage']}{r}",
                            f"{L['Last contact date']}{r}", f"{L['Follow-ups sent (0-4)']}{r}")
        ph, d = f"{L['Phone / WhatsApp']}{r}", f"{L[d0]}{r}"
        closed = f"OR({stg}=\"Contract signed + paid\",{stg}=\"Closed – No response\",{stg}=\"Lost\")"
        ws[f"{L['Next follow-up due']}{r}"] = (
            f'=IF(OR({b}="",{last}="",{closed},N({fu})>={MAXF}),"",{last}+{GAP})')
        ws[f"{L['Days open']}{r}"] = f'=IF(OR({b}="",{d}=""),"",INT(TODAY()-{d}))'
        refunded = (f'OR(COUNTIFS(Clients!$C$2:$C${LAST},{b},Clients!$S$2:$S${LAST},"Paid")>0,'
                    f'AND({ph}<>"",COUNTIFS(Clients!$E$2:$E${LAST},{ph},Clients!$S$2:$S${LAST},"Paid")>0))')
        nxt = f"{L['Next follow-up due']}{r}"
        ws[f"{L['Action flag']}{r}"] = (
            f'=IF({b}="","",IF({refunded},"⚠ Refunded before – no free video",'
            f'IF({closed},"",IF({stg}="","Set a stage",'
            f'IF(N({fu})>={MAXF},"Close – 4 follow-ups sent",'
            f'IF({nxt}="",IF({last}="","Make first contact",""),'
            f'IF(TODAY()>{nxt},"OVERDUE follow-up",IF(TODAY()={nxt},"Follow up today","")))))))')
        if inbound:
            fr = f"{L['First response']}{r}"
            ws[f"{L['Response time (hrs)']}{r}"] = f'=IF(OR({d}="",{fr}=""),"",ROUND(({fr}-{d})*24,1))'

    dv(ws, L["Source"], rng["Inbound sources" if inbound else "Outbound sources"])
    dv(ws, L["Industry"], rng["Industries"])
    dv(ws, L["Owner"], rng["Team"])
    dv(ws, L["Stage"], rng["Lead stages"])
    dv(ws, L["Package discussed"], rng["Packages"])
    dv(ws, L["Lost / closed reason"], rng["Lost / closed reasons"])
    if inbound:
        dv(ws, L["Wants more of"], rng["Wants more of"])
    int_dv(ws, L["Follow-ups sent (0-4)"], 0, 4)

    # formatting rules
    s = L["Stage"]
    full = f"A2:{get_column_letter(len(cols))}{LAST}"
    cf(ws, full, f'${s}2="Contract signed + paid"', "DFF3E3")
    cf(ws, full, f'OR(${s}2="Closed – No response",${s}2="Lost")', None, "9A958E")
    fl = f"{L['Action flag']}2:{L['Action flag']}{LAST}"
    cf(ws, fl, f'LEFT({L["Action flag"]}2,1)="⚠"', "FAD4D4", "9B1C1C", True)
    cf(ws, fl, f'{L["Action flag"]}2="OVERDUE follow-up"', "FF5A1F", "FFFFFF", True)
    cf(ws, fl, f'{L["Action flag"]}2="Follow up today"', "FFE3B3", None, True)
    cf(ws, fl, f'{L["Action flag"]}2="Close – 4 follow-ups sent"', "E4DCF2", "4B2E83", True)
    cf(ws, fl, f'OR({L["Action flag"]}2="Make first contact",{L["Action flag"]}2="Set a stage")', "E6F0FA")

    # example row
    ex = dict(zip([c[0] for c in cols], [None] * len(cols)))
    if inbound:
        ex.update({"Lead ID": "IN-0001", d0: dt.datetime(2026, 10, 15, 10, 12), "Source": "Website form",
                   "Business name": "Pulse Fitness Club (EXAMPLE)", "Industry": "Fitness / wellness",
                   "Contact name": "Sara M.", "Role": "Owner", "Phone / WhatsApp": "+971 50 000 0000",
                   "Email": "sara@example.com", "Instagram": "@pulse.fitness.jlt", "Area": "JLT",
                   "Wants more of": "Enquiries and bookings", "First response": dt.datetime(2026, 10, 15, 10, 41),
                   "Owner": "Usama", "Stage": "Proposal sent", "Last contact date": dt.date(2026, 10, 17),
                   "Follow-ups sent (0-4)": 1, "Meeting date": dt.datetime(2026, 10, 16, 15, 0),
                   "Package discussed": "Growth", "Notes": "Example row – overwrite or delete."})
    else:
        ex.update({"Lead ID": "OUT-0001", d0: dt.date(2026, 10, 13), "Source": "Apollo",
                   "Business name": "Marina Bites Café (EXAMPLE)", "Industry": "Hospitality / F&B",
                   "Contact name": "Omar K.", "Role": "Marketing manager", "Phone / WhatsApp": "+971 55 000 0000",
                   "Email": "omar@example.com", "Instagram": "@marinabites", "LinkedIn": "linkedin.com/in/example",
                   "Area": "Dubai Marina", "Apollo list / campaign": "F&B – Marina – Oct 26", "Owner": "Usama",
                   "Stage": "Replied", "Last contact date": dt.date(2026, 10, 16), "Follow-ups sent (0-4)": 0,
                   "Package discussed": "Launch", "Notes": "Example row – overwrite or delete."})
    for h, v in ex.items():
        if v is not None and dict(cols)[h] == "input":
            ws[f"{L[h]}2"] = v
    for h, _ in cols:
        ws[f"{L[h]}2"].font = Font(name=F, size=10, italic=True, color="6B665F")
    return ws, L

inb, LI = lead_tab("Inbound", True)
outb, LO = lead_tab("Outbound", False)

# ---------------------------------------------------------------- Clients
cl = wb.create_sheet("Clients")
ccols = [("Client ID", "input"), ("Lead ID", "input"), ("Business name", "input"), ("Contact name", "input"),
         ("Phone / WhatsApp", "input"), ("Email", "input"), ("Instagram", "input"), ("Package", "input"),
         ("Monthly fee (AED)", "calc"), ("Contract signed date", "input"), ("Amount paid (AED)", "input"),
         ("Payment method", "input"), ("Free video shoot date", "input"), ("Free video delivered", "input"),
         ("Decision deadline", "calc"), ("Client decision", "input"), ("Status", "calc"),
         ("Back-out reason", "input"), ("Refund status", "input"), ("Refund amount (AED)", "input"),
         ("Refund date", "input"), ("Plan start date", "input"), ("Minimum term ends", "calc"),
         ("Account manager", "input"), ("Videographer", "input"), ("Notes", "input")]
LC = build_table(cl, ccols, {"Business name": 24, "Status": 34, "Notes": 34, "Email": 22, "Client ID": 10})
assert LC["Business name"] == "C" and LC["Phone / WhatsApp"] == "E" and LC["Refund status"] == "S"
style_rows(cl, ccols, LC, {"Monthly fee (AED)": "#,##0", "Amount paid (AED)": "#,##0",
                           "Refund amount (AED)": "#,##0", "Contract signed date": "dd-mmm-yy",
                           "Free video shoot date": "dd-mmm-yy", "Free video delivered": "dd-mmm-yy",
                           "Decision deadline": "dd-mmm-yy", "Refund date": "dd-mmm-yy",
                           "Plan start date": "dd-mmm-yy", "Minimum term ends": "dd-mmm-yy",
                           "Phone / WhatsApp": "@"})
for r in range(2, LAST + 1):
    g = lambda h: f"{LC[h]}{r}"
    cl[g("Monthly fee (AED)")] = (f'=IF({g("Package")}="","",IFERROR(INDEX(Settings!$G$2:$G$4,'
                                  f'MATCH({g("Package")},Settings!$F$2:$F$4,0)),""))')
    cl[g("Decision deadline")] = f'=IF({g("Free video delivered")}="","",WORKDAY({g("Free video delivered")},{WIN}))'
    dl = g("Decision deadline")
    cl[g("Status")] = (
        f'=IF({g("Business name")}="","",'
        f'IF({g("Client decision")}="Backed out",IF({g("Refund status")}="Paid","Refunded – closed",'
        f'IF({g("Back-out reason")}="","Refund – log reason first","Refund in progress")),'
        f'IF({g("Amount paid (AED)")}="","Awaiting payment",'
        f'IF({g("Free video delivered")}="",IF({g("Free video shoot date")}="","Schedule free video",'
        f'"Free video in production"),'
        f'IF({g("Client decision")}="Approved","Active",'
        f'IF(TODAY()>{dl},"Active – plan went ahead",'
        f'"Decision pending – "&NETWORKDAYS(TODAY(),{dl})&" working day(s) left"))))))')
    cl[g("Minimum term ends")] = f'=IF({g("Plan start date")}="","",EDATE({g("Plan start date")},{TERM}))'
dv(cl, LC["Package"], rng["Packages"])
dv(cl, LC["Payment method"], rng["Payment methods"])
dv(cl, LC["Client decision"], rng["Client decision"])
dv(cl, LC["Back-out reason"], rng["Back-out reasons"])
dv(cl, LC["Refund status"], rng["Refund status"])
dv(cl, LC["Account manager"], rng["Team"])
dv(cl, LC["Videographer"], rng["Team"])
S_ = LC["Status"]
sref = f"{S_}2:{S_}{LAST}"
cf(cl, sref, f'LEFT({S_}2,6)="Active"', "DFF3E3", "1E6B3A", True)
cf(cl, sref, f'LEFT({S_}2,8)="Decision"', "FFE3B3", None, True)
cf(cl, sref, f'LEFT({S_}2,6)="Refund"', "FAD4D4", "9B1C1C", True)
cf(cl, sref, f'{S_}2="Awaiting payment"', "FF5A1F", "FFFFFF", True)
ex = {"Client ID": "CL-0001", "Lead ID": "IN-0001", "Business name": "Example Salon (EXAMPLE)",
      "Contact name": "Layla K.", "Phone / WhatsApp": "+971 52 000 0000", "Email": "layla@example.com",
      "Instagram": "@examplesalon", "Package": "Growth", "Contract signed date": dt.date(2026, 10, 12),
      "Amount paid (AED)": 7875, "Payment method": "Bank transfer", "Free video shoot date": dt.date(2026, 10, 14),
      "Free video delivered": dt.date(2026, 10, 19), "Client decision": "Pending",
      "Account manager": "Lianna", "Videographer": "Azeem",
      "Notes": "Example row – overwrite or delete. Paid = AED 7,500 + 5% VAT."}
for h, v in ex.items():
    cl[f"{LC[h]}2"] = v
for h, _ in ccols:
    cl[f"{LC[h]}2"].font = Font(name=F, size=10, italic=True, color="6B665F")

# ---------------------------------------------------------------- Shoots
sh = wb.create_sheet("Shoots")
scols = [("Shoot ID", "input"), ("Client ID", "input"), ("Business name", "calc"), ("Shoot type", "input"),
         ("Shoot date", "input"), ("Time", "input"), ("Location", "input"), ("Videographer", "input"),
         ("Status", "input"), ("Delivered date", "input"), ("Revision rounds used", "input"),
         ("Video link", "input"), ("Notes", "input"), ("Flag", "calc")]
LS = build_table(sh, scols, {"Business name": 24, "Location": 22, "Video link": 26, "Notes": 30, "Flag": 30})
sh.freeze_panes = "D2"
style_rows(sh, scols, LS, {"Shoot date": "dd-mmm-yy", "Delivered date": "dd-mmm-yy", "Time": "hh:mm"})
for r in range(2, LAST + 1):
    g = lambda h: f"{LS[h]}{r}"
    sh[g("Business name")] = (f'=IF({g("Client ID")}="","",IFERROR(INDEX(Clients!$C$2:$C${LAST},'
                              f'MATCH({g("Client ID")},Clients!$A$2:$A${LAST},0)),"Client ID not found"))')
    sh[g("Flag")] = (
        f'=IF({g("Shoot ID")}="","",IF(N({g("Revision rounds used")})>{REV},"Over revision limit",'
        f'IF(AND({g("Shoot type")}="Free video",{g("Delivered date")}="",{g("Shoot date")}<>"",'
        f'TODAY()>WORKDAY({g("Shoot date")},{DELIV})),"LATE – free video promised in 5 working days",'
        f'IF(AND({g("Shoot date")}<>"",{g("Shoot date")}=TODAY()),"Shooting today",""))))')
dv(sh, LS["Shoot type"], rng["Shoot types"])
dv(sh, LS["Videographer"], rng["Team"])
dv(sh, LS["Status"], rng["Shoot status"])
int_dv(sh, LS["Revision rounds used"], 0, 9)
fl = f"{LS['Flag']}2:{LS['Flag']}{LAST}"
cf(sh, fl, f'LEFT({LS["Flag"]}2,4)="LATE"', "FF5A1F", "FFFFFF", True)
cf(sh, fl, f'{LS["Flag"]}2="Over revision limit"', "FAD4D4", "9B1C1C", True)
cf(sh, fl, f'{LS["Flag"]}2="Shooting today"', "FFE3B3", None, True)
ex = {"Shoot ID": "SH-0001", "Client ID": "CL-0001", "Shoot type": "Free video", "Shoot date": dt.date(2026, 10, 14),
      "Time": dt.time(10, 0), "Location": "Client salon, Jumeirah", "Videographer": "Azeem", "Status": "Delivered",
      "Delivered date": dt.date(2026, 10, 19), "Revision rounds used": 1, "Notes": "Example row – overwrite or delete."}
for h, v in ex.items():
    sh[f"{LS[h]}2"] = v
for h, _ in scols:
    sh[f"{LS[h]}2"].font = Font(name=F, size=10, italic=True, color="6B665F")

# ---------------------------------------------------------------- Dashboard
db = wb.create_sheet("Dashboard", 0)
db.sheet_view.showGridLines = False
db.column_dimensions["A"].width = 3
db.column_dimensions["B"].width = 40
for c in "CDE":
    db.column_dimensions[c].width = 16
db.column_dimensions["F"].width = 4
db.column_dimensions["G"].width = 30
for c in "HIJ":
    db.column_dimensions[c].width = 14
db["B1"] = "YONTRO · CRM DASHBOARD"
db["B1"].font = Font(name=F, size=18, bold=True, color=INK)
db["B2"] = "Updates automatically from the Inbound, Outbound, Clients and Shoots tabs. Nothing to type here."
db["B2"].font = Font(name=F, size=10, italic=True, color="6B665F")
db["B3"], db["C3"] = "Today", "=TODAY()"
db["B4"], db["C4"] = "Week starts (Monday)", "=C3-WEEKDAY(C3,2)+1"
db["B5"], db["C5"] = "Month starts", "=DATE(YEAR(C3),MONTH(C3),1)"
for r in (3, 4, 5):
    db[f"B{r}"].font = body
    db[f"C{r}"].font = bold
    db[f"C{r}"].number_format = "dd-mmm-yy"

IB, OB = f"Inbound!$B$2:$B${LAST}", f"Outbound!$B$2:$B${LAST}"
IS, OS = f"Inbound!${LI['Stage']}$2:${LI['Stage']}${LAST}", f"Outbound!${LO['Stage']}$2:${LO['Stage']}${LAST}"
IF_, OF_ = (f"Inbound!${LI['Action flag']}$2:${LI['Action flag']}${LAST}",
            f"Outbound!${LO['Action flag']}$2:${LO['Action flag']}${LAST}")
IM, OM = (f"Inbound!${LI['Meeting date']}$2:${LI['Meeting date']}${LAST}",
          f"Outbound!${LO['Meeting date']}$2:${LO['Meeting date']}${LAST}")
IO, OO = f"Inbound!${LI['Owner']}$2:${LI['Owner']}${LAST}", f"Outbound!${LO['Owner']}$2:${LO['Owner']}${LAST}"
ISrc, OSrc = f"Inbound!${LI['Source']}$2:${LI['Source']}${LAST}", f"Outbound!${LO['Source']}$2:${LO['Source']}${LAST}"
INm, ONm = (f"Inbound!${LI['Business name']}$2:${LI['Business name']}${LAST}",
            f"Outbound!${LO['Business name']}$2:${LO['Business name']}${LAST}")
CS = f"Clients!${LC['Status']}$2:${LC['Status']}${LAST}"
CD = f"Clients!${LC['Client decision']}$2:${LC['Client decision']}${LAST}"
CJ = f"Clients!${LC['Contract signed date']}$2:${LC['Contract signed date']}${LAST}"
CK = f"Clients!${LC['Amount paid (AED)']}$2:${LC['Amount paid (AED)']}${LAST}"
CI = f"Clients!${LC['Monthly fee (AED)']}$2:${LC['Monthly fee (AED)']}${LAST}"
CRs, CRa, CRd = (f"Clients!${LC['Refund status']}$2:${LC['Refund status']}${LAST}",
                 f"Clients!${LC['Refund amount (AED)']}$2:${LC['Refund amount (AED)']}${LAST}",
                 f"Clients!${LC['Refund date']}$2:${LC['Refund date']}${LAST}")
CN = f"Clients!${LC['Free video delivered']}$2:${LC['Free video delivered']}${LAST}"
RT = f"Inbound!${LI['Response time (hrs)']}$2:${LI['Response time (hrs)']}${LAST}"

def section(row, title, col="B", span=4):
    c = db[f"{col}{row}"]
    c.value = title
    c.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    start = ord(col) - 64
    for i in range(start, start + span):
        db.cell(row=row, column=i).fill = fill(INK)

def kpi(row, label, formula, fmt="0", col="B", vcol="C", note=None):
    db[f"{col}{row}"] = label
    db[f"{col}{row}"].font = body
    db[f"{vcol}{row}"] = formula
    db[f"{vcol}{row}"].font = Font(name=F, size=12, bold=True, color=INK)
    db[f"{vcol}{row}"].number_format = fmt
    db[f"{vcol}{row}"].alignment = Alignment(horizontal="right")
    for c in (f"{col}{row}", f"{vcol}{row}"):
        db[c].border = box
    if note:
        db[f"{vcol}{row}"].comment = Comment(note, "Yontro CRM")

# This week
section(7, "THIS WEEK")
db["C8"], db["D8"], db["E8"] = "Inbound", "Outbound", "Total"
for c in ("C8", "D8", "E8"):
    db[c].font = Font(name=F, size=9, bold=True, color="6B665F")
    db[c].alignment = Alignment(horizontal="right")
rows = [("Leads added", f'=COUNTIFS({IB},">="&$C$4,{INm},"<>")', f'=COUNTIFS({OB},">="&$C$4,{ONm},"<>")'),
        ("Meetings on the calendar this week",
         f'=COUNTIFS({IM},">="&$C$4,{IM},"<"&$C$4+7)', f'=COUNTIFS({OM},">="&$C$4,{OM},"<"&$C$4+7)'),
        ("Follow-ups due today or overdue",
         f'=COUNTIF({IF_},"Follow up today")+COUNTIF({IF_},"OVERDUE follow-up")',
         f'=COUNTIF({OF_},"Follow up today")+COUNTIF({OF_},"OVERDUE follow-up")'),
        ("Leads to close (4 follow-ups sent)",
         f'=COUNTIF({IF_},"Close – 4 follow-ups sent")', f'=COUNTIF({OF_},"Close – 4 follow-ups sent")')]
for i, (lab, fi, fo) in enumerate(rows, start=9):
    kpi(i, lab, fi)
    db[f"D{i}"], db[f"E{i}"] = fo, f"=C{i}+D{i}"
    for c in (f"D{i}", f"E{i}"):
        db[c].font = Font(name=F, size=12, bold=True, color=INK)
        db[c].border = box
db["E11"].font = Font(name=F, size=12, bold=True, color=ORANGE)
kpi(13, "Avg inbound response time (hrs)", f'=IFERROR(AVERAGE({RT}),"-")', "0.0",
    note="Target: under 1 hour.")

# This month
section(15, "THIS MONTH")
kpi(16, "Contracts signed + paid", f'=COUNTIFS({CJ},">="&$C$5)')
kpi(17, "Cash collected at signing (AED)", f'=SUMIFS({CK},{CJ},">="&$C$5)', "#,##0")
kpi(18, "Refunds paid (count)", f'=COUNTIFS({CRs},"Paid",{CRd},">="&$C$5)')
kpi(19, "Refunds paid (AED)", f'=SUMIFS({CRa},{CRs},"Paid",{CRd},">="&$C$5)', "#,##0")

# Clients
section(21, "CLIENTS")
kpi(22, "Active clients", f'=COUNTIF({CS},"Active*")')
kpi(23, "Monthly recurring revenue (AED, ex VAT)", f'=SUMIFS({CI},{CS},"Active*")', "#,##0")
kpi(24, "Decisions pending", f'=COUNTIF({CS},"Decision*")')
kpi(25, "Free videos to schedule / in production",
    f'=COUNTIF({CS},"Schedule free video")+COUNTIF({CS},"Free video in production")')
kpi(26, "Trial-to-active rate", f'=IFERROR(COUNTIF({CS},"Active*")/(COUNTIF({CS},"Active*")+COUNTIF({CD},"Backed out")),"-")',
    "0%", note="Of clients whose free-video decision is settled, the share who stayed.")
kpi(27, "Signed but payment not logged", f'=COUNTIF({CS},"Awaiting payment")')

# Pipeline by stage
section(7, "PIPELINE BY STAGE", "G", 4)
db["H8"], db["I8"], db["J8"] = "Inbound", "Outbound", "Total"
for c in ("H8", "I8", "J8"):
    db[c].font = Font(name=F, size=9, bold=True, color="6B665F")
    db[c].alignment = Alignment(horizontal="right")
stages = lists["A"][1]
for i, stg in enumerate(stages, start=9):
    db[f"G{i}"] = f"=Settings!A{i-7}"
    db[f"H{i}"] = f"=COUNTIF({IS},G{i})"
    db[f"I{i}"] = f"=COUNTIF({OS},G{i})"
    db[f"J{i}"] = f"=H{i}+I{i}"
    for c in "GHIJ":
        db[f"{c}{i}"].font = bold if c == "J" else body
        db[f"{c}{i}"].border = box
r0 = 9 + len(stages)
db[f"G{r0}"] = "Total leads"
db[f"H{r0}"], db[f"I{r0}"], db[f"J{r0}"] = f"=SUM(H9:H{r0-1})", f"=SUM(I9:I{r0-1})", f"=SUM(J9:J{r0-1})"
for c in "GHIJ":
    db[f"{c}{r0}"].font = bold

# Open leads by owner
section(r0 + 2, "OPEN LEADS BY OWNER", "G", 4)
db[f"H{r0+3}"], db[f"I{r0+3}"] = "Open leads", "Actions due"
for c in (f"H{r0+3}", f"I{r0+3}"):
    db[c].font = Font(name=F, size=9, bold=True, color="6B665F")
for j, person in enumerate(lists["E"][1]):
    r = r0 + 4 + j
    db[f"G{r}"] = f"=Settings!E{j+2}"
    openf = lambda O, S, Nm: (f'COUNTIFS({O},G{r},{Nm},"<>")-COUNTIFS({O},G{r},{S},"Contract signed + paid")'
                              f'-COUNTIFS({O},G{r},{S},"Closed – No response")-COUNTIFS({O},G{r},{S},"Lost")')
    db[f"H{r}"] = f"={openf(IO, IS, INm)}+{openf(OO, OS, ONm)}"
    db[f"I{r}"] = (f'=COUNTIFS({IO},G{r},{IF_},"OVERDUE follow-up")+COUNTIFS({IO},G{r},{IF_},"Follow up today")'
                   f'+COUNTIFS({OO},G{r},{OF_},"OVERDUE follow-up")+COUNTIFS({OO},G{r},{OF_},"Follow up today")')
    for c in "GHI":
        db[f"{c}{r}"].font = body
        db[f"{c}{r}"].border = box

# Leads by source
rs = r0 + 10
section(rs, "LEADS BY SOURCE (ALL TIME)", "G", 4)
db[f"H{rs+1}"], db[f"I{rs+1}"] = "Leads", "Signed"
srcs = [(s, "in") for s in lists["B"][1]] + [(s, "out") for s in lists["C"][1]]
for j, (s, kind) in enumerate(srcs):
    r = rs + 2 + j
    src, stg = (ISrc, IS) if kind == "in" else (OSrc, OS)
    db[f"G{r}"] = f"{'In' if kind == 'in' else 'Out'} · {s}"
    db[f"H{r}"] = f'=COUNTIF({src},"{s}")'
    db[f"I{r}"] = f'=COUNTIFS({src},"{s}",{stg},"Contract signed + paid")'
    for c in "GHI":
        db[f"{c}{r}"].font = body
        db[f"{c}{r}"].border = box

# ---------------------------------------------------------------- Automations
au = wb.create_sheet("Automations")
au.sheet_view.showGridLines = False
heads = ["#", "When this happens…", "App", "…this happens automatically", "Writes to (tab → columns)", "Phase"]
data = [
    (1, "Website form submitted", "yontro.ae → Make.com", "Add row, Source = Website form, Stage = New; alert Usama on WhatsApp",
     "Inbound → Lead ID, Date received, Source, Business, Contact, Phone, Instagram, Wants more of", "1"),
    (2, "Calendly meeting booked", "Calendly → Make.com", "Find lead by email/phone; set Stage = Meeting booked and Meeting date; reminder 24h before",
     "Inbound / Outbound → Stage, Meeting date", "1"),
    (3, "Prospects saved to an Apollo list", "Apollo → Make.com", "Add rows, skip duplicates by email or phone; Stage = New",
     "Outbound → Lead ID, Date added, Source, Business…Apollo list", "1"),
    (4, "Prospect replies to an Apollo sequence", "Apollo → Make.com", "Set Stage = Replied; Last contact date = today",
     "Outbound → Stage, Last contact date", "1"),
    (5, "Stage set to Contract signed + paid", "Sheets → Make.com", "Create Clients row and a Free video row in Shoots; send Lianna the onboarding checklist",
     "Clients → Client ID…Amount paid; Shoots → Shoot ID, Client ID, Shoot type", "1"),
    (6, "Shoot date entered", "Sheets → Google Calendar", "Create event on Azeem's calendar with location; reminder to client the day before",
     "(calendar only)", "1"),
    (7, "Free video delivered", "Sheets → Make.com", "Decision window starts; Lianna nudged halfway; Usama alerted on deadline day",
     "(reads Clients → Free video delivered, Decision deadline)", "2"),
    (8, "WhatsApp message from a new number", "WhatsApp Business API (e.g. Wati) → Make.com",
     "Add row, Source = WhatsApp; auto-reply with Calendly meeting link", "Inbound → Date received, Source, Phone, Stage", "2"),
    (9, "Instagram DM or comment keyword", "ManyChat → Make.com", "Add row, Source = Instagram DM; reply with meeting link",
     "Inbound → Date received, Source, Instagram, Stage", "3"),
    (10, "Every morning 8:00", "Apps Script / Make.com", "Message each owner their 'Follow up today' and 'OVERDUE' rows",
     "(reads Action flag)", "2"),
]
for j, h in enumerate(heads, start=1):
    c = au.cell(row=1, column=j, value=h)
    c.font, c.fill = hdr_font, hdr_fill
    c.alignment = Alignment(wrap_text=True, vertical="center")
for i, row in enumerate(data, start=2):
    for j, v in enumerate(row, start=1):
        c = au.cell(row=i, column=j, value=v)
        c.font, c.border = body, box
        c.alignment = Alignment(wrap_text=True, vertical="top")
for col, w in zip("ABCDEF", (4, 32, 26, 52, 52, 7)):
    au.column_dimensions[col].width = w
r = len(data) + 3
au[f"A{r}"] = "Rules that keep it clean"
au[f"A{r}"].font = bold
for k, t in enumerate([
    "Each column has ONE writer: an app or a person, never both. Grey columns are formulas – nobody types there.",
    "Every lead gets a Lead ID (IN-0001 / OUT-0001). Phone or email is the duplicate check.",
    "Phase 1 = website form, Calendly, Apollo, Clients, Calendar. Add WhatsApp and Instagram once phase 1 runs smoothly.",
], start=1):
    au[f"A{r+k}"] = f"• {t}"
    au[f"A{r+k}"].font = body

# ---------------------------------------------------------------- Start Here
sh0 = wb.create_sheet("Start Here", 0)
sh0.sheet_view.showGridLines = False
sh0.column_dimensions["A"].width = 3
sh0.column_dimensions["B"].width = 26
sh0.column_dimensions["C"].width = 100
lines = [
    ("title", "YONTRO CRM"),
    ("sub", "One place for every lead – inbound or outbound – from first message to active client."),
    ("gap", None),
    ("h", "HOW TO USE THIS SHEET"),
    ("kv", ("White cells", "You type here. Most have dropdowns – pick from the list.")),
    ("kv", ("Grey cells / grey headers", "Formulas. Don't type here – they calculate themselves.")),
    ("kv", ("Row 2 on each tab", "An EXAMPLE row (grey italic). Overwrite or delete it once you start.")),
    ("kv", ("Settings tab", "Edit dropdown lists, package prices and the rules (follow-up gap, decision window).")),
    ("gap", None),
    ("h", "THE TABS"),
    ("kv", ("Dashboard", "The weekly numbers. Read only.")),
    ("kv", ("Inbound", "Leads who came to us: website, WhatsApp, Instagram, referrals, walk-ins.  Owner: Usama")),
    ("kv", ("Outbound", "Leads we went after: Apollo, LinkedIn, Google Maps.  Owner: Usama")),
    ("kv", ("Clients", "Everyone who signed + paid: free video, decision window, refunds, active plan.  Owner: Lianna")),
    ("kv", ("Shoots", "Every shoot – free videos and plan shoots.  Owner: Azeem")),
    ("kv", ("Automations", "What connects to what (Make.com, Calendly, Apollo, Calendar). The setup checklist.")),
    ("gap", None),
    ("h", "THE PIPELINE"),
    ("kv", ("Selling (Inbound / Outbound)", "New → Contacted → Replied → Meeting booked → Meeting held → Proposal sent → Contract signed + paid")),
    ("kv", ("", "or → Closed – No response (after 4 follow-ups) / Lost")),
    ("kv", ("Trial (Clients + Shoots)", "Signed + paid → Free video shot → Delivered → Decision window")),
    ("kv", ("Outcome (Clients)", "Approves → Active   ·   Says nothing → Active (plan goes ahead)   ·   Backs out → Refund, keeps the video")),
    ("gap", None),
    ("h", "THE RULES WE AGREED"),
    ("kv", ("Free video", "Only for clients who have signed the contract. As many as needed for onboarded clients.")),
    ("kv", ("Payment", "Taken at signing.")),
    ("kv", ("Backing out", "Client can back out after the free video if not satisfied → refund. They keep the free video.")),
    ("kv", ("Silence after delivery", "Plan goes ahead – they have signed and paid.")),
    ("kv", ("Ghosting (before contract)", "4 follow-ups, 3 days apart, each adding new value. Then stop outreach → Closed – No response.")),
    ("kv", ("Repeat refunds", "A business that was refunded before is flagged ⚠ – no second free video.")),
    ("kv", ("Decision window", "NOT DECIDED YET – set to 3 working days as a placeholder (Settings tab, yellow cell).")),
    ("gap", None),
    ("h", "EACH PERSON'S DAY"),
    ("kv", ("Usama", "Inbound + Outbound: filter Owner = Usama and Action flag. Clear OVERDUE first, then 'Follow up today'. Reply to new inbound within 1 hour.")),
    ("kv", ("Azeem", "Shoots: filter Videographer = Azeem. Update Status and Delivered date the day it happens.")),
    ("kv", ("Lianna", "Clients: work every 'Decision pending' row; onboard new signings; log refunds with a reason.")),
    ("kv", ("Owner", "Dashboard once a week.")),
    ("gap", None),
    ("h", "AFTER A FOLLOW-UP"),
    ("kv", ("Update two cells", "Last contact date = today, and Follow-ups sent +1. The sheet works out the next due date.")),
]
r = 1
for kind, v in lines:
    if kind == "title":
        sh0[f"B{r}"] = v
        sh0[f"B{r}"].font = Font(name=F, size=20, bold=True, color=INK)
    elif kind == "sub":
        sh0[f"B{r}"] = v
        sh0[f"B{r}"].font = Font(name=F, size=11, italic=True, color="6B665F")
    elif kind == "h":
        sh0[f"B{r}"] = v
        sh0[f"B{r}"].font = Font(name=F, size=11, bold=True, color="FFFFFF")
        sh0[f"B{r}"].fill = fill(ORANGE)
        sh0[f"C{r}"].fill = fill(ORANGE)
    elif kind == "kv":
        sh0[f"B{r}"], sh0[f"C{r}"] = v
        sh0[f"B{r}"].font = bold
        sh0[f"C{r}"].font = body
        sh0[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        sh0[f"B{r}"].alignment = Alignment(vertical="top", wrap_text=True)
        sh0[f"B{r}"].border = sh0[f"C{r}"].border = box
    r += 1
sh0["C31"].fill = fill("FFFF00")

# tab colours / order
for ws, colr in ((sh0, ORANGE), (db, INK), (inb, "2E7D32"), (outb, "1565C0"), (cl, "6A1B9A"),
                 (sh, "EF6C00"), (au, "757575"), (st, "9E9E9E")):
    ws.sheet_properties.tabColor = colr
wb._sheets = [sh0, db, inb, outb, cl, sh, au, st]
wb.active = 0
wb.save(OUT)
print("saved", OUT)
