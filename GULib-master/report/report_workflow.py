#!/usr/bin/env python3
"""
实验报告生成工作流

Usage:
    python report_workflow.py generate --group mg0_completion
    python report_workflow.py generate --all
    python report_workflow.py compare --group1 mg0_completion --group2 mg1_citeseer
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# 配置
REPORT_DIR = Path("report/analysis")
TEMPLATE_DIR = Path("report/templates")
RESULTS_DIR = Path("results/experiments")

# 阈值配置
THRESHOLDS = {
    "significant_effect": 0.05,
    "reverse_effect": -0.03,
    "high_variance": 0.5
}


def load_summary_files(group: str) -> List[Dict]:
    """Step 1: 加载实验汇总数据"""
    summary_files = list(RESULTS_DIR / group / "phase_a" / "*" / "_summary.json")
    all_data = []

    for sf in summary_files:
        try:
            with open(sf, 'r') as f:
                data = json.load(f)
                all_data.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {sf}: {e}")

    return all_data


def extract_metrics(data: Dict) -> Dict[str, Any]:
    """Step 2: 提取并聚合指标"""
    results = []

    for exp in data.get("experiments", []):
        method = exp.get("method", "unknown")
        strategy = exp.get("strategy", "unknown")

        # 提取关键指标
        metrics = {
            "method": method,
            "strategy": strategy,
            "f1_drop": exp.get("f1_drop", 0),
            "f1_drop_ratio": exp.get("f1_drop_ratio", 0),
            "retrain_gap": exp.get("retrain_gap", 0),
            "mia_auc": exp.get("mia_auc", 0),
            "attack_time": exp.get("attack_time", 0)
        }
        results.append(metrics)

    return aggregate_by_method_strategy(results)


def aggregate_by_method_strategy(results: List[Dict]) -> Dict:
    """按 method × strategy 聚合"""
    agg = {}

    for r in results:
        key = (r["method"], r["strategy"])
        if key not in agg:
            agg[key] = []
        agg[key].append(r)

    # 计算统计量
    summary = {}
    for (method, strategy), items in agg.items():
        f1_drops = [x["f1_drop"] for x in items]
        retrain_gaps = [x["retrain_gap"] for x in items]

        summary[f"{method}_{strategy}"] = {
            "method": method,
            "strategy": strategy,
            "f1_drop_mean": np.mean(f1_drops),
            "f1_drop_std": np.std(f1_drops),
            "f1_drop_min": np.min(f1_drops),
            "f1_drop_max": np.max(f1_drops),
            "retrain_gap_mean": np.mean(retrain_gaps),
            "sample_count": len(items)
        }

    return summary


def detect_problems(aggregated: Dict) -> List[Dict]:
    """Step 3: 问题识别"""
    problems = []

    for key, stats in aggregated.items():
        method = stats["method"]
        strategy = stats["strategy"]
        f1 = stats["f1_drop_mean"]

        # 问题 1: 攻击无效
        if abs(f1) < THRESHOLDS["significant_effect"]:
            problems.append({
                "type": "no_effect",
                "severity": "warning",
                "method": method,
                "strategy": strategy,
                "f1_drop": f1,
                "message": f"{method}+{strategy} 攻击效果不显著 (F1 drop: {f1:.2%})"
            })

        # 问题 2: 反效应
        if f1 < THRESHOLDS["reverse_effect"]:
            problems.append({
                "type": "reverse_effect",
                "severity": "info",
                "method": method,
                "strategy": strategy,
                "f1_drop": f1,
                "message": f"{method}+{strategy} 出现反效应，攻击反而提升性能"
            })

        # 问题 3: 高方差
        if stats["f1_drop_std"] > 0 and stats["f1_drop_std"] / abs(f1) > THRESHOLDS["high_variance"]:
            problems.append({
                "type": "high_variance",
                "severity": "warning",
                "method": method,
                "strategy": strategy,
                "std": stats["f1_drop_std"],
                "message": f"{method}+{strategy} 结果波动大 (std: {stats['f1_drop_std']:.4f})"
            })

    return problems


def generate_suggestions(aggregated: Dict, problems: List[Dict]) -> List[Dict]:
    """Step 4: 生成改进建议"""
    suggestions = []

    # 按方法类型分组
    learning_based = ["GIF", "GNNDelete"]
    shard_based = ["GraphEraser", "GUIDE"]

    # 识别有效策略
    effective = {k: v for k, v in aggregated.items() if v["f1_drop_mean"] > 0.05}
    ineffective = {k: v for k, v in aggregated.items() if v["f1_drop_mean"] < 0.01}

    if effective:
        best = max(effective.items(), key=lambda x: x[1]["f1_drop_mean"])
        suggestions.append({
            "title": "聚焦最有效攻击组合",
            "description": f"{best[1]['method']} + {best[1]['strategy']} 效果最佳 (F1 drop: {best[1]['f1_drop_mean']:.2%})，建议作为主要攻击对象",
            "priority": "high"
        })

    # 检查 learning-based 方法
    lb_issues = [p for p in problems if p["method"] in learning_based and p["type"] == "no_effect"]
    if lb_issues:
        suggestions.append({
            "title": "提高攻击比例 (ratio)",
            "description": "部分 Learning-based 方法攻击效果不显著，建议尝试 ratio=10% 或 20%",
            "priority": "medium"
        })

    # 检查 shard-based 方法
    sb_issues = [p for p in problems if p["method"] in shard_based and p["type"] == "reverse_effect"]
    if sb_issues:
        suggestions.append({
            "title": "Shard-based 方法反效应分析",
            "description": "IF/IM 策略对 Shard-based 方法无效甚至反效，可分析其防御机制作为论文贡献点",
            "priority": "medium"
        })

    return suggestions


def generate_report(group: str, data: Dict, aggregated: Dict, problems: List, suggestions: List) -> str:
    """Step 5: 生成报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 生成表格数据
    table_rows = []
    for key, stats in sorted(aggregated.items()):
        f1 = stats["f1_drop_mean"]
        std = stats["f1_drop_std"]

        # 问题标记
        flag = ""
        if f1 < THRESHOLDS["reverse_effect"]:
            flag = "🔄"
        elif abs(f1) < THRESHOLDS["significant_effect"]:
            flag = "⚠️"
        elif f1 > 0.1:
            flag = "✅"

        table_rows.append(f"| {stats['method']} | {stats['strategy']} | {f1:.2%} | ±{std:.3f} | {stats['sample_count']} | {flag} |")

    table = "\n".join(table_rows)

    # 问题列表
    problem_list = []
    for p in problems:
        emoji = {"no_effect": "⚠️", "reverse_effect": "🔄", "high_variance": "📊"}.get(p["type"], "•")
        problem_list.append(f"- {emoji} {p['message']}")

    problems_text = "\n".join(problem_list) if problem_list else "- 无明显问题"

    # 建议列表
    suggestion_list = []
    for s in suggestions:
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(s["priority"], "•")
        suggestion_list.append(f"### {priority_emoji} {s['title']}\n{s['description']}")

    suggestions_text = "\n\n".join(suggestion_list) if suggestion_list else "- 无特别建议"

    # 组名称映射
    group_names = {
        "mg0_completion": "Cora/GCN 稳定性实验",
        "mg1_citeseer": "Citeseer 数据集实验",
        "mg2_gat": "GAT 模型实验",
        "mg3_citeseer": "Citeseer 扩展实验",
        "mg3_gat": "GAT 扩展实验"
    }

    report = f"""# {group_names.get(group, group)} 技术分析报告

> 生成时间: {timestamp}
> 实验组: {group}

---

## 一、实验数据概览

| Method | Strategy | F1 Drop | Std | N | Flag |
|--------|----------|---------|-----|---|------|
{table}

---

## 二、核心发现

### 2.1 最有效攻击组合

{_get_best_attack(aggregated)}

### 2.2 无效/反效应组合

{_get_ineffective(aggregated)}

---

## 三、问题诊断

{problems_text}

---

## 四、改进建议

{suggestions_text}

---

## 五、下一步行动

- [ ] 分析更多实验组数据
- [ ] 验证问题是否普遍存在
- [ ] 设计针对性实验

---

*本报告由自动化工作流生成*
"""

    return report


