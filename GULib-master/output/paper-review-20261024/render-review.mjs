import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'file:///C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';

const root = 'E:/project/OpenGU/GULib-master';
const folder = path.join(root, 'report/paper/review/2026-10-24-www27');
const stem = process.argv[2] || 'REPORT';
if (!/^[A-Z_]+$/.test(stem)) throw new Error('Invalid document name');
const source = fs.readFileSync(path.join(folder, `${stem}.md`), 'utf8');
const title = source.split('\n')[0].replace(/^#\s+/, '');
let body = marked.parse(source);
body = body.replace(/<img src="([^"]+)"([^>]*)>/g, (_, src, attrs) => {
  const resolved = path.resolve(folder, src);
  if (!resolved.startsWith(path.resolve(root) + path.sep)) throw new Error('Image outside workspace');
  return `<img src="data:image/png;base64,${fs.readFileSync(resolved).toString('base64')}"${attrs}>`;
});
const sections = [];
body = body.replace(/<h2>(.*?)<\/h2>/g, (_, label) => {
  const id = `part-${sections.length + 1}`;
  sections.push(`<a href="#${id}">${label}</a>`);
  return `<h2 id="${id}">${label}</h2>`;
});
body = body.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
const html = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title} · 2026-10-24</title><style>
:root{color-scheme:light;--ink:#202c38;--muted:#627080;--line:#d7dee5;--accent:#18577b}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f3f5f7;color:var(--ink);font:16px/1.85 system-ui,'Microsoft YaHei',sans-serif}.layout{max-width:1420px;margin:auto;display:grid;grid-template-columns:250px minmax(0,1fr);gap:36px;padding:36px 28px 100px}nav{align-self:start;position:sticky;top:30px;font-size:13px}nav strong{display:block;font-size:16px;margin-bottom:18px}nav a{display:block;padding:7px 0;border-bottom:1px solid var(--line);color:var(--muted);text-decoration:none}main{background:white;border:1px solid var(--line);padding:42px 48px;min-width:0;box-shadow:0 6px 30px #24384a08}h1{font-size:32px;line-height:1.35;margin:0 0 20px}h2{font-size:23px;line-height:1.5;margin:48px 0 20px;padding-top:12px;border-top:2px solid #adc2d0;scroll-margin-top:20px}h3{font-size:18px;margin:28px 0 12px}p{margin:14px 0}a{color:var(--accent);text-underline-offset:3px}strong{font-weight:650}.table-scroll{overflow:auto;margin:24px 0}table{border-collapse:collapse;font-size:14px;line-height:1.7;width:100%;min-width:620px}th,td{padding:12px 14px;text-align:left;border:1px solid var(--line);vertical-align:top}th{background:#eaf0f5;font-weight:650}tr:nth-child(even) td{background:#f8fafc}code{font-size:.88em;background:#edf2f6;padding:2px 5px;border-radius:3px;overflow-wrap:anywhere}li{margin:8px 0}img{max-width:100%;height:auto;border:1px solid var(--line);display:block;margin:20px auto}main>p:nth-of-type(1){background:#eef3f7;border-left:4px solid var(--accent);padding:18px 20px}footer{color:var(--muted);font-size:12px;margin-top:48px;border-top:1px solid var(--line);padding-top:15px}@media(max-width:950px){.layout{display:block;padding:16px}nav{position:static;margin-bottom:25px}nav a{display:inline-block;margin-right:15px}main{padding:26px 20px}h1{font-size:27px}}@media print{body{background:white}.layout{display:block;padding:0}nav{display:none}main{border:0;box-shadow:none;padding:0}h2{break-after:avoid}table{font-size:10px;min-width:0}img{max-height:600px;object-fit:contain}a{color:inherit}}
</style></head><body><div class="layout"><nav><strong>${title}</strong><p>2026-10-24 · 中文<br>待作者讨论</p>${sections.join('')}<p><a href="${stem}.md">Markdown 源报告</a></p></nav><main>${body}<footer>由 ${stem}.md 生成。外部来源与本地证据均在相关段落链接；本报告不改变实验验收状态。</footer></main></div></body></html>`;
fs.writeFileSync(path.join(folder, `${stem}.html`), html, 'utf8');
console.log(JSON.stringify({markdownBytes:Buffer.byteLength(source),htmlBytes:Buffer.byteLength(html),sections:sections.length,output:path.join(folder,`${stem}.html`)}));
