/* ---------- period metrics (studio) ---------- */
const PR_MGR="John Smith, Head of Production", PR_ROLE="Videographer", PR_BY="john";
const PR_TARGETS=`per working day: ${goals.trials} Founder Tales trial reels, the best trial posted live, ${goals.yontro} Yontro.ae video, stats and followers logged, 2 ideas planned for tomorrow; client first edits within 48 hours of a shoot and revisions within 24 hours; Founder Tales goal ${goals.ftTarget} followers by ${goals.ftDate}; 10:00 to 19:00.`;
const PR_SCORING="The rating is the average daily score over the days worked (40% Founder Tales output, 30% client edits on time, 20% follower growth vs the pace needed, 10% check-ins and stats logged), out of 10.";
function periodMetrics(rep,start,end){ const days=workedDays(rep,start,end); const att=attendance(rep,days); const n=Math.max(1,days.length);
  const D=days.map(d=>dayStats(rep,d)); const sum=k=>D.reduce((a,x)=>a+(+x[k]||0),0);
  const V=videos.filter(v=>v.repId===rep), S=shoots.filter(s=>s.repId===rep);
  const inR=d=>d&&d>=start&&d<=end;
  const trials=V.filter(v=>v.brand==="ft"&&inR(v.trialDate)&&["trial","live","dropped"].includes(v.status));
  const live=V.filter(v=>v.brand==="ft"&&v.status==="live"&&inR(dOf(v.postedAt)));
  const yon=V.filter(v=>v.brand==="yontro"&&v.status==="done"&&inR(v.doneDate));
  const withStats=[...trials,...live].filter((v,i,a)=>v.stats&&a.indexOf(v)===i);
  const tot=k=>withStats.reduce((a,v)=>a+(+v.stats[k]||0),0);
  const liveW=live.filter(v=>v.stats&&v.stats.wtr); const avgW=liveW.length?Math.round(liveW.reduce((a,v)=>a+(+v.stats.wtr||0),0)/liveW.length):null;
  const top=withStats.slice().sort((a,b)=>vScore(b)-vScore(a)).slice(0,5).map(v=>({title:v.title,hook:v.hook||"",views:+v.stats.views||0,follows:+v.stats.follows||0,shares:+v.stats.shares||0,wtr:v.stats.wtr??null,live:v.status==="live"}));
  const worst=withStats.slice().sort((a,b)=>vScore(a)-vScore(b)).slice(0,2).map(v=>({title:v.title,views:+v.stats.views||0,follows:+v.stats.follows||0,wtr:v.stats.wtr??null}));
  const Sp=S.filter(s=>inR(dOf(s.shotAt))); const checks=Sp.flatMap(shootOnTime); const onT=checks.filter(Boolean).length;
  const apv=Sp.filter(s=>["approved","delivered"].includes(s.status)); const revs=Sp.reduce((a,s)=>a+(s.revisions||[]).length,0);
  const del=S.filter(s=>inR(dOf(s.deliveredAt))); const perClient={}; del.forEach(s=>{ perClient[s.client]=(perClient[s.client]||0)+(+s.delivered||+s.videos||0); });
  const quotas=clients.map(c=>({client:c.name,package:c.package,quota:+c.quota||PKGQ[c.package]||0,delivered:perClient[c.name]||0}));
  const F=followers.slice().sort((a,b)=>a.date.localeCompare(b.date)); const fStart=F.filter(f=>f.date<start).slice(-1)[0]||F.find(f=>f.date>=start); const fEnd=F.filter(f=>f.date<=end).slice(-1)[0];
  const gained=fStart&&fEnd?fEnd.followers-fStart.followers:null; const calDays=Math.max(1,Math.round((new Date(end+"T12:00:00")-new Date(start+"T12:00:00"))/864e5)+1);
  const daysLeft=fEnd?Math.max(1,Math.round((new Date(goals.ftDate+"T12:00:00")-new Date(end+"T12:00:00"))/864e5)):null;
  const best=D.slice().sort((a,b)=>b.score-a.score)[0], low=D.slice().sort((a,b)=>a.score-b.score)[0];
  return {start,end,attendance:att,avgDayScore:D.length?Math.round(D.reduce((a,x)=>a+x.score,0)/D.length):0,
    parts:{output:D.length?Math.round(D.reduce((a,x)=>a+x.parts.output,0)/D.length):0,ontime:D.length?Math.round(D.reduce((a,x)=>a+x.parts.ontime,0)/D.length):0,growth:D.length?Math.round(D.reduce((a,x)=>a+x.parts.growth,0)/D.length):0,discipline:D.length?Math.round(D.reduce((a,x)=>a+x.parts.discipline,0)/D.length):0},
    trials:trials.length,trialsTarget:goals.trials*days.length,live:live.length,liveTarget:goals.live*days.length,yontro:yon.length,yontroTarget:goals.yontro*days.length,
    trialToLive:trials.length?Math.round(live.filter(v=>trials.includes(v)).length/trials.length*100):null,
    views:tot("views"),reach:tot("reach"),likes:tot("likes"),comments:tot("comments"),shares:tot("shares"),saves:tot("saves"),followsFromVideos:tot("follows"),avgWatchThroughLive:avgW,videosWithStats:withStats.length,videosMissingStats:[...trials,...live].filter(v=>!v.stats).length,
    topVideos:top,weakestVideos:worst,
    followersStart:fStart?.followers??null,followersEnd:fEnd?.followers??null,followersGained:gained,followersPerDay:gained!=null?Math.round(gained/calDays*10)/10:null,neededPerDayNow:fEnd?Math.ceil(Math.max(0,goals.ftTarget-fEnd.followers)/daysLeft):null,goal:goals.ftTarget,goalDate:goals.ftDate,
    shoots:Sp.length,editDeadlines:checks.length,editsOnTime:onT,editsLate:checks.length-onT,onTimeRate:checks.length?Math.round(onT/checks.length*100):null,revisionRounds:revs,firstTimeApprovals:apv.filter(s=>!(s.revisions||[]).length).length,approved:apv.length,videosDelivered:del.reduce((a,s)=>a+(+s.delivered||+s.videos||0),0),clientQuotas:quotas,
    checkins:kpis.filter(k=>k.repId===rep&&k.date>=start&&k.date<=end).length,ideasPlanned:V.filter(v=>v.brand==="ft"&&inR(dOf(v.createdAt))&&v.planFor).length,
    bestDay:best?{date:best.date,score:best.score}:null,lowestDay:low?{date:low.date,score:low.score}:null}; }
