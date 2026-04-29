---
name: pms-knowledge-updater
description: "更新 PMS 组件库知识库。当用户提到更新知识库、同步文档、更新组件文档、刷新知识库、pms-base-element 文档更新时使用此技能。也适用于用户说'更新一下知识库'、'同步最新文档'、'刷新组件库文档'等场景。"
---

# PMS 组件库知识库更新技能

用于更新 `pms-element-ui` 知识库，保持知识库与源文档同步。

---

## 📋 更新流程

### 1. 确定更新范围

询问用户要更新哪些内容：

- **全部更新**：重新扫描所有文档，更新所有知识库文件
- **部分更新**：只更新特定类型的组件或特定文件
- **增量更新**：只更新新增或修改的文档

### 2. 扫描源文档目录

源文档目录：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN`

扫描步骤：
1. 列出所有 `.md` 文件
2. 按文件名分类：
   - `base-*` 开头：基础业务组件
   - 表单组件：input, select, form 等
   - 数据展示：table, tag, badge 等
   - 布局导航：layout, menu, tabs 等
   - 反馈组件：dialog, message 等
   - 其他：button, icon 等
   - 文档：quickstart, installation 等

### 3. 更新知识库文件

知识库位置：`C:\Users\hpee2\.config\opencode\skills\pms-element-ui\`

文件映射：

| 源文档 | 知识库文件 |
|--------|-----------|
| base-*.md | 02-基础业务组件.md |
| input.md, select.md, form.md 等 | 03-表单组件.md |
| table.md, tag.md 等 | 04-数据展示组件.md |
| layout.md, menu.md 等 | 05-布局导航组件.md |
| dialog.md, message.md 等 | 06-反馈组件.md |
| button.md, icon.md 等 | 07-其他组件.md |
| quickstart.md, installation.md | 01-快速开始.md |
| functions.md, permission.md 等 | 08-主题和工具.md |

### 4. 更新内容格式

保持以下格式规范：

**组件条目格式**：

```markdown
### 组件名称

**功能说明**：一句话描述

**基础用法**：
\`\`\`vue
<el-component v-model="value" />
\`\`\`

**常用属性**：
| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| prop | 说明 | type | default |

**常用事件**：
| 事件名 | 说明 | 参数 |
|-------|------|------|
| event | 说明 | params |

**注意事项**：
- 注意点1
- 注意点2
```

---

## 🔄 更新策略

### 全量更新

适用于：
- 首次创建知识库
- 大规模文档更新
- 结构调整

步骤：
1. 扫描所有源文档
2. 按分类重新整理
3. 重写知识库文件
4. 更新 README.md 和 SKILL.md

### 增量更新

适用于：
- 少量文档更新
- 新增组件
- 修正错误

步骤：
1. 识别变更的文档
2. 定位对应的知识库文件
3. 更新相关章节
4. 保持其他内容不变

---

## 📝 更新检查清单

更新完成后，检查以下内容：

### 必需检查项

- [ ] 所有 `base-*` 组件都已包含在 `02-基础业务组件.md`
- [ ] 组件分类正确
- [ ] 代码示例格式正确
- [ ] 属性表格完整
- [ ] 中文说明清晰

### 可选检查项

- [ ] 更新了 README.md 中的统计数据
- [ ] 更新了 SKILL.md 中的触发关键词
- [ ] 添加了新的使用场景
- [ ] 更新了最后修改时间

---

## 🎯 快速命令

### 查看源文档列表

```bash
ls C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\*.md
```

### 查看知识库文件

```bash
ls C:\Users\hpee2\.config\opencode\skills\pms-element-ui\
```

### 对比文档数量

```bash
# 源文档数量
ls C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\*.md | Measure-Object

# 知识库文件数量
ls C:\Users\hpee2\.config\opencode\skills\pms-element-ui\*.md | Measure-Object
```

---

## 💡 更新示例

### 示例：新增 BaseNewComponent 组件

1. 读取源文档：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-new-component.md`

2. 更新 `02-基础业务组件.md`：

```markdown
### BaseNewComponent 新组件

**功能说明**：这是一个新的业务组件

**基础用法**：
\`\`\`vue
<el-base-new-component v-model="value" />
\`\`\`

**常用属性**：
| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value | 绑定值 | any | - |

**参考文档**：[源文档路径]
```

3. 更新 README.md：
   - 组件总数 +1
   - 业务组件数量 +1

4. 更新 SKILL.md：
   - 添加到触发关键词：`BaseNewComponent`

---

## 🔧 特殊处理

### Min-Web3 SDK 更新

如果 `functions.md` 或相关文档有更新，需要同步更新 `01-快速开始.md` 中的全局 SDK 部分：

- `window.$utils` 工具函数
- `window.$request` 请求方法
- `window.$permission` 权限控制
- `window.$eventBus` 事件总线

### BaseProTable/BaseProForm 更新

这两个是最复杂的组件，需要特别注意：

- 保留完整的配置说明
- 保留所有示例代码
- 更新属性/事件/方法表格
- 更新最佳实践建议

---

## 📊 更新日志

每次更新后，在 README.md 末尾记录：

```markdown
## 更新日志

### 2026-04-09
- 新增：BaseNewComponent 组件文档
- 更新：BaseProTable 新增 valueDict 配置说明
- 修正：BaseProForm 表单联动示例错误
```

---

## ⚠️ 注意事项

1. **保持格式一致**：使用统一的 Markdown 格式
2. **保留已有内容**：不要删除用户添加的自定义内容
3. **更新时间戳**：每次更新后修改"最后更新时间"
4. **验证链接**：确保文档内部链接有效
5. **检查触发词**：新增组件时要更新 SKILL.md 的触发关键词

---

## 🚀 开始更新

准备好后，告诉我：

1. 要更新哪些内容？（全部/部分/增量）
2. 是否有特定要更新的组件？
3. 是否需要重新分类？

我会根据你的需求更新知识库！