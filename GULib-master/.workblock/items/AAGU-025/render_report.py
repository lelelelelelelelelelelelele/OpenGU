"""Render the AAGU-025 paired decision surface from its verified evidence."""
from pathlib import Path
import html
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
E = HERE / "evidence"
verification = json.loads((E / "verification.json").read_text(encoding="utf-8"))
junit = ET.parse(E / "junit.xml")
cases = list(junit.iter("testcase"))
properties = {
    case.attrib["name"]: {p.attrib["name"]: p.attrib["value"] for p in case.findall("./properties/property")}
    for case in cases
}
cold = properties["test_default_real_entry_cold_hot_and_shared_store"]
qa_path = E / "render-qa.json"
qa = json.loads(qa_path.read_text(encoding="utf-8")) if qa_path.exists() else {"status": "NOT OBSERVED"}
workitem = (HERE / "WORKITEM.md").read_text(encoding="utf-8")
accepted = "当前状态: `accepted`" in workitem
decision, decision_attr = ("接受", "accepted") if accepted else ("待决定", "pending")
md, body = [], []

def heading(level, text):
    md.append("#" * level + " " + text + "\n")
    body.append(f"<h{level}>{html.escape(text)}</h{level}>")

def paragraph(text):
    md.append(text + "\n")
    body.append("<p>" + html.escape(text) + "</p>")

def links(items):
    md.append(" · ".join(f"[{label}]({target})" for label, target in items) + "\n")
    body.append("<p class='links'>" + " · ".join(f"<a href='{html.escape(target)}'>{html.escape(label)}</a>" for label, target in items) + "</p>")

def table(headers, rows):
    md.append("| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |")
    md.extend("| " + " | ".join(map(str, row)) + " |" for row in rows)
    md.append("")
    table_class = " class='checks'" if headers == ["场景", "实际观察", "判断"] else ""
    body.append("<div class='table-wrap'><table" + table_class + "><thead><tr>" + "".join("<th>"+html.escape(h)+"</th>" for h in headers) + "</tr></thead><tbody>")
    for row in rows:
        body.append("<tr>" + "".join("<td>"+html.escape(str(cell))+"</td>" for cell in row) + "</tr>")
    body.append("</tbody></table></div>")

heading(1, "AAGU-025 · 通用缓存原位接入 Cache V2")
paragraph("软件验收 · behavior / integration / data · 2026-09-03")
body.append('<section data-workblock-human-result="2.1">')
heading(2, "Human Result")
heading(3, "实际增量")
paragraph("通用 Result、Selection、Score 现在默认共用 Cache V2，保留正常缓存能力；旧后端、Legacy 回退和自动建目录逻辑已移除。collateral、预热和相关执行入口同步接入，现有正式 Artifact 合同继续可读。")
heading(3, "核心观察")
paragraph("在隔离 CPU 输入上，默认真实入口冷启动 MISS，第二次命中同一个 Evaluation Artifact，两次请求只执行一次训练/遗忘计算；Score 计算也完成冷/热复用。改变图、特征、标签、候选集、划分、模型或种子时，旧结果均未被复用。")
paragraph("干净代码检查点通过 293 项相关回归，通用矩阵 dry-run 展开 180 个 cell。三个真实 Legacy 根与现存 Cache V2 共 75 个文件，路径、大小及 SHA-256 全部保持一致；入口文件访问审计未发现 Legacy 读写或创建。")
links([("完整验证记录", "evidence/verification.json"), ("场景与 Artifact 身份", "evidence/junit.xml"), ("缓存保护清单", "evidence/cache-before.json")])
heading(3, "当前决定")
md.append("> 当前验收决定：`" + decision + "`\n")
body.append('<p class="decision"><span data-workblock-decision="' + decision_attr + '">' + decision + '</span></p>')
paragraph("Agent 建议接受此次软件接入：已观察到默认缓存、精确复用、身份拒绝和数据保护。决定者为用户，决定对象是包含本报告的源分支干净 HEAD。当前停在 awaiting_acceptance；尚未接受或执行 Apply。")
body.append("</section>")

