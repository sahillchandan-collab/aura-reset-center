seed=r"""
const T=new Date().toLocaleDateString("en-CA",{timeZone:"Asia/Dubai"}); const add=n=>{const d=new Date(T+"T12:00:00"); d.setDate(d.getDate()+n); return d.toLocaleDateString("en-CA");};
const now=Date.now(), H=3600e3, M=60e3, U="u1";
const store={videos:{
 v1:{repId:U,brand:"ft",status:"trial",title:"Why Elon named it Tesla",hook:"Elon didn't start Tesla. He bought the name for $75,000.",concept:"Tesla Motors was founded by Eberhard and Tarpenning; Musk invested later and later paid for the trademark.",trialDate:add(-1),stats:{views:8420,reach:7900,likes:612,comments:41,shares:188,saves:96,follows:57,wtr:38,avgWatch:14,duration:37},statsAt:now-2*H,createdAt:now-30*H,updatedAt:now-2*H},
 v2:{repId:U,brand:"ft",status:"trial",title:"The fisherman who out-thought a banker",hook:"A Harvard MBA told a fisherman how to get rich. The fisherman laughed.",concept:"The classic parable retold in 30 seconds, Dubai twist at the end.",trialDate:add(-1),stats:{views:3110,reach:2950,likes:240,comments:12,shares:31,saves:22,follows:9,wtr:27,avgWatch:9,duration:41},statsAt:now-2*H,createdAt:now-30*H,updatedAt:now-2*H},
 v3:{repId:U,brand:"ft",status:"live",title:"Jan Koum: from food stamps to $19 billion",hook:"He signed the WhatsApp deal on the door of the welfare office he used to queue at.",trialDate:add(-3),postedAt:now-48*H,stats:{views:15200,reach:14100,likes:1302,comments:88,shares:410,saves:220,follows:131,wtr:44,avgWatch:16,duration:36},statsAt:now-20*H,createdAt:now-80*H,updatedAt:now-20*H},
 v4:{repId:U,brand:"ft",status:"trial",title:"Phil Knight's $50 logo",hook:"Nike's swoosh cost $35. Then he gave her shares.",trialDate:T,createdAt:now-3*H,updatedAt:now-3*H},
 v5:{repId:U,brand:"ft",status:"idea",title:"Brian Acton: rejected by Facebook, sold to Facebook",hook:"Facebook rejected him. Five years later they paid him $3.6 billion.",planFor:add(1),postAt:add(1)+"T19:00",createdAt:now-H,updatedAt:now-H},
 v6:{repId:U,brand:"yontro",status:"done",title:"3 mistakes Dubai restaurants make on Instagram",doneDate:add(-1),createdAt:now-30*H,updatedAt:now-26*H},
 v7:{repId:U,brand:"ft",status:"dropped",title:"Why McDonald's is a real estate company",hook:"McDonald's doesn't sell burgers. It sells land.",trialDate:add(-3),stats:{views:2900,follows:6,shares:20,wtr:22},statsAt:now-50*H,createdAt:now-80*H,updatedAt:now-48*H}},
clients:{c1:{name:"Al Noor Beauty Salon",package:"Growth",quota:10,contact:"Sara",phone:"050 412 7781",notes:"Bridal and facials. Staff shy on camera.",createdAt:1},c2:{name:"FitZone Gym",package:"Launch",quota:5,contact:"Omar",notes:"Energetic, member transformations.",createdAt:2}},
shoots:{s1:{repId:U,clientId:"c1",client:"Al Noor Beauty Salon",date:add(-1),time:"11:00",location:"Al Noor Beauty Salon, JLT",videos:4,status:"shot",shotAt:now-31*H,dueAt:now+17*H,brief:"Bridal season push",kit:{bat:true,cards:true,mic:true},createdAt:now-50*H,updatedAt:now-31*H},
 s2:{repId:U,clientId:"c2",client:"FitZone Gym",date:T,time:"17:00",location:"FitZone Gym, Business Bay",videos:3,status:"scheduled",brief:"3 member transformation reels",createdAt:now-20*H,updatedAt:now-20*H},
 s3:{repId:U,clientId:"c2",client:"FitZone Gym",date:add(-6),time:"10:00",location:"FitZone Gym, Business Bay",videos:2,status:"delivered",shotAt:now-6*24*H,dueAt:now-4*24*H,sentAt:now-4.5*24*H,revisions:[{askedAt:now-4*24*H,dueAt:now-3*24*H,doneAt:now-3.4*24*H}],approvedAt:now-3*24*H,deliveredAt:now-3*24*H,delivered:2,createdAt:now-8*24*H}},
followers:{},timelog:{e1:{repId:U,date:T,kind:"punch_in",at:now-5*H,place:"Office"},e0:{repId:U,date:add(-1),kind:"punch_in",at:now-29*H,place:"Office"},e00:{repId:U,date:add(-1),kind:"punch_out",at:now-20*H}},kpi:{},chats:{}};
const F=[1702,1716,1731,1745,1779,1801,1858,1871]; F.forEach((n,i)=>{ const d=add(i-8+1); if(i<7) store.followers["ft_"+d]={repId:U,brand:"ft",date:d,followers:n}; });
"""
demo=r"""
/* ---------- PREVIEW MODE ---------- */
const DEMO_AS=(()=>{ try{ return localStorage.getItem("sdemoAs")||"rep"; }catch(_){ return "rep"; } })();
const DEMO_CLAUDE=(()=>{ const real=window.claude;
  const fresh=()=>{ """+seed+r""" const S={}; for(const c in store) for(const id in store[c]) S[c+"/"+id]=store[c][id]; return S; };
  let S=null; try{ const raw=localStorage.getItem("sdemoStore"); if(raw) S=JSON.parse(raw); }catch(_){} if(!S) S=fresh();
  const save=()=>{ try{ localStorage.setItem("sdemoStore",JSON.stringify(S)); }catch(_){} };
  const L=[]; let n=0;
  const colDocs=p=>{ const k=p.split("/").length; return Object.keys(S).filter(x=>x.startsWith(p+"/")&&x.split("/").length===k+1).map(x=>({id:x.split("/").pop(),data:()=>S[x],exists:true})); };
  const fire=()=>{ save(); L.forEach(l=>setTimeout(()=>l.c?l.f({docs:colDocs(l.p)}):l.f(S[l.p]?{exists:true,data:()=>S[l.p]}:{exists:false}),5)); };
  const chk=(p,odd)=>{ if((p.split("/").length%2===1)!==odd) throw new Error("bad path "+p); };
  const cl=d=>JSON.parse(JSON.stringify(d));
  const doc=p=>(chk(p,false),{id:p.split("/").pop(),onSnapshot:f=>{L.push({p,f});setTimeout(()=>f(S[p]?{exists:true,data:()=>S[p]}:{exists:false}),20);return()=>{}},get:async()=>S[p]?{exists:true,data:()=>S[p]}:{exists:false},set:async d=>{S[p]=cl(d);fire()},update:async d=>{if(!S[p])throw new Error("not found");S[p]={...S[p],...cl(d)};fire()},["del"+"ete"]:async()=>{Reflect.deleteProperty(S,p);fire()}});
  const col=p=>(chk(p,true),{orderBy:()=>col(p),limit:()=>col(p),where:()=>col(p),onSnapshot:f=>{L.push({p,f,c:1});setTimeout(()=>f({docs:colDocs(p)}),20);return()=>{}},add:async d=>{const id="d"+Date.now().toString(36)+(++n);S[p+"/"+id]=cl(d);fire();return{id}},doc:id=>doc(p+"/"+id)});
  const owner=DEMO_AS==="owner"; const meId=owner?"u0":"u1";
  const user={me:async()=>({name:owner?"Sahill Chandan":"Azeem Shafi"}),id:async()=>meId,isOwner:async()=>owner,canEdit:async()=>owner,profiles:async()=>({u1:{name:"Azeem Shafi"},u0:{name:"Sahill Chandan"}})};
  return {use:async nm=>nm==="db"?{collection:col,doc}:nm==="user"?user:(real?.use?real.use(nm):null)};
})();
(()=>{ const d=document.createElement("div"); d.className="demobar";
  d.innerHTML=`<b>Preview</b><span>Sample data, saved only in this browser. John is live.</span><span class="demosw"><button type="button" data-demoas="rep" aria-pressed="${DEMO_AS!=="owner"}">Azeem's view</button><button type="button" data-demoas="owner" aria-pressed="${DEMO_AS==="owner"}">Sahill's view</button><button type="button" data-demoreset>Reset</button></span>`;
  document.body.prepend(d);
  d.addEventListener("click",e=>{ const b=e.target.closest("button"); if(!b) return; try{ if(b.dataset.demoas) localStorage.setItem("sdemoAs",b.dataset.demoas); if(b.dataset.demoreset!==undefined){ localStorage.removeItem("sdemoStore"); ["hzSeen","morningTry","wkTry","medSnooze","tourOff_u1","tourOff_u0"].forEach(k=>localStorage.removeItem(k)); } }catch(_){} location.reload(); }); })();
"""
css=""".demobar{position:relative;z-index:12;background:#FF5A1F;color:#111;font-size:12.5px;padding:7px max(16px,env(safe-area-inset-left,0px));display:flex;gap:8px 12px;align-items:center;flex-wrap:wrap}.demobar b{font-family:var(--display);font-weight:900;text-transform:uppercase;letter-spacing:.06em}.demosw{display:flex;gap:6px;margin-left:auto}.demosw button{border:1.5px solid #111;background:transparent;color:#111;border-radius:99px;padding:3px 10px;font-weight:700;font-size:12px}.demosw button[aria-pressed="true"]{background:#111;color:#fff}
"""
p="/home/user/aura-reset-center/docs/studio-crm/yontro-studio.html"; s=open(p).read()
def R(a,b):
    global s; assert s.count(a)==1,a; s=s.replace(a,b)
R("<title>yontro.ae · Studio</title>","<title>Yontro Studio Preview</title>")
R("</style>\n<header",css+"</style>\n<header")
R("/* ---------- boot ---------- */",demo+"\n/* ---------- boot ---------- */")
R("const C=window.claude;","const C=DEMO_CLAUDE;")
open("/home/user/aura-reset-center/docs/studio-crm/yontro-studio-preview.html","w").write(s); print(len(s))
