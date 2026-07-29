---
name: pms-knowledge-updater
description: "更新 PMS 组件库知识库。当用户提到更新知识库、同步文档、更新组件文档、刷新知识库、pms-base-element 文档更新时使用此技能。也适用于用户说'更新一下知识库'、'同步最新文档'、'刷新组件库文档'等场景。"
---

# PMS 组件库知识库更新技能

用于更新 `pms-element-ui` 知识库，保持知识库与源文档同步。

## 首次使用配置

首次使用时，系统会询问以下路径：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 源文档目录 | `C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN` | pms-base-element 组件文档位置 |
| 知识库目录 | `../pms-element-ui/` | 知识库存储位置 |

配置会自动保存到本地，后续使用无需重复输入。

## 核心流程

1. **确定范围** — 全部/部分/增量更新
2. **扫描源文档** — 使用配置的源文档目录
3. **更新知识库** — 使用配置的知识库目录
4. **验证完整性** — 检查组件分类、属性表格、代码格式

## 文件映射

| 源文档 | 知识库文件 |
|--------|-----------|
| base-*.md | 02-基础业务组件.md |
| input/select/form.md | 03-表单组件.md |
| table/tag.md | 04-数据展示组件.md |
| layout/menu.md | 05-布局导航组件.md |
| dialog/message.md | 06-反馈组件.md |
| button/icon.md | 07-其他组件.md |
| quickstart/installation.md | 01-快速开始.md |
| functions/permission.md | 08-主题和工具.md |

## 更新策略

- **全量更新**：首次创建或大规模调整时重写所有文件
- **增量更新**：识别变更文档，只更新相关章节

## 格式规范

组件条目格式参见 `references/format.md`

## 文档限制规则

**重要**：更新知识库时必须遵守以下限制：

| 文件类型 | 最大行数 | 说明 |
|---------|---------|------|
| SKILL.md | 80 行 | 核心入口，渐进式披露 |
| README.md | 100 行 | 知识库总览 |
| 分类概览.md (如 02-基础业务组件.md) | 100 行 | 链接索引表 |
| 组件详细文档 | 200 行 | 放在 references/ 下 |

**拆分原则**：
- 超过 500 行的文档必须拆分
- 每个组件一个独立文件，放在 `references/` 目录
- 概览文件只保留链接索引表
- 保持 SKILL.md 精简（<80 行）

## 特殊处理

- **Min-Web3 SDK**：同步更新全局工具函数（$utils, $request, $permission, $eventBus）
- **BaseProTable/BaseProForm**：保留完整配置和示例

## 开始更新

询问用户：
1. 更新范围？（全部/部分/增量）
2. 是否有特定组件？
3. 是否需要重新分类？

详细流程和示例参见 `references/detailed-guide.md`

## 更新日志

每次更新后，在 `CHANGELOG.md` 中记录变更内容。
