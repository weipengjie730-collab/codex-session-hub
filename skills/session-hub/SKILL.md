---
name: session-hub
description: Manage Codex multi-conversation task memory, handoffs, open questions, decisions, and Obsidian knowledge extraction. Use when the user says or implies: 同步当前对话, 更新当前任务, 生成交接语, 上下文接力, 继续某个任务, 查找历史任务, 哪个对话提过某问题, 列出未解决问题, 提取知识到 Obsidian, 更新 Obsidian 知识卡片, or wants Codex conversations to share task memory without reading full transcripts.
---

# Session Hub

Use this skill to persist compact task memory across Codex conversations.

Core rule: do not promise access to every Codex chat transcript. Only use the current visible conversation plus files previously written to the session hub or Obsidian.

## Defaults

- Session hub root: `${SESSION_HUB_ROOT:-~/Documents/Codex/session-hub}`
- Obsidian knowledge dir: `${OBSIDIAN_KNOWLEDGE_DIR:-~/Documents/Obsidian Vault/40-整理产出/Codex知识卡片}`
- Helper script: `scripts/session_hub.py`
- Templates: `templates/session-template.md`, `templates/handoff-template.md`, `templates/knowledge-card-template.md`

Run `python3 scripts/session_hub.py init` before first write if the hub root does not exist.

## Intent routing

### Sync current conversation

When the user says “同步当前对话”, “更新当前任务”, or similar:

1. Identify the task name. If unclear, infer a short concrete name from the conversation.
2. Summarize only durable task state:
   - current goal
   - status
   - completed work
   - key decisions
   - open questions
   - related files/links
   - next actions
   - next-prompt handoff
3. Write or update `sessions/<slug>.md` in the hub root.
4. Update `index.md`, `open-questions.md`, and `decisions.md` when relevant.
5. Do not store credentials, raw private chat, tokens, cookies, or sensitive secrets.

Use the session template. Prefer direct Markdown edits when updating rich content; use the helper script for initialization, listing, searching, and simple file creation.

### Continue a historical task

When the user says “继续 X 任务” or “读取 X 的上下文”:

1. Search the hub with `python3 scripts/session_hub.py search "X"`.
2. Read the best matching session file.
3. Briefly confirm the recovered task, status, and next action before continuing.
4. If multiple matches are plausible, list 2-3 candidates and ask the user to pick.

### Find where an issue was discussed

When the user asks “哪个对话提过 X”:

1. Search sessions, handoffs, decisions, open questions, and Obsidian knowledge cards.
2. Return matching files and short snippets.
3. Prefer source file paths over vague memory.

### Generate handoff

When the user says “生成交接语”, “上下文接力”, “快满了”, or “新对话继续”:

1. Update the session file first if the current task changed.
2. Create a handoff file under `handoffs/`.
3. Return a concise copy-paste prompt for the next Codex conversation.

### Extract knowledge to Obsidian

When the user says “提取知识到 Obsidian” or asks to沉淀知识:

1. Extract only reusable knowledge, not task chatter.
2. Create one card per durable idea when possible.
3. Include source session, date, tags, and “适用场景”.
4. Write cards to the configured Obsidian knowledge dir.
5. If the user only asked to sync a task, do not write Obsidian cards unless durable knowledge is clearly present or the user asks.

## Quality bar

- Keep entries short enough to be read by future Codex sessions.
- Prefer facts, decisions, and next actions over narrative.
- Use exact file paths and URLs when available.
- Mark uncertainty explicitly.
- Avoid duplicating the same knowledge card; update existing cards when a clear match exists.
