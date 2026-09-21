"""Render AAGU-052 implementation, configuration and table-recovery evidence."""
import argparse
import json
from pathlib import Path

import mistune


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--item',required=True,type=Path)
    parser.add_argument('--candidate',required=True)
    parser.add_argument('--decision',choices=['pending','accepted'],default='pending')
    args=parser.parse_args();ev=args.item/'evidence/rework-20260911'
    baseline=read(ev/'candidate-finite.json');confirm=read(ev/'config-confirm.json')
    verify=read(ev/'verification-finite.json');calibration=read(ev/'config-trajectories.json')
    assert confirm['finished'] and len(confirm['cells'])==9
    assert all(c['status']=='PASS' for c in confirm['cells'])
    assert verify['collection_sha256_verified']
    decision='接受' if args.decision=='accepted' else '待决定'
    rows='\n'.join(f"| {c['dataset']} | {next(x['applied_update_l2'] for x in baseline['cells'] if x['dataset']==c['dataset']):.6e} | {c['applied_update_l2']:.6e} | {c['solver']['relative_residual']:.6f} | {c['solver']['undamped_relative_residual']:.4f} |" for c in confirm['cells'] if c['seed']==42)
    markdown=f'''# AAGU-052 · GIF 实现与配置修复、表01恢复

## Human Result

### 实际增量

修复节点删图下标、首次 HVP 向量求导边界、训练标签使用范围和非有限写回。保持原 GIF 固定预算递推。依据用户进一步授权，修正 scale=1e9/100步几乎没有近似进展的配置；新参数先由九个既定模型曲率和预登记的数值稳定性规则选定，再观察实际输出。

### 核心观察

软件检查 PASS：{verify['cpu_tests']}项CPU检查；三个真实模型写回与独立递推逐位一致。配置修复另完成九个既定模型的真实写回，全部通过匹配方程残差检查。下表为seed42、同一原模型与Random删除集合：

| 数据集 | 原配置实际更新 L2 | 新配置实际更新 L2 | 匹配相对残差 | 无阻尼相对残差 |
| --- | --- | --- | --- | --- |
{rows}

配置固定为 **iteration=2000、scale=65536、damp=0.00390625**，实际方程为 **(H+256I)δ=v**。实际更新增加约1万至1.6万倍，这是选定参数后的观察，不是调参目标。三个seed42输入从2000加倍到4000步，更新变化仅0.019%–0.072%。这支持数值配置产生稳定校正，不证明无阻尼方程已精确求解或完整遗忘已实现。

### 当前决定

> 当前验收决定：`{decision}`

建议接受实现和配置修复，并依据用户“修复后跑完原表”的授权继续软件落地与正式执行。当前正式gate：{verify['formal_gate']}；原表：{verify['matrix']}；部署：{verify['deployed']}。不将局部诊断、dry-run或缓存数量当成整表完成。

## 配置选择依据

九个原模型的Hessian极端Ritz值约覆盖−108.502至42529.358。按预登记1.25倍裕量向上取二次幂，得到shift=256、scale=65536；Ritz值是经验谱估计，不是严格全谱界。统一参数用于全部数据集、种子和Selector，不逐攻击调参。

选定2000步的规则为三个seed42校准输入均满足匹配相对残差≤0.001，且相较4000步更新向量变化≤1%。这是一组配置的数值验证标准，生产有限递推仍如实记录残差，并不通过阈值提前停止。额外六个seed212/2024模型在固定参数下也通过。参数选取未消费测试F1、Retrain差距或攻击排序。

无阻尼缩放改进对照保留：scale65536、1600步时三个残差约0.300/0.163/0.414。未将有限但不稳定的校正称为精确逆，也未用MINRES替换原GIF。旧MINRES和阻尼诊断完整保留。

## 实现正确性与解释边界

原迭代为h₀=v，hₜ₊₁=v+(1−damp)hₜ−Hhₜ/scale，最后δ=h_T/scale，θ_new=θ+δ。独立矩阵幂级数测试覆盖不同步数和正/负曲率；HVP向量必须作为常量。旧首次HVP含额外求导项，不代表每次HVP都同样错或总是翻倍。L=θ²、v=θ、θ=1、scale=2、一步的实际入口回归，旧结果1.0，新结果1.5。

更新小本身不证明遗忘失败，但旧配置残差接近1、几乎零更新的组合确实显示近似进展不足。更新增大同样不能独立证明“内容已删除”；本修复负责正确、稳定且身份可追溯的GIF计算，方法在攻击下的性能和遗忘效果由完整实验另行分析。所有主F1继续在固定原图、同一测试节点和标签上计算。

依据：[作者实现](https://github.com/wujcan/GIF-torch/blob/main/exp/exp_GIF.py)；[论文 Eq.24与附录D](https://wujcan.github.io/papers/www23-gif.pdf)。

## 原表恢复与证据

新表位于experiments/configs/aagu052/table01.yaml，仅GIF数值小表发生语义改变；Dataset/Split、Selector、其他GU、训练和评估配置逐项相同。原270格GU与45匹配Retrain范围保留，原YAML和Cache不覆盖。新配置使用新指纹，新run为aagu052-gif-gate-v1、aagu011-table01-v3、aagu011-references-v2。

- 当前候选：`{args.candidate}`；生产算法测试检查点：`{baseline['candidate']}`。后续变化仅配置、登记与报告。
- [当前执行核验](evidence/rework-20260911/verification-finite.json)
- [配置选择规则](evidence/rework-20260911/config-trajectory-plan.json) / [稳定性轨迹](evidence/rework-20260911/config-trajectories.json)
- [九模型真实写回](evidence/rework-20260911/config-confirm.json) / [回传哈希](evidence/rework-20260911/config-evidence-receipt.json)
- [57项CPU检查](evidence/rework-20260911/cpu-finite-v2.xml) / [独立原递推检查](evidence/rework-20260911/candidate-finite.json)
- [270格新配置dry-run](evidence/rework-20260911/configured-dry-run-table01.json)

完整表格的执行、收集、匹配核验状态以当前执行核验记录为准，未通过的阶段不作完成声明。
'''
    (args.item/'REPORT.md').write_text(markdown,encoding='utf-8')
    body=mistune.create_markdown(plugins=['table'])(markdown)
    start=body.index('<h2>Human Result</h2>');end=body.index('<h2>',start+1)
    body=body[:start]+'<section data-workblock-human-result>'+body[start:end]+'</section>'+body[end:]
    body=body.replace('<code>'+decision+'</code>','<span data-workblock-decision="'+args.decision+'">'+decision+'</span>')
    document='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GIF 实现与配置修复</title><style>body{font:17px/1.8 system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 24px;color:#192737;background:#f6f8fb}h1,h2{line-height:1.3}section{background:white;border-left:5px solid #246b84;padding:20px 28px}table{border-collapse:collapse;width:100%;font-size:15px}td,th{padding:8px;text-align:left;border-bottom:1px solid #d5dce4}a{color:#126680}code{overflow-wrap:anywhere}blockquote{background:#edf3f7;padding:8px 20px;margin:15px 0}</style>'+body+'</html>'
    (args.item/'REPORT.html').write_text(document,encoding='utf-8')
    print(json.dumps({'report':str(args.item/'REPORT.md'),'candidate':args.candidate,'matrix':verify['matrix']}))


if __name__=='__main__':
    main()
