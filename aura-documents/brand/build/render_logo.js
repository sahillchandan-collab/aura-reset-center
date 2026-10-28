const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:4});
for(const v of ['light','dark']){await p.goto('file://'+path.resolve('logo.html')+'?v='+v);await p.evaluate(()=>document.fonts.ready);
await (await p.$('#logo')).screenshot({path:`../logo-${v}.png`,omitBackground:true});}
await b.close();})();
