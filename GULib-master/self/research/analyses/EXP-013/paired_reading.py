"""Readable paired observations for EXP-013; no new experiment or pooled fit."""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from analyze_surrogate import DATASETS, METHODS, save

SEEDS = [42, 212, 2024]
COLORS = ['#0072B2', '#D55E00', '#009E73']
DEFAULT = ('GNNDelete', 'gt_full', 'GIN')


def paired_figure(paired):
    method, selector, source = DEFAULT
    data = paired[(paired.method == method) & (paired.selector == selector) & (paired.source == source)]
    assert len(data) == 9
    with plt.rc_context({'font.family': 'Microsoft YaHei', 'axes.unicode_minus': False}):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.6))
        for ax, dataset in zip(axes, DATASETS):
            part = data[data.dataset == dataset].set_index('seed')
            for seed, color in zip(SEEDS, COLORS):
                row = part.loc[seed]
                ax.plot([0, 1], [row.U_direct, row.U], color=color, marker='o', lw=2, ms=6, alpha=.85)
            ax.set_xlim(-.18, 1.18)
            ax.margins(y=.3)
            ax.set_xticks([0, 1], ['GCN 选点', 'GIN 选点'], fontsize=11)
            ax.set_title(dataset, fontsize=15, fontweight='bold', pad=12)
            ax.set_ylabel('F1 下降（百分点）', fontsize=10)
            ax.grid(axis='y', alpha=.16)
            ax.spines[['top', 'right']].set_visible(False)
            ax.text(.5, -.21, f'三次均值：{part.U_direct.mean():.2f} → {part.U.mean():.2f}',
                    transform=ax.transAxes, ha='center', fontsize=11)
        fig.suptitle('换成 GIN 选点后，F1 下降改变了多少？', fontsize=18, y=.98)
        fig.text(.5, .875, '固定 GNNDelete · gt_full · 10% 删除预算 · 同一个 GCN victim', ha='center', fontsize=11)
        handles = [Line2D([0], [0], color=c, marker='o', lw=2, label=f'seed {s}') for s, c in zip(SEEDS, COLORS)]
        fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5, .055), ncol=3, frameon=False)
        fig.text(.5, .018, '每条线连接同 seed 的一对结果；平线 = 下降相同。各面板纵轴单独缩放，只在面板内比较斜率。',
                 ha='center', fontsize=10, color='#475569')
        fig.subplots_adjust(top=.75, bottom=.30, left=.07, right=.98, wspace=.36)
        save(fig, 'post_paired_reading')