heading(2, "行为与集成判断")
table(["场景", "实际观察", "判断"], [
    ("默认冷/热执行", "真实 AttackManager 与 demo CLI 冷启动写入 Selection/Evaluation；热请求复用同一 Artifact，计算次数为 1。", "PASS"),
    ("Selection 单独命中", "改变目标训练参数或 GU 方法后，Selection 可以精确复用，但 Evaluation 独立 MISS；原选点耗时从 V2 header 读取。", "PASS"),
    ("Score 能力", "真实 TracIn、IM、Hybrid 消费者完成写入与读取；warm Score 的 producer 被 fail-if-called 断言保护。实际权重或特征变化后精确 MISS。", "PASS"),
    ("开关语义", "全局关闭时 Result、Selection、Score 的可选读写均被跳过且不建 store；只关闭 Score 时，Selection/Evaluation 仍可用；单次 use_cache 覆盖也生效。", "PASS"),
    ("身份与完整性", "7 类输入变化均产生新结果身份；损坏 Selection 在计算前拒绝；同一 Score Recipe 的不同内容进入冲突隔离，原 payload 保留。", "PASS"),
    ("Legacy 路径", "文件 open/mkdir/listdir/scandir/remove/rename 审计覆盖默认入口和 CLI，访问违规数为 0；静态扫描仅作为补充。", "PASS"),
    ("正式入口", "已验证 Artifact 经正式输入接口进入真实 pipeline；store 字节不变。既有 Cache V2、target-direct Recipe/manifest/split/stage 回归通过。", "PASS"),
    ("AutoReport", "通用冷启动显示 MISS，热请求显示 HIT；V2 Selection/Evaluation 均绑定 Artifact/hash，标记 authoritative。", "PASS"),
])
paragraph("验证数据为 8 节点合成图和 2 类 CPU 线性模型；测试注入数据准备与具体 GU 方法，训练/重训各执行两步。AttackManager、CLI 参数链、策略、V2 store/resolver 和 AttackPipeline 的选点后执行编排为生产代码。这证明软件接入行为，不构成新数据集上的研究结果，也不代替真实 GPU 方法的科学验收。")

heading(2, "精确冷/热证据")
table(["字段", "观察"], [
    ("冷 Selection", cold["cold_selection_artifact"]),
    ("冷 Evaluation", cold["cold_result_artifact"]),
    ("热 Evaluation", cold["warm_result_artifact"]),
    ("Evaluation Recipe SHA-256", cold["result_recipe_hash"]),
    ("Evaluation Content SHA-256", cold["result_content_hash"]),
    ("两次请求的计算次数", cold["compute_calls_cold_plus_hot"]),
    ("Legacy 文件访问违规数", cold["legacy_access_violations"]),
])
rows = []
for change in ("features", "labels", "graph", "candidates", "split", "model", "seed"):
    p = properties["test_identity_changes_reject_old_result[" + change + "]"]
    rows.append((change, p["old_artifact"], p["new_artifact"]))
table(["变化", "此前 Artifact", "变化后 Artifact（MISS）"], rows)

heading(2, "真实缓存保护")
paragraph("开工前只读记录每个文件的相对路径、大小与 SHA-256；干净候选 Verify 后重新枚举并逐项比对，相等而非仅数量相同。所有临时 Artifact store 均位于测试临时目录。")
table(["真实根目录", "文件数", "字节数", "前后判断"], [
    (name, value["files"], value["bytes"], "完全相同")
    for name, value in verification["protected_caches"].items()
])
paragraph("未发起 SSH 操作，未启动正式 GPU 实验，未移动、删除或改写真实旧 payload，也未改写既存 V2 Artifact。SSH payload 未逐文件复查，因此不声明完成远端数据核验。AAGU-023 inventory、ledger、报告与物理归档仍由原 Block 拥有。")
links([("逐文件保护清单", "evidence/cache-before.json"), ("前后对比及 tree hash", "evidence/verification.json")])

