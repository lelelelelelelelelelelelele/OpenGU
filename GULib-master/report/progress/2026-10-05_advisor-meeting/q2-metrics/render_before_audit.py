"""Render the saved read-only checkpoint audit; never contacts the runner."""
import base64
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt

P=Path(__file__).resolve().parent
x=json.loads((P/'before_audit.json').read_text(encoding='utf-8'))
d=pd.DataFrame(x['records'])
summary=d.groupby(['dataset','method']).saved_before_accuracy.agg(['mean','min','max']).reset_index()
summary.to_csv(P/'before_audit_summary.csv',index=False,encoding='utf-8')
cor=d[d.dataset=='Cora'].copy()
assert len(cor)==20 and cor.test_argmax_mismatches.eq(0).all()
rows=[]
for r in cor.itertuples():
    rows.append({'方法':r.method,'seed':r.seed,'保存的 before':r.saved_before_accuracy,
        '重算 ensemble':r.recomputed_ensemble_before,'单 shard 最低':min(r.per_shard_before),
        '单 shard 最高':max(r.per_shard_before),'最后一个 shard':r.per_shard_before[-1],
        '均匀聚合诊断':r.recomputed_uniform_before,'测试预测不一致数':int(r.test_argmax_mismatches)})
detail=pd.DataFrame(rows)
detail.to_csv(P/'before_audit_cora.csv',index=False,encoding='utf-8')
def table(df):
    def f(v):return f'{v:.3f}' if isinstance(v,(float,np.floating)) else str(v)
    return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(map(f,r))+' |' for r in df.itertuples(index=False,name=None))
fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True)
for ax,m in zip(axes,['GraphEraser','GraphRevoker']):
    g=cor[cor.method==m]
    for i,r in enumerate(g.itertuples()):
        ax.scatter(i+np.linspace(-.15,.15,10),r.per_shard_before,color='#a9b7bf',s=17,alpha=.8,zorder=2)
        ax.scatter(i,r.saved_before_accuracy,facecolors='none',edgecolors='#b96336',marker='o',s=82,lw=1.4,zorder=4)
        ax.scatter(i,r.recomputed_ensemble_before,color='#1a8177',marker='+',s=70,lw=1.4,zorder=5)
        ax.scatter(i,r.recomputed_uniform_before,color='#4873a2',marker='_',s=85,lw=1.3,zorder=3)
    ax.set_xticks(range(10),g.seed.astype(str));ax.set_xlabel('Training seed')
    ax.set_title(m,loc='left',fontweight='bold');ax.set_ylim(10,95)
    ax.grid(axis='y',color='#e5ecef');ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Cora test accuracy (%)')
