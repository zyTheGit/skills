# Git Commit 快速参考

本文档提供 Git Commit 格式的快速参考和实用示例。

---

## 一、格式速查

### 基本格式

```
[<type>](<scope>) <subject> (#pr)
```

### 完整格式（带内容）

```
[<type>](<scope>) <subject> (#pr)

issue：#<issue_number> <详细说明>
```

---

## 二、类型速查表

| 类型 | 使用场景 | 示例 |
|------|---------|------|
| `fix` | 修复 Bug | `[fix](auth) 修复登录验证失败问题` |
| `feature` | 新功能 | `[feature](api) 添加用户权限管理接口` |
| `feature-wip` | 开发中功能 | `[feature-wip](ui) 用户中心 UI 开发中` |
| `improvement` | 功能改进 | `[improvement](search) 优化搜索算法` |
| `style` | 代码风格 | `[style] 统一代码缩进为 2 空格` |
| `typo` | 拼写错误 | `[typo](docs) 修正 README 拼写错误` |
| `refactor` | 代码重构 | `[refactor](db) 重构数据库连接模块` |
| `performance` | 性能优化 | `[performance](query) 优化查询性能` |
| `optimize` | 性能优化 | `[optimize](cache) 优化缓存策略` |
| `test` | 测试相关 | `[test](user) 添加用户服务测试用例` |
| `chore` | 构建/工具 | `[chore] 更新 webpack 配置` |
| `revert` | 回滚提交 | `[revert] 回滚 commit abc123` |
| `deps` | 依赖更新 | `[deps] 升级 lodash 到 4.17.21` |
| `community` | 社区相关 | `[community] 更新 Issue 模板` |

---

## 三、范围（Scope）速查

### 后端常用

- `planner` - 查询规划
- `meta` - 元数据
- `storage` - 存储
- `executor` - 执行器
- `cache` - 缓存
- `config` - 配置
- `log` - 日志
- `profile` - 性能分析

### 数据处理

- `stream-load` - 流式加载
- `broker-load` - Broker 加载
- `routine-load` - 例行加载
- `export` - 导出

### 连接器

- `spark-connector` - Spark
- `flink-connector` - Flink
- `datax` - DataX

### 其他

- `docs` - 文档
- `test` - 测试
- `vectorization` - 向量化

---

## 四、常见场景模板

### 场景 1：Bug 修复

**情况**：修复了用户登录时的验证失败问题

```bash
# 查看变更
git diff --cached

# 生成的 commit
[fix](auth) 修复用户登录验证失败问题

# 详细版本
[fix](auth) 修复用户登录验证失败问题 (#123)

issue：#120 修复 JWT 令牌过期验证逻辑错误
```

### 场景 2：新功能

**情况**：添加了用户权限管理模块

```bash
[feature](permission) 添加用户权限管理模块 (#456)

issue：#450 实现基于角色的权限控制系统
- 添加角色管理接口
- 实现权限验证中间件
- 集成用户角色关联表
```

### 场景 3：功能优化

**情况**：优化了查询性能

```bash
[improvement](query) 优化查询性能 (#789)

issue：#780 通过添加索引提升查询速度
- 优化 WHERE 子句索引使用
- 减少不必要的全表扫描
- 添加查询计划缓存
```

### 场景 4：代码重构

**情况**：重构了数据库连接模块

```bash
[refactor](database) 重构数据库连接模块

- 将连接池逻辑抽取为独立模块
- 优化连接释放机制
- 添加连接健康检查
```

### 场景 5：依赖更新

**情况**：更新了项目依赖

```bash
[deps] 升级核心依赖库版本

- lodash: 4.17.15 -> 4.17.21
- axios: 0.21.0 -> 0.27.2
- 修复安全漏洞 CVE-2021-23337
```

### 场景 6：测试用例

**情况**：添加了用户服务的单元测试

```bash
[test](user-service) 添加用户服务测试用例 (#999)

issue：#995 提升代码覆盖率
- 添加登录接口测试
- 添加注册接口测试
- 添加权限验证测试
```

### 场景 7：文档更新

**情况**：更新了 API 文档

```bash
[docs](api) 更新用户管理 API 文档

- 添加新接口说明
- 更新请求示例
- 补充错误码说明
```

### 场景 8：多类型组合

**情况**：重构代码并提升性能

```bash
[refactor][optimize](cache) 重构缓存模块并优化性能

issue：#100, #101
- 重构缓存键生成逻辑
- 优化缓存淘汰策略
- 减少内存占用 30%
```

### 场景 9：开发中功能

**情况**：提交用户中心功能的第一阶段代码

```bash
[feature-wip](user-center) 用户中心功能开发（第一阶段）

进度：
- 已完成用户信息展示界面
- 已完成基础设置页面
- 待完成：权限管理模块
```

