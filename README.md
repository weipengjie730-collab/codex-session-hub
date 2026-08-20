# Codex Session Hub

Codex Session Hub 是一个本地优先的 Codex 多对话任务记忆系统。

它解决这些问题：

- 同时开多个 Codex 对话时，容易把任务串线；
- 离开工作台一段时间后，忘记某个对话做到哪了；
- 某个问题、决策、坑点散落在不同对话里，不知道去哪找；
- 想让 Codex 从对话中提取可复用知识，沉淀到 Obsidian。

核心思路：**不读取所有聊天全文，不后台监听所有窗口；而是在你触发时，把当前对话压缩成任务记忆和知识卡片。**

## 使用方式

第一版不需要部署服务器，也不是一个网站。它有两种使用方式：

### 方式 A：作为 Codex skill 使用

把 `skills/session-hub` 复制到：

```bash
~/.codex/skills/session-hub
```

然后在 Codex 新对话里说：

```text
同步当前对话到 session hub
```

或：

```text
查一下历史任务里有没有提过“小红书封面生成器”
```

### 方式 B：作为 Codex plugin 使用

本仓库已经包含 `.codex-plugin/plugin.json`，可以作为 Codex plugin 打包安装。

如果你把它发布到 GitHub，可用类似方式安装：

```bash
codex plugin marketplace add yourname/codex-session-hub
codex plugin add codex-session-hub@codex-session-hub
```

安装后，新 Codex 对话里可直接调用 session-hub skill。

## 默认数据位置

Session Hub 默认把任务记忆写到：

```text
~/Documents/Codex/session-hub
```

Obsidian 知识卡片默认写到：

```text
~/Documents/Obsidian Vault/40-整理产出/Codex知识卡片
```

可以通过环境变量修改：

```bash
export SESSION_HUB_ROOT="/path/to/session-hub"
export OBSIDIAN_KNOWLEDGE_DIR="/path/to/obsidian/cards"
```

## 典型触发语

```text
同步当前对话
生成交接语
继续小红书 skill 任务
列出所有进行中的任务
查一下哪个任务提过 GitHub plugin
提取这段对话的知识到 Obsidian
列出未解决问题
```

## 目录结构

```text
codex-session-hub/
├── .codex-plugin/plugin.json
├── AGENTS.md
├── README.md
├── skills/session-hub/
│   ├── SKILL.md
│   ├── scripts/session_hub.py
│   └── templates/
├── examples/
└── docs/
```

## 不做什么

第一版刻意不做：

- 后台监听所有 Codex 对话；
- 自动读取未同步对话全文；
- 云端数据库；
- 大型 Web dashboard；
- 语义向量检索。

这些以后可以加，但第一版先把“同步、交接、搜索、知识卡片”跑通。
