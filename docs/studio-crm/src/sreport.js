/* ---------- John's end-of-day report ---------- */
const DR={}, drSubs={}; let drBusy=false;
function subDayReports(uid){ if(!uid||drSubs[uid]||!db) return; drSubs[uid]=1;
  db.collection(`dayreports/${uid}/days`).onSnapshot(q=>{ const first=DR[uid]===undefined; DR[uid]=q.docs.map(x=>({id:x.id,...x.data()})); if(first&&uid===me) setTimeout(()=>dayReportCatchUp().catch(()=>{}),3000); if(tab==="today") renderToday(); if(tab==="team") renderTeamReports(); },()=>{}); }
function scoreMD(s){ const mark=(v,t)=>v>=t?"✓ On target":v>0?"▲ Partly":"✗ Missed";
  return `| | Target | Today | |
|---|---|---|---|
| Founder Tales trial reels | ${goals.trials} | ${s.trials} | ${mark(s.trials,goals.trials)} |
| Best trial posted live | ${goals.live} | ${s.live} | ${mark(s.live,goals.live)} |
| Yontro.ae video | ${goals.yontro} | ${s.yontro} | ${mark(s.yontro,goals.yontro)} |
| Client edits on time | all | ${s.editsMet} on time${s.editsMissed?`, ${s.editsMissed} late`:""} | ${s.editsMissed?"✗ Late":"✓"} |
| Videos delivered to clients | – | ${s.delivered} | |
| Followers (Founder Tales) | +${s.needPerDay??"?"} a day | ${s.followers!=null?s.followers.toLocaleString()+(s.gained!=null?` (${s.gained>=0?"+":""}${s.gained})`:""):"Not logged"} | ${s.gained==null?"✗ Log it":s.needPerDay&&s.gained>=s.needPerDay?"✓ On pace":"▲ Behind pace"} |
| Stats for yesterday's videos | all | ${s.needStats?`${s.needStats} missing`:"All logged"} | ${s.needStats?"✗":"✓"} |
| Tomorrow's ideas planned | ${goals.trials} | ${s.ideasTom} (${s.ideasSched} scheduled) | ${mark(Math.min(s.ideasTom,s.ideasSched),goals.trials)} |
| Hours worked | 10:00–19:00 | ${s.worked||"No punch-in"}${s.punchIn?` (${s.punchIn}–${s.punchOut||"no punch-out"})`:""}${s.late?" · late start":""} | ${s.breaks?"Breaks "+s.breaks:""} |
| **Day score** | 80+ | **${s.score}/100** | output ${s.parts.output} · on time ${s.parts.ontime} · growth ${s.parts.growth} · logging ${s.parts.discipline} |`; }
function reportMD(name,s,r){ const L=a=>(a||[]).filter(Boolean).map(x=>`- ${String(x).replace(/\n/g," ")}`).join("\n");
  return `# Daily report · ${name} · ${fmtLong(s.date)}

**${MGR1}'s verdict:** ${r.verdict||""}

${scoreMD(s)}

## What went well
${L(r.well)||"- [add: nothing logged today]"}

## What needs fixing
${L(r.fix)}

## Tomorrow's focus
${L(r.tomorrow)}

${r.note?`*${String(r.note).replace(/\*/g,"")}*`:""}`; }
function ruleReport(s){ const well=[],fix=[];
  if(s.trials>=goals.trials) well.push(`Made all ${s.trials} trial reels.`); else fix.push(`${s.trials} of ${goals.trials} trial reels. Film both before 14:00.`);
  if(s.live) well.push("Posted yesterday's winner live."); else fix.push("No trial reel went live. Pick the winner first thing.");
  if(s.yontro) well.push("Yontro.ae video done."); else fix.push("No Yontro.ae video today.");
  if(s.editsMissed) fix.push(`${s.editsMissed} client edit${s.editsMissed>1?"s":""} late. Block edit time right after each shoot.`);
  if(s.followers==null) fix.push("Log the follower count every day.");
  return {verdict:s.score>=80?"Strong day.":"Below target today. Fixable tomorrow.",well,fix,tomorrow:["Post yesterday's best trial live before 11:00.",`Film ${goals.trials} trial reels before 14:00.`,"Log stats and followers before you punch out."],note:""}; }
async function makeDayReport(rep,date,opts={}){ const s=dayStats(rep,date); const name=names[rep]||"Videographer"; let r=null;
  if(sample){ try{ r=await sample.json(`You are ${MGR}, Head of Production at Yontro (Dubai), writing the end-of-day performance report on ${name} (videographer) for both him and Sahill (the owner). His daily targets: ${goals.trials} Founder Tales trial reels, post yesterday's best trial live, ${goals.yontro} Yontro.ae video, client first edits within 48 hours of a shoot and revisions within 24 hours, stats and follower count logged, ${goals.trials} ideas planned for tomorrow with post times. Founder Tales goal: ${goals.ftTarget} followers by ${goals.ftDate}.
TODAY'S DATA (the only facts you may use): ${JSON.stringify(s)}
${studioContext().split("\n").filter(l=>/^TOP|^CLIENT|^UPCOMING/.test(l)).join("\n")}
Write like a fair, direct creative manager: specific, numbers-based, warm but honest. Name real videos, hooks, clients and numbers from the data. Never invent numbers. If something wasn't logged, say so plainly. Each bullet one short sentence.
Return JSON only: {"verdict":"one line, max 15 words","well":["2-4 bullets"],"fix":["2-4 bullets, each with the concrete fix"],"tomorrow":["exactly 3 specific actions"],"note":"one encouraging line to ${name.split(" ")[0]}"}`,{modelTier:"default",cache:false}); }catch(_){ r=null; } }
  if(!r||!r.verdict) r=ruleReport(s);
  const doc={repId:rep,date,verdict:String(r.verdict||""),body:reportMD(name,s,r),stats:{score:s.score,trials:s.trials,live:s.live,yontro:s.yontro,editsMet:s.editsMet,editsMissed:s.editsMissed,followers:s.followers,gained:s.gained,worked:s.worked||""},by:opts.by||"john",createdAt:Date.now()};
  await db.doc(`dayreports/${rep}/days/${date}`).set(doc); return doc; }
