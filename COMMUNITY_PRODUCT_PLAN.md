# 快捷指令生成社区产品规划

## 1. 产品愿景

构建一个面向 iOS、iPadOS 和 macOS 用户的快捷指令社区，让用户可以用自然语言生成 Apple 快捷指令，并安全地浏览、安装、分享和改造其他人的自动化方案。

一句话定义：

```text
让任何人都能用一句话生成快捷指令，并在社区中安全地发现、复用和改造自动化工作流。
```

这个产品不只是一个 `.shortcut` 文件生成器，而是一个围绕快捷指令的内容社区、工具社区和自动化模板市场。

## 2. 核心目标

### 2.1 用户目标

- 不懂快捷指令的用户，可以描述需求并获得可用方案。
- 熟悉快捷指令的用户，可以快速生成初稿并继续调整。
- 创作者可以发布自己的快捷指令，积累影响力。
- 其他用户可以搜索、收藏、安装、评论和改编快捷指令。
- 所有人都能清楚知道一个快捷指令会访问哪些数据、调用哪些权限、是否存在风险。

### 2.2 产品目标

- 跑通“自然语言需求 -> 快捷指令生成 -> 保存 -> 发布 -> 被其他用户发现”的闭环。
- 建立可信的快捷指令内容库。
- 形成围绕快捷指令的创作者生态。
- 为后续付费生成、付费模板、创作者分成和定制服务预留空间。

## 3. 目标用户

### 3.1 普通 Apple 用户

这类用户有具体需求，但不熟悉快捷指令。

典型需求：

- 每天定时提醒喝水、打卡、记录心情。
- 快速整理照片、截图、备忘录。
- 一键发送常用消息。
- 自动创建日程、提醒事项。
- 把网页内容保存到笔记工具。

### 3.2 效率工具用户

这类用户熟悉工具组合，希望减少重复操作。

常见工具：

- Notion
- Obsidian
- Todoist
- Things
- 飞书
- Slack
- ChatGPT
- Google Calendar
- Apple Notes
- Reminders

典型需求：

- 把剪贴板内容格式化后发送到指定工具。
- OCR 截图并保存到笔记。
- 生成日报、周报、会议纪要。
- 串联多个 App 完成固定工作流。

### 3.3 快捷指令创作者

这类用户可以成为社区内容供给者。

他们需要：

- 发布页面。
- 版本管理。
- 下载量、收藏量、评分等反馈。
- 作者主页。
- 被推荐和精选的机会。
- 未来可能需要付费模板、打赏或定制需求入口。

## 4. 核心功能

### 4.1 AI 快捷指令生成器

用户输入自然语言需求，系统生成快捷指令方案。

第一版可以支持：

- 输入快捷指令名称。
- 输入需求描述。
- 选择目标平台：iPhone、iPad、Mac、Apple Watch。
- 选择是否允许联网。
- 选择是否允许访问剪贴板、照片、文件、位置等敏感权限。
- 生成快捷指令说明。
- 生成可下载 `.shortcut` 文件。
- 展示安装说明和风险提示。

建议生成流程：

```text
用户需求
-> 意图解析
-> 缺失信息追问
-> 生成快捷指令蓝图
-> 匹配已知 Shortcut actions
-> 生成 plist / .shortcut
-> 校验
-> 签名
-> 安全扫描
-> 返回下载与说明
```

### 4.2 快捷指令社区浏览

用户可以浏览社区中公开发布的快捷指令。

基础能力：

- 最新快捷指令。
- 热门快捷指令。
- 官方精选。
- 分类浏览。
- 标签筛选。
- 关键词搜索。
- 按平台筛选。
- 按权限风险筛选。

推荐分类：

- AI
- 效率
- 学习
- 生活
- 健康
- 图片
- 视频
- 社交媒体
- 开发者
- 文件处理
- 日程提醒
- 中文 App 工作流

### 4.3 快捷指令详情页

每个快捷指令应该有一个清晰可信的详情页。

建议字段：

- 标题。
- 简短描述。
- 详细说明。
- 作者信息。
- 版本号。
- 更新时间。
- 支持平台。
- 所需权限。
- 风险等级。
- 截图或封面。
- 安装按钮。
- 下载次数。
- 点赞数。
- 收藏数。
- 评论区。
- 更新日志。
- 举报入口。

详情页要重点回答三个问题：

```text
它能做什么？
它怎么安装和使用？
它会访问什么数据，是否安全？
```

### 4.4 发布与分享

用户可以把自己的快捷指令发布到社区。

发布方式：

- 上传 `.shortcut` 文件。
- 粘贴 iCloud Shortcuts 分享链接。
- 从 AI 生成结果直接发布。
- 填写手动创建说明。

发布表单字段：

