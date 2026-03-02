# Implementation Plan - Home UI Navigation Icon Bug Fix

## Phase 1: 故障复现与成因分析
- [ ] Task: 编写自动化测试复现“点击关于我们导致产品图标变更”的 Bug
- [ ] Task: 检查 `dzweb/templates/home/` 和侧边栏逻辑，识别 CSS 类名或 JS 判断冲突点
- [ ] Task: Conductor - User Manual Verification 'Phase 1: 故障复现与成因分析' (Protocol in workflow.md)

## Phase 2: UI 逻辑修复
- [ ] Task: 修复侧边栏图标的“激活”判断逻辑（基于路由精准匹配）
- [ ] Task: 隔离“产品类别”与“关于我们”栏目的 UI 渲染状态，防止样式污染
- [ ] Task: 运行测试并确保复现的测试用例现在通过（Green Phase）
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI 逻辑修复' (Protocol in workflow.md)

## Phase 3: 回归测试与优化
- [ ] Task: 验证所有产品分类跳转时的图标表现依然正确
- [ ] Task: 优化侧边栏图标加载性能（如适用）
- [ ] Task: 运行完整测试套件，确保无 UI 回归
- [ ] Task: Conductor - User Manual Verification 'Phase 3: 回归测试与优化' (Protocol in workflow.md)