### 场景 10：破坏性变更

**情况**：API 接口发生不兼容变更

```bash
[feature](api) 重构用户 API 接口 (#1111)

BREAKING CHANGE: 用户 API 接口变更

影响的接口：
- GET /user/info -> GET /users/:id
- POST /user/update -> PATCH /users/:id

迁移指南：
1. 更新 API 路径
2. 调整请求参数格式
3. 参考文档：docs/migration-guide.md
```

---

## 五、工作流程

### 推荐的 Git 提交流程

```bash
# 1. 查看变更文件
git status

# 2. 查看具体变更
git diff

# 3. 暂存文件
git add <files>

# 4. 查看暂存内容
git diff --cached

# 5. 生成 commit 消息（AI 辅助）
# 在此步骤，AI 会根据变更内容生成符合规范的 commit 消息

# 6. 提交
git commit -m "[type](scope) subject (#pr)"

# 7. 推送
git push origin <branch>
```

---

## 六、检查清单

提交前检查：

- [ ] 标题是否遵循格式 `[type](scope) subject`？
- [ ] type 是否在允许列表中？
- [ ] scope 是否合理？
- [ ] subject 是否清晰简洁？
- [ ] 是否关联了相关的 Issue 或 PR？
- [ ] 标题是否全小写？
- [ ] 内容是否一行不超过 100 字符？

---

## 七、常见错误

### ❌ 错误示例 1：缺少类型

```bash
# 错误
修复登录问题

# 正确
[fix](auth) 修复登录验证问题
```

### ❌ 错误示例 2：类型错误

```bash
# 错误：新功能使用了 fix 类型
[fix](api) 添加用户导出功能

# 正确
[feature](api) 添加用户导出功能
```

### ❌ 错误示例 3：描述模糊

```bash
# 错误
[fix](auth) fix bug

# 正确
[fix](auth) 修复 JWT 令牌过期验证失败问题
```

### ❌ 错误示例 4：标题过长

```bash
# 错误：标题超过 100 字符
[feature](api) 这是一个非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常长的标题

# 正确：简洁明了
[feature](api) 添加用户批量导入功能
```

### ❌ 错误示例 5：使用未定义的类型

```bash
# 错误：使用了未定义的类型
[update](auth) 更新登录逻辑

# 正确：使用已定义的类型
[improvement](auth) 优化登录逻辑
```

---

## 八、类型选择决策树

```
开始
  │
  ├─ 是否修复 Bug？
  │   └─ 是 → fix
  │
  ├─ 是否新增功能？
  │   ├─ 完整功能 → feature
  │   └─ 开发中功能 → feature-wip
  │
  ├─ 是否优化现有功能？
  │   └─ 是 → improvement
  │
  ├─ 是否重构代码？
  │   ├─ 有性能提升 → refactor + optimize
  │   └─ 无功能变化 → refactor
  │
  ├─ 是否优化性能？
  │   └─ 是 → performance 或 optimize
  │
  ├─ 是否测试相关？
  │   └─ 是 → test
  │
  ├─ 是否文档相关？
  │   └─ 是 → docs 或 typo
  │
  ├─ 是否依赖更新？
  │   └─ 是 → deps
  │
  ├─ 是否构建工具？
  │   └─ 是 → chore
  │
  └─ 是否回滚提交？
      └─ 是 → revert
```

---

## 九、高级技巧

### 技巧 1：多个类型组合

当一次提交涉及多个类型时，可以组合使用：

```bash
[fix][test](auth) 修复登录验证并添加测试用例

issue：#100
- 修复 JWT 令牌过期验证逻辑
- 添加登录验证单元测试
```

### 技巧 2：多个范围组合

当影响多个模块时，分别列出：

```bash
[improvement](auth)(user)(api) 统一用户认证流程

issue：#200
- 统一登录、注册、权限验证流程
- 优化 token 生成逻辑
- 更新 API 文档
```

### 技巧 3：WIP 提交

开发中的功能，避免被误发布：

```bash
[feature-wip](dashboard) 数据仪表板开发中

进度：
- 已完成：数据展示组件
- 进行中：图表配置
- 待完成：数据导出功能
```

### 技巧 4：关联多个 Issue

一次提交解决多个问题：

```bash
[fix](database) 修复数据库连接相关问题 (#123)

issue：#100, #101, #102
- Fix #100: 修复连接池泄漏问题
- Fix #101: 修复事务超时问题
- Fix #102: 优化重连机制
```

---

## 十、参考链接

- [Apache Doris Commit 格式规范](https://doris.apache.org/zh-CN/community/how-to-contribute/commit-format-specification)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git 最佳实践](https://git-scm.com/book/zh/v2)

---

**记住**：规范的 commit 消息是团队协作的基础，也是项目可维护性的保障！