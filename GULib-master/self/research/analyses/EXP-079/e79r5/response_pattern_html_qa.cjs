// Read-only local rendering of the generated report; no external browser session.
// Run with the workspace dependency bundle on NODE_PATH.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const crypto = require('node:crypto');

(async () => {
  const report = path.join(__dirname, 'RESPONSE_PATTERN_REPORT.html');
  const reportHash = crypto.createHash('sha256').update(fs.readFileSync(report)).digest('hex');
  const browser = await chromium.launch({headless:true});
  const page = await browser.newPage();
  const errors=[];
  page.on('pageerror', error => errors.push(error.message));
  const results=[];
  try {
    for (const [label,width,height] of [['desktop',1440,1000],['mobile',390,844]]) {
      await page.setViewportSize({width,height});
      await page.goto(pathToFileURL(report).href);
      await page.locator('img').last().waitFor({state:'attached'});
      const state = await page.evaluate(() => ({
        width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
        images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.width,height:i.height})),
        tables:document.querySelectorAll('table').length,
        navigation:[...document.querySelectorAll('nav a')].map(a=>({text:a.textContent,target:document.querySelector(a.getAttribute('href'))?.textContent})),
        externalAssets:[...document.querySelectorAll('script[src],link[rel="stylesheet"],img[src]')].filter(e=>/^https?:/.test(e.src||e.href)).length
      }));
      if (state.scrollWidth!==width || state.images.length!==6 || !state.images.every(i=>i.loaded) || state.externalAssets || state.navigation.some(n=>!n.target)) {
        throw new Error(`Render validation failed: ${JSON.stringify(state)}`);
      }
      await page.screenshot({path:path.join(__dirname,`response_html_${label}.png`)});
      results.push({label,...state});
    }
    if(errors.length)throw new Error(errors.join('\n'));
    const qa={report_sha256:reportHash,browser_version:browser.version(),headless:true,results,page_errors:errors,passed:true};
    fs.writeFileSync(path.join(__dirname,'response_html_qa.json'),JSON.stringify(qa,null,2)+'\n','utf8');
    const receiptPath=path.join(__dirname,'response_report_verification.json');
    const receipt=JSON.parse(fs.readFileSync(receiptPath,'utf8'));
    if(receipt.report_sha256['RESPONSE_PATTERN_REPORT.html']!==reportHash)throw new Error('Receipt report SHA mismatch');
    receipt.html_browser_render='passed';
    receipt.html_browser_evidence='response_html_qa.json';
    fs.writeFileSync(receiptPath,JSON.stringify(receipt,null,2)+'\n','utf8');
    console.log(JSON.stringify(qa,null,2));
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