def interactive_html(paired):
    """Inline data and SVG keep the saved report usable without a server."""
    columns = ['dataset', 'method', 'selector', 'source', 'seed', 'U_direct', 'U']
    data = paired[columns].to_json(orient='records', force_ascii=False, double_precision=15)
    options = lambda values, default: ''.join(
        f'<option value="{v}"{" selected" if v == default else ""}>{v}</option>' for v in values)
    template = '''<section id="paired-reader" style="display:none;background:white;padding:18px;border:1px solid #cbd5e1;border-radius:12px">
<p><strong>逐对看真实结果</strong>：每条线连接同一个 seed 的结果；不混合两个选点算法。</p>
<div style="display:flex;gap:20px;flex-wrap:wrap">
<label>遗忘方法 <select id="paired-method">METHOD_OPTIONS</select></label>
<label>选点算法 <select id="paired-selector">SELECTOR_OPTIONS</select></label>
<label>换成谁选点 <select id="paired-source">SOURCE_OPTIONS</select></label></div>
<p id="paired-title"></p><div id="paired-plot" style="overflow-x:auto"></div>
<p>蓝：seed 42；橙：seed 212；绿：seed 2024。各面板纵轴单独缩放，勿跨面板比较斜率。平线表示下降相同；右端更高表示 surrogate 造成更大下降；负值表示 F1 提升。</p>
<div id="paired-values" style="overflow-x:auto"></div>
<p>每种设置只有三个 seed。此图显示实际配对变化，不把均值接近称作统计等效，也不从三点拟合外推。</p></section>
<script>
(() => {
const data = DATA_JSON;
const datasets = ['Cora','CiteSeer','PubMed'];
const colors = {42:'#0072B2',212:'#D55E00',2024:'#009E73'};
const byId = id => document.getElementById(id);
const text = (x,y,value,size=13,anchor='middle',color='#172536') => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${value}</text>`;
function render() {
  const method=byId('paired-method').value, selector=byId('paired-selector').value, source=byId('paired-source').value;
  const selected=data.filter(r=>r.method===method&&r.selector===selector&&r.source===source);
  byId('paired-title').textContent=`${method} / ${selector}：GCN 选点 → ${source} 选点，均在 GCN victim 上评估。`;
  let svg='<svg viewBox="0 0 1140 365" role="img" aria-label="同 seed 的 F1 下降配对图" style="width:100%;min-width:760px;font-family:Microsoft YaHei,sans-serif">';
  datasets.forEach((dataset,i)=>{
    const rows=selected.filter(r=>r.dataset===dataset).sort((a,b)=>a.seed-b.seed);
    const values=rows.flatMap(r=>[r.U_direct,r.U]);
    const lower=Math.min(...values),upper=Math.max(...values),pad=Math.max((upper-lower)*.30,.15);
    const low=lower-pad, high=upper+pad, left=i*380+80,right=i*380+300;
    const ypos=v=>260-(v-low)/(high-low)*205;
    svg+=text(i*380+190,25,dataset,19);
    for(let t=0;t<=4;t++) {
      const value=low+(high-low)*t/4, y=ypos(value);
      svg+=`<line x1="${left-15}" x2="${right+15}" y1="${y}" y2="${y}" stroke="#e2e8f0"/>`;
      svg+=text(left-20,y+4,value.toFixed(2),11,'end','#64748b');
    }
    rows.forEach(r=>{
      const color=colors[r.seed],a=ypos(r.U_direct),b=ypos(r.U);
      svg+=`<g><title>seed ${r.seed}: ${r.U_direct.toFixed(3)} → ${r.U.toFixed(3)} pp</title><line x1="${left}" x2="${right}" y1="${a}" y2="${b}" stroke="${color}" stroke-width="2.5"/><circle cx="${left}" cy="${a}" r="4.5" fill="${color}"/><circle cx="${right}" cy="${b}" r="4.5" fill="${color}"/></g>`;
    });
    svg+=text(left,291,'GCN 选点',14)+text(right,291,source+' 选点',14);
    const mean=key=>rows.reduce((s,r)=>s+r[key],0)/rows.length;
    svg+=text(i*380+190,323,`三次均值：${mean('U_direct').toFixed(2)} → ${mean('U').toFixed(2)} pp`,14);
  });
  byId('paired-plot').innerHTML=svg+'</svg>';
  let table='<table><thead><tr><th>数据集</th><th>seed</th><th>GCN 选点 drop</th><th>'+source+' 选点 drop</th><th>差值（surrogate − direct）</th></tr></thead><tbody>';
  selected.forEach(r=>{const delta=r.U-r.U_direct;table+=`<tr><td>${r.dataset}</td><td>${r.seed}</td><td>${r.U_direct.toFixed(3)}</td><td>${r.U.toFixed(3)}</td><td>${delta>=0?'+':''}${delta.toFixed(3)}</td></tr>`;});
  byId('paired-values').innerHTML=table+'</tbody></table>';
}
['paired-method','paired-selector','paired-source'].forEach(id=>byId(id).addEventListener('change',render));
render();byId('paired-reader').style.display='block';
const fallback=document.querySelector('img[alt="同seed真实F1下降配对"]');
if(fallback) fallback.style.display='none';
})();
</script>'''
    return (template.replace('METHOD_OPTIONS', options(METHODS, DEFAULT[0]))
            .replace('SELECTOR_OPTIONS', options(['r_point', 'gt_full'], DEFAULT[1]))
            .replace('SOURCE_OPTIONS', options(['SGC', 'GAT', 'GIN'], DEFAULT[2]))
            .replace('DATA_JSON', data.replace('<', '\\u003c')))
