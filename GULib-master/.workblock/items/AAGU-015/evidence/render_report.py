"""Render the paired configuration-checkpoint report from verified definitions."""
from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
ROOT = HERE.parents[3]


def main():
    summary = json.loads((HERE / 'definition-summary.json').read_text(encoding='utf-8'))
    counts = summary['counts']
    title = 'AAGU-015 · Selector 两阶段实验与证据'
    increment = (f"已完成当前阶段的实验方案、实际 YAML 与能力覆盖检查。方案给出 Q1–Q4 的比较、控制和指标，"
                 f"449 份 YAML 保持一致，并重新无写入展开为 {counts['stage_s']} 个 S cell / {counts['stage_u']} 个 GU cell。"
                 "现有入口不能完整覆盖 Stage U，相关缺口已明确记录。本次交付实验定义材料，没有执行全量实验或新增通用实验代码。")
    observations = [
        ('PASS（阶段方案）', '实验方案逐项列出 Q1–Q4、17 个 Selector 分组、固定条件、比较规则、阶段 U 与重训练参照，以及指标输入和解释边界；范围只覆盖当前阶段。'),
        ('PASS（实际配置）', '449 份 YAML 的哈希与既有检查点全部一致；324 张计划再次由实际 parser/dry-run 展开为 306/612 cell，未读数据或调用 producer。两 GU 中没有伪造的 Retrain 方法。'),
        ('PASS（覆盖核对）', '已核对 modular、target-direct、通用评估与 SM-005：各自支持与限制均有源码依据。完整执行覆盖不成立，已明确记录；这项 PASS 指覆盖说明准确，不代表所有消费者通过。'),
        ('PASS（职责和缺口）', '026 的通用代码、SM-005 的远程工具验证与 015 的实验定义分开。Retrain 辅助函数已有，但独立方法未注册；当前 27 个 WorkItem 未找到专门 Block。Metrics 路径仍有主动训练调用。'),
        ('PASS（交付材料）', '方案、配置说明、能力表与配对报告使用一致范围。当前验收对象是实验定义材料；缺失能力及真实输入绑定留给后续明确的实现/执行工作，不自动扩大 015。'),
    ]
    decision = ('Agent 建议接受本阶段的实验方案、配置和能力覆盖材料，由用户决定接受或返工。'
                '接受这些材料不表示 Stage U 全部可执行，也不自动创建 Retrain Block、修复通用代码或启动 GPU/全矩阵。')
    defaults = [
        ('Dataset/Split', 'Cora / CiteSeer / PubMed；70/10/20；split seed 2024'),
        ('模型与训练', 'GCN，两层，hidden 64，dropout 0.5；100 epochs；Adam；lr 0.005；weight decay 0.000001；无 scheduler'),
        ('训练 seeds / 预算', '42、212、2024；训练候选数的 1% / 5%；floor_with_minimum_one'),
        ('Selector 默认', 'last_layer；validation-conditioned 方法使用 val_mask；LiSSA 20 / scale 25 / damp 0.01；B Hutchinson 32 probes / seed 1729'),
        ('对照与 checkpoint', 'random seed 104245；CP3=[1,50,100]；CP6=[1,10,25,50,75,100]'),
        ('GNNDelete', 'unlearn_lr 0.01；50 epochs；alpha 0.5；mse_mean / both_layerwise；Adam'),
        ('GIF', 'iteration 100；scale 1000000000；damp 0；GIF_method=GIF'),
        ('评价', 'post_unlearning_utility_and_retrain_gap；当前 modular 消费者拒绝，不降为 utility-only'),
    ]
    sharing = [
        ('训练准备', str(counts['conditional_preparation_groups']), '3 数据集 × 3 训练 seeds；checkpoint 仍需精确内容验证'),
        ('Score', str(counts['conditional_score_groups']), '15 个模型型方法 × 9，加 degree/random 各 3；Score 与预算无关'),
        ('Selection', str(counts['conditional_selection_groups']), '141 个条件 Score 组 × 2 预算；具体集合重合尚未观测'),
    ]
    questions = [
        ('Q1', 'A↔B；point/simple/graph 的 Hessian-free proxy ↔ 对应 IF/GIF 参考', '同候选 score 相关性与同预算选集重合度'),
        ('Q2', '固定 Hessian 处理与 checkpoint，分别比较 point/simple/graph', '区分 source 改变与求解器改变'),
        ('Q3', 'A/B 参数变化组 ↔ validation-conditioned IF/GIF；附控制', '选集差异不直接推导攻击效果'),
        ('Q4', '每种 source 的 final、CP3、CP6 及对应 final 参考', '轨迹变化与参考一致性分别解释'),
    ]
    gates = [
        ('modular', '部分支持', '17 Selector、固定 Selection→GNNDelete/GIF、utility；当前拒绝 retrain-gap case。'),
        ('target-direct', '固定配方支持', '已有重训练比较路径，GU 表/manifest/构建器限定 GNNDelete；不能直接接收 015 全部组合。'),
        ('通用 runner / collateral', '原语及调用存在', '已有重训练与预测诊断，但使用另一配置/身份合同；015 的完整对应关系未验证。'),
        ('SM-005', '已有实际工具链证据', 'Cora Degree、B-Hutch cold/warm、D-full；不等于 015 矩阵 launcher。'),
        ('Retrain 独立方法', '未注册 / 未完整实现', '辅助 run_retrain 已存在；GU 方法表没有 Retrain，未找到专门 Block。'),
        ('完整执行支持', '未完整覆盖', '输入/Selection 绑定、独立 Retrain、删除语义、扩展评价与已报告的 GU 读回差异需后续处理。'),
    ]
    evidence = [
        ('当前阶段完整实验方案', 'EXPERIMENT_PLAN.md'),
        ('入口覆盖与 Retrain 登记/实现核对', 'CAPABILITY_COVERAGE.md'),
        ('配置说明与生成命令', '../../../experiments/configs/aagu015/README.md'),
        ('阶段 S 源表', '../../../experiments/configs/aagu015/stage_s.yaml'),
        ('阶段 U 源表', '../../../experiments/configs/aagu015/stage_u.yaml'),
        ('有效参数、449 份 YAML 哈希与检查摘要', 'evidence/definition-summary.json'),
        ('本轮源码与配置覆盖核验', 'evidence/capability-audit.json'),
        ('306 个 S cell 与条件共享依赖', 'evidence/stage-s-cells.csv'),
        ('612 个 U cell 与固定 Selection 来源', 'evidence/stage-u-cells.csv'),
        ('可重跑定义验证器', 'evidence/verify.py'),
        ('本轮完整无写入展开', '../../runtime/aagu015/definition-expansion-materials.json'),
        ('原配置检查点的验证回执', '../../runtime/aagu015/verification.json'),
        ('本次桌面首屏渲染', '../../runtime/aagu015/report-materials-desktop.png'),
        ('本次窄屏渲染', '../../runtime/aagu015/report-materials-narrow.png'),
        ('本次完整报告渲染', '../../runtime/aagu015/report-materials-full.png'),
        ('当前 WorkItem', 'WORKITEM.md'),
    ]
    verification = ('复用精确配置检查点 59baa2ae909e7fba92278d9201c635b80be65cdc 上的 8 项针对性回归与两个 CLI dry-run；'
                    '本轮未改 YAML、生成器或消费者。重新完成 449 份 YAML 哈希一致性、324 个实际 parser 计划展开、'
                    'modular retrain-gap 拒绝与 Retrain 方法拒绝检查。source 中 7 个现存保护文件哈希前后相同，其余保护目录仍缺失。'
                    '主项目源码 53e1da5b 的方法注册、入口与 27 个 WorkItem 已核对；SM-005 D-full 回传文件哈希与回执一致。'
                    '这些证据证明材料与实现现状相符，不证明全部实验已执行或产生科研结论。'
                    '旧定义摘要的 execution_ready=false 与 blocking_inputs 描述运行准备，不能解释为本阶段方案材料未交付。')
    render_note = 'HTML 已在 1440×1100 桌面、600×1800 窄屏与 1440×4600 完整页面渲染并查看：标题、正文、表格与决定区可读，无可见重叠或横向截断。此观察只证明报告可读。'
    md = [f'# {title}', '', '## Human Result', '', '### 实际增量', '', increment, '',
          '主要证据：[完整实验方案](EXPERIMENT_PLAN.md) · [能力覆盖与 Retrain 核对](CAPABILITY_COVERAGE.md) · [核验记录](evidence/capability-audit.json)。',
          '', '### 核心观察', '']
    md += [f'{i}. **{status}** — {text}' for i, (status, text) in enumerate(observations, 1)]
    md += ['', '### 当前决定', '', '> 当前验收决定：`待决定`', '', decision, '']
    def md_table(heading, headers, rows):
        md.extend(['## ' + heading, '', '| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |'])
        md.extend('| ' + ' | '.join(row) + ' |' for row in rows)
        md.append('')
    md_table('当前阶段研究问题', ('问题', '主要比较', '判断边界'), questions)
    md_table('默认展开与当前科研配置', ('配置项', '实际展开值'), defaults)
    md_table('条件共享依赖', ('对象', '配置组数', '解释'), sharing)
    caveat = '组标识是有效配置的比较指纹，不是 Recipe/Artifact 哈希、实际训练次数或 HIT。真实数据、候选、checkpoint 与 producer 身份一致后才允许共享。'
    md += [caveat, '']
    md_table('入口覆盖与后续缺口', ('入口/事项', '支持情况', '当前事实'), gates)
    md += ['## 验证与证据', '', verification, '', render_note, '']
    md += [f'- [{label}]({url})' for label, url in evidence]
    md += ['', '## 生成 YAML 示例', '']
    examples = [('阶段 S：Cora / seed42 / 1%', 'stage_s/cora-seed42-r0.01.yaml'),
                ('阶段 U：同一 degree Selection → GNNDelete / GIF', 'stage_u/cora-seed42-r0.01-degree.yaml')]
    snippets = []
    for label, relative in examples:
        content = (ROOT / 'experiments/configs/aagu015/generated' / relative).read_text(encoding='utf-8')
        snippets.append((label, content))
        md += ['### ' + label, '', '```yaml', content.rstrip(), '```', '']
    (ITEM / 'REPORT.md').write_text('\n'.join(md), encoding='utf-8')

    esc = html.escape
    def table(headers, rows):
        return '<div class="table"><table><thead><tr>' + ''.join('<th>' + esc(h) + '</th>' for h in headers) + '</tr></thead><tbody>' + ''.join(
            '<tr>' + ''.join('<td>' + esc(v) + '</td>' for v in row) + '</tr>' for row in rows) + '</tbody></table></div>'
    body = f'<header><p class="eyebrow">AAGU-015 · 实验定义材料 · 待验收</p><h1>{esc(title)}</h1></header>'
    body += '<section data-workblock-human-result="2.1"><h2>Human Result</h2><h3>实际增量</h3><p>' + esc(increment) + '</p><p>主要证据：<a href="EXPERIMENT_PLAN.md">完整实验方案</a> · <a href="CAPABILITY_COVERAGE.md">能力覆盖与 Retrain 核对</a> · <a href="evidence/capability-audit.json">核验记录</a>。</p><h3>核心观察</h3><ol class="observations">'
    body += ''.join('<li><strong>' + esc(status) + '</strong><span>' + esc(text) + '</span></li>' for status, text in observations)
    body += '</ol><h3>当前决定</h3><div class="decision"><span data-workblock-decision="pending">待决定</span><p>' + esc(decision) + '</p></div></section>'
    body += '<section><h2>当前阶段研究问题</h2>' + table(('问题', '主要比较', '判断边界'), questions) + '</section>'
    body += '<section><h2>默认展开与当前科研配置</h2>' + table(('配置项', '实际展开值'), defaults) + '</section>'
    body += '<section><h2>条件共享依赖</h2>' + table(('对象', '配置组数', '解释'), sharing) + '<p>' + esc(caveat) + '</p></section>'
    body += '<section><h2>入口覆盖与后续缺口</h2>' + table(('入口/事项', '支持情况', '当前事实'), gates) + '</section>'
    body += '<section><h2>验证与证据</h2><p>' + esc(verification) + '</p><p>' + esc(render_note) + '</p><ul class="links">'
    body += ''.join('<li><a href="' + esc(url, quote=True) + '">' + esc(label) + '</a></li>' for label, url in evidence) + '</ul></section>'
    body += '<section><h2>生成 YAML 示例</h2>' + ''.join('<details><summary>' + esc(label) + '</summary><pre>' + esc(content) + '</pre></details>' for label, content in snippets) + '</section>'
    style = '''*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#202b38;font:15px/1.65 "Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1160px;margin:auto;padding:30px 32px 70px}header{margin-bottom:24px}h1{font-size:30px;line-height:1.3;margin:8px 0}h2{font-size:21px;margin:0 0 18px}h3{font-size:16px;margin:16px 0 7px}p{margin:7px 0 14px}.eyebrow{color:#45647c;font-size:13px;letter-spacing:.08em}section{background:white;padding:26px 30px;border:1px solid #dfe5e9;border-radius:12px;margin-bottom:22px}.observations{padding-left:23px;margin:5px 0}.observations li{padding:5px 0}.observations strong{font-size:12px;color:#53697a;margin-right:10px}.decision{background:#fff7e5;border-left:4px solid #bc8424;padding:14px 18px}.decision span{font-weight:700;color:#7e5617}.decision p{margin:5px 0 0}.table{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid #e4e9ed;vertical-align:top}th{background:#f1f5f8}td:first-child{font-weight:600;min-width:115px}a{color:#14698f;text-underline-offset:3px;overflow-wrap:anywhere}.links{padding-left:23px}.links li{margin:6px 0}details{border:1px solid #dce4ea;border-radius:8px;margin:12px 0}summary{padding:13px;cursor:pointer;font-weight:600}pre{font:12px/1.6 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;padding:18px;background:#f5f8fa;margin:0}@media(max-width:640px){main{padding:18px 12px}h1{font-size:24px}section{padding:20px 17px}body{font-size:14px}.observations strong{display:block}th,td{padding:9px}td:first-child{min-width:75px}}'''
    (ITEM / 'REPORT.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + esc(title) + '</title><style>' + style + '</style><main>' + body + '</main></html>', encoding='utf-8')


if __name__ == '__main__':
    main()