- 标题。
- 描述。
- 分类。
- 标签。
- 平台。
- 版本号。
- 更新说明。
- 截图。
- 权限声明。
- 是否公开。

### 4.5 互动系统

第一版可以保留轻量互动：

- 点赞。
- 收藏。
- 评论。
- 下载量统计。
- 举报。
- 作者主页。

后续可以加入：

- 评分。
- 关注作者。
- 收藏夹。
- Fork / Remix。
- 需求悬赏。
- 创作者徽章。

## 5. MVP 范围

### 5.1 第一版必须包含

- 用户登录。
- AI 生成快捷指令。
- 生成历史保存。
- `.shortcut` 文件上传。
- `.shortcut` 文件下载。
- 快捷指令发布。
- 快捷指令列表页。
- 快捷指令详情页。
- 搜索。
- 分类。
- 点赞。
- 收藏。
- 基础评论。
- 管理员下架内容。
- 基础安全提示。

### 5.2 第一版暂不包含

- 付费系统。
- 创作者分成。
- 复杂推荐算法。
- 私信。
- 实时通知。
- 完整 Fork 图谱。
- 多语言站点。
- 原生移动 App。
- 高级自动化测试。

### 5.3 第一版成功标准

- 用户能从一句话生成一个快捷指令。
- 用户能下载或保存生成结果。
- 用户能发布一个快捷指令到社区。
- 其他用户能浏览、搜索、收藏和下载。
- 每个快捷指令都有基本权限说明。
- 管理员可以处理违规内容。

## 6. Cloudflare 技术架构

目标技术栈：

```text
Frontend: Cloudflare Pages
API: Cloudflare Workers
Database: Cloudflare D1
Object Storage: Cloudflare R2
Async Jobs: Cloudflare Queues
Bot Protection: Cloudflare Turnstile
AI: OpenAI / Gemini / Anthropic / Cloudflare Workers AI
```

### 6.1 Cloudflare Pages

用于部署前端应用。

适合：

- 社区首页。
- 生成器页面。
- 浏览页。
- 详情页。
- 用户中心。
- 管理后台前端。

前端框架可以继续沿用当前仓库中的 Vite + React + TypeScript。

### 6.2 Cloudflare Workers

用于提供 API 服务。

负责：

- 用户鉴权。
- 快捷指令 CRUD。
- 生成任务创建。
- 文件上传签名。
- 搜索接口。
- 点赞、收藏、评论。
- 管理员操作。
- 调用 AI 模型。
- 向队列投递异步任务。

### 6.3 Cloudflare D1

用于存结构化数据。

适合存：

- 用户。
- 快捷指令元数据。
- 版本。
- 评论。
- 点赞。
- 收藏。
- 举报。
- 生成任务。
- 审核记录。

### 6.4 Cloudflare R2

用于存非结构化文件。

适合存：

- `.shortcut` 文件。
- 快捷指令截图。
- 封面图。
- 用户头像。
- 安全扫描报告附件。
- 生成过程中的临时产物。

### 6.5 Cloudflare Queues

用于异步任务。

适合处理：

- AI 生成任务。
- 文件解析。
- 安全扫描。
- 内容审核。
- 截图处理。
- 下载统计汇总。
- 通知任务。

### 6.6 Cloudflare Turnstile

用于防止机器人滥用。

建议接入位置：

- 注册。
- 登录异常验证。
- 发布快捷指令。
- 评论。
- 生成请求。
- 举报。

### 6.7 AI 模型选择

建议分层使用 AI：

- 复杂快捷指令生成：优先使用能力更强的外部模型 API。
- 分类、标签、摘要、权限说明：可以使用成本更低的模型。
- 内容审核、风险解释：可以放到异步任务中处理。

第一版不要把 AI 生成结果直接当作可信最终结果，需要经过校验和安全扫描。

## 7. 与当前仓库的关系

当前仓库已经具备一个重要基础：用本地 FastAPI 后端、生成 plist，并通过 macOS `shortcuts sign` 生成可导入的 `.shortcut` 文件。

这意味着产品可以分成两个阶段：

### 7.1 阶段一：本地签名 MVP

沿用当前架构：

```text
Vite + React
FastAPI
Gemini / LLM
本地 macOS shortcuts sign
```

适合验证：

- 用户是否真的需要自然语言生成快捷指令。
- 生成质量是否可接受。
- 哪些类型的快捷指令最受欢迎。
- 用户是否愿意发布和分享。

### 7.2 阶段二：Cloudflare 社区平台

把社区能力放到 Cloudflare：

```text
Cloudflare Pages
Cloudflare Workers
Cloudflare D1
Cloudflare R2
Cloudflare Queues
```

同时保留一个“签名服务”：

```text
Cloudflare Worker
-> 创建生成任务
-> 队列
-> macOS 签名 Worker / 私有签名服务
-> 上传 signed .shortcut 到 R2
```