heading(2, "实现边界与审阅记录")
paragraph("通用 GU 只返回聚合指标，不能伪造 Prediction。新增的 Selection-dependent Evaluation 载荷使用既有 FormalArtifactStore、索引、resolver、header 与依赖校验；已有 Prediction-dependent Evaluation 的合同及 Artifact 不变。Cache 层未加入数据加载或实验计算。")
paragraph("删除仅涉及过时的缓存转换/注入/读取源码及其失效测试；预热和监视能力已更新到 V2。不同 k 使用精确请求；此接入不沿用 Legacy 的目录扫描和隐式子集回退。")
paragraph("早期 demo 测试曾经走到 AutoReport 的默认输出位置，新建了 15 条测试事件。已通过创建时间、事件身份及全部临时 Artifact 路径确认归属，原字节移入本 Block 测试证据；测试随后显式隔离三个 AutoReport 输出路径，仓库投影由原 generator 重建，最终与原 tracked 内容一致。事件字节未改写。")
links([("早期测试事件原字节", "evidence/early-test-events.jsonl"), ("接入说明", "../../../docs/generic_cache_v2.md")])

heading(2, "候选与验证范围")
paragraph("候选是当前源分支 refs/heads/codex/aagu-025-unified-cache-v2 的干净 HEAD，包含本报告。行为回归的精确已测检查点为 " + verification["checkpoint"] + "；后续报告提交只增加本 item 的 Record、配对报告和证据，实际差异将单独复核后复用上述通过结果。")
paragraph("Apply target 为 refs/heads/main，基线 7a2c11fb06cff01363d7773c446370e1588ade4a。用户接受前不合并、不推送、不安装、不清理 Claim。")
links([("权威 WorkItem", "WORKITEM.md"), ("最终 HEAD 与差异核验", "../../runtime/aagu025-final-verify.json"), ("pytest 输出", "evidence/regression.txt"), ("dry-run 输出", "evidence/generic-dry-run.txt")])
paragraph("回归：293 passed，1 warning；退出码 0。覆盖通用消费者、CLI、AutoReport、缓存完整性与依赖、target-direct 和运行器。dry-run：180 would_run，退出码 0。新增/修改 Python 源码 AST 解析及 git diff --check 通过。")
paragraph("报告渲染检查：" + qa["status"] + ("。桌面与窄屏已实际查看，决定区和正文可读，无横向溢出或断图。" if qa["status"] == "PASS" else "。尚待实际打开并检查桌面和窄屏。"))
if qa["status"] == "PASS":
    links([("渲染核验记录", "evidence/render-qa.json")])

(HERE / "REPORT.md").write_text("\n".join(md).rstrip()+"\n", encoding="utf-8")
css = """
*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#18242e;font:16px/1.75 'Segoe UI','Microsoft YaHei',sans-serif}
main{max-width:1080px;margin:0 auto;padding:36px 44px 64px}h1{font-size:30px;line-height:1.35;margin:0 0 12px}
h2{font-size:23px;line-height:1.35;margin:40px 0 16px}h3{font-size:17px;margin:18px 0 6px;color:#284c68}
p{margin:7px 0 14px}section{background:white;border:1px solid #d5e0e8;border-top:4px solid #236383;border-radius:10px;padding:20px 28px;margin:22px 0}
section h2{margin:0 0 10px;font-size:14px;text-transform:uppercase;letter-spacing:.07em;color:#627889}
section h3{margin-top:12px}a{color:#16607e;text-decoration:underline;text-underline-offset:3px}.links{font-size:14px}
.decision{display:inline-block;padding:3px 15px;background:#fff2ca;border:1px solid #e7c56d;border-radius:20px;font-weight:650}
.table-wrap{width:100%;overflow-x:auto;margin:16px 0 22px}table{width:100%;border-collapse:collapse;background:#fff;font-size:14px;table-layout:fixed}
th,td{text-align:left;padding:11px 13px;border:1px solid #dbe3e9;vertical-align:top;overflow-wrap:anywhere}th{background:#e8eff4}
.checks th:nth-child(1){width:22%}.checks th:nth-child(2){width:63%}.checks th:nth-child(3){width:15%}
@media(max-width:700px){main{padding:22px 18px 40px}h1{font-size:25px}section{padding:16px 18px}h2{font-size:21px}table{font-size:12px}th,td{padding:8px}}
"""
document = "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AAGU-025 验收报告</title><style>"+css+"</style></head><body><main>"+"\n".join(body)+"</main></body></html>"
(HERE / "REPORT.html").write_text(document, encoding="utf-8")
print("Rendered REPORT.md and REPORT.html from verified checkpoint", verification["checkpoint"])
