// node render_report.cjs <node_modules> [--check]
const fs = require('fs');
const path = require('path');
const {marked} = require(require.resolve('marked', {paths:[process.argv[2]]}));
const item = path.dirname(__dirname);
const md = fs.readFileSync(path.join(item,'REPORT.md'),'utf8');
let body = marked.parse(md);
body = body.replace(/(<h2>Human Result<\/h2>[\s\S]*?)(?=<h2>)/,
    '<section data-workblock-human-result="2.1">$1</section>');
body = body.replace('当前验收决定：<code>待决定</code>',
    '当前验收决定：<span data-workblock-decision="pending">待决定</span>');
body = body.replace('当前验收决定：<code>接受</code>',
    '当前验收决定：<span data-workblock-decision="accepted">接受</span>');
body = body.replaceAll('<table>','<div class="table-wrap"><table>').replaceAll('</table>','</table></div>');
const css = `*{box-sizing:border-box}html{background:#f3f5f8;color:#223345;font-family:"Segoe UI","Microsoft YaHei",sans-serif}body{margin:0 auto;max-width:1100px;padding:28px 32px 70px;font-size:16px;line-height:1.75}main{background:#fff;padding:26px 40px 48px;border:1px solid #dce3eb;border-radius:12px}h1{font-size:29px;line-height:1.35;color:#16374c;margin:0 0 22px}h2{font-size:23px;margin:34px 0 14px;padding-top:8px;border-top:1px solid #dbe3ea}h3{font-size:18px;color:#245365;margin:24px 0 7px}p{margin:7px 0 14px}section{border:1px solid #c9ddd9;border-top:4px solid #237b72;background:#f7fbfa;padding:16px 22px 18px;border-radius:8px}section h2{font-size:16px;letter-spacing:.5px;color:#237b72;border:0;margin:0 0 8px;padding:0}section h3{margin:12px 0 4px}section p{margin:4px 0 9px}blockquote{margin:10px 0;padding:8px 15px;background:#fff1d2;border-left:4px solid #ca9b32}blockquote p{margin:0!important}[data-workblock-decision]{font-weight:700;color:#7c5410}a{color:#147589;text-underline-offset:3px}code{background:#edf1f5;padding:1px 4px;border-radius:3px;font-size:.85em;overflow-wrap:anywhere}pre{background:#152e40;color:#eff5f9;padding:18px 22px;border-radius:6px;overflow:auto;line-height:1.6}pre code{background:none;color:inherit;padding:0;white-space:pre-wrap;word-break:break-word}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.65}th{background:#eaf1f4;text-align:left;color:#244657}th,td{border:1px solid #d8e2e8;padding:10px 13px;vertical-align:top;overflow-wrap:anywhere}td:first-child{font-weight:600;width:21%}.table-wrap{overflow:auto;margin:18px 0}strong{color:#173f51}li{margin:7px 0}@media(max-width:640px){body{padding:10px 8px;font-size:15px}main{padding:20px 16px;border-radius:8px}h1{font-size:24px}h2{font-size:21px}h3{font-size:17px}section{padding:13px}th,td{padding:7px;font-size:13px}pre{padding:12px}}@media print{html{background:white}body{max-width:none;padding:0}main{border:0;padding:0}section{break-inside:avoid}h2,h3{break-after:avoid}}`;
const result='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AAGU-034 · 实验配置与统一执行入口修正</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>\n';
const output=path.join(item,'REPORT.html');
if(process.argv.includes('--check')){
    if(fs.readFileSync(output,'utf8')!==result)throw Error('report projection drift');
    console.log('report projection check: PASS');
}else{fs.writeFileSync(output,result);console.log('Rendered REPORT.html from REPORT.md');}
