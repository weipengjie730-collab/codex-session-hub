#!/usr/bin/env python3
"""Tiny local Markdown helper for Codex Session Hub. Stdlib only."""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from pathlib import Path


def default_root() -> Path:
    return Path(os.environ.get("SESSION_HUB_ROOT", "~/Documents/Codex/session-hub")).expanduser()


def default_obsidian_dir() -> Path:
    return Path(os.environ.get("OBSIDIAN_KNOWLEDGE_DIR", "~/Documents/Obsidian Vault/40-整理产出/Codex知识卡片")).expanduser()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80] or "session"


def ensure(root: Path) -> None:
    for name in ["sessions", "handoffs", "knowledge", "logs"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    for file, title in [
        ("index.md", "# Session Index\n\n"),
        ("open-questions.md", "# Open Questions\n\n"),
        ("decisions.md", "# Decisions\n\n"),
        ("error-solutions.md", "# Error Solutions\n\n"),
    ]:
        p = root / file
        if not p.exists():
            p.write_text(title, encoding="utf-8")


def new_session(root: Path, title: str, status: str, project: str) -> Path:
    ensure(root)
    sid = slugify(title)
    p = root / "sessions" / f"{sid}.md"
    if p.exists():
        return p
    now = datetime.now().isoformat(timespec="seconds")
    content = f"""# {title}

## Metadata

- id: {sid}
- status: {status}
- updated: {now}
- project: {project or '未指定'}
- source: manual

## Current goal

待补充。

## Progress

- 待补充。

## Key decisions

- 待补充。

## Open questions

- [ ] 待补充。

## Related files and links

- 待补充。

## Next actions

- 待补充。

## Continue prompt

请读取 `{p}`，恢复“{title}”任务上下文，先确认当前状态和下一步，再继续。
"""
    p.write_text(content, encoding="utf-8")
    append_once(root / "index.md", f"- [{title}](sessions/{sid}.md) — {status}\n")
    return p


def append_once(path: Path, line: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if line not in text:
        path.write_text(text + line, encoding="utf-8")


def iter_markdown(root: Path, include_obsidian: bool) -> list[Path]:
    files = list(root.rglob("*.md")) if root.exists() else []
    if include_obsidian:
        obs = default_obsidian_dir()
        if obs.exists():
            files.extend(obs.rglob("*.md"))
    return files


def search(root: Path, query: str, include_obsidian: bool, limit: int) -> None:
    q = query.lower()
    hits = []
    for path in iter_markdown(root, include_obsidian):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if q in line.lower():
                hits.append((path, i, line.strip()))
                break
    for path, line_no, line in hits[:limit]:
        print(f"{path}:{line_no}: {line}")


def list_sessions(root: Path) -> None:
    ensure(root)
    for path in sorted((root / "sessions").glob("*.md")):
        title = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].lstrip("# ")
        print(f"{path.stem}\t{title}\t{path}")


def questions(root: Path) -> None:
    ensure(root)
    path = root / "open-questions.md"
    print(path.read_text(encoding="utf-8"))


def handoff(root: Path, session_id: str) -> Path:
    ensure(root)
    session = root / "sessions" / f"{session_id}.md"
    if not session.exists():
        raise SystemExit(f"No session: {session}")
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = root / "handoffs" / f"{now}-{session_id}.md"
    summary = session.read_text(encoding="utf-8")
    title = summary.splitlines()[0].lstrip("# ") if summary else session_id
    content = f"""# Handoff: {title}

- session: {session_id}
- created: {datetime.now().isoformat(timespec='seconds')}

## Copy into the next Codex conversation

请继续 `{title}`。先读取 `{session}` 和本交接文件 `{out}`，确认当前目标、已完成、关键决策、未解决问题和下一步，然后继续推进。不要假设能读取旧对话全文，只以这些文件为准。

## Session snapshot

{summary}
"""
    out.write_text(content, encoding="utf-8")
    print(out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(default_root()))
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    p_new = sub.add_parser("new")
    p_new.add_argument("title")
    p_new.add_argument("--status", default="进行中")
    p_new.add_argument("--project", default="")

    sub.add_parser("list")

    p_search = sub.add_parser("search")
    p_search.add_argument("query")
    p_search.add_argument("--obsidian", action="store_true")
    p_search.add_argument("--limit", type=int, default=20)

    p_handoff = sub.add_parser("handoff")
    p_handoff.add_argument("session_id")

    sub.add_parser("questions")

    args = parser.parse_args()
    root = Path(args.root).expanduser()

    if args.cmd == "init":
        ensure(root)
        default_obsidian_dir().mkdir(parents=True, exist_ok=True)
        print(root)
    elif args.cmd == "new":
        print(new_session(root, args.title, args.status, args.project))
    elif args.cmd == "list":
        list_sessions(root)
    elif args.cmd == "search":
        search(root, args.query, args.obsidian, args.limit)
    elif args.cmd == "handoff":
        handoff(root, args.session_id)
    elif args.cmd == "questions":
        questions(root)


if __name__ == "__main__":
    main()
