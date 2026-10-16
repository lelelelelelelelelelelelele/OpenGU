// Read-only headless rendering; no control of a user's browser session.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
(async()=>{
  const appendix=process.argv[2]==='appendix';
  const prefix=appendix?'appendix':'report';
  const receiptName=appendix?'appendix_report_verification.json':'report_verification.json';
  const qaName=appendix?'appendix_html_qa.json':'html_qa.json';
  const file=path.join(__dirname,appendix?'FIXED_BUDGET_APPENDIX.html':'REPORT.html');
  const sha=crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
  const receipt=JSON.parse(fs.readFileSync(path.join(__dirname,receiptName),'utf8'));
  if(receipt.html_sha256!==sha)throw new Error('Render receipt out of date');
  const browser=await chromium.launch({headless:true});
  const page=await browser.newPage();
  const errors=[];const views=[];
  page.on('pageerror',e=>errors.push(e.message));
  try{
    for(const [label,width,height] of [['desktop',1440,1050],['mobile',390,844]]){
      await page.setViewportSize({width,height});
      await page.goto(pathToFileURL(file).href,{waitUntil:'load'});
      const state=await page.evaluate(()=>({
        width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
        headings:[...document.querySelectorAll('main h2')].map(h=>h.textContent),
        images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.width,height:i.height})),
        tables:document.querySelectorAll('main table').length,
        missingAnchors:[...document.querySelectorAll('nav a')].filter(a=>!document.querySelector(a.getAttribute('href'))).length,
        externalAssets:[...document.querySelectorAll('script[src],link[rel=stylesheet],img[src]')].filter(e=>/^https?:/.test(e.src||e.href)).length,
        placeholder:document.querySelector('main').textContent.includes('@@')
      }));
      if(state.scrollWidth>width||state.images.length!==(appendix?2:1)||!state.images.every(i=>i.loaded)||state.missingAnchors||state.externalAssets||state.placeholder)throw new Error(JSON.stringify(state));
      await page.screenshot({path:path.join(__dirname,`${prefix}_${label}.png`)});
      if(label==='desktop'){
        const image=page.locator('main img').first();
        await image.scrollIntoViewIfNeeded();
        await page.screenshot({path:path.join(__dirname,`${prefix}_figure.png`)});
      }
      views.push({label,...state});
    }
    if(errors.length)throw new Error(errors.join('\n'));
    const qa={passed:true,html_sha256:sha,browser:browser.version(),headless:true,views,page_errors:errors};
    fs.writeFileSync(path.join(__dirname,qaName),JSON.stringify(qa,null,2)+'\n','utf8');
    receipt.browser_render='passed';receipt.browser_evidence=qaName;
    fs.writeFileSync(path.join(__dirname,receiptName),JSON.stringify(receipt,null,2)+'\n','utf8');
    console.log(JSON.stringify(qa,null,2));
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
