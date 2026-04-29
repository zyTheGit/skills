---
name: git-commit-spec
description: Git Commit 格式规范。当用户需要生成 commit 消息、编写提交说明、或询问 commit 格式时使用此技能。遵循 Apache Doris 社区规范，确保提交消息清晰、规范、易于追踪。
---

# Git Commit 格式规范

本技能用于生成符合 Apache Doris 社区标准的 Git Commit 消息。

## 提交消息格式

### 标题格式

```
[<type>](<scope>) <subject> (#pr)
```

**组成部分说明**：

1. **`<type>`**（必需）：提交类型，全小写
2. **`<scope>`**（可选）：影响范围/模块
3. **`<subject>`**（必需）：简短描述
4. **`(#pr)`**（可选）：PR 编号

### 内容格式

```
issue：#<issue_number> <详细说明>
```

- 如无 issue，可不填
- 一行原则不超过 100 个字符
- 内容首字母大写

---

## 提交类型（type）

### 允许的类型列表

| 类型 | 说明 | 示例 |
|------|------|------|
| `fix` | Bug 修复 | 修复登录页面崩溃问题 |
| `feature` | 新增功能 | 添加用户权限管理模块 |
| `feature-wip` | 开发中的功能（部分代码提交） | 用户中心功能开发中（第一阶段） |
| `improvement` | 原有功能的优化和改进 | 优化查询性能 |
| `style` | 代码风格调整 | 统一代码缩进格式 |
| `typo` | 代码或文档勘误 | 修正 README 中的拼写错误 |
| `refactor` | 代码重构（不涉及功能变动） | 重构数据库连接逻辑 |
| `performance` | 性能优化 | 优化内存使用 |
| `optimize` | 性能优化 | 减少查询响应时间 |
| `test` | 单元测试的添加或修复 | 添加用户服务测试用例 |
| `chore` | 构建工具的修改 | 更新 webpack 配置 |
| `revert` | 回滚提交 | 回滚 commit abc123 |
| `deps` | 第三方依赖库的修改 | 升级 lodash 到 4.17.21 |
| `community` | 社区相关的修改 | 更新 Issue 模板 |

### 多类型组合

- **可同时使用多个类型标签**：如代码重构带来了性能提升
- **示例**：`[refactor][optimize]` 或 `[fix][test]`

### 重要规则

❌ **禁止**：使用列表之外的其他类型  
✅ **允许**：如需新增类型，需先更新本文档

---

## 影响范围（scope）

### 推荐的 scope 列表

根据项目特点，选择最合适的范围：

#### 后端模块
- `planner` - 查询规划器
- `meta` - 元数据管理
- `storage` - 存储引擎
- `executor` - 执行器
- `cache` - 缓存模块
- `config` - 配置管理
- `log` - 日志系统
- `profile` - 性能分析

#### 数据加载
- `stream-load` - 流式加载
- `broker-load` - Broker 加载
- `routine-load` - 例行加载
- `sync-job` - 同步任务
- `export` - 数据导出

#### 连接器
- `spark-connector` - Spark 连接器
- `flink-connector` - Flink 连接器
- `datax` - DataX 集成

#### 其他
- `docs` - 文档
- `vectorization` - 向量化
- `test` - 测试

### 规则说明

✅ **优先使用列表中已存在的选项**  
✅ **可添加新的 scope**，但需及时更新本文档  
✅ **多个 scope 可用括号分别列出**：`(storage)(cache)`

---

## 提交描述（subject）

### 编写原则

1. **简洁明了**：一句话说明本次提交的核心内容
2. **动词开头**：使用中文动词（添加、修复、优化、重构等）
3. **小写为主**：标题原则上全部小写
4. **避免过长**：建议不超过 50 个字符

### 示例对比

❌ **不好的示例**：
```
[fix] Fixed the bug
[feature] Added new feature
[improvement] Improve performance
```

✅ **好的示例**：
```
[fix](login) 修复用户登录页面崩溃问题
[feature](auth) 添加基于 JWT 的用户认证功能
[improvement](query) 优化大数据查询性能
```

---

## 完整示例

### 示例 1：简单修复

```
[fix](executor) 修复 DateTimeValue 内存布局问题 (#7022)

Change DateTimeValue memory's layout to old to fix compatibility problems.
```

### 示例 2：新功能

```
[feature](log) 扩展日志接口，支持结构化日志输出 (#6600)

Support structured logging.
```

### 示例 3：多类型多范围

```
[fix][improvement](executor)(load)(config) 修复多个内存问题 (#6699)

1. Fix a memory leak in `collect_iterator.cpp` (Fix #6700)
2. Add a new BE config `max_segment_num_per_rowset` to limit the num of segment in new rowset. (Fix #6701)
3. Make the error msg of stream load more friendly.
```

### 示例 4：性能优化（带详细说明）

