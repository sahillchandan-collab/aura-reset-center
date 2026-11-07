import json,re
src=open('build.py').read()
cfg=src[:src.index("URLS=")].replace("t=open('office.html').read()","")
ns={}; exec(cfg,ns); B=ns['B']; SUG=ns['SUG']
s=open('office.html').read()
def rep(a,b,cnt=1):
    global s
    assert a in s, "MISSING: "+a[:90]
    s=s.replace(a,b,cnt)

# ---- title / accent tokens
rep("<title>__TITLE__</title>","<title>Sahill's HQ</title>")
rep("--accent:__ACCENT__; --accent-ink:__ACCENT_INK__;","--accent:var(--acc-l,#2F4B7C); --accent-ink:var(--acc-ink,#ffffff);")
s=s.replace("--accent:__ACCENT_DARK__;","--accent:var(--acc-d,#8FB0E8);")

# ---- CSS for HQ
rep(".bizbar{",""".view{display:grid;gap:18px;min-width:0}
.hqtop .logo{background:var(--ink);color:var(--bg)}
.offices{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.ocard{background:var(--surface);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:grid;grid-template-rows:auto 1fr;text-decoration:none;color:var(--ink);transition:transform .15s,box-shadow .15s}
.ocard:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.12)}
.ocard .band{background:var(--c);color:var(--ci);padding:14px 16px 12px;display:flex;justify-content:space-between;align-items:flex-start;gap:8px;position:relative;
  background-image:linear-gradient(90deg,rgba(255,255,255,.12) 1px,transparent 1px),linear-gradient(rgba(255,255,255,.12) 1px,transparent 1px);background-size:14px 14px}
.ocard .band h3{font-size:22px;line-height:1.05;color:var(--ci)}
.ocard .band .k{font-family:var(--mono);font-size:10.5px;opacity:.85;letter-spacing:.04em}
.ocard .band .pill{background:var(--surface);border-color:transparent}
.ocard .body{padding:14px 16px;display:grid;gap:10px;align-content:start}
.ocard .goal{font-size:13px;color:var(--muted)}
.staffrow{display:flex;gap:2px;align-items:flex-end;min-height:40px;flex-wrap:wrap}
.staffrow .fig{width:26px;aspect-ratio:1/1.25;position:relative}
.staffrow .fig .torso,.staffrow .fig .head,.staffrow .fig .hair{position:absolute}
.staffrow .fig .torso{left:8%;right:8%;bottom:0;height:52%;background:var(--shirt);border-radius:45% 45% 25% 25%}
.staffrow .fig .head{left:22%;right:22%;top:0;aspect-ratio:1;background:var(--skin);border-radius:50%}
.staffrow .fig .hair{left:18%;right:18%;top:-6%;height:36%;background:var(--hair);border-radius:50% 50% 30% 30%}
.staffrow .busy .fig::after{content:"";position:absolute;left:12%;right:12%;bottom:-8%;height:18%;background:var(--screen);border-radius:2px}
.nums{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-variant-numeric:tabular-nums}
.nums div{background:var(--soft);border-radius:10px;padding:6px 8px}
.nums b{display:block;font-family:var(--display);font-size:19px;line-height:1.1}
.nums span{font-size:11px;color:var(--muted)}
.nums .bad b{color:var(--red)}
.enter{font-weight:700;font-size:13.5px;color:var(--ink)}
.hqcols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;align-items:start}
@media (max-width:860px){.hqcols{grid-template-columns:1fr}}
.list{display:grid;gap:8px}
.li{display:grid;gap:3px;border:1px solid var(--line);border-radius:12px;padding:9px 11px;background:var(--surface);text-decoration:none;color:var(--ink)}
.li:hover{border-color:var(--ink)}
.li .t{font-weight:600;font-size:14px;overflow-wrap:anywhere}
.btag{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);font-size:11px;color:var(--muted)}
.btag::before{content:"";width:8px;height:8px;border-radius:2px;background:var(--c)}
.prio{display:grid;gap:6px;counter-reset:p}
.prio div{display:flex;gap:10px;align-items:baseline;font-size:14px}
.prio div::before{counter-increment:p;content:counter(p);font-family:var(--display);font-weight:800;font-size:18px;color:var(--muted);min-width:16px}
.bizbar{""")

