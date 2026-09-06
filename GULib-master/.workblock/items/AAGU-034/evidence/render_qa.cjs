// node render_qa.cjs <node_modules> <browser executable>
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require(require.resolve('playwright',{paths:[process.argv[2]]}));
(async()=>{
 const browser=await chromium.launch({executablePath:process.argv[3],headless:true});
 const results=[];
 try{
  for(const [name,width,height] of [['desktop',1440,1000],['narrow',390,844]]){
   const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(pathToFileURL(path.join(__dirname,'../REPORT.html')).href);
   await page.screenshot({path:path.join(__dirname,'report-'+name+'.png'),fullPage:false});
   const metrics=await page.evaluate(()=>{
    const decision=document.querySelector('[data-workblock-decision]');
    return {bodyOverflow:document.documentElement.scrollWidth>innerWidth,
     humanResults:document.querySelectorAll('[data-workblock-human-result]').length,
     decisions:document.querySelectorAll('[data-workblock-decision]').length,
     decisionBottom:Math.round(decision.getBoundingClientRect().bottom),
     brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
     title:document.querySelector('h1').innerText};
   });
   if(metrics.bodyOverflow||metrics.humanResults!==1||metrics.decisions!==1||metrics.brokenImages||errors.length)
       throw Error('report layout failure: '+JSON.stringify({metrics,errors}));
   if(name==='desktop'&&metrics.decisionBottom>height)throw Error('desktop decision below first screen');
   if(name==='desktop'){
    await page.screenshot({path:path.join(__dirname,'report-full.png'),fullPage:true});
    for(const [label,title] of [['body','验收问题与实际观察'],['boundary','尚未观察与人类边界']]){
     await page.getByRole('heading',{name:title,exact:true}).scrollIntoViewIfNeeded();
     await page.screenshot({path:path.join(__dirname,'report-'+label+'.png')});
    }
   }
   results.push({name,width,height,metrics,errors});await page.close();
  }
  fs.writeFileSync(path.join(__dirname,'render-qa.json'),JSON.stringify({layer:'local headless Edge',results},null,2)+'\n');
  console.log(JSON.stringify(results));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
