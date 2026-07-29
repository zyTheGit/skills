# PMS 组件库知识库

> 基于 pms-base-element 组件库的完整知识库，按照组件类型分类整理

---

## 📚 知识库导航

### 一、快速开始

- **[01-快速开始.md](./01-快速开始.md)** - 安装指南、快速上手、全局SDK使用
  - 组件库安装与配置
  - 快速上手指南
  - Min-Web3 全局 SDK（工具、请求、事件总线、权限等）

### 二、核心业务组件

- **[02-基础业务组件.md](./02-基础业务组件.md)** - **20个** base-* 开头的核心业务组件
  - **高级表格** (BaseProTable) - 企业级表格解决方案
  - **高级表单** (BaseProForm) - 支持查看/新增/编辑模式
  - **高级搜索** (BaseProSearch) - 复杂搜索条件组合
  - **工具栏** (BaseToolBar) - 独立表格工具栏
  - **底部操作栏** (BasePageFooter) - 表单/详情页底部操作区
  - **视图切换** (BaseViewSwitcher) - card/table 视图切换
  - **流程组件** (BaseProProcess, BaseProcessHandle) - 流程审批
  - **选择器** (BaseOrgantCascader, BaseAffiliatedUnit, BaseDictionary) - 业务选择
  - **上传组件** (BaseChunkUpload, BaseUploadList) - 文件上传管理
  - **预览器** (BaseImgPreviewer, BaseFilePreviewer) - 文件预览
  - **布局图标** (BaseLayout, BaseIcon) - 基础布局和图标
  - **微前端保活** (MicroKeepAliveView) - 子应用页面缓存

### 三、基础组件库

- **[03-表单组件.md](./03-表单组件.md)** - **17个**表单相关组件（已完整收录）
  - Form、Input、Select、DatePicker、Upload、Cascader
  - InputNumber、Radio、Checkbox、Switch、TimePicker
  - DateTimePicker、Rate、Slider、ColorPicker、Transfer

- **[04-数据展示组件.md](./04-数据展示组件.md)** - **19个**数据展示组件（已完整收录）
  - Table、Pagination、Tag、Card、Badge、Progress、Empty、Calendar
  - Descriptions、Image、Carousel、Collapse、Timeline
  - Statistic、Result、Skeleton、Tree

- **[05-布局导航组件.md](./05-布局导航组件.md)** - **10个**布局导航组件
  - Layout、Menu、Tabs、Breadcrumb、Steps
  - Dropdown、PageHeader、Backtop、Container

- **[06-反馈组件.md](./06-反馈组件.md)** - **11个**反馈组件
  - Dialog、Message、MessageBox、Notification、Drawer
  - Loading、Alert、Popconfirm、Popover、Tooltip

- **[07-其他组件.md](./07-其他组件.md)** - **7个**其他组件
  - Button、Link、Icon、InfiniteScroll
  - Avatar、Divider

### 四、主题和工具

- **[08-主题和工具.md](./08-主题和工具.md)** - 主题定制和工具函数
  - 色彩规范、边框样式、过渡动画
  - 主题切换与定制、国际化
  - 权限控制、工具函数库
  - Typography 排版规范
  - ThemeProvider 运行时主题切换
  - 远程组件接入（qiankun 微前端）

---

## 🎯 使用建议

### 按场景查找组件

| 使用场景 | 推荐组件 |
|---------|---------|
| **列表页面** | BaseProTable + BaseProSearch |
| **表单页面** | BaseProForm + 表单组件 |
| **详情页面** | BaseProForm(view模式) + Descriptions |
| **流程审批** | BaseProProcess + BaseProcessHandle |
| **文件上传** | BaseChunkUpload + BaseUploadList |
| **组织选择** | BaseOrgantCascader |
| **字典选择** | BaseDictionary |
| **图片预览** | BaseImgPreviewer |
| **文件预览** | BaseFilePreviewer |
| **页面底部操作** | BasePageFooter |
| **视图切换** | BaseViewSwitcher |

