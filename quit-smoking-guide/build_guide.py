"""Build the free guided-meditation quit-smoking PDF lead magnet."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, KeepTogether, NextPageTemplate)

# ----------------------------------------------------------------------------
# EDIT THESE
# ----------------------------------------------------------------------------
AUTHOR = "Sahill"
HANDLE = "@yourhandle"            # your Instagram handle
DAYS_FREE = 15                    # days since your last cigarette
OUT = "Breathe-Out-The-Habit.pdf"

# ----------------------------------------------------------------------------
# Fonts and palette
# ----------------------------------------------------------------------------
F = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif", F + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", F + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", F + "LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", F + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", F + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", F + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-Italic", boldItalic="Serif-Bold")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic", boldItalic="Sans-Bold")

DEEP = colors.HexColor("#173F3A")     # deep teal
TEAL = colors.HexColor("#2E7D6F")
MINT = colors.HexColor("#DDEDE6")
SAND = colors.HexColor("#F6F1E8")
INK = colors.HexColor("#1F2A2A")
MUTED = colors.HexColor("#5F6F6C")
GOLD = colors.HexColor("#C9A56B")
WHITE = colors.white

W, H = A4
M = 20 * mm

# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
def S(name, **kw):
    base = dict(fontName="Sans", fontSize=10.5, leading=16, textColor=INK, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)

sty = {
    "h1": S("h1", fontName="Serif-Bold", fontSize=26, leading=31, textColor=DEEP, spaceBefore=0, spaceAfter=4),
    "kicker": S("kicker", fontName="Sans-Bold", fontSize=9, leading=12, textColor=TEAL, spaceAfter=6),
    "h2": S("h2", fontName="Serif-Bold", fontSize=15, leading=19, textColor=DEEP, spaceBefore=12, spaceAfter=4),
    "h3": S("h3", fontName="Sans-Bold", fontSize=10.5, leading=14, textColor=TEAL, spaceBefore=5, spaceAfter=2),
    "body": S("body"),
    "lead": S("lead", fontName="Serif", fontSize=13, leading=20, textColor=INK, spaceAfter=10),
    "quote": S("quote", fontName="Serif-Italic", fontSize=12.5, leading=19, textColor=DEEP, leftIndent=14, spaceBefore=6, spaceAfter=10),
    "script": S("script", fontName="Serif", fontSize=11.5, leading=16.5, textColor=INK, spaceAfter=5),
    "cue": S("cue", fontName="Sans-Italic", fontSize=9, leading=12, textColor=MUTED, spaceAfter=5),
    "bullet": S("bullet", leftIndent=14, bulletIndent=2, spaceAfter=4),
    "small": S("small", fontSize=8.5, leading=12, textColor=MUTED),
    "box": S("box", fontSize=10.5, leading=16, textColor=INK, spaceAfter=0),
    "boxtitle": S("boxtitle", fontName="Sans-Bold", fontSize=9, leading=12, textColor=TEAL, spaceAfter=3),
    "cover_title": S("cover_title", fontName="Serif-Bold", fontSize=40, leading=44, textColor=WHITE, spaceAfter=10),
    "cover_sub": S("cover_sub", fontName="Serif", fontSize=16, leading=23, textColor=colors.HexColor("#DDEDE6"), spaceAfter=0),
    "cover_kicker": S("cover_kicker", fontName="Sans-Bold", fontSize=10, leading=13, textColor=GOLD, spaceAfter=14),
    "cover_by": S("cover_by", fontName="Sans", fontSize=10.5, leading=14, textColor=colors.HexColor("#BFD8CF")),
}


def P(text, style="body"):
    return Paragraph(text, sty[style])


def bullets(items):
    return [Paragraph(t, sty["bullet"], bulletText="•") for t in items]


def callout(title, text, bg=MINT):
    inner = [P(title, "boxtitle"), P(text, "box")]
    t = Table([[inner]], colWidths=[W - 2 * M])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
    ]))
    return t


def rule():
    t = Table([[""]], colWidths=[W - 2 * M], rowHeights=[1])
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.6, GOLD)]))
    return t


# ----------------------------------------------------------------------------
# Page decorations
# ----------------------------------------------------------------------------
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(DEEP)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # soft concentric circles, like a breath expanding
    cx, cy = W * 0.72, H * 0.70
    for i, r in enumerate([150, 120, 90, 60, 30]):
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.035 + i * 0.02))
        c.circle(cx, cy, r, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(M, 62 * mm, M + 40 * mm, 62 * mm)
    c.setFillColor(colors.HexColor("#BFD8CF"))
    c.setFont("Sans", 9)
    c.drawString(M, 20 * mm, f"Free guide  •  {HANDLE}  •  Not medical advice")
    c.restoreState()


def draw_page(c, doc):
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(M, H - 14 * mm, W - M, H - 14 * mm)
    c.setFillColor(MUTED)
    c.setFont("Sans", 8)
    c.drawString(M, H - 12 * mm, "BREATHE OUT THE HABIT")
    c.drawRightString(W - M, H - 12 * mm, "A free guided meditation to quit smoking")
    c.setFont("Sans", 8)
    c.drawCentredString(W / 2, 12 * mm, f"{doc.page}")
    c.drawRightString(W - M, 12 * mm, HANDLE)
    c.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=22 * mm, bottomMargin=18 * mm,
                      title="Breathe Out the Habit: A Free Guided Meditation to Quit Smoking",
                      author=AUTHOR, subject="Guided meditation and a 15-day plan to quit smoking")

cover_frame = Frame(M, 70 * mm, W - 2 * M, H - 140 * mm, id="cover", leftPadding=0, rightPadding=0)
body_frame = Frame(M, 18 * mm, W - 2 * M, H - 38 * mm, id="body", leftPadding=0, rightPadding=0)
doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover),
    PageTemplate(id="Body", frames=[body_frame], onPage=draw_page),
])

story = []

# ----------------------------------------------------------------------------
# COVER
# ----------------------------------------------------------------------------
story += [
    P("FREE GUIDE", "cover_kicker"),
    P("Breathe Out<br/>the Habit", "cover_title"),
    Spacer(1, 6),
    P("A guided meditation to quit smoking, plus the 15-day rhythm of breath and movement that got me through it.", "cover_sub"),
    Spacer(1, 26),
    P(f"By {AUTHOR}  •  {DAYS_FREE} days smoke-free and counting", "cover_by"),
    NextPageTemplate("Body"),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: WELCOME
# ----------------------------------------------------------------------------
story += [
    P("A NOTE FROM ME", "kicker"),
    P("I quit 15 days ago. Here is what actually worked.", "h1"),
    Spacer(1, 6),
    P("I am not a doctor, a coach, or a guru. I am someone who smoked, wanted to stop, and finally did. "
      "I tried the willpower route more than once. It never lasted, because a craving does not care how motivated you were this morning.", "lead"),
    P("What finally changed was simple. I stopped fighting cravings and started <b>sitting with them</b>. "
      "Every time the urge came, I did a short guided meditation instead of reaching for a cigarette. "
      "And every day I did some cardio, because a body that has just run does not want smoke in it."),
    P("Two tools. Breath and movement. Fifteen days. That is the whole method, and this guide gives you both."),
    Spacer(1, 4),
    callout("WHAT IS INSIDE",
            "• Why meditation beats willpower for cravings<br/>"
            "• The 3-minute Craving Reset for the moment an urge hits<br/>"
            "• The 10-minute morning guided meditation, word for word<br/>"
            "• A 2-minute evening close<br/>"
            "• The cardio rhythm I paired with it<br/>"
            "• A 15-day tracker you can print or screenshot"),
    Spacer(1, 10),
    P("How to use this guide", "h2"),
    P("Read the next page once so you understand what a craving actually is. Then record yourself reading the meditation scripts on your phone, "
      "slowly, with pauses. Your own voice is calmer to you than any app. From then on, when an urge hits, you press play instead of lighting up."),
    P("If you would rather not record, read the script silently with your eyes half closed. It still works. The words are only there to give your mind somewhere to go."),
    Spacer(1, 6),
    P("<i>This guide shares my personal experience and is not medical advice. Nicotine withdrawal can affect mood, sleep and appetite. "
      "If you have a health condition, are pregnant, or take medication, speak to a doctor before changing your routine.</i>", "small"),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: WHY IT WORKS
# ----------------------------------------------------------------------------
story += [
    P("THE IDEA", "kicker"),
    P("A craving is a wave. You only have to stay afloat for a few minutes.", "h1"),
    Spacer(1, 6),
    P("Here is the thing nobody told me for years: <b>a craving does not last</b>. It builds, peaks, and passes, usually inside three to five minutes, "
      "whether or not you smoke. Smoking does not end the craving. It just teaches your brain that the wave was an emergency.", "lead"),
    P("Willpower tries to hold the wave back. That is exhausting, and the wave is stronger than you. Meditation does the opposite. "
      "You let the wave come, you watch it, you breathe through it, and you notice the exact moment it starts to fade. "
      "Do that ten times and something clicks. The craving is still there, but it has stopped being a command."),
    P("Three things a craving needs from you", "h2"),
]
story += bullets([
    "<b>Speed.</b> It wants you to act before you think. A slow breath removes the speed.",
    "<b>Story.</b> It wants you to believe “just one” or “I have earned it”. Naming the story out loud takes its power away.",
    "<b>Somewhere to go.</b> Your hands and your lungs are used to a ritual. Give them a new one: a breath count, a walk, a glass of water.",
])
story += [
    Spacer(1, 6),
    P("Why cardio belongs next to meditation", "h2"),
    P("Meditation handles the craving in the moment. Cardio handles the hours in between. Fifteen to twenty minutes of walking fast, cycling or running "
      "clears the restlessness that withdrawal leaves behind, lifts your mood, and gives you a daily reason to protect your lungs. "
      "On the days I moved, the cravings were fewer and quieter. On the one day I skipped it, they came back louder."),
    Spacer(1, 4),
    callout("THE RULE I FOLLOWED",
            "Never decide about a cigarette in the middle of a craving. Do the 3-minute Craving Reset first. "
            "Then, if you still want it, decide. In fifteen days I never once still wanted it."),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: CRAVING RESET (3 min)
# ----------------------------------------------------------------------------
story += [
    P("MEDITATION 1  •  3 MINUTES", "kicker"),
    P("The Craving Reset", "h1"),
    P("Use this the moment an urge hits. Standing, sitting, in a car park, in the bathroom at work. Anywhere.", "lead"),
    P("Read slowly. Each line is roughly one breath. A dot line means pause.", "cue"),
    rule(),
    Spacer(1, 8),
    P("Stop where you are. You do not need to fix anything yet.", "script"),
    P("Let your feet feel the floor. Let your shoulders drop, just a little.", "script"),
    P("Notice the craving. Do not push it away. Just find where it lives in your body. Your chest, your throat, your hands, your jaw.", "script"),
    P("Say quietly, in your head: <i>“This is a craving. It is a wave. It will pass.”</i>", "script"),
    P(". . .", "cue"),
    P("Breathe in through your nose for a count of four. One, two, three, four.", "script"),
    P("Hold for a count of two.", "script"),
    P("Breathe out through your mouth for a count of six, slow, like you are fogging a mirror. One, two, three, four, five, six.", "script"),
    P("That is the breath your body has been asking for. Not smoke. Just a long, slow exhale.", "script"),
    P(". . .", "cue"),
    P("Again. In for four. Hold for two. Out for six.", "script"),
    P("And again. In for four. Hold for two. Out for six.", "script"),
    P("Now go back to the place in your body where the craving lives. Is it the same size? Smaller? Has it moved?", "script"),
    P("You do not have to make it go away. You are just watching it change. Waves always change.", "script"),
    P(". . .", "cue"),
    P("Three more breaths, your own pace. With each exhale, imagine breathing out a little grey smoke you no longer need.", "script"),
    P("Last one. In, slow. Out, slower.", "script"),
    P("Notice: you are still here. The craving did its worst and you are fine. That is one more wave you have surfed.", "script"),
    Spacer(1, 6),
    callout("AFTER THE RESET", "Drink a glass of water. Move your body for sixty seconds: walk, stretch, climb a flight of stairs. "
            "Then get on with your day. Tick the tracker. Every reset is a rep.", bg=SAND),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: MORNING MEDITATION (10 min)
# ----------------------------------------------------------------------------
story += [
    P("MEDITATION 2  •  10 MINUTES", "kicker"),
    P("The Morning Breath", "h1"),
    P("Every morning before your first coffee, for all fifteen days. It sets your intention and trains the breath you use in the Craving Reset.", "lead"),
    P("Sit upright on a chair or the edge of your bed. Hands on your thighs. Eyes closed or lowered. Record it, or read it slowly.", "cue"),
    rule(),
    Spacer(1, 6),
    P("Settling in", "h3"),
    P("Take a moment to arrive. Feel the weight of your body on the seat. Feel your feet on the floor.", "script"),
    P("Let your face soften. Let your jaw unclench. Let your tongue rest away from the roof of your mouth.", "script"),
    P("Take one big breath in, and sigh it out through the mouth. Let it be loud. Let it be a release.", "script"),
    P(". . .", "cue"),
    P("The breath", "h3"),
    P("Now breathe naturally through the nose. Do not change it yet. Just watch it. Cool air in. Warm air out.", "script"),
    P("Notice the small pause at the top of each breath, and the small pause at the bottom. Rest in those pauses.", "script"),
    P("Slowly begin to lengthen the exhale. Let each out-breath be a little longer than the in-breath. There is no rush. Nothing to do. Nowhere to be.", "script"),
    P(". . .", "cue"),
    P("Ten slow breaths like this. Count them down in your head, from ten to one. If you lose count, start again at ten. Losing count is not failing. Noticing is the practice.", "script"),
    P(". . . . . .", "cue"),
    P("The body", "h3"),
    P("Bring your attention to your lungs. Picture them for a moment. Two soft, patient sponges that have been working for you every second of your life, even when you were not kind to them.", "script"),
    P("With every clean breath you take today, they are healing. Not in a year. Today. Right now, in this breath.", "script"),
    P("Breathe in and feel your chest widen. Breathe out and feel it settle. Send one breath of thanks to your lungs.", "script"),
    P(". . .", "cue"),
    P("The intention", "h3"),
    P("Now bring to mind the day ahead. See the moments where a cigarette used to live. The coffee. The drive. The break. The evening.", "script"),
    P("For each one, picture yourself there, breathing instead. In for four. Out for six. Calm. Unhurried. Free.", "script"),
    P("Say quietly, once: <i>“Today I do not smoke. When the wave comes, I breathe, and it passes.”</i>", "script"),
    P("Say it once more, and mean it a little more this time.", "script"),
    P(". . .", "cue"),
    P("Closing", "h3"),
    P("One more full breath. Feel your feet, feel your hands, hear the room. When you are ready, open your eyes, stand up slowly, and drink a glass of water. Your day has begun, and it has begun clean.", "script"),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: EVENING CLOSE + CARDIO
# ----------------------------------------------------------------------------
story += [
    P("MEDITATION 3  •  2 MINUTES", "kicker"),
    P("The Evening Close", "h1"),
    P("Do this lying in bed, lights off. It is short on purpose. Its job is to end the day with proof, so you wake up believing you can do it again.", "lead"),
    rule(),
    Spacer(1, 6),
    P("Lie back. Let the bed take your weight. Breathe out long, and let the day go with it.", "script"),
    P("Look back over today. Find every craving that came. Count them. Each one you did not smoke through is a win. Count the wins.", "script"),
    P("Say quietly: <i>“Today I did not smoke. That is one more day my lungs got to breathe clean.”</i>", "script"),
    P("Picture tomorrow morning. You, sitting up, doing the Morning Breath again. It is already familiar. It is already yours.", "script"),
    P("Breathe in for four. Out for six. Let sleep come when it comes.", "script"),
    Spacer(1, 14),
    P("THE MOVEMENT HALF", "kicker"),
    P("The cardio rhythm I paired with it", "h2"),
    P("You do not need a gym or a plan. You need to get slightly out of breath once a day, ideally at the time you used to crave most. "
      "For me that was late afternoon. Here is the pattern I used for fifteen days."),
]
cardio = Table([
    ["Days", "What I did", "Why"],
    ["1 to 5", "15-minute brisk walk, fast enough that talking is slightly hard.", "Withdrawal peaks here. Walking burns off the restlessness without adding stress."],
    ["6 to 10", "20 minutes: walk 2 min, jog 1 min, repeat. Or a bike ride, or stairs.", "Cravings are fewer now. Harder breathing reminds you what clean lungs feel like."],
    ["11 to 15", "25 minutes of whatever you enjoy: run, cycle, swim, skipping, a class.", "This is habit territory. Make it something you want to keep after day 15."],
], colWidths=[22 * mm, 70 * mm, W - 2 * M - 92 * mm])
cardio.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Sans-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("FONTNAME", (0, 1), (0, -1), "Sans-Bold"), ("TEXTCOLOR", (0, 1), (0, -1), DEEP),
    ("FONTNAME", (1, 1), (-1, -1), "Sans"), ("TEXTCOLOR", (1, 1), (-1, -1), INK),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SAND, WHITE]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEADING", (0, 0), (-1, -1), 13),
    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("LINEBELOW", (0, -1), (-1, -1), 0.6, GOLD),
]))
# wrap cells in paragraphs so text wraps
cell_sty = S("cell", fontSize=9.5, leading=13, spaceAfter=0)
cell_b = S("cellb", fontName="Sans-Bold", fontSize=9.5, leading=13, textColor=DEEP, spaceAfter=0)
cell_h = S("cellh", fontName="Sans-Bold", fontSize=9.5, leading=13, textColor=WHITE, spaceAfter=0)
data = cardio._cellvalues
wrapped = [[Paragraph(x, cell_h) for x in data[0]]] + [[Paragraph(r[0], cell_b)] + [Paragraph(x, cell_sty) for x in r[1:]] for r in data[1:]]
cardio._cellvalues = wrapped
story += [
    Spacer(1, 4), cardio, Spacer(1, 8),
    P("<b>One rule:</b> finish every session with the Craving Reset breath, three rounds. In for four, hold two, out for six. "
      "You are linking the feeling of a clear chest to the breath you will use when the next wave comes."),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: 15-DAY TRACKER
# ----------------------------------------------------------------------------
story += [
    P("YOUR TURN", "kicker"),
    P("The 15-Day Tracker", "h1"),
    P("Print this page or screenshot it. Tick each box as you go. Fifteen rows, three ticks a day. That is forty-five small proofs that you are someone who does not smoke.", "lead"),
]
hdr = ["Day", "Morning Breath", "Cardio", "Evening Close", "Cravings surfed"]
rows = [hdr] + [[str(i), "□", "□", "□", ""] for i in range(1, 16)]
tw = W - 2 * M
tracker = Table(rows, colWidths=[16 * mm, 34 * mm, 30 * mm, 34 * mm, tw - 114 * mm], rowHeights=[9 * mm] + [10.5 * mm] * 15)
tracker.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Sans-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("FONTNAME", (0, 1), (0, -1), "Serif-Bold"), ("FONTSIZE", (0, 1), (0, -1), 12), ("TEXTCOLOR", (0, 1), (0, -1), DEEP),
    ("FONTNAME", (1, 1), (3, -1), "Sans"), ("FONTSIZE", (1, 1), (3, -1), 16), ("TEXTCOLOR", (1, 1), (3, -1), TEAL),
    ("ALIGN", (0, 0), (3, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SAND]),
    ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#CFDBD6")),
    ("LINEBELOW", (0, 5), (-1, 5), 1.2, GOLD),
    ("LINEBELOW", (0, 10), (-1, 10), 1.2, GOLD),
    ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
]))
story += [
    Spacer(1, 4), tracker, Spacer(1, 8),
    P("Gold lines mark the end of each five-day block. Day 5 is the hardest wall. Day 10 is when it gets quiet. Day 15 is when you realise you have not thought about it since lunch.", "small"),
    PageBreak(),
]

# ----------------------------------------------------------------------------
# PAGE: WHAT NEXT
# ----------------------------------------------------------------------------
story += [
    P("BEFORE YOU GO", "kicker"),
    P("Three things that made the difference", "h1"),
    Spacer(1, 4),
]
story += bullets([
    "<b>I told people.</b> Not everyone. Two friends and my Instagram. Saying it out loud made it real, and every message of support was one more reason to keep going.",
    "<b>I changed the ritual, not just the cigarette.</b> Coffee moved to after the morning meditation. The after-meal smoke became the after-meal walk. The habit needed a new shape, not an empty gap.",
    "<b>I counted wins, not days.</b> Days feel slow. Cravings surfed feel like progress. By the end I had beaten more than a hundred waves, and that number was the thing I was proud of.",
])
story += [
    Spacer(1, 10),
    rule(),
    Spacer(1, 10),
    P("Watch the full video", "h2"),
    P(f"I filmed the whole story: the first three days, the exact meditation I used, the cardio, and the moment it stopped being hard. "
      f"It is on my Instagram at <b>{HANDLE}</b>. Watch it when you need a reminder that this is possible."),
    Spacer(1, 6),
    P("Stay in touch", "h2"),
    P(f"Follow <b>{HANDLE}</b> for daily reminders, new meditations, and the day-16-onwards plan. "
      f"If this guide helps you, send me a message and tell me which day you are on. I read every one, and I remember what day 3 felt like."),
    Spacer(1, 14),
    callout("PASS IT ON", "This guide is free. If someone you love is trying to quit, send it to them. The link is in my bio.", bg=SAND),
    Spacer(1, 24),
    P("You have quit before, for the length of every single breath you took between cigarettes. Now you are just breathing out, and not breathing back in.", "quote"),
    Spacer(1, 4),
    P(f"— {AUTHOR}", "cue"),
    Spacer(1, 30),
    P("<b>Disclaimer.</b> This guide reflects my personal experience of quitting smoking and is shared for general information only. It is not medical, psychological or professional advice, "
      "and it is not a substitute for care from a qualified health professional. Results vary. If you experience severe withdrawal symptoms, low mood, or have any health concerns, please consult a doctor. "
      f"© {AUTHOR}. You may share this PDF freely in its original, unedited form.", "small"),
]

doc.build(story)
print("Wrote", OUT)
