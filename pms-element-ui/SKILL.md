---
name: pms-element-ui
description: "PMS 内部组件库知识库。当用户提到 pms-base-element、BaseProTable、BaseProForm、BaseProSearch、BaseToolBar、BasePageFooter、BaseViewSwitcher、BaseDictionary、BaseChunkUpload、BaseOrgantCascader、BaseTree、BaseImport、BaseImgPreviewer、BaseFilePreviewer、BaseLayout、BaseIcon、BaseUploadList、BaseProProcess、BaseProcessHandle、BaseAffiliatedUnit、MicroKeepAliveView 等业务组件时使用此技能。也适用于用户询问表格配置、表单配置、字典选择、文件上传、组织机构选择、工具栏配置、底部操作栏、视图切换、Min-Web3 SDK、权限控制、标签页管理、微前端保活等场景。"
---

# PMS 组件库知识库

基于 pms-base-element 组件库的知识库，包含 88+ 组件文档。

## 📚 知识库导航

| 文档 | 说明 |
|-----|------|
| [01-快速开始.md](./01-快速开始.md) | 安装配置、Min-Web3 全局 SDK |
| [02-基础业务组件.md](./02-基础业务组件.md) | 20个核心业务组件 ⭐ |
| [03-表单组件.md](./03-表单组件.md) | 17个表单相关组件 |
| [04-数据展示组件.md](./04-数据展示组件.md) | 19个数据展示组件 |
| [05-布局导航组件.md](./05-布局导航组件.md) | 10个布局导航组件 |
| [06-反馈组件.md](./06-反馈组件.md) | 11个反馈组件 |
| [07-其他组件.md](./07-其他组件.md) | 7个其他组件 |
| [08-主题和工具.md](./08-主题和工具.md) | 主题定制、国际化、权限 |

## 🎯 常用场景速查

### 列表页面
```vue
<el-base-pro-table :columns="columns" :request="fetchData" />
```
参考：[02-基础业务组件.md](./02-基础业务组件.md) - BaseProTable

### 表单页面
```vue
<el-base-pro-form :visible.sync="visible" :columns="columns" @submit="handleSubmit" />
```
参考：[02-基础业务组件.md](./02-基础业务组件.md) - BaseProForm

### 搜索栏
```vue
<el-base-pro-search :columns="columns" :model.sync="searchForm" @search="handleSearch" />
```
参考：[02-基础业务组件.md](./02-基础业务组件.md) - BaseProSearch

### 字典选择
```vue
<el-base-dictionary v-model="value" app-code="biz-contract" dist-type-code="contract_type" />
```
参考：[02-基础业务组件.md](./02-基础业务组件.md) - BaseDictionary

### 文件上传
```vue
<el-base-chunk-upload action="/api/upload" :file-list.sync="fileList" auto-upload />
```
参考：[02-基础业务组件.md](./02-基础业务组件.md) - BaseChunkUpload

## 🔧 全局 SDK (Min-Web3)

### window.$utils
```javascript
window.$utils.openTab({ appName: 'app-user', name: 'detail-123', path: '/detail/123' });
window.$utils.formatDate(new Date(), 'YYYY-MM-DD');
window.$utils.storage.set('token', 'xxx', 3600000);
```

### window.$request
```javascript
const users = await window.$request.get({ url: '/users', params: { page: 1 } });
```

### window.$permission
```javascript
if (window.$permission.check('user:add')) { /* 显示按钮 */ }
```

### window.$eventBus
```javascript
window.$eventBus.on('route:restore', (payload) => { /* ... */ });
window.$eventBus.emit('message:fromApp', { type: 'USER_UPDATED' });
```

详细文档参见各分类文件。