function openDayReport(d){ openS(`<div class="head"><h2 id="sheetTitle">${MGR1}'s report · ${esc(fmtD(d.date))}</h2><button class="btn ghost sm" type="button" data-close>Close</button></div>
  <div class="tag">${esc(names[d.repId]||"")} · shared with ${esc((names[d.repId]||"him").split(" ")[0])} and Sahill</div>${paperHTML({type:"Daily report",body:d.body})}
  <div class="btnrow">${downloads?`<button class="btn or" type="button" data-drdl="${esc(d.repId)}|${esc(d.date)}">Download</button>`:""}${d.repId===me||isOwner?`<button class="btn" type="button" data-drredo="${esc(d.repId)}|${esc(d.date)}">Ask ${MGR1} to rewrite it</button>`:""}</div>`); }
function renderDayReport(){ const el=$("#reportCard"); if(!el) return; const st=viewRep?shiftState(viewRep,dxb()):null; const today=(DR[viewRep]||[]).find(r=>r.date===dxb());
  if(today){ el.hidden=false; el.innerHTML=`<div class="coach"><div class="av" aria-hidden="true">J</div><div style="flex:1;min-width:0"><h2>${MGR1}'s report on today</h2><div class="tag">Score ${esc(today.stats?.score??"–")}/100</div></div><button class="btn or sm" type="button" data-dropen="${esc(today.repId)}|${esc(today.date)}">Read</button></div><div style="font-size:14.5px">${esc(today.verdict||"")}</div>`; return; }
  if(st&&st.outAt&&viewRep===me){ el.hidden=false; el.innerHTML=`<div class="coach"><div class="av" aria-hidden="true">J</div><div style="flex:1"><h2>Your day is done</h2><div class="tag">${MGR1} writes your report when you punch out.</div></div><button class="btn or sm" type="button" data-drmake>Get it now</button></div>`; return; }
  el.hidden=true; }
function renderTeamReports(){ const el=$("#teamDayReports"); if(!el||!isOwner) return; const all=[]; for(const u in DR) DR[u].forEach(d=>all.push(d)); all.sort((a,b)=>b.date.localeCompare(a.date)||(b.createdAt||0)-(a.createdAt||0));
  el.innerHTML=all.length?all.slice(0,20).map(d=>`<button type="button" class="item" style="text-align:left;width:100%;cursor:pointer" data-dropen="${esc(d.repId)}|${esc(d.date)}"><span class="ic">${ICON.coach}</span><div style="min-width:0"><div class="t">${esc(names[d.repId]||"")} · ${esc(fmtD(d.date))} · ${esc(d.stats?.score??"–")}/100</div><div class="s">${esc(d.stats?.trials??0)} trials · ${esc(d.stats?.live??0)} live · ${esc(d.stats?.yontro??0)} Yontro · ${esc(d.verdict||"")}</div></div><span class="stage">Open</span></button>`).join(""):`<div class="empty">${MGR1} writes a report each time Azeem punches out. If he forgets, it's written at 20:53.</div>`; }
async function dayReportAfterPunchOut(){ if(!me||viewRep!==me||drBusy) return; drBusy=true; toast(`${MGR1} is writing your report on today…`);
  try{ const d=await makeDayReport(me,dxb()); document.querySelectorAll(".toast").forEach(t=>t.remove()); openDayReport(d); }catch(e){ toast(`${MGR1} couldn't write the report: `+(e?.message||e?.code||"error")); } drBusy=false; }
async function dayReportCatchUp(){ if(!me||isOwner||drBusy) return; const L=DR[me]; if(L===undefined) return; const t=dxb();
  for(let i=1;i<=3;i++){ const d=addDays(t,-i); if(tlog.some(e=>e.repId===me&&e.date===d&&e.kind==="punch_in")&&!L.some(x=>x.date===d)){ drBusy=true; try{ await makeDayReport(me,d,{by:"john-catchup"}); }catch(_){} drBusy=false; } } }
document.addEventListener("click",async e=>{ const b=e.target.closest("[data-dropen],[data-drdl],[data-drredo],[data-drmake]"); if(!b) return; const d=b.dataset;
  const find=k=>{ const [u,dt]=k.split("|"); return (DR[u]||[]).find(x=>x.date===dt); };
  if(d.dropen){ const r=find(d.dropen); if(r) openDayReport(r); return; }
  if(d.drdl){ const r=find(d.drdl); if(!r||!downloads) return; try{ await downloads.save({filename:`Yontro studio report - ${names[r.repId]||""} - ${r.date}.html`,data:new Blob([brandedFile({title:"Daily report "+r.date,type:"Daily report",body:r.body})],{type:"text/html"})}); }catch(_){} return; }
  if(d.drredo){ const [u,dt]=d.drredo.split("|"); b.disabled=true; b.textContent=`${MGR1} is rewriting…`; try{ const r=await makeDayReport(u,dt); openDayReport(r); }catch(err){ toast("Couldn't rewrite it."); b.disabled=false; } return; }
  if(d.drmake!==undefined){ dayReportAfterPunchOut(); return; }
});
