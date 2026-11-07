import re
SD="/home/user/aura-reset-center/docs/studio-crm/"
src=open("/home/user/aura-reset-center/docs/sales-crm/yontro-sales.html").read()
L=src.split("\n")
def between(a,b,inclusive_a=True):
    i=src.index(a); j=src.index(b,i); return src[i if inclusive_a else i+len(a):j]
fonts=[l for l in L[:6] if l.startswith("<link") or l.startswith("<meta")]
css=between("<style>\n","\n</style>",False)
header=src[src.index('<header class="top">'):src.index("</header>")+9]
header=header.replace("<span>Yontro Sales<br><small>YONTRO.AE / SALES CRM</small></span>","<span>Yontro Studio<br><small>YONTRO.AE / STUDIO</small></span>").replace("How to use this CRM","How to use Yontro Studio")
assert "Yontro Studio" in header
script=src[src.index("<script>")+8:src.rindex("</script>")]
def sc(a,b):
    i=script.index(a); j=script.index(b,i); return script[i:j]
icon=sc("const ICON={","const LABEL=")
helpers=sc("const LABEL=","let db=null")
clock=sc("/* ---------- time clock ---------- */","/* office code")
docs=sc("const LOGO_WORD=","function leadInfo(")
assets=sc("const LOGO_SVG=","function agreementHTML(")
agreement=sc("function agreementHTML(","/* ---------- papers:")
papers=sc("/* ---------- papers:","/* ---------- first-use tour")
tour=sc("/* ---------- first-use tour","/* ---------- Hamza's end-of-day")
period=sc("/* ---------- weekly & monthly reports (shared)","/* ---------- period metrics (sales)")
# --- adapt papers/wellbeing to John ---
def rp(s,a,b,cnt=1):
    assert s.count(a)==cnt,(s.count(a),a[:70]); return s.replace(a,b)
