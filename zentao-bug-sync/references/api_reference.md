# 禅道 12.x REST API 参考

## 认证

禅道 12.x 使用 Token 认证：

```
POST {base_url}/api.php/v1/tokens
Body: {"account": "admin", "password": "123456"}
Response: {"token": "xxx", "user": {...}}
```

后续请求在 Header 中携带：
```
token: xxx
```

## BUG 相关 API

### 获取 BUG 列表
```
GET /api.php/v1/bugs
Query: product_id, status, limit, page
```

### 获取 BUG 详情
```
GET /api.php/v1/bugs/{bugId}
```

### 创建 BUG
```
POST /api.php/v1/bugs
Body: {product, module, title, severity, pri, steps, expect, result, ...}
```

### 更新 BUG
```
PUT /api.php/v1/bugs/{bugId}
Body: {status, solution, assignedTo, ...}
```

## 状态值

| 值 | 含义 |
|----|------|
| active | 激活 |
| resolved | 已解决 |
| closed | 已关闭 |

## 解决方案

| 值 | 含义 |
|----|------|
| bydesign | 设计如此 |
| fixed | 已修复 |
| external | 外部原因 |
| wontfix | 不予解决 |
| postponed | 延期处理 |
| cannotreproduce | 无法重现 |

## 严重程度

| 值 | 含义 |
|----|------|
| 1 | 致命 |
| 2 | 严重 |
| 3 | 一般 |
| 4 | 建议 |

## 优先级

| 值 | 含义 |
|----|------|
| 1 | 紧急 |
| 2 | 高 |
| 3 | 中 |
| 4 | 低 |