### 按功能类型查找

| 功能类型 | 相关文档 |
|---------|---------|
| **数据录入** | 03-表单组件.md |
| **数据展示** | 04-数据展示组件.md |
| **页面布局** | 05-布局导航组件.md |
| **用户反馈** | 06-反馈组件.md |
| **业务功能** | 02-基础业务组件.md |
| **工具函数** | 01-快速开始.md (全局SDK) |

---

## 📊 组件统计

- **总组件数**：89个
- **业务组件**：20个 (22.5%)
- **表单组件**：17个 (19.1%)
- **数据展示**：19个 (21.3%)
- **布局导航**：12个 (13.5%)
- **反馈组件**：9个 (10.1%)
- **其他组件**：12个 (13.5%)

---

## 🔗 相关链接

- 组件库文档：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN`
- 全局SDK文档：见 `01-快速开始.md` 中的 Min-Web3 SDK 部分
- 权限控制：见 `08-主题和工具.md` 中的权限部分

---

## 💡 快速参考

### 最常用的业务组件

1. **BaseProTable** - 企业级表格，自动处理分页、搜索、排序
2. **BaseProForm** - 高级表单，支持查看/新增/编辑模式
3. **BaseProSearch** - 高级搜索，支持复杂条件组合
4. **BaseToolBar** - 独立工具栏，支持刷新、密度、列设置、全屏
5. **BaseDictionary** - 字典选择，自动加载数据字典
6. **BaseChunkUpload** - 文件上传，支持大文件分片

### 最常用的基础组件

1. **Dialog** - 对话框，最常用的模态交互
2. **Message** - 消息提示，操作反馈
3. **Form** - 表单，数据收集和验证
4. **Table** - 表格，数据展示
5. **Button** - 按钮，交互触发

---

**最后更新时间**：2026-07-29

---

## 📝 更新日志

### 2026-07-29
- 新增：远程组件接入说明（qiankun 微前端架构）
- 更新：08-主题和工具.md 新增第九章"远程组件接入"
- 更新：README.md 导航目录补充远程组件内容

### 2026-06-11
- 新增：MicroKeepAliveView 微前端页签保活组件文档
- 更新：Input 新增 trim 属性（自动清除输入值空格）
- 更新：组件总数 88→89，业务组件 19→20

### 2026-06-09
- 增量更新：新增 26 个 Element 组件文档
- 新增（表单）：InputNumber、Radio、Checkbox、Switch、TimePicker、DateTimePicker、Rate、Slider、ColorPicker、Transfer
- 新增（数据展示）：Descriptions、Image、Carousel、Collapse、Timeline、Statistic、Result、Skeleton、Tree
- 新增（布局）：Container
- 新增（反馈）：Tooltip
- 新增（其他）：Avatar、Divider
- 新增（主题工具）：Typography 排版规范、ThemeProvider 运行时主题切换
- 更新：03-表单组件 7→17 节，04-数据展示 9→18 节，05-布局导航 9→10 节，06-反馈 10→11 节，07-其他 5→7 节，08-主题工具 6→8 节

### 2026-05-13
- 新增：BasePageFooter 页面底部操作栏组件文档
- 新增：BaseViewSwitcher 视图切换组件文档
- 更新：BaseProTable 新增 single-selectable 单项禁用控制
- 更新：BaseProProcess 新增 status-images、auto-load-logs、抽屉事件/方法、Slots
- 更新：BaseProcessHandle 新增 footer-bleed、left-width 等属性及待办说明
- 修正：02-基础业务组件.md 章节编号
- 更新：组件总数 86→88

### 2026-04-23
- 新增：BaseToolBar 工具栏组件文档
- 更新：Tabs 标签页新增 lineless（隐藏下划线）和 size（尺寸）属性

### 2026-04-09
- 初始化知识库
- 完成所有组件文档整理
