---
name: pms-element-ui
description: "PMS 内部组件库知识库。当用户提到 pms-base-element、BaseProTable、BaseProForm、BaseProSearch、BaseToolBar、BaseDictionary、BaseChunkUpload、BaseOrgantCascader 等业务组件时使用此技能。也适用于用户询问表格配置、表单配置、字典选择、文件上传、组织机构选择、工具栏配置、Min-Web3 SDK（window.$utils、window.$request、window.$permission、window.$eventBus）、权限控制、标签页管理等场景。"
---

# PMS 组件库知识库

基于 pms-base-element 组件库的完整知识库，包含 86+ 组件的详细文档和代码示例。

---

## 📚 知识库导航

### 快速入口

| 文档 | 说明 |
|-----|------|
| **[01-快速开始.md](./01-快速开始.md)** | 安装配置、Min-Web3 全局 SDK |
| **[02-基础业务组件.md](./02-基础业务组件.md)** | 17个核心业务组件（重点）⭐ |
| **[03-表单组件.md](./03-表单组件.md)** | 17个表单相关组件 |
| **[04-数据展示组件.md](./04-数据展示组件.md)** | 19个数据展示组件 |
| **[05-布局导航组件.md](./05-布局导航组件.md)** | 12个布局导航组件 |
| **[06-反馈组件.md](./06-反馈组件.md)** | 9个反馈组件 |
| **[07-其他组件.md](./07-其他组件.md)** | 4个其他组件 |
| **[08-主题和工具.md](./08-主题和工具.md)** | 主题定制、国际化、权限、工具函数 |

---

## 🎯 常用场景速查

### 列表页面

```vue
<el-base-pro-table
  :columns="columns"
  :request="fetchData"
  show-index
  show-single-selection
/>
```

**参考文档**：[02-基础业务组件.md](./02-基础业务组件.md) - BaseProTable

### 表单页面

```vue
<el-base-pro-form
  :visible.sync="visible"
  :mode="mode"
  :columns="columns"
  @submit="handleSubmit"
/>
```

**参考文档**：[02-基础业务组件.md](./02-基础业务组件.md) - BaseProForm

### 搜索栏

```vue
<el-base-pro-search
  :columns="columns"
  :model.sync="searchForm"
  @search="handleSearch"
/>
```

**参考文档**：[02-基础业务组件.md](./02-基础业务组件.md) - BaseProSearch

### 字典选择

```vue
<el-base-dictionary
  v-model="value"
  app-code="biz-contract"
  dist-type-code="contract_type"
/>
```

**参考文档**：[02-基础业务组件.md](./02-基础业务组件.md) - BaseDictionary

### 文件上传

```vue
<el-base-chunk-upload
  action="/api/upload"
  :file-list.sync="fileList"
  auto-upload
/>
```

**参考文档**：[02-基础业务组件.md](./02-基础业务组件.md) - BaseChunkUpload

---

## 🔧 全局 SDK (Min-Web3)

### window.$utils - 工具函数

```javascript
// 标签页管理
window.$utils.openTab({
  appName: 'app-user',
  name: 'user-detail-123',
  path: '/app-user/detail/123',
  title: '用户详情'
});

// 日期格式化
window.$utils.formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss');

// 本地存储
window.$utils.storage.set('token', 'xxx', 3600000);
const token = window.$utils.storage.get('token');

// 防抖节流
const debouncedFn = window.$utils.debounce(fn, 500);
const throttledFn = window.$utils.throttle(fn, 500);
```

**参考文档**：[01-快速开始.md](./01-快速开始.md) - Min-Web3 全局 SDK

### window.$request - 统一请求

```javascript
const users = await window.$request.get({ url: '/users', params: { page: 1 } });
const result = await window.$request.post({ url: '/users', data: { name: 'test' } });
```

**参考文档**：[01-快速开始.md](./01-快速开始.md) - window.$request

### window.$permission - 权限控制

```javascript
// 检查权限
if (window.$permission.check('user:add')) {
  // 显示添加按钮
}

// 检查任一权限
if (window.$permission.checkAny(['user:add', 'user:edit'])) {
  // 显示操作按钮
}
```

**参考文档**：[01-快速开始.md](./01-快速开始.md) - window.$permission

### window.$eventBus - 事件总线

```javascript
// 订阅
window.$eventBus.on('route:restore', (payload) => {
  console.log('路由恢复', payload);
});

// 发布
window.$eventBus.emit('message:fromApp', {
  appName: 'app-user',
  type: 'USER_UPDATED'
});
```

**参考文档**：[01-快速开始.md](./01-快速开始.md) - window.$eventBus

---

## 📖 详细文档

完整文档请查看各分类文件：

- **[README.md](./README.md)** - 知识库总览
- **[01-快速开始.md](./01-快速开始.md)** - 安装、Min-Web3 SDK
- **[02-基础业务组件.md](./02-基础业务组件.md)** - 核心业务组件详解
- **[03-表单组件.md](./03-表单组件.md)** - 表单组件详解
- **[04-数据展示组件.md](./04-数据展示组件.md)** - 数据展示组件详解
- **[05-布局导航组件.md](./05-布局导航组件.md)** - 布局导航组件详解
- **[06-反馈组件.md](./06-反馈组件.md)** - 反馈组件详解
- **[07-其他组件.md](./07-其他组件.md)** - 其他组件详解
- **[08-主题和工具.md](./08-主题和工具.md)** - 主题定制和工具函数

---

**最后更新时间**：2026-04-23