papers=rp(papers,"Hamza Qureshi, Sales Lead and line manager","John Smith, Head of Production and line manager")
papers=rp(papers,'EMPLOYEE WHO ASKED: ${names[uid]||"a member of the sales team"} (Yontro sales team)','EMPLOYEE WHO ASKED: ${names[uid]||"a member of the production team"} (Yontro production team)')
papers=rp(papers,"You are Hamza Qureshi, Sales Lead at Yontro in Dubai and a caring manager.","You are John Smith, Head of Production at Yontro in Dubai and a caring manager.")
papers=rp(papers,"practical for a day of cold calls and visits selling social media packages to Dubai businesses","practical for a day of filming Founder Tales trial reels, a Yontro.ae video and client shoots and edits")
papers=rp(papers,"You are Hamza Qureshi, a caring manager","You are John Smith, a caring manager")
papers=rp(papers,'''$("#paperQuick").innerHTML=`<button type="button" data-newag>${ICON.contract}Service agreement</button><button type="button" data-newletter>${ICON.letter}Ask Hamza for a letter</button>`;''','''$("#paperQuick").innerHTML=`<button type="button" data-newletter>${ICON.letter}Ask John for a letter</button>`;''')
papers=rp(papers,'''$("#paperNote").textContent=`Contracts and letters become official only once Sahill signs and stamps them${signing.bypassContracts?". Right now Hamza can sign standard 3-month contracts on his behalf":""}.`;''','''$("#paperNote").textContent="Letters become official only once Sahill signs and stamps them.";''')
papers=papers.replace('aria-hidden="true">H</span>','aria-hidden="true">J</span>')
papers=papers.replace("Hamza","John")
assert "Hamza" not in papers
# --- tour steps ---
TOUR='''const TOUR=[
 {title:"Welcome to Yontro Studio",text:"This is where you run your day: Founder Tales reels, Yontro.ae videos and client shoots. John Smith, Head of Production, is your manager here. This short tour shows what to do on each screen."},
 {tab:"today",sel:"#morningCard",title:"1. Your morning brief",text:"Every morning: a message from John, yesterday's numbers and John's report on your day. Read it before you start."},
 {tab:"today",sel:"#shiftCard",title:"2. Start and end your day here",text:"Punch in when you start (10:00), use breaks, and punch out when you finish. When you punch out, John writes your report."},
 {tab:"today",sel:"#kpis",title:"3. Today's targets and score",text:"2 Founder Tales trial reels, 1 posted live, 1 Yontro.ae video. Your score out of 100 updates as you work."},
 {tab:"today",sel:"#checklist",card:true,title:"4. Your checklist builds itself",text:"Post yesterday's best trial live, log stats and followers, film 2 trial reels and the Yontro video, today's shoots, client edits with countdowns, plan tomorrow's ideas, check in with John."},
 {tab:"today",sel:"#quick",card:true,title:"5. Quick add",text:"Add a trial reel, an idea, a Yontro video, a shoot, today's followers or a new client in one tap."},
 {tab:"today",sel:"#wellCard",title:"6. Look after yourself",text:"Daily affirmation, a water tracker with reminders, a 10-minute silence break and a private chat with John about how you feel."},
 {tab:"content",sel:"#ftFollow",card:true,title:"7. Follower growth",text:"Log the Founder Tales follower count every day. You'll see the gain, the daily pace needed for 5,000 and how far you are."},
 {tab:"content",sel:"#vidChips",title:"8. Every video in one place",text:"Ideas → Editing → Trial reel → Live (or Dropped). Tap a video to add stats (views, follows, shares, watch-through) or ask John to review it. Best performers ranks them."},
 {tab:"content",sel:"#hookLib",card:true,title:"9. Hook library",text:"Your best hooks collect here automatically, ranked by results. Reuse what works."},
 {tab:"clients",sel:"#dueList",card:true,title:"10. Edits due",text:"Mark a shoot as done and the clock starts: first edit within 48 hours, each revision within 24. Amber means under 12 hours, red means late."},
 {tab:"clients",sel:"#shootList",card:true,title:"11. Shoots",text:"Book shoots with date, place and brief. John drafts the shot list, you tick the kit check, paste footage and edit links, and log approvals step by step."},
 {tab:"clients",sel:"#clientList",card:true,title:"12. Videos owed per client",text:"Each client's package (Launch 5, Growth 10, Scale 15 a month) against videos delivered this month."},
 {tab:"cal",sel:"#week",title:"13. Your week",text:"Shoots, edit deadlines, trial reels and scheduled posts in one calendar."},
 {tab:"score",sel:"#scoreBody",title:"14. Your success score",text:"40% Founder Tales output, 30% client edits on time, 20% follower growth vs goal, 10% check-ins and stats logged. Plus watch-through, trial-to-live rate and first-time approvals."},
 {tab:"papers",sel:"#paperQuick",card:true,title:"15. Letters",text:"Need sick leave, annual leave, a salary certificate or an NOC? Ask John. Sahill signs and stamps it and it comes back here."},
 {sel:"#hzBtn",title:"16. John is always here",text:"Ask: anything, plus letters. Check-in: your daily numbers. Ideas: tomorrow's videos from what performed. Review: feedback on a hook or script. How I'm doing: private."},
 {title:"Your daily rhythm",text:"Punch in → post yesterday's winner → log stats and followers → film 2 trial reels and the Yontro video → shoots and edits on time → plan tomorrow → check in with John → Punch out. Tap ? any time to see this again.",last:true}
];'''
tour=re.sub(r"const TOUR=\[.*?\n\];",lambda m:TOUR,tour,count=1,flags=re.S)
assert "Yontro Studio" in tour
extra_icons='Object.assign(ICON,{play:\'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M10 9l5 3-5 3z"/></svg>\',cam:\'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/></svg>\',idea:\'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9V16h7v-2.1A6 6 0 0012 3z"/></svg>\'});\n'
studio_css='''
nav.tabs button{font-size:11px;padding-left:0;padding-right:0}
.due{font-family:var(--mono);font-size:11.5px;padding:2px 8px;border-radius:99px;background:var(--soft);white-space:nowrap}.due.soon{background:var(--amber);color:#111}.due.over{background:var(--red);color:#fff}
.vstat{display:flex;gap:3px 10px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:3px}
.minis{display:flex;gap:6px 14px;flex-wrap:wrap;font-size:13.5px}.minis b{font-family:var(--display);font-weight:900}
.cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}.cmpc{border:1.5px solid var(--line);border-radius:12px;padding:10px;display:grid;gap:4px;align-content:start}.cmpc.win{border-color:var(--green);background:color-mix(in srgb,var(--green) 8%,var(--surface))}.cmpr{display:flex;justify-content:space-between;font-size:12.5px;gap:8px}
.bigscore{display:flex;align-items:baseline;gap:4px}.bigscore b{font-family:var(--display);font-size:56px;font-weight:900;line-height:1}.bigscore span{color:var(--muted);font-weight:700}
.parts{display:grid;gap:10px}.parts .head span{font-size:13.5px;font-weight:600}
.wkbars{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center}.wkb{height:110px;background:var(--soft);border-radius:8px;display:flex;align-items:flex-end;overflow:hidden}.wkb i{display:block;width:100%;background:var(--or)}
'''
views='''<main class="wrap" id="app">
  <div id="banner" class="notice" hidden></div>
  <section id="v-today" class="view" style="display:grid;gap:14px">
    <div class="head"><div><div class="tag" id="todayDate"></div><h1 id="hello">Today</h1></div></div>
    <div class="card hl" id="morningCard"></div>
    <div class="card shift" id="shiftCard"></div>
    <div class="card" id="liveMeeting" hidden></div>
    <div class="kpis" id="kpis"></div>
    <div class="card"><div class="head"><h2>Today's checklist</h2><span class="tag" id="ckCount"></span></div><div class="list" id="checklist"></div></div>
    <div class="card"><div class="head"><h2>Quick add</h2></div><div class="quick" id="quick"></div></div>
    <div class="card" id="reportCard" hidden></div>
    <div class="card" id="periodCard" hidden></div>
    <div class="card" id="wellCard" hidden></div>
  </section>
  <section id="v-content" class="view" hidden style="display:grid;gap:14px">
    <div class="head"><div><div class="tag">Founder Tales and Yontro.ae</div><h1>Content</h1></div><div class="btnrow"><button class="btn sm" type="button" data-hzopen="ideas">Ideas from John</button><button class="btn or" type="button" data-newvid="ft-trial">+ Video</button></div></div>
    <div class="card" id="ftFollow"></div>
    <div class="card hl" id="ftCompare" hidden></div>
    <div class="card"><div class="chips" id="vidChips" role="group" aria-label="Filter videos"></div><div class="list" id="vidList"></div></div>
    <div class="card"><div class="head"><h2>Hook library</h2><span class="tag">Your best-performing hooks</span></div><div class="list" id="hookLib"></div></div>
  </section>
  <section id="v-clients" class="view" hidden style="display:grid;gap:14px">
    <div class="head"><div><div class="tag">Shoots, edits and deliveries</div><h1>Clients</h1></div><div class="btnrow"><button class="btn sm" type="button" data-newclient>+ Client</button><button class="btn or" type="button" data-newshoot>+ Shoot</button></div></div>
    <div class="card"><div class="head"><h2>Edits due</h2><span class="tag">48h first edit · 24h per revision</span></div><div class="list" id="dueList"></div></div>
    <div class="card"><div class="head"><h2>Shoots</h2></div><div class="list" id="shootList"></div></div>
    <div class="card"><div class="head"><h2>Videos owed this month</h2></div><div class="list" id="clientList"></div></div>
  </section>
  <section id="v-cal" class="view" hidden style="display:grid;gap:14px">
    <div class="head"><h1>Calendar</h1><div style="display:flex;gap:6px"><button class="btn sm" type="button" id="wkPrev" aria-label="Previous week">‹</button><button class="btn sm" type="button" id="wkToday">This week</button><button class="btn sm" type="button" id="wkNext" aria-label="Next week">›</button></div></div>
    <div class="week" id="week"></div>
    <div class="card"><div class="head"><h2 id="dayTitle"></h2><button class="btn sm or" type="button" data-newshoot>+ Shoot</button></div><div class="list" id="dayList"></div></div>
  </section>
  <section id="v-score" class="view" hidden style="display:grid;gap:14px">
    <div class="head"><div><div class="tag">Success rate and performance</div><h1>Score</h1></div></div>
    <div id="scoreBody" style="display:grid;gap:14px"></div>
  </section>
  <section id="v-papers" class="view" hidden style="display:grid;gap:14px">
    <div class="head"><div><div class="tag">Official letters</div><h1>Papers</h1></div></div>
    <div class="card" id="ownerPend" hidden></div>
    <div class="card"><div class="head"><h2>Letters</h2></div><div class="quick" id="paperQuick" style="grid-template-columns:repeat(2,minmax(0,1fr))"></div><div class="tag" id="paperNote"></div><div class="list" id="paperList"></div></div>
    <div class="card" id="signCard" hidden></div>
  </section>
  <section id="v-team" class="view" hidden style="display:grid;gap:14px">
    <div class="head"><h1>Studio team</h1><span class="tag">Only you see this</span></div>
    <div class="card"><div class="head"><h2>Today</h2></div><div class="scroll"><table id="attTable"></table></div></div>
    <div class="card"><div class="head"><h2>John's daily reports</h2><span class="tag">Written at punch-out · backstop 20:53</span></div><div class="list" id="teamDayReports"></div></div>
    <div class="card"><div class="head"><h2>Weekly and monthly reports</h2><span class="tag">Rated out of 10</span></div><div id="teamPeriods" style="display:grid;gap:10px"></div></div>
    <div class="card"><div class="head"><h2>Latest check-ins</h2></div><div class="list" id="teamCheckins"></div></div>
    <div class="card" id="goalCard"></div>
    <div class="card"><div class="head"><h2>John's playbook</h2><span class="tag">What John knows about Founder Tales, Yontro and clients</span></div><textarea id="playbook" style="min-height:200px" aria-label="Playbook"></textarea><div><button class="btn or" type="button" id="savePlaybook">Save playbook</button></div></div>
    <div class="card"><h2>Add a team member</h2><p class="tag" style="margin:0">Share this page with them from the Share menu (Contributor access). They get their own login and John as their manager.</p></div>
  </section>
</main>
<button type="button" class="hzbtn" id="hzBtn" aria-label="Chat with John, your manager" aria-expanded="false" aria-controls="hz">J<i class="dot" id="hzDot" hidden></i><span class="lbl" id="hzLbl" hidden>John checked in</span></button>
<aside class="hz" id="hz" hidden aria-label="John, your manager">
  <div class="hzh"><div class="coach"><div class="av" aria-hidden="true">J</div><div><h2>John Smith</h2><div class="tag">Head of Production · your manager</div></div></div><button class="btn sm" type="button" id="hzClose" style="margin-left:auto;background:#222;color:#fff;border-color:#555" aria-label="Close chat">Close</button></div>
  <div class="hzb">
    <div class="seg" role="group" aria-label="What to do with John">
      <button type="button" data-mode="ask" aria-pressed="true">Ask</button><button type="button" data-mode="checkin" aria-pressed="false">Check-in</button><button type="button" data-mode="ideas" aria-pressed="false">Ideas</button><button type="button" data-mode="review" aria-pressed="false">Review</button><button type="button" data-mode="well" aria-pressed="false">How I'm doing</button>
    </div>
    <div id="modeBar"></div>
    <div class="chat" id="chat" aria-live="polite"></div>
    <form class="composer" id="chatForm"><label for="chatIn" style="position:absolute;left:-9999px">Message John</label><textarea id="chatIn" maxlength="3000" placeholder="Message John…"></textarea><button class="btn or" type="submit" id="chatSend">Send</button></form>
  </div>
</aside>
<div class="nudge" id="nudge" hidden role="status"></div>
<div class="med" id="med" hidden role="dialog" aria-modal="true" aria-label="Ten minutes of silence"><div><div class="tag">10 MINUTES OF SILENCE</div><div class="breath" aria-hidden="true"><span id="breathTxt">Breathe in</span></div><div class="medtime" id="medTime">10:00</div><p id="medHint"></p><div class="btnrow" style="justify-content:center"><button class="btn sm" type="button" id="medPause">Pause</button><button class="btn sm" type="button" id="medEnd">End</button></div></div></div>
<nav class="tabs" aria-label="Sections"><div class="in" id="tabs"></div></nav>
<div class="sheet-bg" id="sheetBg" hidden><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="sheetTitle" id="sheet"></div></div>'''
js=icon+extra_icons+helpers+"const PKG={Launch:5000,Growth:7500,Scale:10000};\nconst TARGET={calls:100,booked:4,held:2};\n"+clock+docs+assets+agreement+papers+tour+period+open(SD+"src/sreport.js").read()+open(SD+"src/studio.js").read()+open(SD+"src/speriod.js").read()
html="<title>yontro.ae · Studio</title>\n"+"\n".join(fonts)+"\n<style>\n"+css+studio_css+"\n</style>\n"+header+"\n"+views+"\n<script>\n"+js+"\n</script>\n"
open("/home/user/aura-reset-center/docs/studio-crm/yontro-studio.html","w").write(html)
print(len(html))