# ---- HTML: nav + HQ view + office view wrapper
rep("""  <nav class="bizbar" aria-label="Switch business">__BIZBAR__</nav>
  <header class="top">""","""  <nav class="bizbar" aria-label="Switch business" id="bizbar"></nav>
  <div id="hqView" class="view">
    <header class="top hqtop">
      <div class="brand"><div class="logo" aria-hidden="true">S</div><div style="min-width:0"><div class="tag">SAHILL CHANDAN · DUBAI · <span id="hqDate"></span></div><h1>Sahill's HQ</h1><div class="goalline" id="hqLine">Loading your offices…</div></div></div>
      <div class="kpis"><div class="kpi"><b id="hStaff">–</b><span>staff</span></div><div class="kpi"><b id="hBusy">–</b><span>at work now</span></div><div class="kpi"><b id="hOpen">–</b><span>open tasks</span></div><div class="kpi"><b id="hLate">–</b><span>overdue</span></div></div>
    </header>
    <div class="toolbar"><button class="primary" type="button" id="briefBtn">Morning brief</button><button class="dark" type="button" id="cosBtn">Talk to Chief of Staff</button></div>
    <div id="hqBanner" class="notice" hidden></div>
    <section class="offices" id="offices" aria-label="Your businesses"></section>
    <div class="hqcols">
      <section class="panel"><div class="panel-head"><h2>Needs you</h2><span class="tag">Overdue and high priority, all offices</span></div><div class="list" id="attention"></div></section>
      <section class="panel"><div class="panel-head"><h2>Latest work handed in</h2><span class="tag">Across all offices</span></div><div class="list" id="handed"></div></section>
    </div>
    <div class="hqcols">
      <section class="panel"><div class="panel-head"><h2>Priority order</h2><span class="tag">How your time is split</span></div><div class="prio"><div><span><b>Cash already owed:</b> Botany rents and cheques</span></div><div><span><b>Revenue:</b> Yontro sales, Aura sales</span></div><div><span><b>Growth assets:</b> Founder Tales</span></div><div><span><b>Long-term bets:</b> publication, founders network, Barter</span></div></div></section>
      <section class="panel"><div class="panel-head"><h2>Briefs</h2><span class="tag">From your Chief of Staff</span></div><div class="minutes" id="briefs"></div></section>
    </div>
  </div>
  <div id="officeView" class="view" hidden>
  <header class="top">""")
rep("""<div class="logo" aria-hidden="true">__INITIAL__</div>""","""<div class="logo" aria-hidden="true" id="bizInitial"></div>""")
rep("""<div class="tag">__KIND__ · VIRTUAL OFFICE</div>
        <h1>__NAME__</h1>""","""<div class="tag"><span id="bizKind"></span> · VIRTUAL OFFICE</div>
        <h1 id="bizName"></h1>""")
rep("""<span id="goalText">__GOAL__</span>""","""<span id="goalText"></span>""")
rep("""  <nav class="switch" aria-label="More">""","""  </div>
  <nav class="switch" aria-label="More">""")
rep("""Part of Sahill's GM Board · <a""","""Sahill's HQ · <a""")
rep("""<div class="tag">__NAME__ · OFFICE MANAGER</div><h2 id="chatH">Tell the office what to do</h2>""","""<div class="tag" id="chatTag"></div><h2 id="chatH"></h2>""")
rep("""Who should join __NAME__?""","""Who should join <span id="hireBiz"></span>?""")
assert "__" not in s.split("<script>")[0].replace("__proto",""), [l for l in s.split("<script>")[0].split("\n") if "__" in l]

# ---- JS: config + prefixes
rep("const BIZ = __BIZJSON__;","""const BIZES = __BIZESJSON__;
const HQ = {name:"Sahill's HQ",accent:"#2F4B7C",ink:"#ffffff",dark:"#8FB0E8"};
let BIZ = BIZES[0], view="hq", cur=null;
const SLUGS=BIZES.map(b=>b.slug); const bizOf=s=>BIZES.find(b=>b.slug===s);
const P=()=>"biz/"+cur+"/"; const CP=()=>view==="hq"?"hq/main/":P();
const ALL={}; SLUGS.forEach(s=>ALL[s]={agents:[],tasks:[],routines:[],reports:[],memory:[],chat:[],meta:{goal:bizOf(s).goal,status:bizOf(s).status,note:bizOf(s).note}});
const HQD={chat:[],memory:[],briefs:[]};""")
rep("const ROOMS = BIZ.rooms; const WORK = ROOMS.filter(r=>r.id!==\"break\"&&r.id!==\"board\");","let ROOMS = BIZ.rooms; let WORK = ROOMS.filter(r=>r.id!==\"break\"&&r.id!==\"board\");")
s=s.replace('db.collection("chat")','db.collection(CP()+"chat")').replace('db.collection("memory")','db.collection(CP()+"memory")').replace('db.doc("memory/','db.doc(CP()+"memory/')
s=s.replace('db.collection("','db.collection(P()+"').replace('db.doc("','db.doc(P()+"')
s=s.replace('db.collection(P()+"chat")','db.collection(CP()+"chat")')

# runTask: capture prefix
rep("""  const room=taskRoom(t); const ctl=new AbortController();""","""  const room=taskRoom(t); const ctl=new AbortController(); const pre=P(); const bname=BIZ.name;""")
rep("""if(t.status==="todo"&&db) db.doc(P()+"tasks/"+id)""","""if(t.status==="todo"&&db) db.doc(pre+"tasks/"+id)""")
rep("""    await db.doc(P()+"tasks/"+id).update({output:r.text""","""    await db.doc(pre+"tasks/"+id).update({output:r.text""")
rep("""toast(`${firstName(a.name)} handed in the work. Review it, then mark it done.`);""","""toast(`${firstName(a.name)} (${bname}) handed in the work. Review it, then mark it done.`);""")
# board meeting capture
rep("""  if(meeting) return; meeting=true;""","""  if(meeting) return; meeting=true; const pre=P(), meta0={...meta};""")
rep("""await db.collection(P()+"reports").add({title:"Board meeting\"""","""await db.collection(pre+"reports").add({title:"Board meeting\"""")
rep("""await db.doc(P()+"meta/business").set({...meta,status:s,updatedAt:Date.now()});}
    toast("Meeting over.""","""await db.doc(pre+"meta/business").set({...meta0,status:s,updatedAt:Date.now()});}
    toast("Meeting over.""")