function periodScore(m){ return Math.round(m.avgDayScore)/10; }
function metricsMD(m,kind){ const pct=(a,b)=>b?Math.round(a/b*100)+"%":"–"; const a=m.attendance; const nn=x=>x==null?"–":Number(x).toLocaleString("en-US");
  return `## Output against target
| | Target | Actual | Hit |
|---|---|---|---|
| Founder Tales trial reels | ${m.trialsTarget} | ${m.trials} | ${pct(m.trials,m.trialsTarget)} |
| Trial reels posted live | ${m.liveTarget} | ${m.live} | ${pct(m.live,m.liveTarget)} |
| Yontro.ae videos | ${m.yontroTarget} | ${m.yontro} | ${pct(m.yontro,m.yontroTarget)} |
| Client edits on time | all | ${m.editsOnTime} of ${m.editDeadlines} | ${m.onTimeRate==null?"–":m.onTimeRate+"%"} |

## Founder Tales growth
| Followers start | Followers end | Gained | A day | Needed a day now | Goal |
|---|---|---|---|---|---|
| ${nn(m.followersStart)} | ${nn(m.followersEnd)} | ${m.followersGained==null?"–":(m.followersGained>=0?"+":"")+nn(m.followersGained)} | ${nn(m.followersPerDay)} | ${nn(m.neededPerDayNow)} | ${nn(m.goal)} by ${fmtShort(m.goalDate)} |

## Video performance (${m.videosWithStats} videos with stats${m.videosMissingStats?`, ${m.videosMissingStats} missing`:""})
| Views | Reach | Likes | Comments | Shares | Saves | Follows | Avg watch-through (live) | Trial → live |
|---|---|---|---|---|---|---|---|---|
| ${nn(m.views)} | ${nn(m.reach)} | ${nn(m.likes)} | ${nn(m.comments)} | ${nn(m.shares)} | ${nn(m.saves)} | ${nn(m.followsFromVideos)} | ${m.avgWatchThroughLive==null?"–":m.avgWatchThroughLive+"%"} | ${m.trialToLive==null?"–":m.trialToLive+"%"} |
${m.topVideos.length?`
**Top videos**

| Video | Views | Follows | Shares | Watch-through |
|---|---|---|---|---|
${m.topVideos.map(v=>`| ${esc(v.title)}${v.live?" (live)":""} | ${nn(v.views)} | ${nn(v.follows)} | ${nn(v.shares)} | ${v.wtr==null?"–":v.wtr+"%"} |`).join("\n")}
`:""}
## Client work
| Shoots | Edit deadlines met | Late | Revision rounds | Approved first time | Videos delivered |
|---|---|---|---|---|---|
| ${m.shoots} | ${m.editsOnTime} | ${m.editsLate} | ${m.revisionRounds} | ${m.firstTimeApprovals} of ${m.approved} | ${m.videosDelivered} |
${kind==="month"&&m.clientQuotas.length?`
| Client | Package | Videos owed | Delivered |
|---|---|---|---|
${m.clientQuotas.map(q=>`| ${esc(q.client)} | ${esc(q.package||"")} | ${q.quota} | ${q.delivered} |`).join("\n")}
`:""}
## Attendance and discipline
| Days worked | Average start | Late starts | Hours worked | Hours a day | Check-ins | Average day score |
|---|---|---|---|---|---|---|
| ${a.days} | ${a.avgStart} | ${a.late} | ${a.hours} | ${a.avgHours} | ${m.checkins} of ${a.days} | ${m.avgDayScore}/100 |

Score parts (average): output ${m.parts.output} · edits on time ${m.parts.ontime} · growth ${m.parts.growth} · logging ${m.parts.discipline}.${m.bestDay?` Best day: **${fmtD(m.bestDay.date)}** (${m.bestDay.score}/100). Lowest: ${fmtD(m.lowestDay.date)} (${m.lowestDay.score}/100).`:""}`; }
