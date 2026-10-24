import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
if(path.basename(dir)!=='teaser')throw new Error('Renderer must remain in outputs/source');
const browser=await chromium.launch({channel:'msedge',headless:true});
const checks=[];
const requested=process.argv.slice(2);
if(requested.some(s=>s!=='teaser'))throw new Error('Expected teaser');
const targets=requested.length?requested:['teaser'];
try {
  for(const base of targets) {
    const svg=fs.readFileSync(path.join(dir,base+'.svg'),'utf8').replace(/^<\?xml[^>]+>\s*/,'');
    const [,width,height]=svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
    const paperWidth=174,paperHeight=paperWidth*height/width;
    const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:2});
    await page.route('**/*', route=>route.abort());
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>*{box-sizing:border-box}html,body{margin:0;padding:0;background:white}svg{display:block;width:100%;height:auto}@page{size:${paperWidth}mm ${paperHeight}mm;margin:0}@media print{html,body{width:${paperWidth}mm;height:${paperHeight}mm}}</style></head><body>${svg}</body></html>`);
    await page.evaluate(()=>document.fonts.ready);
    await page.screenshot({path:path.join(dir,base+'.png'),fullPage:true});
    await page.pdf({path:path.join(dir,base+'.pdf'),width:`${paperWidth}mm`,height:`${paperHeight}mm`,printBackground:true,preferCSSPageSize:true,margin:{top:0,right:0,bottom:0,left:0}});
    const labels=await page.locator('svg text').evaluateAll(items=>items.map(e=>{
      const b=e.getBoundingClientRect();
      return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};
    }));
    const outside=labels.filter(b=>b.x<15||b.y<15||b.x+b.w>width-15||b.y+b.h>height-2);
    const overlaps=[];
    for(let i=0;i<labels.length;i++) for(let j=i+1;j<labels.length;j++) {
      const a=labels[i],b=labels[j];
      const overlapX=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x);
      const overlapY=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);
      if(overlapX>2&&overlapY>2) overlaps.push({a:a.text,b:b.text,overlapX,overlapY});
    }
    const arrowChecks=await page.evaluate(()=>{
      const labels=[...document.querySelectorAll('svg text')].map(e=>({text:e.textContent,b:e.getBoundingClientRect()}));
      const arrows=[...document.querySelectorAll('svg path[data-arrow-shaft]')];
      const crossings=[];
      for(const arrow of arrows){
        const length=arrow.getTotalLength();
        for(const {text,b} of labels){
          for(let s=0;s<=length;s+=.5){
            const p=arrow.getPointAtLength(s).matrixTransform(arrow.getScreenCTM());
            if(p.x>b.x&&p.x<b.x+b.width&&p.y>b.y&&p.y<b.y+b.height){
              crossings.push({path:arrow.getAttribute('d'),text});break;
            }
          }
        }
      }
      return {count:arrows.length,crossings};
    });
    const qa={figure:base,canvas:[width,height],pngScale:2,paperSizeMM:[paperWidth,paperHeight],labelCount:labels.length,outside,overlaps,arrowChecks};
    checks.push(qa);
    console.log(JSON.stringify(qa));
    if(outside.length||overlaps.length||arrowChecks.crossings.length) process.exitCode=1;
    await page.close();
  }
  fs.writeFileSync(path.join(dir,requested.length===1?requested[0]+'-render-check.json':'render-check.json'),JSON.stringify(checks,null,2),'utf8');
} finally {await browser.close();}
