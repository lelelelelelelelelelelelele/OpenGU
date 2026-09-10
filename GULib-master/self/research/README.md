# 实验研究总览与配置单

[打开研究总览](index.html) · [独立SVG框图](diagram/research-framework.svg)

Phase 1 / Phase 2 是已有研究阶段，IF / IM 是方法分组。IM保持独立研究线，不从IF进度推断其运行前置。X1–X8保留核心研究问题；没有配置单的问题显示“配置单待形成”，不自动扩张已批准矩阵。

研究总览只列出回答明确研究问题的配置与分析。工程能力验证、预热和缓存复用检查由原工程任务承接，不作为研究节点、实验单或附属Gate展示。预算变化只有在用于研究剂量响应等明确问题时才纳入。

## 唯一来源

- [framework.json](framework.json) 只拥有研究阶段、方法标签、问题分类与配置单目录，不保存任务状态、优先级、Claim或Block依赖。
- [experiments/](experiments/) 每张JSON是独立实验配置单的内容源：问题、完整实验故事、评价、输出、准备缺口与明确核对的运行/分析引用。独立HTML由它生成，不是旧EXP WorkItem的重命名。
- `experiments/configs/` 的既有YAML拥有可执行定义。配置单不复制可执行参数树，也不修改现有YAML；人类可读范围必须与所引用版本核对。新的运行定义未定时标记draft，不把旧表当作新表启动。
- 指定run.json与产物保存运行事实；分析报告保存结论。关联WorkItem仅作为原始讨论、历史或软件前提，不读取其生命周期推断实验完成。
- [旧覆盖CSV](../dashboard/config_inventory.csv) 仅保留历史原始材料，不参与新总览或配置单生成。

## 更新与生成

普通Block新增、编辑、推进不会更新这些文件。只有研究设计或已核对的实验事实变化时更新对应配置单，不恢复WORKPLAN、逐Block状态表或自动暂存hook。

```powershell
python -B -X utf8 scripts/dashboard/gen_research_overview.py
python -B -X utf8 scripts/dashboard/gen_research_overview.py --check --check-links --verify-evidence
python -B -X utf8 -m pytest -q tests/test_research_overview.py
```

Linked worktree中加 `--canonical-root E:/project/OpenGU/GULib-master`，让记录与结果链接指向唯一canonical来源；源码/YAML仍指向本候选。DocMap从canonical项目的既有兄弟位置解析。可用`--output-dir`生成独立预览，全部内部链接按输出位置计算，不复制记录或结果。

HTML/SVG/PNG是忽略的本地生成物；生成器只写目标页面，修改记录或重新生成不会制造额外tracked diff。源码、样式、目录与配置单内容进入同一软件候选。

## 状态语义

准备：draft待形成，defined配置已定，review范围待复核，preparing运行准备中，waiting等待输入。配置已定不是GPU准入。

运行：unknown待核对，unbound未绑定，pending显式待跑，running/partial/failed有对应运行事实，completed须指定run身份和条件数，not_required仅用于离线分析单。无结果链接不能自动计0；存在预热证据不能算主矩阵完成。

分析：not_started、working、review、complete，独立于运行状态。已有结果可进入待分析；分析单可以引用多张输入。review不等于科学接受。运行队列不包含未知是否运行的条目。

`--check-links`只核对路径存在；`--verify-evidence`额外核对显式绑定的manifest摘要、experiment/run/code身份、配置路径、逻辑条件去重与每个声明产物SHA-256。不扫描其他运行，不调用producer、同步或调度程序。

研究问题以可折叠完整段落呈现：说明动机、比较和解释边界，再从同一配置单来源显示运行与分析进度。X1–X8只作为内部关联标识；已有结果数量不代表整个研究问题完成。

总览优先按IF簇、IM簇、共同参照和跨实验分析组织实验；每项实验可跳到问题说明，问题说明反向列出相关实验。详情页直接通过项目已有PyYAML解析引用配置，按原键顺序展示YAML与文件名；生成时读取文件，页面不是实时编辑器，不展开引用文件或运行配置。手工控制/变量/范围副本已删除。