```
[optimize](load) 减少大批量数据加载时的段文件数量 (#6947)

## 问题背景
在加载过程中，每个 tablet 会有一个 memtable 保存传入数据。
当 memtable 数据超过 100MB 时，会刷新到磁盘生成 segment 文件。
假设表有 N 个 buckets(tablets)，最大内存占用为 N * 100MB。

## 解决方案
不刷新所有 memtable，而是只刷新部分。
引入抖动机制确保各 memtable 大小不均匀，
从而保证只在 memtable 足够大时才触发刷新。

## 测试结果
加载 48 buckets 表，内存限制 2G：
- 修改前：平均 memtable 大小 44MB
- 修改后：平均 memtable 大小 82MB
```

### 示例 5：文档更新

```
[docs](readme) 更新安装说明和快速开始指南

- 添加 Docker 安装方式
- 更新依赖版本要求
- 补充常见问题解答
```

---

## 工作流程

### 当用户请求生成 commit 消息时：

1. **分析变更内容**
   - 查看暂存的文件：`git diff --cached`
   - 查看未暂存的文件：`git diff`
   - 查看状态：`git status`

2. **确定提交类型**
   - 根据文件变更内容选择合适的 type
   - 如有多个类型变化，组合多个 type

3. **确定影响范围**
   - 从推荐的 scope 列表中选择
   - 或根据实际模块添加新的 scope

4. **编写标题**
   - 遵循格式：`[<type>](<scope>) <subject> (#pr)`
   - 确保简洁明了，全小写

5. **编写内容**（可选）
   - 如有 issue，格式：`issue：#<issue_number> <说明>`
   - 如无 issue，直接写说明
   - 一行不超过 100 字符

6. **审查和确认**
   - 向用户展示生成的 commit 消息
   - 根据反馈进行调整

---

## 常见场景处理

### 场景 1：修复 Bug

**输入**：修复了用户登录时的崩溃问题

**输出**：
```
[fix](auth) 修复用户登录时的崩溃问题
```

### 场景 2：新功能开发中（未完成）

**输入**：提交用户中心功能的第一阶段代码

**输出**：
```
[feature-wip](user-center) 用户中心功能开发（第一阶段）
```

### 场景 3：代码重构 + 性能优化

**输入**：重构了数据库连接逻辑，并提升了性能

**输出**：
```
[refactor][optimize](database) 重构数据库连接逻辑并优化性能
```

### 场景 4：依赖更新

**输入**：更新 lodash 到最新版本

**输出**：
```
[deps] 升级 lodash 到 4.17.21
```

### 场景 5：测试用例

**输入**：为用户服务添加单元测试

**输出**：
```
[test](user-service) 添加用户服务单元测试用例
```

### 场景 6：文档修正

**输入**：修正 README 中的拼写错误

**输出**：
```
[typo](docs) 修正 README 中的拼写错误
```

---

## 特殊规则

### 多个 PR 或 Issue

- 多个 PR：`(#[number1])` 和 `(#[number2])` 分别列出
- 多个 Issue：在内容中分别列出 `Fix #6700` 和 `Fix #6701`

### Breaking Changes

如有破坏性变更，在内容中添加：

```
BREAKING CHANGE: 说明破坏性变更的影响和迁移方法
```

### WIP 提交

开发中的功能使用 `feature-wip` 类型，避免误发布：

```
[feature-wip](module) 功能开发中（说明当前进度）
```

---

## 最佳实践

### ✅ 推荐做法

1. **频繁提交**：小步快跑，每个提交专注一个变更
2. **清晰描述**：让他人（包括未来的自己）能快速理解
3. **关联 Issue**：如有相关 Issue，务必关联
4. **测试先行**：修复 Bug 时先写测试用例
5. **审查变更**：提交前检查 `git diff --cached`

### ❌ 避免做法

1. **模糊消息**：`fix bug`、`update code`、`changes`
2. **混合类型**：一个提交包含不相关的多个变更
3. **超长标题**：超过 100 字符的标题
4. **遗漏类型**：不使用类型标签直接写描述
5. **错误类型**：新功能使用 `fix` 类型

---

## 快速参考卡片

```
格式：[<type>](<scope>) <subject> (#pr)

类型：fix | feature | feature-wip | improvement | style | typo | 
     refactor | performance | optimize | test | chore | revert | 
     deps | community

范围：planner | meta | storage | executor | cache | config | log |
     stream-load | broker-load | routine-load | docs | test | ...

示例：
[fix](auth) 修复登录验证逻辑 (#123)
[feature](api) 添加用户权限管理接口
[optimize](query) 优化大数据查询性能
[test](user-service) 添加用户服务测试用例
```

---

## 总结

本技能帮助生成规范化的 Git Commit 消息：

1. **遵循格式**：`[type](scope) subject (#pr)`
2. **选择类型**：从预定义列表中选择，可组合
3. **明确范围**：使用推荐的 scope 或添加新的
4. **简洁描述**：一句话说清楚做了什么
5. **关联上下文**：通过 PR 和 Issue 关联代码变更

**记住**：好的 commit 消息是项目可维护性的基础！