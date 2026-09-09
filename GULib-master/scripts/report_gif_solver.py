"""Render AAGU-052's paired decision report from collected numerical evidence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mistune


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--item',required=True,type=Path)
    parser.add_argument('--candidate',required=True)
    a=parser.parse_args();ev=a.item/'evidence'
    result=read(ev/'compare-v1.json');confirmation=read(ev/'confirm-v1.json');curvature=read(ev/'curvature-v2.json')
    assert result['finished'] and confirmation['finished']
    assert len(result['cells'])==18 and len(confirmation['cells'])==2
    producer=read(ev/'local-producer.json')
    assert all(row['producer']==producer for row in confirmation['cells'])
    full={row['k']:row for row in result['cells'] if row['arm']=='full-shift20'}
    old={row['k']:row for row in result['cells'] if row['arm']=='old'}
    retrain={row['k']:row for row in result['retrain']}
    assert all(row['graph_matches_declared_deletion'] and row['matched_residual']<=.001 for row in full.values())
    assert all(row['status']=='converged' and row['solver']['relative_residual']<=.001 for row in confirmation['cells'])
    assert all(row['status']=='rejected' for row in result['cells'] if row['arm']=='full-undamped')
    assert all(row['state_hash']==result['checkpoint']['state_hash'] for row in result['cells'] if row['status']=='rejected')
    pct=lambda value:f'{value*100:.3f}%'
    main_table=table(['删除训练节点','旧求解残差','修复后匹配残差','原模型 / 旧GIF F1','修复GIF F1','Retrain F1'],[
        [k,f"{old[k]['matched_residual']:.6f}",f"{full[k]['matched_residual']:.6f}",'87.823%',
         pct(full[k]['original_test']['micro_f1']),pct(retrain[k]['original_test']['micro_f1'])] for k in full])
    edge_table=table(['删除节点','应保留边数','旧GIF实际边数','旧GIF残留关联边','修复后边集合'],[
        [row['k'],row['expected_edges'],row['actual_edges'],row['actual_incident_edges'],'与应保留图完全一致'] for row in curvature['cells']])
    gap_table=table(['删除节点','原模型→Retrain 概率RMSE','修复GIF→Retrain 概率RMSE','类别差异：原模型→修复GIF','参数相对L2'],[
        [k,f"{retrain[k]['baseline_gap']['probability_rmse']:.6f}",
         f"{next(row for row in retrain[k]['comparisons'] if row['arm']=='full-shift20')['gap']['probability_rmse']:.6f}",
         f"{retrain[k]['baseline_gap']['flips']} → {next(row for row in retrain[k]['comparisons'] if row['arm']=='full-shift20')['gap']['flips']}",
         f"{full[k]['relative_parameter_l2']:.6f}"] for k in full])
    confirmation_table=table(['训练seed','原模型 F1','修复GIF F1','Retrain F1','匹配残差','与Retrain类别差异：原模型→GIF'],[
        [row['seed'],pct(row['before_f1']),pct(row['after_f1']),pct(row['retrain_f1']),
         f"{row['solver']['relative_residual']:.6f}",f"{row['baseline_retrain_gap']['flips']} → {row['retrain_gap']['flips']}"]
        for row in confirmation['cells']])
    arms=table(['对照','删除节点','返回状态','匹配残差','原图F1','测试类别翻转'],[
        [row['arm'],row['k'],'拒绝更新' if row['status']=='rejected' else '返回更新',
         f"{row.get('matched_residual',row.get('solver',{}).get('relative_residual')):.6f}",
         pct(row['original_test']['micro_f1']),row['original_test']['flips']] for row in result['cells']])
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(11,3.9),layout='constrained')
    for k,row in full.items():
        trace=row['solver']['trace']
        axes[0].semilogy([v['iteration'] for v in trace],[v['relative_residual'] for v in trace],label=f'k={k}')
    axes[0].axhline(.001,color='#555',linestyle='--',label='tolerance 0.001')
    axes[0].set(xlabel='Richardson iterations',ylabel='Matched relative residual',title='Shift = 20.48; original sum-loss Hessian')
    axes[0].legend();axes[0].grid(alpha=.2)
    for i,k in enumerate(full):
        axes[1].bar(i-.23,retrain[k]['baseline_gap']['probability_rmse'],width=.23,color='#8995a6',label='Baseline vs retrain' if i==0 else None)
        gap=next(row for row in retrain[k]['comparisons'] if row['arm']=='full-shift20')['gap']
        axes[1].bar(i,gap['probability_rmse'],width=.23,color='#087e8b',label='Fixed GIF vs retrain' if i==0 else None)
    axes[1].set(xticks=list(range(3)),xticklabels=['10','189','947'],xlabel='Deleted training nodes',ylabel='Test probability RMSE',title='Small improvement; substantial gap remains')
    axes[1].legend();axes[1].grid(axis='y',alpha=.2)
    fig.savefig(ev/'solver-evidence.svg');fig.savefig(ev/'solver-evidence.png',dpi=160);plt.close(fig)
    markdown=f'''# AAGU-052 · GIF 数值求解有效性与原图评估研究

## Human Result

### 实际增量

修复 GIF 节点删图的下标错误，并把求解残差、有限值与未收敛拒绝写入真实更新路径。完成 18 次固定输入配对更新、2 次既有 seed/Selection 的真实 adapter 确认；新增 1 次缺失的10节点 Retrain，其余匹配参照复用。

### 核心观察

**局部代码修复通过；完整遗忘有效性仍未确认。** 旧 GIF 不仅几乎没有解出更新方程，内部删图还残留本应删除的关联边。修复后的阻尼方程在三档删除量和两次额外确认上均达到相对残差≤0.001；但它仍明显不同于完整 Retrain。

{main_table}

所有主 F1 使用同一原图、542个测试节点、原标签与 eval 模式。旧残差对应 Hδ=v，新残差对应 (H+20.48I)δ=v；二者目标不同，不能把新残差达标说成已经精确求解无阻尼方程。

### 当前决定

> 当前验收决定：`待决定`

**建议接受本次局部软件修复与有界研究交付。** 不建议据此接受“GIF等价于Retrain”或恢复正式生产矩阵。由用户决定是否接受当前候选；049继续独立待验收。

## 已证实的两处问题

**PASS — 节点删图修复。** 原函数先筛出单向边，再把筛后位置当作原始边位置，并以偏移的反向查找拼接，导致误删与漏删。4节点显式测试在旧实现上失败；新实现直接按两端点筛除关联边，保留边顺序与设备。真实三档边集合与统一 retained_graph 完全相等。

{edge_table}

因此049报告中的“移除6314条关联边”描述统一保留图/配对语义，不能解释为旧GIF内部梯度实际消费了该图。049历史证据保持原样，本报告追加这一新发现。

**PASS — 未收敛不再冒充有效更新。** 旧默认scale=1e9、100步、damp=0，三档残差仍接近1。现在先检查匹配方程的残差，达标才调用模型写回；失败时抛出带迭代轨迹的明确错误。CPU验证失败后模型逐位不变，真实Output生产链也不发布Prediction Artifact。新的求解函数进入GIF producer指纹，旧Artifact保持只读。

## 方程、曲率与参数选择

设L为原图训练节点的交叉熵求和，H=∇²L；v为原图受影响训练人口loss梯度减去删除后图保留影响人口loss梯度。更新符号是θ_new=θ+δ。所有训练参数参与，本例92231个标量；更新loss不读取验证/测试标签。

旧递推h←v+(1−damp)h−Hh/scale，δ=h/scale，等价于δ←δ+[v−(H+scale×damp·I)δ]/scale。原始目标没有显式L2项；训练使用的Adam weight decay不能直接当作此处的damp。

真实Hessian的负Rayleigh方向约−10.8836、正方向约3283.579，负方向特征残差约0.00291。它证明存在负曲率，不能由“把scale调小”保证原无阻尼递推稳定。40步Lanczos提供Ritz估计，不是完整谱界或可逆性证明。原图sum CE梯度范数约83.30，checkpoint也不能当作精确驻点。

按曲率预登记scale=4096，比较shift=20.48和81.92（damp=0.005和0.02），上限分别4000和1500步。选择规则是在三档都达标的预登记候选中选最小shift，未按测试F1选择。shift20.48实际在1941、1565、1302步达标。改成scale4096但保持无阻尼的200步对照三档均未收敛，已拒绝写回。

**目标差异必须保留。** 修复候选在无阻尼方程Hδ=v上的残差依次仍为{full[10]['undamped_residual']:.3f}、{full[189]['undamped_residual']:.3f}、{full[947]['undamped_residual']:.3f}。本次确认的是显式阻尼局部近似的数值求解，不是原方程精确解，也不是完整遗忘证明。

选点侧scale=25的默认参照使用mean交叉熵、默认last_layer参数人口、20步、damp=0.01，其shift为0.25（mean-loss单位）。GIF此处使用sum loss、全训练参数和不同的右端项；不能复制25。CPU显式交叉熵Hessian验证了：sum→mean时，H、v、scale与shift必须一致缩放，才能保持同一解。

## 固定原图的Retrain差距

![求解轨迹与概率差距](evidence/solver-evidence.svg)

{gap_table}

概率RMSE按测试节点×类别的softmax概率计算；类别差异是与匹配Retrain预测不同的测试节点数。50%条件的RMSE由0.056092降至0.049296，类别差异由38降至36，仍有明显差距。10节点条件F1不变，但概率已变化；F1不变本身不是失败判据。

{confirmation_table}

额外确认沿用已有Cora随机Selection、seed212和seed2024的checkpoint与匹配Retrain，未新增选点或重训。seed2024的类别差异从9增至11，虽然概率RMSE略降，因此不能宣称所有预测差距一致改善；seed212即使F1等于Retrain，仍有10个测试节点预测不同。

## 为什么需要分开修复对照

仅修求解、保留错误删图时，10节点条件就有11个测试类别翻转；完整修复同条件为0。这说明放大更新会放大错误输入的影响，不能把更大的F1变化当成更正确的遗忘。

{arms}

## 验证、身份与范围

- **PASS / 软件与数值验证**：13项最终针对性CPU测试覆盖显式二次型及交叉熵Hessian参考解、sum/mean缩放、阻尼残差、负曲率失败、非有限值、零右端项、训练标签边界、删边顺序、失败不写模型/Output及producer变化。另复用同字节实现的37项消费者/IDEA测试；其中2项旧fixture的scale类型修正后单独通过。共50个不同测试问题通过，不把失败fixture记录删除。
- **PASS / 真实诊断交付**：18/24次更新预算已用，含3次明确拒绝；2/6次额外确认已用；1/3次新增Retrain已用。初次曲率检查的CPU/CUDA比较错误发生在任何更新之前；更新后的汇总索引错误没有重跑更新，通过只读compare阶段补全。失败日志、旧运行目录均保留。
- **PASS / 输入与输出身份**：原图及持久化split、checkpoint、Selection和Retrain引用核验；真实adapter producer与本地候选一致。完整模型与数据留在SSH，回传摘要、哈希与引用。[输入输出清单](evidence/input-output-manifest.json) / [最终核验](evidence/final-verification.json)。
- **NOT CONFIRMED / 科研有效性**：没有证明GIF等价于完整Retrain，没有隐私或完整遗忘证明；大删除下的一阶局部近似、阻尼目标和非精确驻点都限制结论。仅覆盖Cora/GCN和本次既有输入，不外推所有数据/模型，也不承诺恢复五月效果。
- IDEA源码存在同类无收敛检查递推，但本次仅排查关联，未修改或重跑IDEA。IF选点、正式Cache、049历史及生产矩阵保持原样。
- 旧全局默认参数未被本例参数替换；在新检查下未收敛会明确失败。这里的4096/0.005是经过本次有界验证的配置，不是全数据集默认值。

当前候选：`{a.candidate}`。最初真实更新绑定7122ba70，后续57ea01a4只修改诊断恢复/确认工具与测试；生产修复字节相同。最终报告生成工具的改变不影响已测模型更新。049监督边界复用来源为47282e6，未接受或合并049。本次未合并、push、安装或启动正式矩阵。

## 复查入口

[WorkItem](WORKITEM.md) · [固定输入计划](evidence/PLAN.md) · [预登记参数](evidence/source-updates-v1/update-plan.json) · [曲率数据](evidence/curvature-v2.json) · [18次更新及Retrain比较](evidence/compare-v1.json) · [2次真实adapter确认](evidence/confirm-v1.json) · [所有对照CSV](evidence/cells.csv) · [复跑说明](evidence/REPRODUCE.md)
'''
    (a.item/'REPORT.md').write_text(markdown,encoding='utf-8')
    render=mistune.create_markdown(plugins=['table'])
    human,body=markdown.split('## 已证实的两处问题',1)
    human=human.replace('## Human Result','').replace('> 当前验收决定：`待决定`','<p>当前验收决定：<span data-workblock-decision="pending">待决定</span></p>')
    # Raw HTML is limited to the trusted decision projection and embedded figure.
    render=mistune.create_markdown(escape=False,plugins=['table'])
    body_html=render('## 已证实的两处问题'+body)
    svg=(ev/'solver-evidence.svg').read_text(encoding='utf-8')
    svg=svg[svg.index('<svg'):]
    body_html=body_html.replace('<img src="evidence/solver-evidence.svg" alt="求解轨迹与概率差距" />',svg)
    html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AAGU-052 · GIF 求解研究</title>
<style>body{margin:0;background:#f0f3f5;color:#182a36;font:16px/1.75 "Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1120px;margin:32px auto;padding:36px 44px;background:white;border-top:6px solid #087e8b}h1{font-size:29px;line-height:1.4;margin:0 0 20px}h2{margin-top:44px;font-size:24px}h3{font-size:18px;margin:18px 0 8px;color:#087180}p{margin:10px 0}a{color:#06788e}table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}th{background:#e7f2f3;text-align:left}th,td{padding:9px 10px;border-bottom:1px solid #dbe3e7}code{font-size:.9em;overflow-wrap:anywhere}li{margin:10px 0}svg,img{max-width:100%;height:auto}section[data-workblock-human-result]{padding-bottom:22px;border-bottom:2px solid #d8e6e8}span[data-workblock-decision]{background:#fff0ca;padding:3px 12px;border-radius:4px}blockquote{border-left:4px solid #b8cdd1;margin:12px 0;padding-left:15px}@media(max-width:760px){main{margin:0;padding:22px 16px}table{display:block;overflow:auto}h1{font-size:25px}}</style><main>'''+ '<section data-workblock-human-result>'+render(human)+'</section>'+body_html+'</main></html>'
    (a.item/'REPORT.html').write_text(html,encoding='utf-8')
    with (ev/'cells.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        fields=['arm','k','status','matched_residual','undamped_residual','micro_f1','flips','relative_parameter_l2']
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for row in result['cells']:
            record={key:row.get(key) for key in fields}
            record.update(micro_f1=row['original_test']['micro_f1'],flips=row['original_test']['flips'])
            if row['status']=='rejected':record['matched_residual']=row['solver']['relative_residual']
            writer.writerow(record)
    print('Rendered paired report and scientific figures')


if __name__=='__main__':main()
