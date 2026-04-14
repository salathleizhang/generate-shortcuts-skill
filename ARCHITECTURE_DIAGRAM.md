# AI 生成快捷指令网站架构图

## Demo 版总览

```mermaid
flowchart LR
    User["用户<br/>手机 / 电脑浏览器"] --> Web["Vite + React 前端<br/>输入需求<br/>localhost:5174"]
    Web --> API["FastAPI 后端<br/>运行在你的 Mac 上<br/>localhost:8000"]
    API --> Prompt["Prompt Builder<br/>拼接用户需求 + Skill 文档"]
    Prompt --> LLM["AI 模型<br/>生成 Shortcut plist"]
    LLM --> Validator["校验器<br/>检查 plist / action / UUID"]
    Validator --> Signer["Mac 签名服务<br/>shortcuts sign"]
    Signer --> File["签名后的 .shortcut 文件"]
    File --> Download["下载链接"]
    Download --> User
```

## 你的 Mac 在 Demo 里的角色

```mermaid
flowchart TB
    subgraph Mac["你的 Mac"]
        Vite["Vite Dev Server<br/>React 前端"]
        API["Uvicorn + FastAPI<br/>本地后端服务"]
        Docs["当前 Skill 文档<br/>SKILL.md / ACTIONS.md / PLIST_FORMAT.md"]
        Temp["临时文件目录<br/>unsigned / signed shortcuts"]
        CLI["macOS shortcuts CLI<br/>shortcuts sign"]

        Vite --> API
        API --> Docs
        API --> Temp
        API --> CLI
        CLI --> Temp
    end

    Browser["用户浏览器"] --> Vite
    API --> Model["外部 LLM API"]
    Model --> API
    API --> Vite
    Vite --> Browser
```

## 一次生成请求的流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant W as Vite + React 前端
    participant B as FastAPI 后端
    participant M as AI 模型
    participant V as 校验器
    participant S as shortcuts sign

    U->>W: 输入需求
    W->>B: 提交生成请求
    B->>B: 读取 Skill 文档并构造 Prompt
    B->>M: 请求生成 Shortcut plist
    M-->>B: 返回 plist 内容
    B->>V: 校验 plist 结构
    V-->>B: 返回校验结果
    B->>S: 调用 macOS 签名命令
    S-->>B: 输出 signed .shortcut
    B-->>W: 返回下载链接
    W-->>U: 用户下载并导入快捷指令
```

## MVP 模块拆分

```mermaid
flowchart TB
    Frontend["Vite + React 前端<br/>输入需求 / 显示状态 / 下载文件"]
    Backend["FastAPI 后端<br/>接收请求 / 管理任务 / 返回结果"]
    CORS["CORS 配置<br/>允许 localhost:5174 调用"]
    PromptBuilder["Prompt Builder<br/>把用户需求变成高质量生成指令"]
    Generator["Shortcut Generator<br/>调用 AI 生成 plist"]
    Validator["Validator<br/>验证 Shortcut 结构"]
    Signer["Signer<br/>调用 shortcuts sign"]
    Store["File Store<br/>保存临时文件并定期清理"]

    Frontend --> Backend
    Backend --> CORS
    Backend --> PromptBuilder
    PromptBuilder --> Generator
    Generator --> Validator
    Validator --> Signer
    Signer --> Store
    Store --> Backend
    Backend --> Frontend
```

## 推荐的第一版部署方式

```mermaid
flowchart LR
    Tester["测试用户"] --> Tunnel["临时公网入口<br/>Cloudflare Tunnel / ngrok / Tailscale Funnel"]
    Tunnel --> Frontend["你的 Mac<br/>Vite + React"]
    Frontend --> Backend["你的 Mac<br/>FastAPI + Signer"]
    Backend --> LLM["LLM API"]
    Backend --> Shortcut["生成并签名 .shortcut"]
    Shortcut --> Tester
```

## 以后产品化的架构

```mermaid
flowchart LR
    User["用户"] --> CloudWeb["云端 Web 服务"]
    CloudWeb --> CloudAPI["云端 API<br/>可选 FastAPI"]
    CloudAPI --> Queue["任务队列"]
    Queue --> MacWorker["Mac 签名 Worker<br/>Mac mini / Mac 云主机"]
    MacWorker --> LLM["LLM API"]
    MacWorker --> Storage["文件存储<br/>signed .shortcut"]
    Storage --> CloudAPI
    CloudAPI --> CloudWeb
    CloudWeb --> User
```

## 建议目录结构

```mermaid
flowchart TB
    Repo["generate-shortcuts-skill/"]
    FrontendDir["frontend/<br/>Vite + React"]
    BackendDir["backend/<br/>FastAPI"]
    SkillDocs["Skill 文档<br/>SKILL.md / ACTIONS.md / PLIST_FORMAT.md / ..."]
    Tmp["backend/tmp/<br/>临时 .shortcut 文件"]

    Repo --> FrontendDir
    Repo --> BackendDir
    Repo --> SkillDocs
    BackendDir --> Tmp
    BackendDir --> SkillDocs
```

## 最小 Demo 结论

第一版可以先不做复杂 agent 系统。

最小可行链路是：

```text
Vite React 网页输入 -> FastAPI 后端 -> AI 生成 plist -> 校验 -> shortcuts sign -> 下载 .shortcut
```

等这个链路跑通后，再考虑增加：

- 自动修复失败的 plist。
- 多轮追问。
- 更强的动作检索。
- 模板库。
- 任务队列。
- 专门的 Mac 签名 Worker。
