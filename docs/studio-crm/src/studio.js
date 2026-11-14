/* ================= YONTRO STUDIO (Azeem) ================= */
const MGR="John Smith", MGR1="John";
const STATS=[["views","Views"],["reach","Reach"],["likes","Likes"],["comments","Comments"],["shares","Shares"],["saves","Saves"],["follows","Follows"],["wtr","Watch-through %"],["avgWatch","Avg watch (s)"],["duration","Length (s)"]];
const PKGQ={Launch:5,Growth:10,Scale:15};
let db=null,user=null,sample=null,me=null,isOwner=false,viewRep=null,names={},downloads=null;
let videos=[],shoots=[],clients=[],followers=[],kpis=[],chats=[],tlog=[],playbook="",goals={ftTarget:5000,ftDate:"2027-01-15",trials:2,live:1,yontro:1};
let leads=[],acts=[]; /* used by shared modules */
let tab="today",mode="ask",session="",busy=false,vidF="ft-active",calDay=dxb(),calWeek=weekStart(dxb());
const mine=L=>L.filter(x=>x.repId===viewRep);
const STUDIO_PLAYBOOK=`FOUNDER TALES (foundertales.ae): Instagram and TikTok Reels telling inspiring founder stories, Dubai-based. Goal: 5,000 followers by mid-January 2027. Daily system: 2 new videos posted as Instagram trial reels (shown to non-followers first); next day the better performer goes live on the main feed. Curiosity hooks about famous brands ("Why Elon named it Tesla") have worked best; long outros hurt retention, keep CTAs under 3 seconds and end with a teaser for the next episode. Episodes so far include Nikola Tesla, Phil Knight, The Businessman and the Fisherman, Jan Koum, Brian Acton.
YONTRO (yontro.ae): Dubai social media marketing agency. Azeem makes 1 video a day for Yontro's own page.
CLIENT SHOOTS: packages Launch 5 videos / Growth 10 / Scale 15 a month. Shoots at the client's premises in Dubai (Sharjah, Ajman, Abu Dhabi carry a travel charge). First edit to the client within 48 hours of the shoot; each revision round within 24 hours; 2 revision rounds are included; nothing is posted without client approval.`;
const fmtShortD=iso=>iso?new Date(iso+"T12:00:00").toLocaleDateString("en-GB",{day:"numeric",month:"short"}):"";
const leftTxt=ms=>{ const m=Math.round(ms/60000); const a=Math.abs(m); const s=a>=1440?`${Math.floor(a/1440)}d ${Math.floor(a%1440/60)}h`:a>=60?`${Math.floor(a/60)}h ${a%60}m`:`${a}m`; return m<0?`${s} overdue`:`${s} left`; };
const dtStr=ms=>new Date(ms).toLocaleString("en-GB",{weekday:"short",day:"numeric",month:"short",hour:"2-digit",minute:"2-digit",timeZone:"Asia/Dubai"});
const postMs=v=>v.postAt?new Date(v.postAt+":00+04:00").getTime():0;
const dOf=ms=>ms?dxb(new Date(ms)):"";
function leadInfo(name){ const c=clients.find(x=>x.name.toLowerCase()===String(name||"").toLowerCase()); return c?`Client ${c.name}, ${c.package||""} package, contact ${c.contact||"?"}.`:"No client record."; }
function renderDocsPanel(){}
function segVal(id){ return $(id)?.querySelector('[aria-pressed="true"]')?.dataset.v||""; }
function closeSheet(){ $("#sheetBg").hidden=true; $("#sheet").classList.remove("wide"); }

/* ---------- shoot deadlines ---------- */
function shootDeadline(s){ if(s.status==="shot") return s.dueAt||0; if(s.status==="revisions"){ const r=(s.revisions||[]).slice(-1)[0]; return r&&!r.doneAt?r.dueAt:0; } return 0; }
function shootOnTime(s){ const out=[]; if(s.sentAt&&s.dueAt) out.push(s.sentAt<=s.dueAt); (s.revisions||[]).forEach(r=>{ if(r.doneAt) out.push(r.doneAt<=r.dueAt); }); return out; }
const SST={scheduled:["Scheduled",""],shot:["Editing · first draft due","st-proposal"],review:["With client for approval","st-meeting"],revisions:["Revision due","st-proposal"],approved:["Approved","st-won"],delivered:["Delivered","st-won"],cancelled:["Cancelled","st-lost"]};
const VST={idea:["Idea",""],editing:["Editing","st-proposal"],trial:["Trial reel","st-meeting"],live:["Live","st-won"],dropped:["Dropped",""],done:["Done","st-won"]};