fig.suptitle('Before audit: saved prediction = recomputed initial ensemble',x=.07,ha='left',fontsize=15,fontweight='bold')
fig.legend(handles=[plt.Line2D([],[],marker='o',ls='',color='#a9b7bf',label='Individual shards'),plt.Line2D([],[],marker='o',mfc='none',ls='',color='#b96336',label='Saved before'),plt.Line2D([],[],marker='+',ls='',color='#1a8177',label='Recomputed ensemble'),plt.Line2D([],[],marker='_',ls='',color='#4873a2',label='Uniform weights (diagnostic)')],loc='upper center',bbox_to_anchor=(.5,.94),ncol=4,frameon=False,fontsize=9)
fig.text(.07,.02,'20 initial checkpoints; CPU inference only; zero test-label mismatches. Gray points are the ten shards in each checkpoint.',fontsize=9)
fig.subplots_adjust(left=.07,right=.98,top=.77,bottom=.15,wspace=.12)
for ext in ['png','pdf']:fig.savefig(P/f'before_checkpoint_audit.{ext}',dpi=170,facecolor='white')
plt.close(fig)
md=f'''# Before 来源核验：单 shard，还是完整 ensemble？

2026-10-18 · EXP-079/e79r5 · 只读核验，未训练或修改缓存

**结论：当前图中的 Cora before 来自完整初始 ensemble，未复现“最后一个 shard 被当成 before”的问题。GraphRevoker 的低起点是真实保存在这一批 checkpoint 中的表现，但原因和配置代表性尚未核实。** 不能把“数值可复算”扩大成“实现和实验配置已经合理”。

## 1. 本轮实际核验了什么

1. 按 run.json 的精确 Output 身份读取两种分片方法、三数据集、十 seed 的 60 个 D-full/GCN 条件，核对 Output 文件哈希与绑定 Dataset/Split，直接从保存的 logits_before 和测试标签计算准确率。60 个结果均与回传 metrics.json 一致。
2. 按 Output 内的 ensemble_state_hash 查找对应初始 checkpoint，核对 method、training、parameters 和 data identity，没有用当前默认参数重新训练。
3. 对 Cora 的 20 个初始 checkpoint 核验文件及 state 哈希，加载全部十个 shard、assignment 和聚合 weights，在 CPU 上重新前向。20 组 ensemble 的测试预测均与保存的 before 完全一致（每组 542 个测试节点，类别预测不一致数均为 0）。CPU/GPU 浮点输出最大绝对差为 {cor.max_abs_logit_diff.max():.6g}，未改变测试 argmax。
4. 同时分别计算每个 shard 的结果，以及使用相同 shard、改为均匀权重的聚合诊断。后者仅用于排查，不替换正式指标、不重训、不写回 Cache。

CiteSeer/PubMed 的 40 组只核对保存预测和初始 checkpoint 身份，未独立前向重算。完整原始证据在 [before_audit.json](before_audit.json)，只读脚本为 [audit_before_remote.py](audit_before_remote.py)。

## 2. 图里的数值与单 shard 数值有明显区别

![Cora：单 shard、保存 before、重算 ensemble 与均匀聚合](before_checkpoint_audit.png)

橙色空心圆是保存的 before，绿色加号是从初始 checkpoint 重算的完整 ensemble；两者重合。灰点是各单 shard，蓝横线是均匀权重诊断。

{table(summary.rename(columns={'dataset':'数据集','method':'方法','mean':'十 seed before 均值','min':'最低 seed','max':'最高 seed'}))}

例如 Cora / seed 42：GraphEraser 的十个 shard 为 70.11%–75.46%，完整 ensemble 为 86.72%；GraphRevoker 的单 shard 为 36.16%–72.88%，完整 ensemble 为 75.46%。这两项 before 都不是最后一个 shard 的值。

## 3. 为什么仍需要检查 GraphRevoker 的初始质量

GraphRevoker 的 Cora before 均值为 70.68%，seed 范围 59.96%–75.83%；GraphEraser 为 85.78%。对同一批 shard 使用均匀权重，GraphRevoker 的均值为 {cor[cor.method=='GraphRevoker'].recomputed_uniform_before.mean():.2f}%，没有简单恢复到八十多。这只能排除“换成均匀权重就能普遍修复”的简单解释，不能证明聚合实现无误。

已绑定的配置为十 shard、GCN 2 层/64 隐藏维度、3000 epochs、lr=0.05、weight_decay=0.0001；GraphEraser 使用 lpa_base，GraphRevoker 使用 gpa，后者 gpa_epochs=10；两者当前聚合均为 optimal。应进一步审查分区的节点和类别分布、分区训练充分性、shard 训练与聚合图是否符合 intended protocol，以及与原方法实验设置的差异。上述差异不等同于已确认的 bug，本轮没有改参数或启动重跑。

因此图 1 只能说：**在当前配置和 checkpoint 下，GraphRevoker 的初始 ensemble 性能较低，gap 解释必须考虑这个起点。** 暂不把它写成 GraphRevoker 的固有性质，更不据此宣称它天然不如其他 GU。

## 4. 与历史单 shard 误取问题的关系

用户指出的历史问题与既有审计记忆一致：旧 Step0 曾将最后一个 shard 的约 71.03% 当成 before，记忆中的完整聚合 before 约 84.69%。这是历史审计记录，本轮没有重新打开那次原始日志，不将其当成当前配置的正确替代值。当前 e79r5 的明确身份、保存预测及 Cora checkpoint 重算是本轮判断依据。

## 5. 全部 Cora 逐 seed 核验结果

{table(detail)}

## 复现与影响范围

原运行 SHA：`{x['execution_sha']}`。核验时远端 SHA：`{x['current_remote_sha']}`。用于重算的 ShardEnsemble、GCNNet、create_model，以及原始 before 生成/utility 函数已与原运行版本作 AST 对照，均相同；Output 自己的生成 producer 和初始 checkpoint 身份另在 JSON 中逐项保留，不能用当前 checkout SHA 冒充最初生成版本。

本次只读 SQLite、Output、绑定数据和初始 checkpoint；不修改缓存、训练参数、远端源码或科学接受状态。新增 CPU 重算而非 GPU 训练。已回传的 before 数值无需替换；论文图注需明确“当前配置的初始 ensemble”，并保留初始质量待审阅的限制。

[逐 seed CSV](before_audit_cora.csv) · [汇总 CSV](before_audit_summary.csv) · [矢量图](before_checkpoint_audit.pdf) · [渲染脚本](render_before_audit.py) · [返回三张叙事图](STORIES.html)。
'''
(P/'BEFORE_AUDIT.md').write_text(md,encoding='utf-8')
body=MarkdownIt('commonmark',{'html':False}).enable('table').render(md)
body=body.replace('src="before_checkpoint_audit.png"','src="data:image/png;base64,'+base64.b64encode((P/'before_checkpoint_audit.png').read_bytes()).decode()+'"')
style='body{margin:0;background:#eef3f4;color:#253c49;font:16px/1.85 "Microsoft YaHei",sans-serif}main{max-width:1200px;margin:auto;padding:35px;background:white}img{width:100%}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;border-bottom:1px solid #d8e3e8;padding:8px}th{background:#edf5f5}a{color:#167d77}code{overflow-wrap:anywhere}h2{margin-top:40px}@media(max-width:750px){main{padding:18px}table{display:block;overflow:auto}}'
(P/'BEFORE_AUDIT.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Before ensemble 核验</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
print(summary.to_string(index=False))
print('Cora max logit difference:',cor.max_abs_logit_diff.max())
