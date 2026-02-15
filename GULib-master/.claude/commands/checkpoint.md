# Git 存档检查点

在当前 step 完成后执行 git 存档。

## 流程

1. **检查验收条件**: 读取 `self/flow.md` 中当前 step 的验收条件清单
2. **运行测试**: 执行 `python -m pytest tests/ -v` 确认所有测试通过
3. **验收判定**:
   - 全部通过 → 继续存档
   - 有失败 → 列出失败项，停止存档，给出修复建议
4. **Git 操作**:
   - `git add` 相关文件（不用 `git add -A`，逐个添加）
   - `git commit -m "step-{N}: {描述}"`
   - 如果是里程碑 step，追加 `git tag`
5. **更新 flow.md**: 将验收条件中的 `[ ]` 改为 `[x]`
6. **输出报告**:
   ```
   ===== Checkpoint: Step {N} =====
   Tests:    {passed}/{total} passed
   Status:   PASS / FAIL
   Commit:   {hash} step-{N}: {描述}
   Tag:      {tag or "none"}
   Next:     Step {N+1}: {下一步简述}
   ================================
   ```

用户输入: $ARGUMENTS
