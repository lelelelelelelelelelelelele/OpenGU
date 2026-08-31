# AAGU-024 · COMP-042 exact candidate 真实 AAGU 探针

探针日期：2026-09-01  
COMP-042 candidate：`f6832b9dec0be903d9f8d83f50ba2bc2864dfbd7`  
COMP source branch：`refs/heads/codex/comp-042-mixed-version-campaign`  
COMP product checkout：`E:\project\workblockgraph`，探针时 HEAD 与 candidate 一致

## 输入隔离

为避免 WorkBlock Companion 的任何产品写能力触及 live AAGU，本探针把 canonical A 当前 `.workblock` 复制到新的临时 Git repository：

- fixture：`C:\Users\ADMIN\AppData\Local\Temp\aagu-024-companion-f6832b9-960b17f5a60046e1a4bd27c4c23ea52b`；
- fixture HEAD：`bcbe688fde20e55af68cadda64fed93f13bcd196`；
- fixture status：clean；
- WorkItems：24；
- graph SHA-256：`B3E59FD43EB7F543A0F11FEA9EA5267759C1AD44AB74A07F8EFDC735BAEB5A3B`；
- registry 位于独立 temp runtime，未写入 fixture 或 live AAGU。

复制前对 live `.workblock/graph.json` 与全部 24 个 `WORKITEM.md` 保存了 25 个 SHA-256。失败后重新计算，`liveChanged=[]`；fixture 也仍是 clean。

## 实际调用与结果

使用 exact candidate 的 `src/project-registry.js` 注册 fixture，再由 `src/project-workspace.js` 调用 `getCompanionView()`。结果在任何 UI 截图之前 fail closed：

```text
Error: Unsupported Item Type at ...\.workblock\items\AAGU-001\WORKITEM.md: Block.
    at parseWorkItemRecord (...\src\project-source-adapter.js:280:24)
```

根因是 `project-source-adapter.js` 对任何声明了 Item Version 的 Record 只接受正则 ``^`(Todo|Block)`$``；真实 AAGU 当前格式包含：

- 本次 14 个已迁移的 2.1 members：`Item Type: Block`；
- 严禁修改的 AAGU-006、009、019：显式 `Item Version: 2.0` + `Item Type: Block`；
- 当前 installed 2.1 `block-workflow` 与 Human Surface validator 并未把反引号 Item Type 声明为协议门禁。

因此不能通过修改 live 受保护 WorkItems，或只在 fixture 中添加反引号，来声称真实 AAGU 已被 exact candidate 加载。这个 probe 结论是 `FAIL`，已回传 COMP-042 在同一 Block 内返工。

## 当前决定

不使用 `f6832b9...` 形成 AAGU-024 视觉 PASS，不生成替代截图，不 fallback 到旧 Companion。AAGU-024 Claim 保持 `ongoing`，等待 COMP-042 修正并提供新 exact candidate。

## 后续修复

COMP-042 在同一 Block 内返工并形成新 exact candidate `08be674abc60c9249982a1c3f341a080cd8b5121`。新 candidate 精确接受 declared 2.0/2.1 的 `Todo`、`` `Todo` ``、`Block`、`` `Block` `` 四种现有标量形式，同时继续拒绝大小写漂移、双引号和复合类型。AAGU-024 随后从 fresh registry 重新加载同一 clean snapshot 并通过；最终正向证据见 `companion-aagu-acceptance.md`。