def _get_best_attack(aggregated: Dict) -> str:
    """获取最有效攻击组合"""
    positive = {k: v for k, v in aggregated.items() if v["f1_drop_mean"] > 0}
    if not positive:
        return "无明显有效的攻击组合"

    best = max(positive.items(), key=lambda x: x[1]["f1_drop_mean"])
    return f"- {best[1]['method']} + {best[1]['strategy']}: F1 drop = {best[1]['f1_drop_mean']:.2%}"


def _get_ineffective(aggregated: Dict) -> str:
    """获取无效/反效应组合"""
    items = []
    for key, stats in aggregated.items():
        f1 = stats["f1_drop_mean"]
        if f1 < THRESHOLDS["significant_effect"]:
            flag = "反效应" if f1 < 0 else "效果不显著"
            items.append(f"- {stats['method']} + {stats['strategy']}: F1 drop = {f1:.2%} ({flag})")

    return "\n".join(items) if items else "- 无"


def save_report(group: str, content: str):
    """保存报告"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = REPORT_DIR / f"{timestamp}_{group}_analysis.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Report saved to: {filename}")
    return filename


def analyze_group(group: str) -> Dict:
    """分析单个实验组"""
    print(f"Analyzing group: {group}...")

    # Step 1: 加载数据
    all_data = load_summary_files(group)
    if not all_data:
        print(f"Warning: No data found for group {group}")
        return {}

    # Step 2: 提取指标
    aggregated = {}
    for data in all_data:
        metrics = extract_metrics(data)
        aggregated.update(metrics)

    # Step 3: 问题识别
    problems = detect_problems(aggregated)

    # Step 4: 改进建议
    suggestions = generate_suggestions(aggregated, problems)

    return {
        "group": group,
        "aggregated": aggregated,
        "problems": problems,
        "suggestions": suggestions
    }


def main():
    parser = argparse.ArgumentParser(description="实验报告生成工作流")
    subparsers = parser.add_subparsers(dest="command")

    # generate 命令
    gen_parser = subparsers.add_parser("generate", help="生成报告")
    gen_parser.add_argument("--group", type=str, help="实验组名称")
    gen_parser.add_argument("--all", action="store_true", help="生成所有实验组报告")

    # analyze 命令
    ana_parser = subparsers.add_parser("analyze", help="仅分析数据")
    ana_parser.add_argument("--group", type=str, required=True)

    # compare 命令
    cmp_parser = subparsers.add_parser("compare", help="对比实验组")
    cmp_parser.add_argument("--group1", type=str, required=True)
    cmp_parser.add_argument("--group2", type=str, required=True)

    args = parser.parse_args()

    if args.command == "generate":
        groups = [args.group] if args.group else ["mg0_completion", "mg1_citeseer", "mg2_gat"]
        for g in groups:
            result = analyze_group(g)
            if result:
                report = generate_report(g, {}, result["aggregated"], result["problems"], result["suggestions"])
                save_report(g, report)

    elif args.command == "analyze":
        result = analyze_group(args.group)
        print(json.dumps(result, indent=2, default=str))

    elif args.command == "compare":
        r1 = analyze_group(args.group1)
        r2 = analyze_group(args.group2)
        # TODO: 实现对比逻辑
        print("Compare feature not implemented yet")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