/* ---------- day metrics & score ---------- */
/* working days are Mon-Sat: "tomorrow" after Saturday is Monday, "yesterday" on Monday is Saturday */
const isSun=d=>new Date(d+"T12:00:00Z").getUTCDay()===0;
const nextWork=d=>{ let x=addDays(d,1); if(isSun(x)) x=addDays(x,1); return x; };
const prevWork=d=>{ let x=addDays(d,-1); if(isSun(x)) x=addDays(x,-1); return x; };
const PLANNED=["idea","editing"];
function dayStats(rep,date){ const V=videos.filter(v=>v.repId===rep), S=shoots.filter(s=>s.repId===rep);
  const trials=V.filter(v=>v.brand==="ft"&&v.trialDate===date&&["trial","live","dropped"].includes(v.status));
  const live=V.filter(v=>v.brand==="ft"&&v.status==="live"&&dOf(v.postedAt)===date);
  const yontro=V.filter(v=>v.brand==="yontro"&&v.status==="done"&&v.doneDate===date);
  const y=prevWork(date); const needStats=V.filter(v=>v.brand==="ft"&&(v.trialDate===y||dOf(v.postedAt)===y)&&!v.statsAt);
  const ideasTom=V.filter(v=>v.brand==="ft"&&PLANNED.includes(v.status)&&v.planFor===nextWork(date));
  const ideasSched=ideasTom.filter(v=>v.postAt);
  const dEnd=new Date(date+"T23:59:59+04:00").getTime(), dStart=new Date(date+"T00:00:00+04:00").getTime();
  let met=0,missed=0; S.forEach(s=>{ const chk=[]; if(s.dueAt&&s.dueAt>=dStart&&s.dueAt<=dEnd) chk.push(s.sentAt?s.sentAt<=s.dueAt:Date.now()<s.dueAt?null:false); (s.revisions||[]).forEach(r=>{ if(r.dueAt>=dStart&&r.dueAt<=dEnd) chk.push(r.doneAt?r.doneAt<=r.dueAt:Date.now()<r.dueAt?null:false); }); chk.forEach(c=>{ if(c===true) met++; if(c===false) missed++; }); });
  const delivered=S.filter(s=>dOf(s.deliveredAt)===date).reduce((a,s)=>a+(+s.delivered||+s.videos||0),0);
  const shotToday=S.filter(s=>dOf(s.shotAt)===date).length;
  const fl=followers.find(f=>f.date===date), fy=followers.filter(f=>f.date<date).sort((a,b)=>b.date.localeCompare(a.date))[0];
  const gained=fl&&fy?fl.followers-fy.followers:null;
  const fb=fl||fy; const need=fb?Math.max(0,Math.ceil((goals.ftTarget-fb.followers)/Math.max(1,Math.round((new Date(goals.ftDate+"T12:00:00")-new Date(date+"T12:00:00"))/864e5)))):null;
  const ci=kpis.find(k=>k.repId===rep&&k.date===date); const st=shiftState(rep,date);
  const out=Math.min(trials.length,goals.trials)/goals.trials*0.5+Math.min(live.length,goals.live)/goals.live*0.3+Math.min(yontro.length,goals.yontro)/goals.yontro*0.2;
  const ontime=met+missed?met/(met+missed):1;
  const growth=gained==null?0:need?Math.max(0,Math.min(1,gained/need)):1;
  const disc=(ci?0.5:0)+(needStats.length?0:0.5);
  const score=Math.round(100*(0.4*out+0.3*ontime+0.2*growth+0.1*disc));
  return {date,trials:trials.length,trialList:trials.map(v=>({title:v.title,hook:v.hook,stats:v.stats||null})),live:live.length,liveList:live.map(v=>v.title),yontro:yontro.length,needStats:needStats.length,ideasTom:ideasTom.length,ideasSched:ideasSched.length,
    editsMet:met,editsMissed:missed,delivered,shotToday,followers:fl?.followers??null,gained,needPerDay:need,checkin:!!ci,blockers:ci?.blockers||"",
    punchIn:st.inAt?hm(st.inAt):null,punchOut:st.outAt?hm(st.outAt):null,worked:st.inAt?dur(st.worked):null,breaks:st.inAt?dur(st.breakMs):null,late:st.inAt?(new Date(st.inAt).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",hour12:false,timeZone:"Asia/Dubai"})>"10:15"):false,
    parts:{output:Math.round(out*100),ontime:Math.round(ontime*100),growth:Math.round(growth*100),discipline:Math.round(disc*100)},score}; }
function vScore(v){ const s=v.stats||{}; return (+s.follows||0)*40+(+s.shares||0)*8+(+s.saves||0)*5+(+s.views||0)*0.05+(+s.wtr||0)*3+(+s.comments||0)*2+(+s.likes||0)*0.5; }
function studioContext(){ const t=dxb(), d=dayStats(viewRep,t), y=dayStats(viewRep,prevWork(t));
  const top=mine(videos).filter(v=>v.brand==="ft"&&v.stats).sort((a,b)=>vScore(b)-vScore(a)).slice(0,6).map(v=>`"${v.title}" hook: ${v.hook||"?"}; ${v.stats.views||0} views, ${v.stats.follows||0} follows, ${v.stats.shares||0} shares, WTR ${v.stats.wtr||"?"}%`).join(" | ");
  const due=mine(shoots).filter(s=>shootDeadline(s)).map(s=>`${s.client}: ${SST[s.status][0]} ${leftTxt(shootDeadline(s)-Date.now())}`).join("; ");
  const up=mine(shoots).filter(s=>s.status==="scheduled"&&s.date>=t).slice(0,5).map(s=>`${s.client} ${s.date} ${s.time||""} at ${s.location||"?"}`).join("; ");
  return `PERSON: ${names[viewRep]||"Azeem"}, videographer. Today ${t}.
TODAY SO FAR: ${d.trials}/${goals.trials} Founder Tales trial reels, ${d.live}/${goals.live} posted live, ${d.yontro}/${goals.yontro} Yontro video, ${d.needStats} videos still missing stats, ${d.ideasTom} ideas planned for tomorrow (${d.ideasSched} with post times), followers ${d.followers??"not logged"}${d.gained!=null?` (${d.gained>=0?"+":""}${d.gained} vs yesterday, need ${d.needPerDay}/day for ${goals.ftTarget} by ${goals.ftDate})`:""}.
YESTERDAY: ${y.trials} trials, ${y.live} live, ${y.yontro} Yontro, score ${y.score}/100.
TOP FOUNDER TALES VIDEOS: ${top||"no stats yet"}
CLIENT EDITS DUE: ${due||"none"}
UPCOMING SHOOTS: ${up||"none"}`; }
const repContext=studioContext;

/* ---------- render ---------- */
function renderWho(){ if(isOwner){ const reps=[...new Set([...videos,...shoots,...kpis,...tlog].map(x=>x.repId).filter(Boolean))];
  $("#who").innerHTML=reps.length?`Viewing <select id="repPick" aria-label="Whose work">${reps.map(r=>`<option value="${esc(r)}" ${r===viewRep?"selected":""}>${esc(names[r]||"Videographer")}${r===me?" (you)":""}</option>`).join("")}</select>`:`<span>Owner view</span>`; } else $("#who").textContent=names[me]||""; }
function renderTabs(){ const pn=isOwner?ownerPending().length:0;
  const T=[["today","Today",ICON.today],["content","Content",ICON.play],["clients","Clients",ICON.cam],["cal","Calendar",ICON.cal],["score","Score",ICON.team],["papers","Papers",ICON.contract],...(isOwner?[["team","Team",ICON.lead]]:[])];
  $("#tabs").innerHTML=T.map(([k,l,i])=>`<button type="button" data-tab="${k}" ${tab===k?'aria-current="page"':""}>${i}<span>${l}${k==="papers"&&pn?` (${pn})`:""}</span></button>`).join("");
  document.querySelectorAll(".view").forEach(v=>v.hidden=v.id!=="v-"+tab); }
function renderAll(){ ownerSubs(); renderWho(); renderTabs(); if(tab==="today") renderToday(); if(tab==="content") renderContent(); if(tab==="clients") renderClients(); if(tab==="cal") renderCal(); if(tab==="score") renderScore(); if(tab==="team") renderTeam(); if(tab==="papers"&&!document.activeElement?.closest?.("#v-papers form")) renderPapers(); if(hzOpen) renderChat(); }
function ckItem(done,title,sub,btn,urgent){ return `<div class="item ${done?"done":""} ${urgent&&!done?"late":""}"><span class="ic" style="${done?"background:var(--green);color:#fff":""}">${done?"✓":"•"}</span><div style="min-width:0"><div class="t">${title}</div>${sub?`<div class="s">${sub}</div>`:""}</div>${btn||"<span></span>"}</div>`; }
function renderToday(){ const t=dxb(), y=prevWork(t), d=dayStats(viewRep,t), first=(names[viewRep]||"").split(" ")[0];
  $("#todayDate").textContent=fmtLong(t).toUpperCase(); $("#hello").textContent=first?`Good ${new Date().toLocaleString("en-GB",{hour:"2-digit",hour12:false,timeZone:"Asia/Dubai"})<"12"?"morning":"day"}, ${first}`:"Today";
  renderShift(); renderMorning();
  const tile=(v,tg,l)=>`<div class="kpi"><b>${v}${tg?`<small> / ${tg}</small>`:""}</b><span>${l}</span>${tg?`<div class="bar"><i class="${v>=tg?"ok":""}" style="width:${Math.min(100,v/tg*100)}%"></i></div>`:""}</div>`;
  $("#kpis").innerHTML=tile(d.trials,goals.trials,"Trial reels today")+tile(d.live,goals.live,"Posted live")+tile(d.yontro,goals.yontro,"Yontro video")+`<div class="kpi"><b>${d.score}<small>/100</small></b><span>Today's score</span><div class="bar"><i class="${d.score>=80?"ok":""}" style="width:${d.score}%"></i></div></div>`;
  const yTrials=mine(videos).filter(v=>v.brand==="ft"&&v.trialDate===y&&v.status==="trial");
  const dues=mine(shoots).filter(s=>shootDeadline(s)).sort((a,b)=>shootDeadline(a)-shootDeadline(b));
  const todayShoots=mine(shoots).filter(s=>s.date===t&&s.status==="scheduled");
  const planToday=mine(videos).filter(v=>v.brand==="ft"&&PLANNED.includes(v.status)&&v.planFor===t);
  const items=[
    ckItem(d.live>=goals.live,"Post yesterday's best trial reel live",d.live?esc(mine(videos).filter(v=>v.status==="live"&&dOf(v.postedAt)===t).map(v=>v.title).join(", ")):yTrials.length?`${yTrials.length} trial reels from yesterday to compare`:"No trial reels from yesterday",d.live?"":`<button class="btn sm or" type="button" data-compare>Pick winner</button>`,true),
    ckItem(d.needStats===0,goals.metricool?"Paste the Instagram link on yesterday's reels":"Record stats for yesterday's videos",d.needStats?(goals.metricool?`${d.needStats} still missing stats. Metricool fills them in at 08:13 and 20:13 once the reel's Instagram link is on the video.`:`${d.needStats} video${d.needStats>1?"s":""} still missing views, follows, shares, watch-through`):"All stats in",d.needStats?`<button class="btn sm" type="button" data-gostats>${goals.metricool?"Open":"Add stats"}</button>`:""),
    ckItem(d.followers!=null,goals.metricool?"Founder Tales followers (synced from Metricool)":"Log today's Founder Tales followers",d.followers!=null?`${d.followers.toLocaleString()}${d.gained!=null?` · ${d.gained>=0?"+":""}${d.gained} today`:""}`:"Takes 10 seconds",d.followers==null?`<button class="btn sm" type="button" data-followers>Log</button>`:""),
    ...(planToday.length?[ckItem(false,"Today's plan (made "+(isSun(addDays(t,-1))?"Saturday":"yesterday")+")",planToday.map(v=>`<button type="button" class="btn ghost sm" data-vid="${esc(v.id)}" style="padding:2px 8px;margin:2px 4px 2px 0">${esc(v.title)}${v.postAt?" · "+esc(v.postAt.slice(11,16)):""}</button>`).join(""),"")]:[]),
    ckItem(d.trials>=goals.trials,`Make ${goals.trials} Founder Tales trial reels`,`${d.trials} of ${goals.trials} done`,d.trials<goals.trials?`<button class="btn sm or" type="button" data-newvid="ft-trial">+ Trial reel</button>`:""),
    ckItem(d.yontro>=goals.yontro,"Make today's Yontro.ae video",`${d.yontro} of ${goals.yontro} done`,d.yontro<goals.yontro?`<button class="btn sm" type="button" data-newvid="yontro">+ Yontro video</button>`:""),
    ...todayShoots.map(s=>ckItem(false,`Shoot: ${esc(s.client)}${s.time?" · "+esc(s.time):""}`,esc(s.location||""),`<button class="btn sm blue" type="button" data-shoot="${esc(s.id)}">Open</button>`)),
    ...dues.map(s=>{ const ms=shootDeadline(s)-Date.now(); return ckItem(false,`${s.status==="revisions"?"Revision":"First edit"}: ${esc(s.client)}`,`<span class="due ${ms<0?"over":ms<12*3600e3?"soon":""}">${leftTxt(ms)}</span> · due ${esc(dtStr(shootDeadline(s)))}`,`<button class="btn sm" type="button" data-shoot="${esc(s.id)}">Open</button>`,ms<0); }),
    ckItem(d.ideasTom>=goals.trials&&d.ideasSched>=goals.trials,`Plan ${isSun(addDays(t,1))?"Monday":"tomorrow"}: ${goals.trials} ideas with post times`,`${d.ideasTom} ideas · ${d.ideasSched} scheduled${d.ideasTom?": "+esc(mine(videos).filter(v=>v.brand==="ft"&&PLANNED.includes(v.status)&&v.planFor===nextWork(t)).map(v=>v.title).join(", ")):""}`,`<span class="btnrow"><button class="btn sm" type="button" data-newvid="ft-idea">+ Idea</button><button class="btn sm dark" type="button" data-hzopen="ideas">Ask ${MGR1}</button></span>`),
    ckItem(d.checkin,`Daily check-in with ${MGR1}`,d.checkin?"Done":"2 minutes, before you punch out",d.checkin?"":`<button class="btn sm or" type="button" data-go="checkin">Start</button>`)];
  const done=items.filter(x=>x.includes('item done')).length; $("#ckCount").textContent=`${done} of ${items.length} done`;
  $("#checklist").innerHTML=items.join("");
  $("#quick").innerHTML=[["ft-trial",ICON.play,"Trial reel"],["ft-idea",ICON.idea,"FT idea"],["yontro",ICON.cam,"Yontro video"],["shoot",ICON.cal,"Shoot"],["followers",ICON.team,"Followers"],["client",ICON.lead,"Client"]].map(([k,i,l])=>`<button type="button" ${k==="shoot"?"data-newshoot":k==="followers"?"data-followers":k==="client"?"data-newclient":`data-newvid="${k}"`}>${i}${l}</button>`).join("");
  renderWell(); renderDayReport(); renderPeriodCard(); }
function renderMorning(){ const el=$("#morningCard"); const y=prevWork(dxb()); const rep=(DR[viewRep]||[]).find(r=>r.date===y)||(DR[viewRep]||[]).slice().sort((a,b)=>b.date.localeCompare(a.date))[0];
  const ys=dayStats(viewRep,y); const mm=viewRep===me?(well.morning||MOTIV[dayNo()%MOTIV.length]):"";
  el.innerHTML=`<div class="coach"><div class="av" aria-hidden="true">J</div><div style="flex:1;min-width:0"><h2>Morning brief</h2><div class="tag">${MGR}, Head of Production</div></div></div>
  ${mm?`<div style="font-size:15px">${esc(mm)}</div>`:""}
  <div class="tag" style="margin-top:2px">YESTERDAY</div><div class="minis"><span><b>${ys.trials}/${goals.trials}</b> trials</span><span><b>${ys.live}/${goals.live}</b> live</span><span><b>${ys.yontro}/${goals.yontro}</b> Yontro</span><span><b>${ys.editsMet}</b> edits on time${ys.editsMissed?` · <b style="color:var(--red)">${ys.editsMissed}</b> late`:""}</span><span><b>${ys.score}</b>/100</span></div>
  ${rep?`<div style="font-size:14px">${esc(rep.verdict||"")}</div><div><button class="btn sm or" type="button" data-dropen="${esc(rep.repId)}|${esc(rep.date)}">Read ${MGR1}'s report on ${esc(rep.date===y?"yesterday":fmtD(rep.date))}</button></div>`:`<div class="tag">${MGR1}'s report appears here after your first full day.</div>`}`; }
function vidRow(v){ const st=VST[v.status]||["",""]; const s=v.stats; const sub=[v.brand==="ft"?"Founder Tales":"Yontro.ae",v.trialDate?`trial ${fmtShortD(v.trialDate)}`:"",v.postedAt?`live ${fmtShortD(dOf(v.postedAt))}`:"",v.postAt&&!v.postedAt?`post ${dtStr(postMs(v))}`:"",v.planFor&&v.status==="idea"?`for ${fmtShortD(v.planFor)}`:""].filter(Boolean).join(" · ");
  const stat=s?`<div class="vstat">${s.views!=null&&s.views!==""?`<span>${(+s.views).toLocaleString()} views</span>`:""}${s.follows?`<span>+${s.follows} follows</span>`:""}${s.shares?`<span>${s.shares} shares</span>`:""}${s.wtr?`<span>${s.wtr}% watched</span>`:""}</div>`:(["trial","live"].includes(v.status)?`<div class="vstat"><span style="color:var(--red)">No stats yet</span></div>`:"");
  return `<button type="button" class="item" style="text-align:left;width:100%;cursor:pointer" data-vid="${esc(v.id)}"><span class="ic">${v.status==="idea"?ICON.idea:ICON.play}</span><div style="min-width:0"><div class="t">${esc(v.title||"Untitled")}</div><div class="s">${esc(sub)}</div>${stat}</div><span class="stage ${st[1]}">${st[0]}</span></button>`; }
function renderContent(){ const t=dxb(), V=mine(videos);
  const fl=followers.slice().sort((a,b)=>b.date.localeCompare(a.date)); const cur=fl[0]; const wk=fl.find(f=>f.date<=addDays(t,-7));
  const daysLeft=Math.max(1,Math.round((new Date(goals.ftDate+"T12:00:00")-new Date(t+"T12:00:00"))/864e5)); const need=cur?Math.ceil(Math.max(0,goals.ftTarget-cur.followers)/daysLeft):null;
  $("#ftFollow").innerHTML=`<div class="head"><h2>Founder Tales followers</h2><button class="btn sm" type="button" data-followers>Log today</button></div>
   ${cur?`<div class="kpis" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div class="kpi"><b>${cur.followers.toLocaleString()}</b><span>on ${esc(fmtShortD(cur.date))}</span></div><div class="kpi"><b>${wk?((cur.followers-wk.followers>=0?"+":"")+(cur.followers-wk.followers)):"–"}</b><span>last 7 days</span></div><div class="kpi"><b>${need}</b><span>needed a day</span></div></div>
   <div class="bar" style="height:10px"><i style="width:${Math.min(100,cur.followers/goals.ftTarget*100)}%"></i></div><div class="tag">Goal ${goals.ftTarget.toLocaleString()} by ${esc(fmtShort(goals.ftDate))} · ${daysLeft} days left</div>`:`<div class="empty">Log the follower count every day so we can see what each video brings.</div>`}`;
  const yt=V.filter(v=>v.brand==="ft"&&v.trialDate===prevWork(t)&&["trial","live","dropped"].includes(v.status));
  $("#ftCompare").hidden=!yt.length; if(yt.length) $("#ftCompare").innerHTML=compareHTML(yt);
  const F={"ft-active":["Founder Tales",v=>v.brand==="ft"&&!["dropped"].includes(v.status)],"ideas":["Ideas",v=>v.status==="idea"],"live":["Live",v=>v.status==="live"],"yontro":["Yontro.ae",v=>v.brand==="yontro"],"dropped":["Dropped",v=>v.status==="dropped"],"best":["Best performers",v=>!!v.stats]};
  $("#vidChips").innerHTML=Object.entries(F).map(([k,[l]])=>`<button type="button" class="chip" data-vf="${k}" aria-pressed="${vidF===k}">${l}</button>`).join("");
  let L=V.filter(F[vidF][1]); L=vidF==="best"?L.sort((a,b)=>vScore(b)-vScore(a)).slice(0,15):L.sort((a,b)=>(b.updatedAt||b.createdAt||0)-(a.updatedAt||a.createdAt||0));
  $("#vidList").innerHTML=L.map(vidRow).join("")||`<div class="empty">Nothing here yet.</div>`;
  const hooks=V.filter(v=>v.brand==="ft"&&v.stats&&v.hook).sort((a,b)=>vScore(b)-vScore(a)).slice(0,8);
  $("#hookLib").innerHTML=hooks.length?hooks.map(v=>`<div class="item"><span class="ic">${ICON.idea}</span><div style="min-width:0"><div class="t">“${esc(v.hook)}”</div><div class="s">${esc(v.title)} · ${(+v.stats.views||0).toLocaleString()} views · +${+v.stats.follows||0} follows · ${v.stats.wtr||"?"}% watched</div></div><span></span></div>`).join(""):`<div class="empty">Your best hooks collect here once videos have stats.</div>`; }
function compareHTML(L){ const best=L.slice().sort((a,b)=>vScore(b)-vScore(a))[0]; const has=L.some(v=>v.stats);
  return `<div class="head"><h2>Yesterday's trial reels</h2><span class="tag">${has?"Winner by follows, shares, saves, watch-through":"Add stats to pick the winner"}</span></div>
  <div class="cmp">${L.map(v=>{ const s=v.stats||{}; const win=has&&v===best; return `<div class="cmpc ${win?"win":""}">${win?`<div class="stage st-won" style="justify-self:start">Winner</div>`:""}<b>${esc(v.title)}</b><div class="tag">${esc(v.hook||"")}</div>${STATS.slice(0,8).map(([k,l])=>`<div class="cmpr"><span>${l}</span><b>${s[k]??"–"}</b></div>`).join("")}
   <div class="btnrow">${v.status==="trial"?`<button class="btn sm ${win?"or":""}" type="button" data-golive="${esc(v.id)}">Post live</button>`:`<span class="stage ${VST[v.status][1]}">${VST[v.status][0]}</span>`}<button class="btn sm ghost" type="button" data-stats="${esc(v.id)}">Stats</button></div></div>`; }).join("")}</div>`; }
function renderClients(){ const now=Date.now(); const S=mine(shoots);
  const dues=S.filter(s=>shootDeadline(s)).sort((a,b)=>shootDeadline(a)-shootDeadline(b));
  $("#dueList").innerHTML=dues.map(s=>{ const ms=shootDeadline(s)-now; return `<button type="button" class="item ${ms<0?"late":""}" style="text-align:left;width:100%;cursor:pointer" data-shoot="${esc(s.id)}"><span class="ic">${ICON.cam}</span><div style="min-width:0"><div class="t">${esc(s.client)} · ${s.status==="revisions"?`revision ${(s.revisions||[]).length}`:"first edit"}</div><div class="s">due ${esc(dtStr(shootDeadline(s)))}</div></div><span class="due ${ms<0?"over":ms<12*3600e3?"soon":""}">${leftTxt(ms)}</span></button>`; }).join("")||`<div class="empty">No edits due. When you mark a shoot as shot, the 48-hour clock starts here.</div>`;
  const up=S.filter(s=>["scheduled"].includes(s.status)).sort((a,b)=>(a.date+(a.time||"")).localeCompare(b.date+(b.time||"")));
  const other=S.filter(s=>["review","approved"].includes(s.status));
  $("#shootList").innerHTML=[...up,...other].map(s=>`<button type="button" class="item" style="text-align:left;width:100%;cursor:pointer" data-shoot="${esc(s.id)}"><span class="ic">${ICON.cal}</span><div style="min-width:0"><div class="t">${esc(s.client)}</div><div class="s">${esc(fmtD(s.date))}${s.time?" · "+esc(s.time):""}${s.location?" · "+esc(s.location):""} · ${+s.videos||0} videos</div></div><span class="stage ${SST[s.status][1]}">${SST[s.status][0]}</span></button>`).join("")||`<div class="empty">No shoots booked.</div>`;
  const m=dxb().slice(0,7);
  $("#clientList").innerHTML=clients.slice().sort((a,b)=>a.name.localeCompare(b.name)).map(c=>{ const q=+c.quota||PKGQ[c.package]||0; const del=shoots.filter(s=>s.clientId===c.id&&dOf(s.deliveredAt).startsWith(m)).reduce((a,s)=>a+(+s.delivered||+s.videos||0),0);
    return `<button type="button" class="item" style="text-align:left;width:100%;cursor:pointer" data-client="${esc(c.id)}"><span class="ic">${ICON.lead}</span><div style="min-width:0"><div class="t">${esc(c.name)}</div><div class="s">${esc(c.package||"")} · ${del} of ${q} videos delivered this month</div><div class="bar" style="margin-top:4px"><i class="${del>=q?"ok":""}" style="width:${q?Math.min(100,del/q*100):0}%"></i></div></div><span class="stage">${q-del>0?q-del+" to go":"Done"}</span></button>`; }).join("")||`<div class="empty">Add Yontro's clients here with their package. The CRM tracks videos owed each month.</div>`; }
function renderCal(){ const t=dxb(); const days=[...Array(7)].map((_,i)=>addDays(calWeek,i));
  const ev=d=>{ const L=[]; mine(shoots).forEach(s=>{ if(s.date===d&&s.status!=="cancelled") L.push({at:s.time||"",t:`Shoot · ${s.client}`,s:s.location||"",k:"shoot",id:s.id}); const dl=shootDeadline(s); if(dl&&dOf(dl)===d) L.push({at:new Date(dl).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",timeZone:"Asia/Dubai"}),t:`Edit due · ${s.client}`,s:SST[s.status][0],k:"shoot",id:s.id,late:dl<Date.now()}); });
    mine(videos).forEach(v=>{ if(v.postAt&&v.postAt.slice(0,10)===d&&!v.postedAt) L.push({at:v.postAt.slice(11,16),t:`Post · ${v.title}`,s:v.brand==="ft"?"Founder Tales":"Yontro.ae",k:"vid",id:v.id}); if(v.trialDate===d) L.push({at:"",t:`Trial reel · ${v.title}`,s:VST[v.status][0],k:"vid",id:v.id}); });
    return L.sort((a,b)=>(a.at||"99").localeCompare(b.at||"99")); };
  $("#week").innerHTML=days.map(d=>{ const n=ev(d).length; return `<button type="button" class="day ${d===t?"today":""}" data-day="${d}" aria-pressed="${d===calDay}">${new Date(d+"T12:00:00").toLocaleDateString("en-GB",{weekday:"short"})}<b>${+d.slice(8)}</b><span class="dots">${"<i></i>".repeat(Math.min(n,4))}</span></button>`; }).join("");
  $("#dayTitle").textContent=fmtLong(calDay);
  $("#dayList").innerHTML=ev(calDay).map(e=>`<button type="button" class="item ${e.late?"late":""}" style="text-align:left;width:100%;cursor:pointer" ${e.k==="shoot"?`data-shoot="${esc(e.id)}"`:`data-vid="${esc(e.id)}"`}><span class="ic">${e.k==="shoot"?ICON.cam:ICON.play}</span><div style="min-width:0"><div class="t">${esc(e.t)}</div><div class="s">${esc([e.at,e.s].filter(Boolean).join(" · "))}</div></div><span></span></button>`).join("")||`<div class="empty">Nothing on this day.</div>`; }
function weekScore(rep,ws){ const t=dxb(); const days=[...Array(6)].map((_,i)=>addDays(ws,i)).filter(d=>d<=t); const S=days.map(d=>dayStats(rep,d)).filter(x=>tlog.some(e=>e.repId===rep&&e.date===x.date&&e.kind==="punch_in")||x.trials||x.yontro);
  const avg=k=>S.length?Math.round(S.reduce((a,x)=>a+(k?x.parts[k]:x.score),0)/S.length):0;
  return {days:S.length,score:avg(),output:avg("output"),ontime:avg("ontime"),growth:avg("growth"),discipline:avg("discipline"),trials:S.reduce((a,x)=>a+x.trials,0),live:S.reduce((a,x)=>a+x.live,0),yontro:S.reduce((a,x)=>a+x.yontro,0),met:S.reduce((a,x)=>a+x.editsMet,0),missed:S.reduce((a,x)=>a+x.editsMissed,0),gained:S.reduce((a,x)=>a+(x.gained||0),0)}; }
function renderScore(){ const t=dxb(), ws=weekStart(t); const W=weekScore(viewRep,ws); const weeks=[3,2,1,0].map(i=>({ws:addDays(ws,-7*i),...weekScore(viewRep,addDays(ws,-7*i))}));
  const V=mine(videos); const live30=V.filter(v=>v.status==="live"&&v.stats&&Date.now()-(v.postedAt||0)<30*864e5); const avgW=live30.length?Math.round(live30.reduce((a,v)=>a+(+v.stats.wtr||0),0)/live30.length):null;
  const tri30=V.filter(v=>v.brand==="ft"&&v.trialDate&&Date.now()-new Date(v.trialDate+"T12:00:00")<30*864e5&&["trial","live","dropped"].includes(v.status)); const hit=tri30.length?Math.round(V.filter(v=>v.status==="live"&&Date.now()-(v.postedAt||0)<30*864e5).length/tri30.length*100):null;
  const S30=mine(shoots).filter(s=>Date.now()-(s.shotAt||0)<30*864e5&&s.shotAt); const ot=S30.flatMap(shootOnTime); const otr=ot.length?Math.round(ot.filter(Boolean).length/ot.length*100):null;
  const ap=S30.filter(s=>["approved","delivered"].includes(s.status)); const fpa=ap.length?Math.round(ap.filter(s=>!(s.revisions||[]).length).length/ap.length*100):null;
  const tile=(v,l,sub)=>`<div class="kpi"><b>${v??"–"}</b><span>${l}</span>${sub?`<span class="tag">${sub}</span>`:""}</div>`;
  $("#scoreBody").innerHTML=`<div class="card"><div class="head"><h2>This week's success score</h2><span class="tag">${W.days} working day${W.days===1?"":"s"}</span></div>
   <div class="bigscore"><b>${W.score}</b><span>/100</span></div>
   <div class="parts">${[["Founder Tales output",W.output,"40%"],["Client edits on time",W.ontime,"30%"],["Follower growth vs goal",W.growth,"20%"],["Check-ins and stats logged",W.discipline,"10%"]].map(([l,v,w])=>`<div><div class="head"><span>${l} <span class="tag">${w}</span></span><b>${v}</b></div><div class="bar"><i class="${v>=80?"ok":""}" style="width:${v}%"></i></div></div>`).join("")}</div></div>
  <div class="card"><div class="head"><h2>Last 4 weeks</h2></div><div class="wkbars">${weeks.map(w=>`<div><div class="wkb"><i style="height:${w.score}%"></i></div><b>${w.score}</b><span class="tag">${esc(fmtShortD(w.ws))}</span></div>`).join("")}</div></div>
  <div class="kpis">${tile(W.trials,"Trial reels this week",`target ${goals.trials*6}`)}${tile(W.live,"Posted live",`target ${goals.live*6}`)}${tile(W.yontro,"Yontro videos",`target ${goals.yontro*6}`)}${tile((W.gained>=0?"+":"")+W.gained,"Followers gained")}</div>
  <div class="kpis">${tile(avgW!=null?avgW+"%":null,"Avg watch-through","live videos, 30 days")}${tile(hit!=null?hit+"%":null,"Trial → live rate","30 days")}${tile(otr!=null?otr+"%":null,"Client edits on time","30 days")}${tile(fpa!=null?fpa+"%":null,"Approved first time","30 days")}</div>`; }
function renderTeam(){ if(!isOwner) return; const t=dxb();
  const reps=[...new Set([...videos,...shoots,...kpis,...tlog].map(x=>x.repId).filter(Boolean))].filter(r=>r!==me);
  $("#attTable").innerHTML=`<thead><tr><th>Name</th><th>Selfie</th><th>Status</th><th>In</th><th>Out</th><th>Worked</th><th>Breaks</th><th>Score today</th><th>Week</th></tr></thead><tbody>${reps.map(r=>{ const st=shiftState(r,t), d=dayStats(r,t), w=weekScore(r,weekStart(t)); const s=st.brk?"On break":st.on?"On shift":st.outAt?"Done":"Not in";
    return `<tr><td>${nameCell(r)}</td><td>${selfieCell(r,st.firstIn)}</td><td>${s}</td><td>${st.inAt?hm(st.inAt):"–"}${d.late?" (late)":""}</td><td>${st.outAt?hm(st.outAt):"–"}</td><td>${st.inAt?dur(st.worked):"–"}</td><td>${st.inAt?dur(st.breakMs):"–"}</td><td>${d.score}</td><td>${w.score}</td></tr>`; }).join("")||`<tr><td colspan="9">Nobody has punched in yet.</td></tr>`}</tbody>`;
  renderTeamReports(); renderTeamPeriods();
  const K=kpis.slice().sort((a,b)=>(b.createdAt||0)-(a.createdAt||0)).slice(0,8);
  $("#teamCheckins").innerHTML=K.map(k=>`<div class="item"><span class="ic">${ICON.coach}</span><div style="min-width:0"><div class="t">${esc(names[k.repId]||"")} · ${esc(fmtD(k.date))}</div><div class="s">${k.trials??"–"} trials · ${k.live??"–"} live · ${k.yontro??"–"} Yontro · ${k.edits??"–"} edits${k.blockers?" · blocker: "+esc(k.blockers):""}</div>${k.feedback?`<div style="font-size:13px;margin-top:4px">${MGR1}: ${esc(k.feedback)}</div>`:""}</div><span></span></div>`).join("")||`<div class="empty">No check-ins yet.</div>`;
  if(!$("#goalCard").contains(document.activeElement)) $("#goalCard").innerHTML=`<div class="head"><h2>Targets</h2><span class="tag">Used for the daily checklist and score</span></div>
   <div class="grid2"><label class="f" for="gT">Founder Tales follower goal<input id="gT" inputmode="numeric" value="${esc(goals.ftTarget)}"></label><label class="f" for="gD">By<input id="gD" type="date" value="${esc(goals.ftDate)}"></label></div>
   <div class="grid2"><label class="f" for="gTr">Trial reels a day<input id="gTr" inputmode="numeric" value="${esc(goals.trials)}"></label><label class="f" for="gY">Yontro videos a day<input id="gY" inputmode="numeric" value="${esc(goals.yontro)}"></label></div>
   <div><button class="btn or" type="button" id="saveGoals">Save targets</button></div>`;
  if(document.activeElement!==$("#playbook")) $("#playbook").value=playbook||STUDIO_PLAYBOOK; }

/* ---------- sheets ---------- */
function openS(html,wide){ $("#sheet").classList.toggle("wide",!!wide); $("#sheet").innerHTML=html; $("#sheetBg").hidden=false; }
function videoSheet(v,pre){ v=v||{}; const f={brand:"ft",status:"idea",...pre,...v}; const t=dxb(); const isNew=!v.id;
  const seg=(id,opts,val)=>`<div class="seg" id="${id}">${opts.map(([k,l])=>`<button type="button" data-v="${k}" aria-pressed="${String(val)===String(k)}">${l}</button>`).join("")}</div>`;
  const stOpts=f.brand==="ft"?[["idea","Idea"],["editing","Editing"],["trial","Trial reel"],["live","Live"],["dropped","Dropped"]]:[["idea","Idea"],["editing","Editing"],["done","Done"]];
  openS(`<div class="head"><h2 id="sheetTitle">${isNew?"New video":esc(f.title||"Video")}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>
  <form id="vidForm" data-id="${esc(v.id||"")}" style="display:grid;gap:10px">
   <label class="f">For${seg("vBrand",[["ft","Founder Tales"],["yontro","Yontro.ae"]],f.brand)}</label>
   <label class="f" for="vTitle">Title<input id="vTitle" required value="${esc(f.title||"")}" placeholder="e.g. Why Elon named it Tesla"></label>
   <label class="f" for="vHook">Hook (first 3 seconds)<input id="vHook" value="${esc(f.hook||"")}" placeholder="e.g. Elon didn't invent Tesla. He bought the name."></label>
   <label class="f" for="vConcept">Concept<textarea id="vConcept" placeholder="The story, the angle, the twist, how it ends">${esc(f.concept||"")}</textarea></label>
   <label class="f">Status${seg("vStatus",stOpts,f.status)}</label>
   <div class="grid2"><label class="f" for="vTrial">Trial reel date<input id="vTrial" type="date" value="${esc(f.trialDate||"")}"></label><label class="f" for="vPlan">Planned for<input id="vPlan" type="date" value="${esc(f.planFor||"")}"></label></div>
   <label class="f" for="vPost">Scheduled post time<input id="vPost" type="datetime-local" value="${esc(f.postAt||"")}"></label>
   <label class="f" for="vLink">Instagram link (paste it once posted, so stats sync)<input id="vLink" inputmode="url" value="${esc(f.link||"")}" placeholder="Paste a link"></label>
   <label class="f" for="vNotes">Notes<textarea id="vNotes">${esc(f.notes||"")}</textarea></label>
   <button class="btn or" type="submit">Save</button></form>
  ${v.id?`<div class="btnrow">${["trial","live"].includes(f.status)?`<button class="btn" type="button" data-stats="${esc(v.id)}">${f.stats?"Update stats":"Add stats"}</button>`:""}${f.status==="trial"?`<button class="btn or" type="button" data-golive="${esc(v.id)}">Post live</button>`:""}<button class="btn dark" type="button" data-review="${esc(v.id)}">${MGR1}, review this</button><button class="btn ghost" type="button" data-del="${esc(v.id)}" data-coll="videos">Delete</button></div>
  ${f.stats?`<div class="card" style="background:var(--soft)"><b>Performance</b><div class="vstat">${STATS.map(([k,l])=>f.stats[k]!==undefined&&f.stats[k]!==""?`<span>${l}: <b>${esc(f.stats[k])}</b></span>`:"").join("")}</div><div class="tag">${f.stats.source==="metricool"?"From Metricool · ":""}Updated ${esc(dtStr(f.statsAt||Date.now()))}</div></div>`:""}
  ${f.review?`<div class="card" style="background:var(--soft)"><b>${MGR1}'s review</b><div style="white-space:pre-wrap;font-size:14px">${esc(f.review)}</div></div>`:""}`:""}`); }
function statsSheet(v){ const s=v.stats||{};
  openS(`<div class="head"><h2 id="sheetTitle">Stats · ${esc(v.title)}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>
  <div class="tag">${s.source==="metricool"?`Synced from Metricool ${esc(dtStr(v.statsAt||Date.now()))}. Correct anything that looks wrong.`:goals.metricool?"Metricool fills these in automatically once the Instagram link is on the video. You can type them in meanwhile.":`From Instagram Insights${v.brand==="ft"?" (Founder Tales)":""}. Fill what you have.`}</div>
  <form id="statsForm" data-id="${esc(v.id)}" style="display:grid;gap:10px"><div class="grid2">${STATS.map(([k,l])=>`<label class="f" for="st_${k}">${l}<input id="st_${k}" inputmode="decimal" value="${esc(s[k]??"")}"></label>`).join("")}</div><button class="btn or" type="submit">Save stats</button></form>`); }
function followersSheet(){ const t=dxb(); const cur=followers.find(f=>f.date===t);
  openS(`<div class="head"><h2 id="sheetTitle">Founder Tales followers today</h2><button class="btn ghost sm" type="button" data-close>Close</button></div><form id="flForm" style="display:grid;gap:10px"><label class="f" for="flN">Followers on Instagram right now<input id="flN" inputmode="numeric" required value="${esc(cur?.followers??"")}"></label><button class="btn or" type="submit">Save</button></form>`); setTimeout(()=>$("#flN")?.focus(),50); }
function goLiveSheet(v){ const now=new Date(); const def=dxb()+"T"+String(Math.max(10,Math.min(21,now.getHours()+1))).padStart(2,"0")+":00";
  openS(`<div class="head"><h2 id="sheetTitle">Post live · ${esc(v.title)}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div><div class="tag">Mark it as posted now, or schedule a time and mark it when it goes up.</div>
  <form id="liveForm" data-id="${esc(v.id)}" style="display:grid;gap:10px"><label class="f" for="lvAt">Post time<input id="lvAt" type="datetime-local" value="${esc(v.postAt||def)}"></label><div class="btnrow"><button class="btn or" type="submit" data-now="1">Posted now</button><button class="btn" type="submit" data-now="0">Schedule</button></div></form>`); }
function clientSheet(c){ c=c||{};
  openS(`<div class="head"><h2 id="sheetTitle">${c.id?esc(c.name):"New client"}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>
  <form id="clForm" data-id="${esc(c.id||"")}" style="display:grid;gap:10px"><label class="f" for="cName">Business<input id="cName" required value="${esc(c.name||"")}"></label>
   <label class="f">Package<div class="seg" id="cPkg">${Object.keys(PKGQ).map(p=>`<button type="button" data-v="${p}" aria-pressed="${(c.package||"Growth")===p}">${p} · ${PKGQ[p]} videos</button>`).join("")}</div></label>
   <div class="grid2"><label class="f" for="cContact">Contact<input id="cContact" value="${esc(c.contact||"")}"></label><label class="f" for="cPhone">Phone / WhatsApp<input id="cPhone" inputmode="tel" value="${esc(c.phone||"")}"></label></div>
   <label class="f" for="cNotes">Brand notes (style, do's and don'ts)<textarea id="cNotes">${esc(c.notes||"")}</textarea></label>
   <div class="btnrow"><button class="btn or" type="submit">Save</button>${c.id?`<button class="btn" type="button" data-newshoot="${esc(c.id)}">+ Shoot</button><button class="btn ghost" type="button" data-del="${esc(c.id)}" data-coll="clients">Delete</button>`:""}</div></form>`); }
const KIT=[["bat","Batteries charged"],["cards","Memory cards empty"],["mic","Mic and spare batteries"],["light","Lights"],["gimbal","Gimbal / tripod"],["brief","Brief confirmed with client"]];
function shootSheet(s,pre){ s=s||{}; const f={status:"scheduled",videos:3,...pre,...s}; const now=Date.now(); const dl=shootDeadline(f);
  const travel=/sharjah|ajman|abu dhabi/i.test(f.location||"");
  const steps={scheduled:`<button class="btn or" type="button" data-sact="shot">Shoot done · start 48h clock</button>`,shot:`<button class="btn or" type="button" data-sact="sent">First edit sent to client</button>`,review:`<button class="btn green" type="button" data-sact="approved">Client approved</button><button class="btn" type="button" data-sact="rev">Client asked for changes</button>`,revisions:`<button class="btn or" type="button" data-sact="revsent">Revision sent</button>`,approved:`<button class="btn green" type="button" data-sact="delivered">Delivered final videos</button>`};
  openS(`<div class="head"><h2 id="sheetTitle">${s.id?`Shoot · ${esc(f.client)}`:"Schedule a shoot"}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>
  ${s.id?`<div class="tag"><span class="stage ${SST[f.status][1]}">${SST[f.status][0]}</span>${dl?` · <span class="due ${dl<now?"over":dl-now<12*3600e3?"soon":""}">${leftTxt(dl-now)}</span>`:""}${(f.revisions||[]).length?` · ${(f.revisions||[]).length} revision round${(f.revisions||[]).length>1?"s":""}${(f.revisions||[]).length>2?" (over the 2 included)":""}`:""}</div>
   <div class="btnrow">${steps[f.status]||""}${f.status!=="cancelled"&&f.status!=="delivered"?`<button class="btn ghost sm" type="button" data-sact="cancel">Cancel shoot</button>`:""}</div>`:""}
  <form id="shForm" data-id="${esc(s.id||"")}" style="display:grid;gap:10px">
   <label class="f" for="shClient">Client<select id="shClient">${clients.map(c=>`<option value="${esc(c.id)}" ${c.id===f.clientId?"selected":""}>${esc(c.name)}</option>`).join("")}<option value="__yontro" ${f.clientId==="__yontro"?"selected":""}>Yontro.ae (own content)</option></select></label>
   ${clients.length?"":`<div class="tag">No clients yet. <button class="btn sm" type="button" data-newclient>+ Add a client</button></div>`}
   <div class="grid2"><label class="f" for="shDate">Date<input id="shDate" type="date" required value="${esc(f.date||addDays(dxb(),1))}"></label><label class="f" for="shTime">Time<input id="shTime" type="time" value="${esc(f.time||"11:00")}"></label></div>
   <label class="f" for="shLoc">Location<input id="shLoc" value="${esc(f.location||"")}" placeholder="Business name and area"></label>
   ${travel?`<div class="tag" style="color:var(--amber)">Outside Dubai: a travel charge applies. Check Sahill has quoted it.</div>`:""}
   <label class="f" for="shVids">Videos from this shoot<input id="shVids" inputmode="numeric" value="${esc(f.videos)}"></label>
   <label class="f" for="shBrief">Brief (what the client wants)<textarea id="shBrief" placeholder="Offer to push, people on camera, products, style">${esc(f.brief||"")}</textarea></label>
   <label class="f" for="shList">Shot list<textarea id="shList" style="min-height:110px" placeholder="Tap 'John, draft the shot list' or write your own">${esc(f.shotList||"")}</textarea></label>
   <div><button class="btn sm dark" type="button" data-shotlist>${MGR1}, draft the shot list</button></div>
   <div class="card" style="background:var(--soft);gap:6px"><b>Kit check</b>${KIT.map(([k,l])=>`<label style="display:flex;gap:8px;align-items:center;font-size:14px"><input type="checkbox" data-kit="${k}" style="width:auto" ${f.kit?.[k]?"checked":""}> ${l}</label>`).join("")}</div>
   <div class="grid2"><label class="f" for="shRaw">Raw footage link<input id="shRaw" inputmode="url" value="${esc(f.footageLink||"")}"></label><label class="f" for="shEdit">Edit link<input id="shEdit" inputmode="url" value="${esc(f.editLink||"")}"></label></div>
   <label class="f" for="shNotes">Notes and client feedback<textarea id="shNotes">${esc(f.notes||"")}</textarea></label>
   <div class="btnrow"><button class="btn or" type="submit">${s.id?"Save":"Book shoot"}</button>${s.id?`<button class="btn ghost" type="button" data-del="${esc(s.id)}" data-coll="shoots">Delete</button>`:""}</div></form>`); }
function pickWinnerSheet(){ const y=prevWork(dxb()); const L=mine(videos).filter(v=>v.brand==="ft"&&v.trialDate===y&&["trial","live","dropped"].includes(v.status));
  if(!L.length) return toast("No trial reels from yesterday."); openS(`<div class="head"><h2 id="sheetTitle">Pick yesterday's winner</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>${compareHTML(L)}<div class="tag">Post the winner live. The other one is marked Dropped automatically.</div>`); }

/* ---------- John (manager chat) ---------- */
function rules(){ const base=`You are ${MGR}, Head of Production at Yontro in Dubai, managing and coaching ${names[viewRep]||"Azeem"}, the videographer. He makes 2 Founder Tales trial reels a day and posts the winner live the next day, makes 1 Yontro.ae video a day, and shoots and edits client videos (first edit within 48 hours of the shoot, each revision within 24 hours).
${playbook||STUDIO_PLAYBOOK}
${studioContext()}
Money in AED. Never invent numbers or results.`;
  if(mode==="well") return `You are ${MGR}, ${names[viewRep]||"Azeem"}'s manager at Yontro in Dubai, and you genuinely care about his wellbeing. This is a private wellbeing chat: Sahill and the company cannot read it and you never report it. No work talk or targets unless he raises it. Warm, human, brief (1-3 short lines, WhatsApp style), one gentle question at a time (sleep, stress, energy, creative burnout, family). Offer one small practical idea only when it helps (a break, a walk, water, the 10-minute silence in the app, time off). If he mentions feeling hopeless, unsafe or thoughts of self-harm, respond with care, encourage him to reach someone he trusts now, and share UAE support: the national mental support line 800 4673 (800 HOPE), or 999 in an emergency. Never diagnose. Today ${dxb()}.`;
  if(mode==="ask") return base+`\n\nMODE: OPEN CHAT. Answer questions, unblock him, plan his day, keep him motivated. Short replies (1-4 lines) unless asked. If he needs an official letter (sick leave, annual leave, salary certificate, experience letter, NOC, letter to a client), get the facts and call draft_letter; Sahill signs and stamps it.`;
  if(mode==="checkin") return base+`\n\nMODE: DAILY CHECK-IN. Ask one or two at a time: 1) trial reels made today and their concepts, 2) which of yesterday's trials went live and why it won, 3) stats logged and the follower count, 4) the Yontro video, 5) client edits sent or delayed, 6) tomorrow's ideas and post times, 7) anything blocking him. Use his logged numbers. Then call save_checkin, give one line of honest feedback and ONE concrete tip for tomorrow. 1-3 short lines per message.`;
  if(mode==="ideas") return base+`\n\nMODE: IDEAS. Brainstorm Founder Tales (and Yontro.ae when asked) video ideas built on what has performed best: give each idea a title, a scroll-stopping hook for the first 3 seconds and a one-line concept. When he likes ideas, call save_idea for each (planned for tomorrow unless he says otherwise). Short.`;
  return base+`\n\nMODE: REVIEW. He shares a concept, hook or script. Critique it like a short-form video editor: hook strength in the first 3 seconds, story structure, retention risks, length, CTA under 3 seconds, ending teaser. Give the 3 most useful fixes and a rewritten hook. Max 10 lines.`; }
async function john(text,opts={}){
  if(busy) return; text=String(text||"").trim(); if(!text&&!opts.system) return;
  if(!sample){ if(mode==="well") return toast("This private chat needs Claude on your own account. The other modes work."); if(!text) text=mode==="checkin"?"Start my daily check-in":"Hi John"; 
    try{ await db.collection("chats").add({repId:viewRep,mode,session:"",role:"rep",text,pending:true,createdAt:Date.now()}); toast(`Sent. ${MGR1} replies at 11:30, 13:30, 16:30 or 19:30.`); }catch(e){ toast("Couldn't send: "+(e?.message||e?.code||"error")); } renderChat(); return; }
  const rep=viewRep; const coll=mode==="well"?`data/users/${me}/well/chat`:"chats"; if(mode==="well"&&rep!==me) return;
  if(text&&!opts.hidden){ try{ await db.collection(coll).add({repId:rep,mode,session:"",role:"rep",text,createdAt:Date.now()}); }catch(e){ return toast("Couldn't send: "+(e?.message||e?.code||"error")); } }
  busy=true; renderChat();
  const hist=(mode==="well"?wchats:chats).filter(c=>c.repId===rep&&c.mode===mode).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0)).slice(-24).map(c=>({role:c.role==="rep"?"user":"assistant",content:c.text}));
  const msgs=[{role:"user",content:rules()},...hist]; if(text&&!opts.hidden) msgs.push({role:"user",content:text}); if(opts.system) msgs.push({role:"user",content:opts.system});
  let tools;
  if(mode==="ask") tools=[{name:"draft_letter",description:"Draft an official letter on Yontro letterhead for Sahill to approve, sign and stamp.",inputSchema:{type:"object",properties:{type:{type:"string"},details:{type:"string"},client:{type:"string"}},required:["type","details"]},
    execute:async i=>{ const id=await createLetter(rep,String(i.type||"Letter"),String(i.details||""),String(i.client||"")); await db.collection("chats").add({repId:rep,mode:"ask",session:"",role:"hamza",kind:"paper",paperId:id,text:`Draft ready: ${i.type} letter. Check it, then send it to Sahill.`,createdAt:Date.now()}); return "Drafted; the person sees a card to open it. Tell him in one line to check it and send it to Sahill (Papers)."; }}];
  if(mode==="checkin") tools=[{name:"save_checkin",description:"Save today's check-in and your one-line feedback.",inputSchema:{type:"object",properties:{trials:{type:"number"},live:{type:"number"},yontro:{type:"number"},edits:{type:"number",description:"client edits or revisions sent today"},blockers:{type:"string"},feedback:{type:"string"}},required:["feedback"]},
    execute:async i=>{ await db.doc(`kpi/${rep}_${dxb()}`).set({repId:rep,date:dxb(),trials:+i.trials||0,live:+i.live||0,yontro:+i.yontro||0,edits:+i.edits||0,blockers:String(i.blockers||""),feedback:String(i.feedback||""),createdAt:Date.now()}); return "saved"; }}];
  if(mode==="ideas") tools=[{name:"save_idea",description:"Save a video idea to his list.",inputSchema:{type:"object",properties:{title:{type:"string"},hook:{type:"string"},concept:{type:"string"},brand:{type:"string",enum:["ft","yontro"]},planFor:{type:"string",description:"YYYY-MM-DD"}},required:["title","hook"]},
    execute:async i=>{ const now=Date.now(); await db.collection("videos").add({repId:rep,brand:i.brand==="yontro"?"yontro":"ft",status:"idea",title:String(i.title),hook:String(i.hook||""),concept:String(i.concept||""),planFor:/^\d{4}-\d{2}-\d{2}$/.test(i.planFor||"")?i.planFor:nextWork(dxb()),createdAt:now,updatedAt:now}); return "saved"; }}];
  let reply="";
  try{ const r=await sample(msgs,{modelTier:"default",cache:false,...(tools?{tools}:{})}); reply=r.text.trim(); }
  catch(e){ reply=e?.code==="not_granted"?"I need Claude access on this page to talk. Allow it from the Permissions menu.":e?.code==="rate_limited"?"I'm busy right now. Try again in a few minutes.":"Something went wrong: "+(e?.message||e?.code||"error"); }
  try{ await db.collection(coll).add({repId:rep,mode,session:"",role:"hamza",kind:opts.kind||"",text:reply||"…",createdAt:Date.now()+1}); }catch(_){}
  busy=false; renderAll(); }
function renderChat(){
  if(mode==="well"&&viewRep!==me){ $("#modeBar").innerHTML=`<div class="tag">Wellbeing chats are private between each person and ${MGR1}. Nobody else can read them, including you.</div>`; $("#chat").innerHTML=""; $("#chatForm").hidden=true; return; } $("#chatForm").hidden=false;
  const L=(mode==="well"?wchats:chats).filter(c=>c.repId===viewRep&&c.mode===mode).sort((a,b)=>(a.createdAt||0)-(b.createdAt||0)).slice(-40);
  const bar={ask:`<div class="chips"><button class="chip" type="button" data-say="Plan my day">Plan my day</button><button class="chip" type="button" data-say="I need a letter from the company">I need a letter</button><button class="chip" type="button" data-say="Which of yesterday's trial reels should go live and why?">Which reel goes live?</button></div>`,
    checkin:`<div class="tag">${MGR1} asks about today's videos, edits and blockers, and logs it.</div>${L.length?"":`<button class="btn or sm" type="button" id="startCheckin">Start today's check-in</button>`}`,
    ideas:`<div class="chips"><button class="chip" type="button" data-say="Give me 5 Founder Tales ideas for tomorrow based on what performed best">5 ideas for tomorrow</button><button class="chip" type="button" data-say="Give me 3 Yontro.ae video ideas">Yontro ideas</button><button class="chip" type="button" data-say="Write 5 stronger hooks for my next video">Better hooks</button></div>`,
    review:`<div class="tag">Paste a concept, hook or script and ${MGR1} critiques it for retention.</div>`,
    well:`<div class="tag">Private: only you and ${MGR1} see this. Sahill can't read it.</div><div class="chips"><button class="chip" type="button" data-say="I'm feeling stressed today">Feeling stressed</button><button class="chip" type="button" data-say="I'm creatively drained">Creatively drained</button><button class="chip" type="button" data-meditate>10-minute silence</button></div>`}[mode]||"";
  $("#modeBar").innerHTML=bar;
  const empty={ask:`Hi, I'm ${MGR1}, your production manager. Ask me anything: today's plan, a reel, a client edit, or a letter you need.`,checkin:"Ready when you are. Tap Start to begin today's check-in.",ideas:"Let's find tomorrow's videos. Pick a chip or tell me a founder or brand you want to cover.",review:"Paste a hook, concept or script and I'll tell you what will keep people watching.",well:"This chat is just between us. How are you doing today, really?"}[mode];
  $("#chat").innerHTML=(L.length?L:[{role:"hamza",text:empty}]).map(m=>`<div class="msg ${m.role==="rep"?"rep":"hamza"}">${esc(m.text)}${m.kind==="paper"&&m.paperId?`<button class="btn sm or" type="button" style="display:block;margin-top:6px" data-openpaper="${esc(m.paperId)}" data-puid="${esc(m.repId)}">Open it</button>`:""}${m.createdAt?`<span class="w">${new Date(m.createdAt).toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",timeZone:"Asia/Dubai"})}</span>`:""}</div>`).join("")+(busy?`<div class="msg hamza"><span class="dots-anim">${MGR1} is typing</span></div>`:"")+(L.some(m=>m.pending)?`<div class="msg hamza"><i>${MGR1} replies here at 11:30, 13:30, 16:30 or 19:30.</i></div>`:"");
  const c=$("#chat"); c.scrollTop=c.scrollHeight; $("#chatSend").disabled=busy||(!sample&&mode==="well"); $("#chatIn").placeholder=mode==="checkin"?"Type your answer…":`Message ${MGR1}…`; }

/* ---------- staff names ---------- */
const staffNames={}; let askedName=false;
function subStaff(){ db.collection("staff").onSnapshot(q=>{ q.docs.forEach(d=>{ const n=(d.data().name||"").trim(); if(n){ staffNames[d.id]=n; names[d.id]=n; } }); renderAll(); ensureMyName(); },()=>{}); }
async function ensureMyName(){ if(!me||staffNames[me]||askedName) return; askedName=true;
  let n=""; try{ n=((await user?.me?.())?.name||"").trim(); }catch(_){} if(isOwner) n="Sahill Chandan";
  if(n){ try{ await db.doc("staff/"+me).set({name:n,at:Date.now()}); }catch(_){} return; }
  setTimeout(()=>{ if(!$("#sheetBg").hidden||staffNames[me]) return; nameSheet(me,""); },1500); }
function nameSheet(uid,cur){ $("#sheet").classList.remove("wide");
  $("#sheet").innerHTML=`<div class="head"><h2 id="sheetTitle">${uid===me?"What's your name?":"Rename"}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>
  <form id="nameForm" data-uid="${esc(uid)}" style="display:grid;gap:10px"><label class="f" for="nmIn">${uid===me?"Shown on your reports and to your manager":"Name shown on attendance and reports"}<input id="nmIn" required value="${esc(cur||"")}" placeholder="e.g. Usama Rehman"></label><button class="btn or" type="submit">Save</button></form>`;
  $("#sheetBg").hidden=false; setTimeout(()=>$("#nmIn")?.focus(),50); }
document.addEventListener("submit",async e=>{ if(e.target.id!=="nameForm") return; e.preventDefault(); const uid=e.target.dataset.uid, n=$("#nmIn").value.trim(); if(!n) return;
  try{ await db.doc("staff/"+uid).set({name:n,at:Date.now()}); staffNames[uid]=n; names[uid]=n; toast("Saved."); closeSheet(); renderAll(); }catch(err){ toast("Couldn't save: "+(err?.code||"error")); } });
document.addEventListener("click",e=>{ const b=e.target.closest("[data-rename]"); if(!b) return; nameSheet(b.dataset.rename,staffNames[b.dataset.rename]||names[b.dataset.rename]||""); });
const nameCell=r=>`<b>${esc(names[r]||"Unnamed")}</b>${r===me?" (you)":""}${isOwner?` <button type="button" class="btn ghost sm" data-rename="${esc(r)}" aria-label="Rename" style="padding:0 6px">✎</button>`:""}`;


/* ---------- allow-Claude button ---------- */
function aiBanner(who){ const b=$("#banner"); b.innerHTML=`${esc(who)} needs your OK to use Claude on this page (one time). <button class="btn sm or" type="button" id="allowAI" style="margin-left:6px">Allow ${esc(who)}</button>`; b.hidden=false; }
document.addEventListener("click",async e=>{ if(e.target.id!=="allowAI") return; const b=e.target; b.disabled=true;
  try{ const P=await window.claude?.use?.("permissions"); if(!P){ toast("Use the page's ⋯ menu → Permissions → turn on Claude, then refresh."); b.disabled=false; return; }
    const r=await P.request(["sample"]); const st=(r&&(r.sample||r["sample"]))||"";
    if(st==="granted"){ toast("Allowed. Reloading…"); setTimeout(()=>location.reload(),600); return; }
    if(st==="denied"){ try{ await P.manage(); }catch(_){ toast("Open the page's ⋯ menu → Permissions and turn on Claude."); } setTimeout(()=>location.reload(),400); return; }
    toast("Open the page's ⋯ menu → Permissions and turn on Claude, then refresh."); }catch(_){ toast("Open the page's ⋯ menu → Permissions and turn on Claude, then refresh."); }
  b.disabled=false; });
/* ---------- events ---------- */
document.addEventListener("click",async e=>{
  const b=e.target.closest("button,[data-vid],[data-shoot],[data-client]"); if(!b) return; const d=b.dataset;
  if(d.tab){ tab=d.tab; renderAll(); scrollTo(0,0); return; }
  if(d.close!==undefined){ closeSheet(); return; }
  if(d.del){ if(!d.confirm){ d.confirm="1"; b.textContent="Tap again to delete"; return; } try{ await db.doc(d.coll+"/"+d.del).delete(); toast("Deleted."); closeSheet(); }catch(err){ toast("Couldn't delete."); } return; }
  if(d.newvid){ if(!viewRep) return toast("Sign in first."); const t=dxb(); const pre=d.newvid==="ft-trial"?{brand:"ft",status:"trial",trialDate:t}:d.newvid==="ft-idea"?{brand:"ft",status:"idea",planFor:nextWork(t),postAt:nextWork(t)+"T19:00"}:{brand:"yontro",status:"editing"}; videoSheet(null,pre); return; }
  if(d.vid){ const v=videos.find(x=>x.id===d.vid); if(v) videoSheet(v); return; }
  if(d.stats){ const v=videos.find(x=>x.id===d.stats); if(v) statsSheet(v); return; }
  if(d.golive){ const v=videos.find(x=>x.id===d.golive); if(v) goLiveSheet(v); return; }
  if(d.compare!==undefined){ pickWinnerSheet(); return; }
  if(d.gostats!==undefined){ const y=prevWork(dxb()); const v=mine(videos).find(v=>v.brand==="ft"&&(v.trialDate===y||dOf(v.postedAt)===y)&&!v.statsAt); if(v) statsSheet(v); return; }
  if(d.followers!==undefined){ followersSheet(); return; }
  if(d.newclient!==undefined){ clientSheet(null); return; }
  if(d.client){ const c=clients.find(x=>x.id===d.client); if(c) clientSheet(c); return; }
  if(d.newshoot!==undefined){ shootSheet(null,d.newshoot?{clientId:d.newshoot}:{}); return; }
  if(d.shoot){ const s=shoots.find(x=>x.id===d.shoot); if(s) shootSheet(s); return; }
  if(d.vf){ vidF=d.vf; renderContent(); return; }
  if(d.day){ calDay=d.day; renderCal(); return; }
  if(b.id==="wkPrev"){ calWeek=addDays(calWeek,-7); calDay=calWeek; renderCal(); return; }
  if(b.id==="wkNext"){ calWeek=addDays(calWeek,7); calDay=calWeek; renderCal(); return; }
  if(b.id==="wkToday"){ calWeek=weekStart(dxb()); calDay=dxb(); renderCal(); return; }
  if(d.mode){ mode=d.mode; syncModeBtns(); renderChat(); return; }
  if(d.go==="checkin"){ openHz("checkin"); if(!chats.some(c=>c.repId===viewRep&&c.mode==="checkin"&&dxb(new Date(c.createdAt||0))===dxb())) john("",{system:"Start today's check-in now with your first question."}); return; }
  if(b.id==="startCheckin"){ john("",{system:"Start today's check-in now with your first question."}); return; }
  if(d.say){ john(d.say); return; }
  if(d.review){ const v=videos.find(x=>x.id===d.review); if(!v) return; if(!sample){ mode="review"; await db.collection("chats").add({repId:viewRep,mode:"review",session:"",role:"rep",text:`Please review my video "${v.title}". Hook: ${v.hook||"(none)"}. Concept: ${v.concept||"(none)"}.`,pending:true,videoId:v.id,createdAt:Date.now()}); toast(`Sent to ${MGR1}. His review appears in the chat at his next reply time.`); return; } b.disabled=true; b.textContent=`${MGR1} is watching…`;
    try{ const r=await sample(`${rules().split("\n\nMODE")[0]}\n\nMODE: REVIEW. Critique this ${v.brand==="ft"?"Founder Tales":"Yontro.ae"} video like a short-form editor: hook in the first 3 seconds, structure, retention risks, length, CTA under 3 seconds, ending teaser.${v.stats?" Use its stats to explain what worked or not.":""} Give 3 fixes and one rewritten hook. Max 10 lines.\nTITLE: ${v.title}\nHOOK: ${v.hook||"(none)"}\nCONCEPT: ${v.concept||"(none)"}\nSTATS: ${JSON.stringify(v.stats||{})}`,{modelTier:"default",cache:false}); await db.doc("videos/"+v.id).update({review:r.text.trim(),updatedAt:Date.now()}); videoSheet({...v,review:r.text.trim()}); }catch(err){ toast(`${MGR1} couldn't review it right now.`); b.disabled=false; } return; }
  if(d.shotlist!==undefined){ if(!sample){ const c0=clients.find(x=>x.id===$("#shClient").value); await db.collection("chats").add({repId:viewRep,mode:"ask",session:"",role:"rep",text:`Please draft a shot list for the ${c0?.name||"Yontro"} shoot on ${$("#shDate").value} at ${$("#shLoc").value||"their premises"}: ${$("#shVids").value||3} videos. Brief: ${$("#shBrief").value||"(none)"}.`,pending:true,shootId:$("#shForm")?.dataset.id||"",createdAt:Date.now()}); toast(`Sent to ${MGR1}. The shot list appears in the chat at his next reply time.`); return; } const c=clients.find(x=>x.id===$("#shClient").value); b.disabled=true; b.textContent=`${MGR1} is writing…`;
    try{ const r=await sample(`You are ${MGR}, Head of Production at Yontro (Dubai social media agency). Write a practical shot list for a ${$("#shVids").value||3}-video shoot for ${c?.name||"Yontro"} at ${$("#shLoc").value||"their premises"}. Brief: ${$("#shBrief").value||"(none)"}. Brand notes: ${c?.notes||"(none)"}. Package: ${c?.package||"?"}. For each video: working title, hook shot (first 3 seconds), 4-6 shots (wide/close/detail/b-roll/talking head), on-camera lines if any, and vertical 9:16 notes. Plain text, numbered, concise. Never invent prices or offers; use [ask client: …] where needed.`,{modelTier:"default",cache:false}); $("#shList").value=r.text.trim(); toast("Shot list drafted. Edit it, then Save."); }catch(err){ toast("Couldn't draft it."); } b.disabled=false; b.textContent=`${MGR1}, draft the shot list`; return; }
  if(d.sact){ const id=$("#shForm")?.dataset.id; const s=shoots.find(x=>x.id===id); if(!s) return; const now=Date.now(); let p={};
    if(d.sact==="shot") p={status:"shot",shotAt:now,dueAt:now+48*3600e3};
    if(d.sact==="sent") p={status:"review",sentAt:now};
    if(d.sact==="rev") p={status:"revisions",revisions:[...(s.revisions||[]),{askedAt:now,dueAt:now+24*3600e3}]};
    if(d.sact==="revsent"){ const R=(s.revisions||[]).slice(); if(R.length) R[R.length-1]={...R[R.length-1],doneAt:now}; p={status:"review",revisions:R}; }
    if(d.sact==="approved") p={status:"approved",approvedAt:now};
    if(d.sact==="delivered") p={status:"delivered",deliveredAt:now,delivered:+s.videos||0};
    if(d.sact==="cancel") p={status:"cancelled"};
    try{ await db.doc("shoots/"+id).update({...p,updatedAt:now}); toast({shot:"48-hour clock started.",sent:"Sent. Waiting for client approval.",rev:"Revision logged: 24 hours to send it.",revsent:"Revision sent.",approved:"Approved.",delivered:"Delivered. Counted towards this month.",cancel:"Cancelled."}[d.sact]); shootSheet({...s,...p}); }catch(err){ toast("Couldn't update."); } return; }
  if(b.id==="saveGoals"){ const g={ftTarget:+$("#gT").value||5000,ftDate:$("#gD").value||"2027-01-15",trials:Math.max(1,+$("#gTr").value||2),live:1,yontro:Math.max(0,+$("#gY").value||1)}; try{ await db.doc("meta/goals").set({...g,updatedAt:Date.now()}); toast("Targets saved."); }catch(err){ toast("Couldn't save."); } return; }
  if(b.id==="savePlaybook"){ try{ await db.doc("meta/playbook").set({text:$("#playbook").value,updatedAt:Date.now()}); toast(`Saved. ${MGR1} now uses it.`); }catch(err){ toast("Couldn't save."); } return; }
  if(b.id==="makeReport"){ return; }
  if(b.id==="punchIn"){ punchInSheet(); return; }
  if(b.id==="punchOut"){ punchOutSheet(); return; }
  if(b.id==="breakStart"){ await logEvent("break_start"); toast("Break started. Enjoy."); return; }
  if(b.id==="breakEnd"){ await logEvent("break_end"); toast("Welcome back."); return; }
  const seg=b.closest(".seg"); if(seg&&b.dataset.v!==undefined){ seg.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",String(x===b))); if(seg.id==="vBrand"){ const v=videos.find(x=>x.id===$("#vidForm").dataset.id)||{}; videoSheet(v.id?{...v,brand:b.dataset.v}:null,{...collectVid(),brand:b.dataset.v}); } return; }
});
function collectVid(){ const g=id=>($(id)?.value||"").trim(); return {brand:segVal("#vBrand")||"ft",status:segVal("#vStatus")||"idea",title:g("#vTitle"),hook:g("#vHook"),concept:g("#vConcept"),trialDate:g("#vTrial"),planFor:g("#vPlan"),postAt:g("#vPost"),link:g("#vLink"),notes:g("#vNotes")}; }
document.addEventListener("change",async e=>{ if(e.target.id==="repPick"){ viewRep=e.target.value; renderAll(); } if(e.target.dataset?.kit){ const id=$("#shForm")?.dataset.id; if(!id) return; const s=shoots.find(x=>x.id===id); try{ await db.doc("shoots/"+id).update({kit:{...(s?.kit||{}),[e.target.dataset.kit]:e.target.checked}}); }catch(_){} } });
$("#sheetBg").addEventListener("click",e=>{ if(e.target.id==="sheetBg") closeSheet(); });
document.addEventListener("keydown",e=>{ if(e.key==="Escape"&&!$("#sheetBg").hidden) closeSheet(); });
document.addEventListener("submit",async e=>{ const f=e.target; const now=Date.now();
  try{
  if(f.id==="vidForm"){ e.preventDefault(); const v=collectVid(); if(!v.title) return toast("Give it a title."); const id=f.dataset.id; const old=videos.find(x=>x.id===id);
    if(v.status==="done"&&!(old?.doneDate)) v.doneDate=dxb(); if(v.status==="trial"&&!v.trialDate) v.trialDate=dxb(); if(v.status==="live"&&!(old?.postedAt)) v.postedAt=now;
    if(id) await db.doc("videos/"+id).update({...v,updatedAt:now}); else await db.collection("videos").add({repId:viewRep,...v,createdAt:now,updatedAt:now}); toast("Saved."); closeSheet(); return; }
  if(f.id==="statsForm"){ e.preventDefault(); const s={}; STATS.forEach(([k])=>{ const x=$("#st_"+k).value.trim(); if(x!=="") s[k]=+x.replace(/[^\d.]/g,""); }); s.source="manual"; await db.doc("videos/"+f.dataset.id).update({stats:s,statsAt:now,updatedAt:now}); toast("Stats saved."); closeSheet(); return; }
  if(f.id==="flForm"){ e.preventDefault(); const n=+$("#flN").value.replace(/[^\d]/g,""); if(!n) return; await db.doc(`followers/ft_${dxb()}`).set({repId:viewRep,brand:"ft",date:dxb(),followers:n,createdAt:now}); toast("Followers logged."); closeSheet(); return; }
  if(f.id==="liveForm"){ e.preventDefault(); const nowFlag=e.submitter?.dataset.now==="1"; const at=$("#lvAt").value; const v=videos.find(x=>x.id===f.dataset.id);
    await db.doc("videos/"+v.id).update(nowFlag?{status:"live",postedAt:now,postAt:at,updatedAt:now}:{postAt:at,updatedAt:now});
    if(nowFlag){ const others=videos.filter(x=>x.id!==v.id&&x.brand==="ft"&&x.trialDate===v.trialDate&&x.status==="trial"); for(const o of others) await db.doc("videos/"+o.id).update({status:"dropped",updatedAt:now}); }
    toast(nowFlag?"Live. Log its stats tomorrow.":"Scheduled."); closeSheet(); return; }
  if(f.id==="clForm"){ e.preventDefault(); const c={name:$("#cName").value.trim(),package:segVal("#cPkg")||"Growth",contact:$("#cContact").value.trim(),phone:$("#cPhone").value.trim(),notes:$("#cNotes").value.trim()}; c.quota=PKGQ[c.package]; if(!c.name) return;
    if(f.dataset.id) await db.doc("clients/"+f.dataset.id).update({...c,updatedAt:now}); else await db.collection("clients").add({...c,createdAt:now}); toast("Client saved."); closeSheet(); return; }
  if(f.id==="shForm"){ e.preventDefault(); const cid=$("#shClient").value; const c=clients.find(x=>x.id===cid); const kit={}; document.querySelectorAll("[data-kit]").forEach(x=>kit[x.dataset.kit]=x.checked);
    const s={clientId:cid,client:cid==="__yontro"?"Yontro.ae":(c?.name||""),date:$("#shDate").value,time:$("#shTime").value,location:$("#shLoc").value.trim(),videos:+$("#shVids").value||0,brief:$("#shBrief").value,shotList:$("#shList").value,kit,footageLink:$("#shRaw").value.trim(),editLink:$("#shEdit").value.trim(),notes:$("#shNotes").value};
    if(!s.client) return toast("Pick a client.");
    if(f.dataset.id) await db.doc("shoots/"+f.dataset.id).update({...s,updatedAt:now}); else await db.collection("shoots").add({repId:viewRep,...s,status:"scheduled",createdAt:now,updatedAt:now}); toast(f.dataset.id?"Saved.":"Shoot booked."); closeSheet(); return; }
  if(f.id==="punchForm"){ e.preventDefault(); if(!selfieData){ toast("Take a selfie first."); return; } await punchInWithSelfie($("#pPlace").value.trim()); toast("Punched in. Have a great day."); closeSheet(); return; }
  if(f.id==="punchOutForm"){ e.preventDefault(); const st=shiftState(viewRep,dxb()); if(st.brk) await logEvent("break_end"); await logEvent("punch_out",{place:$("#poPlace").value.trim()}); toast(`Punched out. You worked ${dur(shiftState(viewRep,dxb()).worked)}.`); closeSheet(); setTimeout(()=>dayReportAfterPunchOut(),600); return; }
  if(f.id==="chatForm"){ e.preventDefault(); const v=$("#chatIn").value; $("#chatIn").value=""; john(v); return; }
  }catch(err){ toast("Couldn't save: "+(err?.message||err?.code||"error")); }
});
$("#chatIn").addEventListener("keydown",e=>{ if(e.key==="Enter"&&!e.shiftKey){ e.preventDefault(); $("#chatForm").requestSubmit(); } });
setInterval(()=>{ if(tab==="clients"&&$("#sheetBg").hidden) renderClients(); if(tab==="today"&&$("#sheetBg").hidden&&!document.activeElement?.closest?.("#v-today")) renderToday(); },60000);

/* ---------- boot ---------- */
renderTabs(); renderToday();
(async()=>{
  const timer=setTimeout(()=>{ if(!db){ $("#banner").textContent="Open this page signed in to claude.ai to see your work."; $("#banner").hidden=false; } },10000);
  const C=window.claude;
  const [d,u,s]=await Promise.all([C?.use?.("db"),C?.use?.("user"),C?.use?.("sample")].map(p=>Promise.resolve(p).catch(()=>null)));
  user=u; sample=s||null; downloads=await C?.use?.("downloads")?.catch?.(()=>null)||null; if(!d) return; db=d; clearTimeout(timer);
  try{ me=await user?.id?.(); }catch(_){ me=null; } isOwner=!!(await user?.isOwner?.().catch(()=>false));
  viewRep=me; if(!me){ $("#banner").textContent="Sign in to claude.ai to get your own login."; $("#banner").hidden=false; }
  
  if(isOwner) tab="team";
  const docs=q=>q.docs.map(x=>({id:x.id,...x.data()}));
  const refreshNames=async()=>{ try{ const ids=[...new Set([me,...videos.map(x=>x.repId),...shoots.map(x=>x.repId),...kpis.map(x=>x.repId),...tlog.map(x=>x.repId)].filter(Boolean))]; if(user?.profiles&&ids.length){ const ps=await user.profiles(ids); ids.forEach(i=>{ if(ps?.[i]?.name&&!staffNames[i]) names[i]=ps[i].name; }); } }catch(_){} renderAll(); };
  const onErr=e=>{ $("#banner").textContent="Couldn't load ("+(e?.code||"error")+")."; $("#banner").hidden=false; };
  db.collection("videos").onSnapshot(q=>{ videos=docs(q); if(!$("#sheetBg").hidden&&document.activeElement?.closest?.("#sheet")) { renderTabs(); return; } renderAll(); },onErr);
  db.collection("shoots").onSnapshot(q=>{ shoots=docs(q); renderAll(); },onErr);
  db.collection("clients").onSnapshot(q=>{ clients=docs(q); renderAll(); },onErr);
  db.collection("followers").onSnapshot(q=>{ followers=docs(q); renderAll(); },onErr);
  db.collection("kpi").onSnapshot(q=>{ kpis=docs(q); refreshNames(); },onErr);
  db.collection("timelog").onSnapshot(q=>{ tlog=docs(q); renderAll(); },onErr);
  db.collection("chats").onSnapshot(q=>{ chats=docs(q); if(hzOpen) renderChat(); hzDot(); },onErr);
  db.doc("meta/playbook").onSnapshot(x=>{ playbook=x.exists?(x.data().text||""):""; if(tab==="team") renderTeam(); },()=>{});
  db.doc("meta/goals").onSnapshot(x=>{ if(x.exists) goals={...goals,...x.data()}; renderAll(); },()=>{});
  db.doc("meta/company").onSnapshot(x=>{ company=x.exists?{trn:"",...x.data()}:{trn:""}; },()=>{});
  db.doc("meta/signing").onSnapshot(x=>{ signing={...signing,...(x.exists?x.data():{})}; signingLoaded=true; paperRefresh(); },()=>{ signingLoaded=true; });
  db.collection("queue").onSnapshot(q=>{ queue=docs(q); ownerSubs(); },()=>{});
  if(me){ subApprovals(me); subWell(); db.collection(`data/users/${me}/well/chat`).onSnapshot(q=>{ wchats=docs(q); wLoaded=true; hzDot(); if(hzOpen&&mode==="well") renderChat(); weekendCheck(); },()=>{}); setTimeout(()=>{ try{ wellTick(); }catch(_){} },4000); }
  refreshNames(); subStaff(); setTimeout(()=>{ tourAuto().catch(()=>{}); },2500);
})();

/* refresh the screen whenever a form closes: data that arrived while it was open is shown straight away */
(()=>{ const bg=document.getElementById("sheetBg"); if(!bg) return; new MutationObserver(()=>{ if(bg.hidden){ try{ renderAll(); }catch(_){} } }).observe(bg,{attributes:true,attributeFilter:["hidden"]}); })();