原因是 Apple Shortcuts 的签名步骤依赖 macOS `shortcuts` CLI。纯 Cloudflare 环境不直接提供这个 CLI，所以 `.shortcut` 签名需要单独处理。

可选方案：

- 继续用一台 Mac mini 作为签名服务。
- 使用自托管 macOS runner。
- 第一阶段只提供手动创建说明和未签名草稿，减少签名依赖。
- 对社区上传的 iCloud 分享链接，只保存链接和元数据，不重新签名。

## 8. 数据模型草案

### 8.1 users

```text
id
username
display_name
avatar_key
bio
email
auth_provider
role
created_at
updated_at
```

### 8.2 shortcuts

```text
id
author_id
title
slug
summary
description
category_id
status
visibility
current_version_id
platforms
risk_level
download_count
like_count
favorite_count
comment_count
created_at
updated_at
published_at
```

### 8.3 shortcut_versions

```text
id
shortcut_id
version
file_key
source_type
icloud_url
file_size
checksum
release_notes
scan_status
scan_result_json
created_at
```

### 8.4 shortcut_assets

```text
id
shortcut_id
asset_type
object_key
alt_text
sort_order
created_at
```

### 8.5 categories

```text
id
name
slug
description
sort_order
```

### 8.6 tags

```text
id
name
slug
```

### 8.7 shortcut_tags

```text
shortcut_id
tag_id
```

### 8.8 likes

```text
user_id
shortcut_id
created_at
```

### 8.9 favorites

```text
user_id
shortcut_id
created_at
```

### 8.10 comments

```text
id
shortcut_id
user_id
parent_id
body
status
created_at
updated_at
```

### 8.11 reports

```text
id
reporter_id
target_type
target_id
reason
details
status
created_at
resolved_at
```

### 8.12 generation_jobs

```text
id
user_id
prompt
name
target_platform
status
model
blueprint_json
result_shortcut_id
error_message
created_at
updated_at
```

### 8.13 audit_logs

```text
id
actor_id
action
target_type
target_id
metadata_json
created_at
```

## 9. API 草案

### 9.1 生成相关

```text
POST /api/generation-jobs
GET  /api/generation-jobs/:id
POST /api/generation-jobs/:id/publish
```

### 9.2 快捷指令相关

```text
GET    /api/shortcuts
POST   /api/shortcuts
GET    /api/shortcuts/:slug
PATCH  /api/shortcuts/:id
DELETE /api/shortcuts/:id
POST   /api/shortcuts/:id/like
DELETE /api/shortcuts/:id/like
POST   /api/shortcuts/:id/favorite
DELETE /api/shortcuts/:id/favorite
```

### 9.3 文件相关

```text
POST /api/uploads/presign
GET  /api/files/:key/download
```

### 9.4 评论相关

```text
GET  /api/shortcuts/:id/comments
POST /api/shortcuts/:id/comments
PATCH /api/comments/:id
DELETE /api/comments/:id
```

### 9.5 管理相关

```text
GET  /api/admin/reports
POST /api/admin/shortcuts/:id/feature
POST /api/admin/shortcuts/:id/unpublish
POST /api/admin/comments/:id/hide
```

## 10. 页面规划

### 10.1 首页

首页优先放生成器，而不是大段营销介绍。

核心内容：

- 一句话需求输入框。
- 推荐示例。
- 热门快捷指令。
- 精选分类。

### 10.2 生成器页

核心内容：

- 快捷指令名称。
- 需求描述。
- 目标平台。
- 权限偏好。
- 生成进度。
- 生成结果说明。
- 下载按钮。
- 保存为草稿。
- 发布到社区。

### 10.3 探索页

核心内容：

- 搜索框。
- 分类导航。
- 热门、最新、精选筛选。
- 快捷指令卡片列表。

### 10.4 详情页

核心内容：

- 标题。
- 作者。
- 描述。
- 安装按钮。
- 权限说明。
- 风险提示。
- 截图。
- 使用说明。
- 评论。
- 相关推荐。

### 10.5 发布页

核心内容：

- 上传 `.shortcut` 文件。
- 粘贴 iCloud 链接。
- 填写元数据。
- 自动解析权限。
- 保存草稿。
- 发布。

### 10.6 用户主页

核心内容：

- 用户资料。
- 发布的快捷指令。
- 收藏。
- 点赞记录。

### 10.7 管理后台

核心内容：

- 待审核内容。
- 举报列表。
- 用户管理。
- 精选管理。
- 下架操作。

## 11. 安全与信任

快捷指令社区必须把安全作为核心产品能力。

### 11.1 风险来源

常见风险：

- 读取剪贴板。
- 访问照片。
- 访问文件。
- 获取位置。
- 发送网络请求。
- 调用第三方 API。
- 上传用户数据。
- 在 macOS 上执行脚本。
- 使用未知 URL Scheme。