# autopilot only in office view
rep("if(autoBusy||!db||!sample||!canWrite||meeting) return;","if(view!==\"office\"||autoBusy||!db||!sample||!canWrite||meeting) return;")
# hire header uses BIZ.name ok. Idle wander guard
rep("setInterval(()=>{ // idle wandering","setInterval(()=>{ if(view!==\"office\") return; // idle wandering")
rep("let rz; new ResizeObserver(()=>{clearTimeout(rz);rz=setTimeout(()=>{const n=","let rz; new ResizeObserver(()=>{clearTimeout(rz);rz=setTimeout(()=>{if(view!==\"office\")return;const n=")

# ---- replace chat block
a=s.index("/* ---------- office chat ---------- */"); b=s.index("function renderChat(){")
CHAT=r'''/* ---------- chat: office manager (office view) or chief of staff (HQ) ---------- */
const workOf=slug=>bizOf(slug).rooms.filter(r=>r.id!=="break"&&r.id!=="board");
const deptIn=(slug,a)=>a.dept||bizOf(slug).agentDept[a.id]||workOf(slug)[0].id;
const normBiz=q=>{const s=String(q||"").toLowerCase().trim(); if(!s) return null; return SLUGS.find(x=>x===s)||BIZES.find(b=>b.name.toLowerCase().includes(s)||s.includes(b.name.toLowerCase().split(" ")[0].toLowerCase()))?.slug||null;};
const findAgentIn=(slug,q)=>{ if(!q) return null; const L=ALL[slug].agents; const s=String(q).toLowerCase().trim(); return L.find(a=>a.id===q)||L.find(a=>a.name.toLowerCase()===s)||L.find(a=>a.name.toLowerCase().split(/\s+/)[0]===s.split(/\s+/)[0])||L.find(a=>a.role.toLowerCase().includes(s)); };
const findRoomIn=(slug,q)=>{ if(!q) return null; const s=String(q).toLowerCase(); const W=workOf(slug); return W.find(r=>r.id===s)||W.find(r=>r.name.toLowerCase().includes(s)||s.includes(r.name.toLowerCase())); };
function stateOf(slug,full){
  const d=ALL[slug], b=bizOf(slug), nameOf=id=>d.agents.find(a=>a.id===id)?.name||"unassigned";
  const open=d.tasks.filter(t=>t.status!=="done");
  return `== ${b.name} [business id: ${slug}] (${b.kind})
GOAL: ${d.meta.goal||b.goal} | STATUS: ${(STATUS[d.meta.status]||STATUS.grey)[0]}${d.meta.note?" ("+d.meta.note+")":""}
${full?"ABOUT: "+b.about+"\n":""}ROOMS: ${workOf(slug).map(r=>r.id+"="+r.name).join("; ")}
STAFF: ${d.agents.map(a=>`[${a.id}] ${a.name}, ${a.role}, desk ${deptIn(slug,a)}${a.auto?", autopilot":""}${(a.rules||[]).length?", rules: "+a.rules.map(r=>r.text).join("; "):""}`).join(" | ")||"none"}
OPEN TASKS: ${open.slice(0,full?60:15).map(t=>`[${t.id}] ${t.title} (${t.status}, ${nameOf(t.agentId)}${t.due?", due "+t.due:""}${t.priority==="high"?", high":""}${t.output?", work handed in":""}${(t.feedback||[]).length?", "+t.feedback.length+" comments":""})`).join(" | ")||"none"}
${full?"ROUTINES: "+(d.routines.map(r=>`${nameOf(r.agentId)}: ${r.title} (${cadenceText(r)})`).join(" | ")||"none")+"\n":""}MEMORY: ${d.memory.slice(-(full?40:6)).map(m=>m.text).join(" / ")||"none"}`;
}
const RULES=()=>{
  const head=`Owner: Sahill Chandan, Dubai. Money in AED. Dates like "7 November 2026". Today: ${fmtDate(todayISO())} (${todayISO()}).`;
  if(view==="office") return `You are the office manager of ${BIZ.name}'s virtual office inside Sahill's HQ. You run a team of AI agents. When Sahill asks for something, act with your tools: create or update tasks and assign them to the right agent (pick by role and desk), set start=true when he wants it done now, hire agents with a person's name and a job designation, add routines for recurring work, update the goal or status, and call remember for every new fact, number, decision, preference or contact he tells you (one short sentence each). Never invent figures. Agents cannot contact people or spend money. After acting, reply in 1-4 short plain sentences saying what you did and who is on it; ask one question only if something essential is missing. When he comments on or corrects an agent's work, use give_feedback (redo=true if it should be fixed now; make_rule=true if it's how they should always work). Use tools rather than describing what you would do. The business id for every tool is "${cur}".
${head}
${stateOf(cur,true)}`;
  return `You are Sahill's Chief of Staff in Sahill's HQ, overseeing all five businesses and their AI teams. Priority rule: cash already owed first (Botany rents and cheques), then revenue (Yontro, Aura), then growth assets (Founder Tales), then long-term bets (Barter). When Sahill tells you something or asks for something, act with your tools on the right business id: create or update tasks for the right agent (start=true if he wants it now), give feedback on agents' work (redo and/or make it a standing rule), hire, add routines, set status, and call remember for every fact, number or decision (business "hq" for things that are about Sahill or all businesses). If he asks what to focus on, answer from the data below and take a position. Never invent figures. Reply in short plain sentences, naming the business and agent for each action.
${head}
HQ MEMORY: ${HQD.memory.slice(-30).map(m=>m.text).join(" / ")||"none"}
${SLUGS.map(x=>stateOf(x,false)).join("\n")}`;
};
let actLog=[], startQueue=[];
const BIZP={type:"string",description:"business id: yontro, botany, foundertales, aura or barter"};
function slugFor(i){ const s=normBiz(i.business)||(view==="office"?cur:null); if(!s) throw new Error("Say which business: yontro, botany, foundertales, aura or barter"); return s; }
const pathOf=slug=>"biz/"+slug+"/";
const chatTools=[
 {name:"create_task",description:"Create a task in a business and assign it to an agent. Returns the task id. start=true sends the agent to do it now.",
  inputSchema:{type:"object",properties:{business:BIZP,title:{type:"string"},agent:{type:"string",description:"agent id or name"},room:{type:"string",description:"room id"},due:{type:"string",description:"YYYY-MM-DD"},priority:{type:"string",enum:["high","normal","low"]},notes:{type:"string",description:"brief for the agent"},start:{type:"boolean"}},required:["title"]},
  execute:async i=>{const slug=slugFor(i); const a=findAgentIn(slug,i.agent); const room=findRoomIn(slug,i.room)?.id||(a?deptIn(slug,a):workOf(slug)[0].id); const ref=db.collection(pathOf(slug)+"tasks").doc();
   await ref.set({title:String(i.title).slice(0,200),agentId:a?.id||"",dept:room,due:/^\d{4}-\d{2}-\d{2}$/.test(i.due||"")?i.due:"",priority:["high","normal","low"].includes(i.priority)?i.priority:"normal",notes:String(i.notes||"").slice(0,3000),status:"todo",createdAt:Date.now()});
   if(i.start&&a) startQueue.push({slug,id:ref.id}); actLog.push(`${bizOf(slug).name} · Task: ${i.title} → ${a?.name||"unassigned"}${i.start&&a?" (starting)":""}`); return {id:ref.id,assignedTo:a?.name||null};}},
 {name:"update_task",description:"Change a task: status (todo, doing, done), agent, due date, priority, or start=true to send the agent to work on it now.",
  inputSchema:{type:"object",properties:{business:BIZP,task_id:{type:"string"},status:{type:"string",enum:["todo","doing","done"]},agent:{type:"string"},due:{type:"string"},priority:{type:"string",enum:["high","normal","low"]},start:{type:"boolean"}},required:["task_id"]},
  execute:async i=>{const slug=slugFor(i); const t=ALL[slug].tasks.find(x=>x.id===i.task_id); if(!t) throw new Error("No task with that id in "+slug); const u={}; if(i.status) u.status=i.status; if(i.status==="done") u.doneAt=new Date().toISOString();
   if(i.agent){const a=findAgentIn(slug,i.agent); if(!a) throw new Error("No agent called "+i.agent); u.agentId=a.id;} if(i.due) u.due=i.due; if(i.priority) u.priority=i.priority;
   if(Object.keys(u).length) await db.doc(pathOf(slug)+"tasks/"+t.id).update(u); if(i.start) startQueue.push({slug,id:t.id}); actLog.push(`${bizOf(slug).name} · Updated: ${t.title}${i.status?" → "+i.status:""}${i.start?" (starting)":""}`); return "ok";}},
 {name:"hire_agent",description:"Hire a new AI agent in a business: a person's name, a job designation, a room id for their desk, and instructions on how they work.",
  inputSchema:{type:"object",properties:{business:BIZP,name:{type:"string"},designation:{type:"string"},room:{type:"string"},instructions:{type:"string"},autopilot:{type:"boolean"}},required:["name","designation"]},
  execute:async i=>{const slug=slugFor(i); const ref=await db.collection(pathOf(slug)+"agents").add({name:String(i.name).slice(0,40),role:String(i.designation).slice(0,80),dept:findRoomIn(slug,i.room)?.id||workOf(slug)[0].id,mind:String(i.instructions||"").slice(0,2000),auto:!!i.autopilot,createdAt:Date.now()});
   actLog.push(`${bizOf(slug).name} · Hired: ${i.name}, ${i.designation}`); return {id:ref.id};}},
 {name:"update_agent",description:"Change an agent's name, designation, desk room, instructions or autopilot (true = works through their queue automatically).",
  inputSchema:{type:"object",properties:{business:BIZP,agent:{type:"string"},name:{type:"string"},designation:{type:"string"},room:{type:"string"},instructions:{type:"string"},autopilot:{type:"boolean"}},required:["agent"]},
  execute:async i=>{const slug=slugFor(i); const a=findAgentIn(slug,i.agent); if(!a) throw new Error("No agent called "+i.agent); const u={}; if(i.name) u.name=String(i.name); if(i.designation) u.role=String(i.designation); if(i.room&&findRoomIn(slug,i.room)) u.dept=findRoomIn(slug,i.room).id; if(i.instructions) u.mind=String(i.instructions); if(typeof i.autopilot==="boolean") u.auto=i.autopilot;
   await db.doc(pathOf(slug)+"agents/"+a.id).update(u); actLog.push(`${bizOf(slug).name} · Updated ${a.name}${typeof i.autopilot==="boolean"?" · autopilot "+(i.autopilot?"on":"off"):""}`); return "ok";}},
 {name:"add_routine",description:"Add a recurring job for an agent. cadence daily, weekly or monthly; day 0-6 (0 = Sunday) for weekly.",
  inputSchema:{type:"object",properties:{business:BIZP,agent:{type:"string"},title:{type:"string"},cadence:{type:"string",enum:["daily","weekly","monthly"]},day:{type:"number"},brief:{type:"string"}},required:["agent","title","cadence"]},
  execute:async i=>{const slug=slugFor(i); const a=findAgentIn(slug,i.agent); if(!a) throw new Error("No agent called "+i.agent); await db.collection(pathOf(slug)+"routines").add({agentId:a.id,title:String(i.title).slice(0,160),cadence:["daily","weekly","monthly"].includes(i.cadence)?i.cadence:"weekly",day:Math.max(0,Math.min(6,Number(i.day)||1)),brief:String(i.brief||"").slice(0,1000),createdAt:Date.now()});
   actLog.push(`${bizOf(slug).name} · Routine: ${a.name} · ${i.title}`); return "ok";}},
 {name:"set_status",description:"Update a business's goal and/or status (red, amber, green, grey, parked) with a short reason.",
  inputSchema:{type:"object",properties:{business:BIZP,status:{type:"string",enum:["red","amber","green","grey","parked"]},note:{type:"string"},goal:{type:"string"}}},
  execute:async i=>{const slug=slugFor(i); const m={...ALL[slug].meta}; if(i.status) m.status=i.status; if(i.note!==undefined) m.note=String(i.note); if(i.goal) m.goal=String(i.goal); await db.doc(pathOf(slug)+"meta/business").set({goal:m.goal,status:m.status,note:m.note||"",updatedAt:Date.now()}); actLog.push(`${bizOf(slug).name} · Status: ${(STATUS[m.status]||STATUS.grey)[0]}`); return "ok";}},
 {name:"give_feedback",description:"Comment on an agent's work on a task. redo=true sends it back to be redone following the comment now; make_rule=true also saves the comment as a standing rule the agent follows on every future job.",
  inputSchema:{type:"object",properties:{business:BIZP,task_id:{type:"string"},comment:{type:"string"},redo:{type:"boolean"},make_rule:{type:"boolean"}},required:["task_id","comment"]},
  execute:async i=>{const slug=slugFor(i); const t=ALL[slug].tasks.find(x=>x.id===i.task_id); if(!t) throw new Error("No task with that id in "+slug); const at=new Date().toISOString(); const fb=[...(t.feedback||[]),{text:String(i.comment).slice(0,2000),at}];
   await db.doc(pathOf(slug)+"tasks/"+t.id).update({feedback:fb}); const a=ALL[slug].agents.find(x=>x.id===t.agentId);
   if(i.make_rule&&a) await db.doc(pathOf(slug)+"agents/"+a.id).update({rules:[...(a.rules||[]),{text:String(i.comment).slice(0,400),at}]});
   if(i.redo&&a) startQueue.push({slug,id:t.id,ov:{feedback:fb}});
   actLog.push(`${bizOf(slug).name} · Feedback to ${a?.name||"agent"} on "${t.title}"${i.redo?" (redoing)":""}${i.make_rule?" · new standing rule":""}`); return "ok";}},
 {name:"add_rule",description:"Add a standing rule an agent must follow on every future job (how to do their work).",
  inputSchema:{type:"object",properties:{business:BIZP,agent:{type:"string"},rule:{type:"string"}},required:["agent","rule"]},
  execute:async i=>{const slug=slugFor(i); const a=findAgentIn(slug,i.agent); if(!a) throw new Error("No agent called "+i.agent); await db.doc(pathOf(slug)+"agents/"+a.id).update({rules:[...(a.rules||[]),{text:String(i.rule).slice(0,400),at:new Date().toISOString()}]}); actLog.push(`${bizOf(slug).name} · Rule for ${a.name}: ${i.rule}`); return "ok";}},
 {name:"remember",description:"Save one fact, number, decision, contact or preference Sahill told you, as one short sentence. business = a business id, or \"hq\" for things about Sahill or all businesses.",
  inputSchema:{type:"object",properties:{business:{type:"string"},fact:{type:"string"}},required:["fact"]},
  execute:async i=>{const isHq=String(i.business||"").toLowerCase()==="hq"; const slug=isHq?null:(normBiz(i.business)||(view==="office"?cur:null)); const path=slug?pathOf(slug):"hq/main/";
   await db.collection(path+"memory").add({text:String(i.fact).slice(0,600),createdAt:Date.now(),source:view==="hq"?"hq-chat":"chat"}); actLog.push(`${slug?bizOf(slug).name:"HQ"} · Remembered: ${i.fact}`); return "saved";}},
];
'''
s=s[:a]+CHAT+s[b:]

