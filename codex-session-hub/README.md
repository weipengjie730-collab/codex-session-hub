# Codex Session Hub

我经常会同时开几个 Codex 对话：一个在写代码，一个在查资料，一个在整理文档，另一个可能还停在 GitHub 发布流程里。任务一多，问题就来了：

- 回来以后忘了某个对话做到哪一步；
- 两个相似任务串在一起，开始说 A，结果把 B 的决策带进来；
- 某个报错、命令、方案明明讨论过，但不知道散在哪个对话里；
- 想把有价值的经验沉淀到 Obsidian，最后却只剩聊天记录越堆越长。

**Codex Session Hub** 是为这个场景做的一个本地优先小工具。它不是另一个知识库，也不是后台监控器，而是一套很朴素的约定：在合适的时候，让 Codex 把当前任务压缩成几份可读的 Markdown，之后新的对话可以直接接着这些文件继续工作。

## 它解决什么

Session Hub 主要管四类东西：

1. **任务状态**：这个任务现在要做什么，已经完成了什么，下一步是什么。
2. **关键决策**：为什么选这个方案，不选那个方案。
3. **遗留问题**：哪些问题还没解决，别在新对话里忘掉。
4. **知识卡片**：把可复用的方法、坑点、命令沉淀到 Obsidian。

核心原则是：

> 不假装能读取所有旧对话，也不保存完整聊天记录。只保存你明确同步过的任务摘要、交接语、决策和知识卡片。

这样做的好处是文件少、可控、能搜索，也方便你自己打开看。

## 适合谁

如果你有下面这些习惯，这个项目会比较有用：

- 经常同时开多个 Codex 任务；
- 会把 Codex 当成长期工作台，而不是一次性问答；
- 希望旧任务能被新对话接上；
- 用 Obsidian 管项目、知识或复盘；
- 不想为了一个小需求先部署数据库、后端和 dashboard。

如果你只是偶尔让 Codex 改一个文件，那这个项目可能没必要。

## 它不是什么

第一版刻意不做这些事：

- 不后台监听所有 Codex 对话；
- 不自动读取没有同步过的旧聊天全文；
- 不上传到云端数据库；
- 不做复杂权限系统；
- 不做花哨 dashboard；
- 不做向量检索。

这些都可以以后加，但一开始没必要。先把“能交接、能找回、能沉淀”跑通。

## 快速开始

把 skill 目录复制到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R skills/session-hub ~/.codex/skills/session-hub
```

初始化本地记录目录：

```bash
python3 ~/.codex/skills/session-hub/scripts/session_hub.py init
```

默认会写到：

```text
~/Documents/Codex/session-hub
```

Obsidian 知识卡片默认写到：

```text
~/Documents/Obsidian Vault/40-整理产出/Codex知识卡片
```

如果你想改位置：

```bash
export SESSION_HUB_ROOT="/path/to/session-hub"
export OBSIDIAN_KNOWLEDGE_DIR="/path/to/obsidian/cards"
```

## 在 Codex 里怎么用

安装后，可以在 Codex 对话里直接说：

```text
同步当前对话到 session hub
```

或者：

```text
生成这个任务的交接语
```

再或者：

```text
查一下历史任务里有没有提过 GitHub 插件授权
```

常用触发语：

```text
同步当前对话
更新当前任务
生成交接语
继续某个任务
列出所有进行中的任务
查一下哪个任务提过某个问题
列出未解决问题
提取这段对话的知识到 Obsidian
```

## 命令行用法

这个项目的脚本只用 Python 标准库，不需要安装依赖。

初始化：

```bash
python3 skills/session-hub/scripts/session_hub.py init
```

新建任务记录：

```bash
python3 skills/session-hub/scripts/session_hub.py new "GitHub 发布 Session Hub" --project "codex-session-hub"
```

列出任务：

```bash
python3 skills/session-hub/scripts/session_hub.py list
```

搜索：

```bash
python3 skills/session-hub/scripts/session_hub.py search "GitHub"
```

连 Obsidian 知识卡片一起搜：

```bash
python3 skills/session-hub/scripts/session_hub.py search "封面生成" --obsidian
```

生成交接文件：

```bash
python3 skills/session-hub/scripts/session_hub.py handoff github-发布-session-hub
```

## 文件会长什么样

初始化后，本地目录大概是这样：

```text
~/Documents/Codex/session-hub/
├── index.md
├── open-questions.md
├── decisions.md
├── error-solutions.md
├── sessions/
├── handoffs/
├── knowledge/
└── logs/
```

单个任务记录会包含：

- 当前目标；
- 已完成进度；
- 关键决策；
- 未解决问题；
- 相关文件和链接；
- 下一步动作；
- 可粘贴到新对话的继续提示词。

示例见：[`examples/example-session.md`](examples/example-session.md)

## 和 Obsidian 的关系

Session Hub 不替代 Obsidian。它更像 Codex 工作台的“任务暂存层”。

- 当前任务、交接语、未解决问题：放在 Session Hub；
- 可以反复复用的经验、方法、坑点：沉淀到 Obsidian；
- 不确定有没有长期价值的内容：先留在任务记录里，不急着做知识卡片。

更多建议见：[`docs/obsidian-integration.md`](docs/obsidian-integration.md)

## 作为 Codex plugin 使用

仓库里带了 `.codex-plugin/plugin.json`。如果你的 Codex 支持从 GitHub 安装 plugin，可以按类似方式安装：

```bash
codex plugin marketplace add weipengjie730-collab/codex-session-hub
codex plugin add codex-session-hub@codex-session-hub
```

如果 plugin 安装方式变动，最稳的办法仍然是直接复制 `skills/session-hub` 到 `~/.codex/skills/session-hub`。

## 设计取舍

这个项目目前选择 Markdown，而不是数据库。原因很简单：

- 可以直接用编辑器打开；
- Git 能追踪变化；
- grep 就能搜；
- 不绑定某个服务；
- 坏了也容易修。

等 Markdown 真开始不够用，再考虑 SQLite、MCP 或本地 dashboard。现在先不提前复杂化。

## 目录结构

```text
codex-session-hub/
├── .codex-plugin/plugin.json
├── AGENTS.md
├── README.md
├── docs/
│   ├── obsidian-integration.md
│   └── roadmap.md
├── examples/
│   └── example-session.md
└── skills/
    └── session-hub/
        ├── SKILL.md
        ├── scripts/session_hub.py
        └── templates/
```

## 安全边界

不要把这些内容写进 Session Hub：

- token；
- cookie；
- 密码；
- 私钥；
- `.env` 内容；
- 未经处理的私密聊天全文。

它应该记录“任务怎么继续”，不是复制一份你的全部上下文。

## Roadmap

近期更值得做的是：

- 更好的 update 命令；
- 重复知识卡片检测；
- 冲突合并策略；
- 更清晰的任务状态列表；
- 可选的本地 dashboard。

详细版本规划见：[`docs/roadmap.md`](docs/roadmap.md)

## License

MIT。
