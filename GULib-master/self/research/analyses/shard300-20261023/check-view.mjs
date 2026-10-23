import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const {chromium}=await import('file:///C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs');
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const checks=[];
try {
  const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
  for(const name of ['REPORT','EXP011_REPORT','EXP079_REPORT']) {
    await page.goto(pathToFileURL(path.join(dir,name+'.html')).href);
    await page.locator('img').first().scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(dir,'preview-'+name+'.png')});
    const desktop=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,
      images:[...document.images].filter(x=>x.loading!=='lazy'||x.getBoundingClientRect().top<innerHeight).every(x=>x.complete&&x.naturalWidth>0)}));
    if(desktop.overflow||!desktop.images)throw new Error(name+' desktop render failure');
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>scrollTo(0,0));
    await page.screenshot({path:path.join(dir,'preview-'+name+'-mobile.png')});
    const mobileOverflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    if(mobileOverflow)throw new Error(name+' mobile overflow');
    checks.push({page:name+'.html',desktop, mobileOverflow});
    await page.setViewportSize({width:1440,height:1100});
  }
  const v=JSON.parse(fs.readFileSync(path.join(dir,'validation.json'),'utf8'));
  v.browser_checks=checks;
  fs.writeFileSync(path.join(dir,'validation.json'),JSON.stringify(v,null,2)+'\n');
  console.log(JSON.stringify(checks));
} finally { await browser.close(); }
