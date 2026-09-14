// Run with Playwright available through NODE_PATH. Starts no services and publishes nothing.
const {chromium} = require('playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const base=process.env.ATLAS_PREVIEW_URL||'http://127.0.0.1:8874/ai-legislation/';
const out=process.env.ATLAS_REVIEW_DIR||'/tmp/aegises-ai-review';
const assert=(condition,message)=>{if(!condition)throw Error(message)};
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:process.env.ATLAS_CHROME||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base,{waitUntil:'networkidle'});
 const counts=await page.evaluate(()=>({states:document.querySelectorAll('.state-record').length,figures:document.querySelectorAll('figure').length,missingAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.hash.slice(1)).filter(id=>id&&!document.getElementById(id))}));
 assert(counts.states===51&&counts.figures===6,'Incorrect atlas counts');assert(!counts.missingAnchors.length,'Broken internal anchors');
 await page.locator('#state-search').fill('Colorado');assert(await page.locator('.state-record:visible').count()===1,'Search must return Colorado');
 await page.locator('#state-search').fill('zz-no-matching-state');assert(await page.locator('.filter-empty').isVisible(),'Empty-result recovery message missing');
 await page.locator('button[type=reset]').click();await page.waitForFunction(()=>document.querySelectorAll('.state-record:not([hidden])').length===51);assert(await page.locator('.state-record:visible').count()===51,'Reset must restore ledger');
 await page.locator('#pathway-filter').selectOption('rights');assert(await page.locator('.state-record:visible').count()===4,'Pathway filter mismatch');
 await page.locator('#findings a[href="#state-CO"]').click();assert(await page.locator('#state-CO').isVisible(),'Citation must reveal a filtered state');
 const localFiles=await page.evaluate(()=>[...new Set([...document.querySelectorAll('a[href],img[src]')].map(e=>e.getAttribute('href')||e.getAttribute('src')).filter(u=>u&&!/^(https?:|#|mailto:|\/)/.test(u)))]);
 for(const rel of localFiles){if(rel.endsWith('social-preview.png'))continue;const r=await page.request.get(new URL(rel,base).href);assert(r.ok(),`Missing local download: ${rel}`);}
 const svgReport=[];
 for(const file of fs.readdirSync(path.join(root,'assets')).filter(x=>x.endsWith('.svg'))){
  await page.goto(base+'assets/'+file);
  const audit=await page.evaluate(()=>{const texts=[...document.querySelectorAll('text')].map(t=>({t:t.textContent,b:t.getBBox()}));const bounds=document.querySelector('svg').viewBox.baseVal;const clip=texts.filter(x=>x.b.x<0||x.b.y<0||x.b.x+x.b.width>bounds.width+.1||x.b.y+x.b.height>bounds.height+.1).map(x=>x.t);const overlaps=[];for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){const a=texts[i].b,b=texts[j].b;if(a.x<b.x+b.width-1&&a.x+a.width>b.x+1&&a.y<b.y+b.height-1&&a.y+a.height>b.y+1)overlaps.push([texts[i].t,texts[j].t]);}return {clip,overlaps};});
  svgReport.push({file,...audit});assert(!audit.clip.length,`Clipped text in ${file}`);assert(!audit.overlaps.length,`Overlapping text in ${file}: ${JSON.stringify(audit.overlaps)}`);
  await require('sharp')(path.join(root,'assets',file)).resize({width:1200}).png().toFile(path.join(out,file.replace('.svg','.png')));
 }
 await page.goto(base,{waitUntil:'networkidle'});await page.screenshot({path:path.join(out,'hero.png')});
 await page.setViewportSize({width:1200,height:630});
 // A separate social plate avoids clipping a live publication screenshot.
 await page.setContent('<html><head><style>body{margin:0;background:#102c39;color:#f5f6f0;font-family:Arial}main{padding:55px 64px}.brand{letter-spacing:5px;font-size:18px}.kicker{margin-top:50px;color:#43c1b5;font-size:13px;letter-spacing:2px}h1{font:84px/1.03 Georgia;margin:23px 0}p{font:27px/1.4 Georgia;color:#c9dedd;margin:0}.meta{border-top:1px solid #35505b;margin-top:40px;padding-top:22px;font-size:12px;letter-spacing:1px;color:#b2c6c9}</style></head><body><main><div class="brand">AEGISES</div><div class="kicker">STATE AI LEGISLATIVE MATURITY ATLAS</div><h1>Beyond the bill count<span style="color:#43c1b5">.</span></h1><p>The maturity of AI legislation across the United States.</p><div class="meta">50 STATES + DC &nbsp;&nbsp; / &nbsp;&nbsp; SIX ANALYTICAL FIGURES &nbsp;&nbsp; / &nbsp;&nbsp; SEPTEMBER 2026</div></main></body></html>');
 await page.screenshot({path:path.join(root,'assets/social-preview.png')});
 await page.setViewportSize({width:390,height:844});await page.goto(base,{waitUntil:'networkidle'});await page.screenshot({path:path.join(out,'mobile.png')});
 assert(await page.evaluate(()=>document.body.scrollWidth<=innerWidth),'Mobile page overflow');
 await page.setViewportSize({width:768,height:1024});await page.reload({waitUntil:'networkidle'});assert(await page.evaluate(()=>document.body.scrollWidth<=innerWidth),'Tablet page overflow');
 await page.setViewportSize({width:1440,height:1100});await page.goto(base,{waitUntil:'networkidle'});
 await page.pdf({path:path.join(root,'state-ai-legislative-maturity.pdf'),format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:8px;width:100%;margin:0 15mm;color:#597078;display:flex;justify-content:space-between"><span>AEGISES · STATE AI LEGISLATIVE MATURITY · 14 SEP 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',preferCSSPageSize:true});
 const nojs=await browser.newPage({javaScriptEnabled:false});await nojs.goto(base);assert(await nojs.locator('.state-record').count()===51,'No-JavaScript ledger missing');await nojs.close();
 assert(!errors.length,'Browser errors: '+errors.join('; '));
 const report={checked_at:new Date().toISOString(),preview:base,counts,local_files:localFiles.length,svg_text_audit:svgReport,search:true,empty_recovery:true,filter:true,citation_recovery:true,mobile_390:true,tablet_768:true,no_javascript_content:true,browser_errors:errors};
 fs.writeFileSync(path.join(root,'research/validation.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
