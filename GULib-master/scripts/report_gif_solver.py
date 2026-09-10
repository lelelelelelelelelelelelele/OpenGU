"""Render the current AAGU-052 repair evidence, preserving historical probes."""
import argparse
import html
import json
from pathlib import Path

import mistune


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--item',required=True,type=Path)
    parser.add_argument('--candidate',required=True)
    args=parser.parse_args()
    evidence=args.item/'evidence/rework-20260911'
    result=json.loads((evidence/'candidate-finite.json').read_text())
    verification=json.loads((evidence/'verification-finite.json').read_text())
    assert result['finished'] and len(result['cells'])==3
    assert verification['gpu_all_pass'] and verification['collection_sha256_verified']
    assert result['candidate']==verification['tested_candidate']
    rows='\n'.join(f"| {c['dataset']} | {c['k']} | {c['reference_parameter_max_abs_error']:.1e} | {c['applied_update_l2']:.6e} | {c['solver']['relative_residual']:.6f} |" for c in result['cells'])
    markdown=f'''# AAGU-052 · GIF 实现修复与表01恢复

## Human Result

### 实际增量

修复节点删图下标、首次 HVP 向量求导边界、训练标签使用范围和模型写回检查。按用户“只需要 GIF 是正确的”的澄清，恢复原 GIF 的固定次数近似递推，保留残差诊断；撤回将 residual≤1e-3 作为生产硬门槛及改用 MINRES 的方案。非有限计算和非有限参数仍在写入前拒绝。

### 核心观察

软件检查 PASS：{verification['cpu_tests']} 项 CPU 检查通过。Cora、CiteSeer、PubMed 的既有原表输入在 SSH/GPU 上执行，实际写回参数与独立 autograd-vector 参考递推逐位一致；内部删图匹配既有节点删除合同。真实探针只写隔离诊断，没有生成正式表格或 Cache Output。

| 数据集 | 删除节点 | 参数参考最大绝对差 | 实际更新 L2 | Hδ=v 相对残差 |
| --- | --- | --- | --- | --- |
{rows}

原表配置仍为 iteration=100、scale=1e9、damp=0。更新很小，残差接近1；这支持“代码正确执行了该配置规定的有限近似”，**不支持“该配置准确近似了 H⁻¹v”**。是否适合后续攻击机制分析需结合这一限制，不能把无明显变化直接解释为 GIF 抗攻击能力强。未按 F1 或 Retrain 差距选择参数。

### 当前决定

> 当前验收决定：`待决定`

建议接受实现层面的修复。原表恢复尚未完成：正式 gate、270 格 GU 和45格参照均未启动，SSH 活跃检出正在执行 AAGU-053 整表，部署前置条件尚不满足。用户此前已要求修复后跑完原表；执行占用解除后，沿用该授权完成必要版本同步及登记的新 run，不把本报告当作整表完成凭据。

## 正确性边界

原 GIF 的迭代为 h₀=v，hₜ₊₁=v+(1-damp)hₜ−Hhₜ/scale，最后 δ=h_T/scale，θ_new=θ+δ。测试用独立显式矩阵幂级数覆盖正/负曲率、阻尼和不同步数；生产代码不提前停止，不隐式改阻尼。残差阈值只标记诊断，不能改变固定预算结果。

首次 HVP 必须将向量视为常量。旧代码对含梯度图的 h₀ 再次求导，产生额外项；不是所有后续 HVP 都同样出错，也不总是翻倍。实际入口回归 L=θ²、v=θ、θ=1、scale=2、一步时，正确更新为1.5，旧实现为1.0。新实现通过独立参考。

“未收敛却写回”原先被过度概括为实现错误。有限迭代本身属于原方法；必须修复的是错误递推、错误 HVP、错误删图、错误监督或非有限结果冒充有效输出。2.95%的残差不是2.95%的参数误差、F1损失或遗忘失败率，也不是本项目已确立的实现验收门槛。

依据：[作者实现](https://github.com/wujcan/GIF-torch/blob/main/exp/exp_GIF.py)；[论文 Eq.24 与附录D](https://wujcan.github.io/papers/www23-gif.pdf)。这些依据约束算法实现，不证明当前大 scale 配置具有良好的近似精度。

## 原表恢复与证据

原范围：3 数据集 × 5 Selector × 6 GU × 3 seeds × 10%，270 格；45 匹配 Retrain。三个 dry-run 保持原配置指纹。新登记 run 为 aagu052-gif-gate-v1、aagu011-table01-v3、aagu011-references-v2。GIF producer 更新后不能复用旧 GIF Output；其他产物只经完整身份核验后复用，旧 Cache 和历史失败保留。

- 当前候选：`{args.candidate}`；数值测试检查点：`{result['candidate']}`。
- [独立真机参考](evidence/rework-20260911/candidate-finite.json) / [回传哈希核验](evidence/rework-20260911/candidate-finite-receipt.json)
- [57项CPU结果](evidence/rework-20260911/cpu-finite-v2.xml) / [当前核验状态](evidence/rework-20260911/verification-finite.json)
- [270格dry-run](evidence/rework-20260911/dry-run-table01.json) / [执行占用](evidence/rework-20260911/shared-runner-occupancy.log)
- [历史无阻尼MINRES诊断](evidence/rework-20260911/unshifted-float64.json)：保留失败与方法边界，已撤回生产替换建议。

未观察到当前候选正式 gate、整表重跑或部署。未据此接受任何科研结论。
'''
    (args.item/'REPORT.md').write_text(markdown,encoding='utf-8')
    render=mistune.create_markdown(plugins=['table'])
    body=render(markdown)
    start=body.index('<h2>Human Result</h2>')
    end=body.index('<h2>',start+1)
    body=body[:start]+'<section data-workblock-human-result>'+body[start:end]+'</section>'+body[end:]
    body=body.replace('<code>待决定</code>','<span data-workblock-decision="pending">待决定</span>')
    document='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GIF 实现修复</title><style>body{font:17px/1.8 system-ui,sans-serif;max-width:1080px;margin:40px auto;padding:0 24px;color:#192737;background:#f6f8fb}h1,h2{line-height:1.3}section{background:white;border-left:5px solid #246b84;padding:20px 28px}table{border-collapse:collapse;width:100%;font-size:15px}td,th{padding:8px;text-align:left;border-bottom:1px solid #d5dce4}a{color:#126680}code{overflow-wrap:anywhere}blockquote{background:#edf3f7;padding:8px 20px;margin:15px 0}</style>'+body+'</html>'
    (args.item/'REPORT.html').write_text(document,encoding='utf-8')
    print(json.dumps({'candidate':args.candidate,'report':str(args.item/'REPORT.md'),'formal_matrix':'NOT STARTED'}))


if __name__=='__main__':
    main()