# renderChat greeting + suggestions by view
rep("""    :`<div class="msg assistant">Hi Sahill. I run the ${esc(BIZ.name)} office. Tell me what you need: I'll assign it to the right person, start the work, and remember anything you tell me.</div>`;""",
"""    :`<div class="msg assistant">${view==="hq"?"Hi Sahill. I'm your Chief of Staff across all five businesses. Tell me what's happening or what you need, and I'll put the right agent on it and remember it.":"Hi Sahill. I run the "+esc(BIZ.name)+" office. Tell me what you need: I'll assign it to the right person, start the work, and remember anything you tell me."}</div>`;""")
rep("""const sug=BIZ.suggestions||[];""","""const sug=view==="hq"?HQ_SUG:(BIZ.suggestions||[]);""")
# after chat: start queue across businesses
rep("""  const q=startQueue.slice(); startQueue=[];
  for(const id of q){ await new Promise(r=>setTimeout(r,500)); runTask(id); }""","""  const q=startQueue.slice(); startQueue=[];
  if(q.length){ const first=q[0].slug; if(view!=="office"||cur!==first){ toast(`Taking you to ${bizOf(first).name} to watch the work.`); location.hash=first; await new Promise(r=>setTimeout(r,1200)); }
    for(const it of q.filter(x=>x.slug===first)){ await new Promise(r=>setTimeout(r,500)); runTask(it.id,it.ov); }
    const rest=q.filter(x=>x.slug!==first); if(rest.length) toast(`${rest.length} more task${rest.length>1?"s":""} queued in other offices. Autopilot or the daily run picks them up.`); }""")