### 11.2 风险分级

建议分为：

```text
低风险：只处理本地文本、提醒、日历等低敏操作。
中风险：访问剪贴板、文件、照片、网络请求。
高风险：上传数据、执行脚本、获取位置、调用未知服务。
```

### 11.3 信任标识

可以为快捷指令显示：

- 已扫描。
- 官方精选。
- 作者已验证。
- 无高风险权限。
- 社区高评分。
- 最近更新。
- 来源可追溯。

## 12. 生成质量控制

AI 生成快捷指令需要严格约束。

建议策略：

- 使用已知 Action 白名单。
- 要求模型输出结构化 blueprint。
- 后端根据 blueprint 生成 plist。
- 禁止模型直接决定危险网络请求。
- 对敏感权限进行二次确认。
- 对生成结果做 plist 校验。
- 对控制流、变量引用、参数类型做校验。
- 生成失败时允许自动修复一次或两次。

理想生成结构：

```text
用户需求
-> JSON blueprint
-> validator
-> plist builder
-> signer
-> scanner
-> result
```

这样比让模型直接生成最终 `.shortcut` 更稳定。

## 13. 运营启动方案

社区早期最重要的是内容供给。

建议上线前准备：

- 30 到 50 个高质量快捷指令。
- 每个核心分类至少 5 个。
- 10 个适合中文用户的场景。
- 10 个 AI 相关快捷指令。
- 10 个效率工具相关快捷指令。
- 5 个图片/视频处理快捷指令。
- 5 个生活记录快捷指令。

可做的精选集合：

- iPhone 新手必备快捷指令。
- AI 工作流快捷指令。
- 学生党效率工具箱。
- 自媒体创作者工具箱。
- Mac 自动化入门。
- 中文 App 常用自动化。

## 14. 商业化方向

第一版不需要急着做商业化，但架构应预留空间。

可选方向：

- 免费基础生成，高级生成订阅。
- 高级模型生成次数包。
- 复杂快捷指令定制。
- 创作者付费模板。
- 付费精选集合。
- 团队自动化模板。
- 企业私有快捷指令库。
- 高级安全扫描。

## 15. 里程碑

### 15.1 Milestone 1：生成器可用

- 自然语言输入。
- 生成 `.shortcut`。
- 本地签名。
- 下载文件。
- 基础错误处理。

### 15.2 Milestone 2：社区基础

- 登录。
- 发布快捷指令。
- 浏览列表。
- 详情页。
- 上传文件。
- 下载统计。

### 15.3 Milestone 3：互动与信任

- 点赞。
- 收藏。
- 评论。
- 举报。
- 管理员下架。
- 权限说明。
- 风险等级。

### 15.4 Milestone 4：Cloudflare 部署

- 前端迁移到 Cloudflare Pages。
- API 迁移到 Cloudflare Workers。
- D1 数据模型落地。
- R2 文件存储落地。
- Queues 异步任务落地。
- Turnstile 接入。

### 15.5 Milestone 5：创作者生态

- 作者主页。
- 版本管理。
- 精选机制。
- Fork / Remix。
- 创作者数据面板。

## 16. 关键风险

### 16.1 Apple Shortcuts 签名依赖

`.shortcut` 文件的签名最好使用 macOS `shortcuts sign`。Cloudflare Workers 无法直接运行这个命令，因此需要保留独立 macOS 签名服务，或在早期只支持说明生成和用户上传。

### 16.2 AI 生成不稳定

模型可能生成不存在的 action、错误参数或不可运行的控制流。需要通过结构化 blueprint、白名单和校验器降低风险。

### 16.3 安全信任问题

快捷指令可能访问敏感数据。社区必须突出权限说明、风险等级、举报和审核。

### 16.4 内容冷启动

社区没有内容时用户留不住。上线前需要准备一批高质量模板。

### 16.5 平台兼容性

iOS、iPadOS 和 macOS 的 Shortcut actions 支持可能不同，需要记录目标平台并尽量做兼容提示。

## 17. 下一步建议

建议按以下顺序推进：

1. 先把当前生成器 MVP 稳定下来。
2. 增加生成历史和快捷指令元数据。
3. 增加发布、浏览、详情页。
4. 引入 D1/R2 的数据和文件抽象。
5. 设计 macOS 签名服务与 Cloudflare Worker 的任务协作。
6. 增加权限扫描和风险提示。
7. 准备首批精选快捷指令内容。

第一阶段的核心判断不是技术是否完整，而是：

```text
用户是否愿意用自然语言生成快捷指令？
用户是否愿意安装别人分享的快捷指令？
创作者是否愿意发布自己的快捷指令？
```

只要这三个问题有正向反馈，就值得继续把它从生成工具推进成社区平台。
