const $ = id => document.getElementById(id);
let state, current, active = 'fig3', busy = false;
let previewObserver;
function showSource(source) {
  $('source-panel').hidden = !source; $('preview').hidden = source;
  $('html-view').setAttribute('aria-pressed',String(!source));
  $('source-view').setAttribute('aria-pressed',String(source));
}
async function api(url, data, raw = false) {
  const response = await fetch(url, data === undefined ? {} : {method:'POST', headers:{'X-Review-Token':state.token,'Content-Type':raw?'application/zip':'application/json'},body:raw?data:JSON.stringify(data)});
  if (!response.ok) { const result = await response.json(); throw new Error(result.error); }
  return response.json();
}
function message(text) { $('message').textContent = text; }
function cloudView(cloud) {
  $('sync-status').textContent = cloud.status || '未验证';
  $('sync-detail').textContent = cloud.detail || '先从既有项目下载最新源码，检查差异后再上传。';
  $('overleaf').href = cloud.project;
  $('cloud-diff').textContent = JSON.stringify({检查时间:cloud.checkedAt,待上传:cloud.differences,云端变化:cloud.cloudChanged,云端独有保留:cloud.cloudOnly},null,2);
  $('package').hidden = !cloud.differences?.length || !!cloud.cloudChanged?.length || cloud.status === '未验证';
  $('pull').hidden = !cloud.cloudChanged?.length || cloud.status === '未验证';
}
async function load() {
  const result = await api('/api/block?id='+active);
  current = result.block;
  $('title').textContent = current.title; $('number').textContent = 'BLOCK '+(Object.keys({fig3:0,fig4:0,exp014:0}).indexOf(active)+1)+' / 3';
  $('path').textContent = current.path+':'+current.line; $('source').value = current.source;
  $('git-diff').textContent = result.diff || '相对 Git HEAD 没有未提交的论文修改。';
  document.querySelectorAll('nav button').forEach(b=>b.setAttribute('aria-current',String(b.dataset.id===active)));
  $('events').replaceChildren();
  for (const event of result.events.filter(e=>e.kind!=='edit-intent').reverse()) {
    const el=document.createElement('article');el.className='event';
    const date=document.createElement('small'); date.textContent=new Date(event.time).toLocaleString()+' · '+(event.kind==='edit'?'修改':'意见');el.append(date);
    const text=document.createElement('p');text.textContent=event.reason;el.append(text);
    if(event.diff){const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent='查看修改前后差异';const pre=document.createElement('pre');pre.textContent=event.diff;details.append(summary,pre);el.append(details);}
    $('events').append(el);
  }
  if(!$('events').children.length){const p=document.createElement('p');p.className='note';p.textContent='本块暂无意见。保存后会记录对应源码版本。';$('events').append(p);}
  message('正在从 LaTeX 生成 HTML 文字…');
  const preview=await api('/api/preview?id='+active);
  await new Promise((resolve,reject)=>{
    const frame=$('preview');
    previewObserver?.disconnect();frame.style.height='160px';
    frame.onload=()=>{
      const body=frame.contentDocument?.body;
      if(!body){reject(new Error('HTML 正文加载失败。'));return;}
      const resize=()=>{frame.style.height=Math.ceil(body.getBoundingClientRect().height+30)+'px';};
      previewObserver=new ResizeObserver(resize);previewObserver.observe(body);resize();resolve();
    };
    frame.onerror=()=>reject(new Error('HTML 正文加载失败。'));frame.src=preview.url;
  });
  message('HTML 正文已更新，可直接选择和复制文字。');
}
async function action(fn){if(busy)return;busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);try{await fn();}catch(e){message(e.message);}finally{busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);}}
$('refresh').onclick=()=>action(async()=>{state=await api('/api/state');cloudView(state.cloud);await load();});
$('source-link').onclick=()=>{showSource(true);$('source-panel').scrollIntoView({behavior:'smooth'});};
$('html-view').onclick=()=>showSource(false);
$('source-view').onclick=()=>showSource(true);
$('add-comment').onclick=()=>action(async()=>{await api('/api/comment',{id:active,version:current.version,text:$('comment').value});$('comment').value='';await load();message('意见已保存，并绑定当前源码版本。');});
$('save').onclick=()=>action(async()=>{await api('/api/save',{id:active,version:current.version,source:$('source').value,reason:$('reason').value});$('reason').value='';state=await api('/api/state');cloudView(state.cloud);await load();});
$('cloud-zip').onchange=()=>action(async()=>{const file=$('cloud-zip').files[0];if(file){const result=await api('/api/cloud/check',await file.arrayBuffer(),true);cloudView(result);message('云端快照检查完成。源码 ZIP 本身不证明云端编译成功。');}});
$('pull').onclick=()=>action(async()=>{cloudView(await api('/api/cloud/pull',{}));await load();message('云端修改已取回。发生冲突时不会写入源码。');});
action(async()=>{state=await api('/api/state');cloudView(state.cloud);for(const block of state.blocks){const button=document.createElement('button');button.textContent=block.title;button.dataset.id=block.id;button.onclick=()=>action(async()=>{if($('source').value!==current.source){message('当前有未保存修改，请先保存，或刷新后放弃修改。');return;}active=block.id;await load();});$('blocks').append(button);}await load();});