rep("""function openChat(){$("#chatDrawer").hidden=false;""","""function openChat(){chatHeader();$("#chatDrawer").hidden=false;""")

# ---- replace boot
a=s.index("/* ---------- boot ---------- */"); b=s.index("</script>")
BOOT=r'''/* ---------- views ---------- */
const HQ_SUG=["What should I focus on today?","Botany: a tenant paid AED 30,000 today","Ask Omar and Fatima for a status update now"];
function applyAccent(c){const r=document.documentElement.style;r.setProperty("--acc-l",c.accent);r.setProperty("--acc-d",c.dark);r.setProperty("--acc-ink",c.ink);}
function chatHeader(){ if(view==="hq"){$("#chatTag").textContent="SAHILL'S HQ · CHIEF OF STAFF";$("#chatH").textContent="Talk to your Chief of Staff";$("#chatIn").placeholder="e.g. Botany: unit 1204 bounced a AED 25,000 cheque. Get Daniel on it.";$("#openChat").lastChild.textContent="Chief of Staff";}
  else {$("#chatTag").textContent=BIZ.name.toUpperCase()+" · OFFICE MANAGER";$("#chatH").textContent="Tell the office what to do";$("#chatIn").placeholder="e.g. Ask "+(agents[0]?firstName(agents[0].name):"the team")+" to start on the top task now";$("#openChat").lastChild.textContent="Office chat";} }
function syncGlobals(){ if(view==="office"){const d=ALL[cur];agents=d.agents;tasks=d.tasks;routines=d.routines;reports=d.reports;meta=d.meta;chat=d.chat;memory=d.memory;} else {chat=HQD.chat;memory=HQD.memory;} }
function renderNav(){ $("#bizbar").innerHTML=`<a href="#hq" style="--c:var(--ink)" ${view==="hq"?'aria-current="page"':""}><span class="d" aria-hidden="true"></span>Sahill's HQ</a><span class="sep" aria-hidden="true"></span>`+BIZES.map(b=>`<a href="#${b.slug}" style="--c:${b.accent}" ${view==="office"&&cur===b.slug?'aria-current="page"':""}><span class="d" aria-hidden="true"></span>${esc(b.name)}</a>`).join(""); }
function enterOffice(slug){
  view="office"; cur=slug; BIZ=bizOf(slug); ROOMS=BIZ.rooms; WORK=ROOMS.filter(r=>r.id!=="break"&&r.id!=="board"); applyAccent(BIZ);
  for(const [,p] of pos) p.el?.remove(); pos.clear(); selection={kind:"office"}; roomFilter="all"; meeting=false; $("#callMeeting").disabled=false; $("#callMeeting").textContent="Call a board meeting";
  syncGlobals();
  $("#bizInitial").textContent=BIZ.initial; $("#bizKind").textContent=BIZ.kind.toUpperCase(); $("#bizName").textContent=BIZ.name; $("#hireBiz").textContent=BIZ.name;
  ["#taskForm","#statusForm"].forEach(x=>$(x).hidden=true); $("#hireModal").hidden=true;
  $("#hqView").hidden=true; $("#officeView").hidden=false; renderNav(); chatHeader();
  renderChips(); buildFloor(); renderAll(); renderReports(); if(!$("#chatDrawer").hidden) renderChat();
  document.title=BIZ.name+" · Sahill's HQ"; window.scrollTo(0,0);
}
function showHQ(){
  view="hq"; cur=null; applyAccent(HQ); for(const [,p] of pos) p.el?.remove(); pos.clear(); syncGlobals();
  $("#officeView").hidden=true; $("#hqView").hidden=false; $("#hireModal").hidden=true; renderNav(); chatHeader(); renderHQ(); if(!$("#chatDrawer").hidden) renderChat();
  document.title="Sahill's HQ"; window.scrollTo(0,0);
}
function route(){ const h=location.hash.slice(1); if(SLUGS.includes(h)) enterOffice(h); else showHQ(); }
window.addEventListener("hashchange",route);
function busyIn(slug,a){ return !!running.get("agent:"+a.id) || ALL[slug].tasks.some(t=>t.agentId===a.id&&t.status==="doing"); }
function renderHQ(){
  if(view!=="hq") return;
  const today=todayISO(); let staff=0,busy=0,open=0,late=0;
  $("#hqDate").textContent=fmtDate(today).toUpperCase();
  $("#offices").innerHTML=BIZES.map(b=>{const d=ALL[b.slug]; const o=d.tasks.filter(t=>t.status!=="done"); const lt=o.filter(t=>t.due&&t.due<today); const dn=d.tasks.filter(t=>t.status==="done").length; const bz=d.agents.filter(a=>busyIn(b.slug,a));
    staff+=d.agents.length; busy+=bz.length; open+=o.length; late+=lt.length;
    const [lab,cls]=STATUS[d.meta.status]||STATUS.grey; const lr=d.reports.slice().sort((x,y)=>y.createdAt-x.createdAt)[0];
    return `<a class="ocard" href="#${b.slug}" style="--c:${b.accent};--ci:${b.ink}"><div class="band"><div><div class="k">${esc(b.kind.toUpperCase())}</div><h3>${esc(b.name)}</h3></div><span class="pill ${cls}">${lab}</span></div>
    <div class="body"><div class="goal"><b style="color:var(--ink)">Goal:</b> ${esc(d.meta.goal||b.goal)}${d.meta.note?`<br><span class="tag">${esc(d.meta.note)}</span>`:""}</div>
    <div class="staffrow" aria-label="Staff">${d.agents.map(a=>`<span class="${busyIn(b.slug,a)?"busy":""}" title="${esc(a.name)} · ${esc(a.role)}">${figHTML(a)}</span>`).join("")||'<span class="tag">No staff yet</span>'}</div>
    <div class="tag">${bz.length?bz.map(a=>esc(firstName(a.name))).join(", ")+" at work":"Nobody working right now"}</div>
    <div class="nums"><div><b>${d.agents.length}</b><span>staff</span></div><div><b>${o.length}</b><span>open</span></div><div class="${lt.length?"bad":""}"><b>${lt.length}</b><span>overdue</span></div><div><b>${dn}</b><span>done</span></div></div>
    <div class="row" style="justify-content:space-between"><span class="tag">${lr?"Last meeting "+esc(fmtTime(lr.createdAt)):"No board meeting yet"}</span><span class="enter">Enter office →</span></div></div></a>`;}).join("");
  $("#hStaff").textContent=staff;$("#hBusy").textContent=busy;$("#hOpen").textContent=open;$("#hLate").textContent=late;
  const red=BIZES.filter(b=>ALL[b.slug].meta.status==="red").map(b=>b.name);
  $("#hqLine").innerHTML=`5 businesses · ${staff} AI staff · ${open} open tasks${late?` · <b style="color:var(--red)">${late} overdue</b>`:""}${red.length?` · Red: ${esc(red.join(", "))}`:""}`;
  const att=[]; BIZES.forEach(b=>ALL[b.slug].tasks.forEach(t=>{ if(t.status!=="done"&&((t.due&&t.due<today)||t.priority==="high")) att.push({b,t}); }));
  att.sort((x,y)=>String(x.t.due||"9").localeCompare(String(y.t.due||"9")));
  $("#attention").innerHTML=att.slice(0,10).map(({b,t})=>{const a=ALL[b.slug].agents.find(x=>x.id===t.agentId);const lateT=t.due&&t.due<today;return `<a class="li" href="#${b.slug}"><span class="btag" style="--c:${b.accent}">${esc(b.name)}</span><span class="t">${esc(t.title)}</span><span class="tag">${a?esc(a.name):"Unassigned"}${t.due?` · <span class="${lateT?"s-red":""}">${lateT?"overdue since ":"due "}${esc(fmtDate(t.due))}</span>`:""}${t.priority==="high"?" · high":""}</span></a>`;}).join("")||'<div class="empty">Nothing overdue or urgent. Good.</div>';
  const hw=[]; BIZES.forEach(b=>ALL[b.slug].tasks.forEach(t=>{ if(t.output&&t.outputAt) hw.push({b,t}); })); hw.sort((x,y)=>Date.parse(y.t.outputAt)-Date.parse(x.t.outputAt));
  $("#handed").innerHTML=hw.slice(0,8).map(({b,t})=>`<a class="li" href="#${b.slug}"><span class="btag" style="--c:${b.accent}">${esc(b.name)} · ${esc(t.outputBy||"")}</span><span class="t">${esc(t.title)}</span><span class="tag">${esc(fmtTime(Date.parse(t.outputAt)))} · ${esc(String(t.output).split("\n")[0].slice(0,110))}</span></a>`).join("")||'<div class="empty">No work handed in yet. Enter an office and send an agent to work, or switch on autopilot.</div>';
  $("#briefs").innerHTML=HQD.briefs.slice().sort((x,y)=>y.createdAt-x.createdAt).slice(0,8).map((r,i)=>`<details ${i===0?"open":""}><summary>${esc(fmtTime(r.createdAt))} · ${esc(r.title||"Morning brief")}</summary><div class="output">${esc(r.body)}</div></details>`).join("")||'<div class="empty">No briefs yet. Tap Morning brief for today\'s top priorities across all five businesses.</div>';
}
async function morningBrief(){
  if(!sample) return toast("Claude isn't available on this view.");
  const btn=$("#briefBtn"); btn.disabled=true; btn.textContent="Writing your brief…";
  const prompt=`You are Sahill's Chief of Staff. Write his brief for ${fmtDate(todayISO())} across all five businesses. Priority rule: cash already owed first (Botany), then revenue (Yontro, Aura), then growth (Founder Tales), then long-term bets (Barter).
HQ memory: ${HQD.memory.slice(-20).map(m=>m.text).join(" / ")||"none"}
${SLUGS.map(x=>stateOf(x,false)).join("\n")}

Format, plain text: one line verdict. Then "Top 3 today" (each: business, action, who). Then one line per business: status and the single next move. Then "Overdue" if any. Then one question for Sahill. Direct, take a position, never invent figures.`;
  try{ const r=await sample(prompt,{modelTier:"default",cache:false}); await db.collection("hq/main/briefs").add({title:"Morning brief",body:r.text,createdAt:Date.now()}); toast("Brief ready."); }
  catch(e){ toast(e?.code==="not_granted"?"Allow Claude on this page from its Permissions menu.":"Couldn't write the brief: "+(e?.message||"error")); }
  btn.disabled=false; btn.textContent="Morning brief";
}
$("#briefBtn").onclick=morningBrief; $("#cosBtn").onclick=()=>openChat();

/* ---------- boot ---------- */
renderNav(); route();
(async()=>{
  const timer=setTimeout(()=>{ if(!db){ $("#hqBanner").textContent="Couldn't reach your saved data. Open this page signed in to claude.ai."; $("#hqBanner").hidden=false; banner("Couldn't reach your saved data. Open this page signed in to claude.ai."); } },10000);
  const C=window.claude;
  const [d,s2,u]=await Promise.all([C?.use?.("db"),C?.use?.("sample"),C?.use?.("user")].map(p=>Promise.resolve(p).catch(()=>null)));
  sample=s2||null;
  if(u){ try{ if(await u.can("data.write")===false) canWrite=false; }catch{} }
  if(!d) return;
  db=d; clearTimeout(timer);
  if(!canWrite){ banner("You're visiting. Only Sahill and editors can hire, assign or send agents to work."); ["#openHire","#callMeeting","#newTaskBtn","#editStatus","#openChat","#briefBtn","#cosBtn"].forEach(x=>$(x).hidden=true); }
  else if(!sample) banner("Claude isn't available on this view, so agents can't do work here. You can still hire and assign.");
  const onErr=e=>banner("Couldn't load saved data ("+(e?.code||"error")+").");
  const docs=q=>q.docs.map(x=>({id:x.id,...x.data()}));
  const touch=(slug,what)=>{ if(view==="office"&&cur===slug){ syncGlobals(); if(what==="chat"||what==="memory"){ $("#memCount").textContent=memory.length; if(!$("#chatDrawer").hidden) renderChat(); } else if(what==="reports"){renderReports();renderSide();} else if(what==="routines"){renderSide();} else if(what==="meta"){renderMeta();} else {renderAll(); if(what==="agents"&&!$("#hireModal").hidden) renderCands();} } else if(view==="hq") renderHQ(); };
  for(const slug of SLUGS){ const p="biz/"+slug+"/", D=ALL[slug];
    db.collection(p+"agents").onSnapshot(q=>{D.agents=docs(q).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0));touch(slug,"agents");},onErr);
    db.collection(p+"tasks").onSnapshot(q=>{D.tasks=docs(q);touch(slug,"tasks");},onErr);
    db.collection(p+"routines").onSnapshot(q=>{D.routines=docs(q);touch(slug,"routines");},onErr);
    db.collection(p+"reports").onSnapshot(q=>{D.reports=docs(q);touch(slug,"reports");},onErr);
    db.collection(p+"memory").onSnapshot(q=>{D.memory=docs(q).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0));touch(slug,"memory");},onErr);
    db.collection(p+"chat").orderBy("createdAt","desc").limit(80).onSnapshot(q=>{D.chat=docs(q).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0));touch(slug,"chat");},onErr);
    db.doc(p+"meta/business").onSnapshot(x=>{if(x.exists) D.meta={...D.meta,...x.data()};touch(slug,"meta");},onErr);
  }
  db.collection("hq/main/chat").orderBy("createdAt","desc").limit(80).onSnapshot(q=>{HQD.chat=docs(q).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0));if(view==="hq"){syncGlobals();if(!$("#chatDrawer").hidden)renderChat();}},onErr);
  db.collection("hq/main/memory").onSnapshot(q=>{HQD.memory=docs(q).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0));if(view==="hq"){syncGlobals();$("#memCount").textContent=memory.length;if(!$("#chatDrawer").hidden)renderChat();}},onErr);
  db.collection("hq/main/briefs").onSnapshot(q=>{HQD.briefs=docs(q);renderHQ();},onErr);
})();
'''
s=s[:a]+BOOT+s[b:]

# memory delete in HQ path handled by CP(). Hire uses P() fine.
BZ=[]
for b in B:
    BZ.append({**{k:b[k] for k in ["slug","name","kind","goal","status","note","about","rooms","agentDept","candidates","accent","ink","dark","initial"]},"corridorY":50,"suggestions":SUG[b["slug"]]})
s=s.replace("__BIZESJSON__",json.dumps(BZ).replace("</","<\\/"))
assert "__BIZ" not in s
open("sahills-hq.html","w").write(s)
print("built", len(s))
