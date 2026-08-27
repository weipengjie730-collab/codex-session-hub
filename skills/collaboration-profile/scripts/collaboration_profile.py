#!/usr/bin/env python3
"""Consent-based source pack builder for selected local Codex sessions."""
from __future__ import annotations
import argparse, json, os, re
from datetime import datetime
from pathlib import Path

ROOT = Path("~/.codex/sessions").expanduser()
OUT = Path(os.environ.get("COLLABORATION_PROFILE_ROOT", "~/Documents/Codex/collaboration-profile")).expanduser()
PATTERNS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]"),
    (r"\b(?:sk|ghp|github_pat|xoxb|xoxp)_[A-Za-z0-9_-]{16,}\b", "[REDACTED_TOKEN]"),
    (r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b", "[REDACTED_JWT]"),
    (r"(?i)(password|passwd|api[_ -]?key|secret)\s*[:=]\s*[^\s,;]{6,}", r"\1=[REDACTED]"),
]

def redact(text: str) -> str:
    for pattern, replacement in PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.S if "PRIVATE" in pattern else 0)
    return text

def events(path: Path):
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            value = json.loads(line)
            if isinstance(value, dict): yield value
        except json.JSONDecodeError: pass

def texts(payload: dict) -> list[str]:
    return [str(x.get("text", "")) for x in payload.get("content", []) if isinstance(x, dict) and x.get("type") in {"input_text", "output_text", "text"} and x.get("text")]

def summary(path: Path):
    preview, users, assistants, stamp, cwd = "", 0, 0, "", ""
    for item in events(path):
        payload = item.get("payload") or {}
        if item.get("type") == "session_meta": stamp, cwd = str(payload.get("timestamp", item.get("timestamp", ""))), str(payload.get("cwd", ""))
        if item.get("type") != "response_item" or not isinstance(payload, dict): continue
        blocks, role = texts(payload), payload.get("role")
        if role == "user":
            users += 1
            if not preview and blocks: preview = re.sub(r"\s+", " ", redact(" ".join(blocks))).strip()[:100]
        elif role == "assistant": assistants += 1
    return stamp, cwd, users, assistants, preview or "(no user text found)"

def index(args):
    root = Path(args.source).expanduser()
    for path in sorted(root.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:args.limit]:
        stamp, cwd, users, assistants, preview = summary(path)
        print(f"{path}\n  time: {stamp or datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec='minutes')}\n  cwd: {cwd or '-'}\n  messages: user {users} / assistant {assistants}\n  preview: {preview}\n")

def pack(args):
    root = Path(args.source).expanduser().resolve()
    selected = []
    for raw in args.session:
        path = Path(raw).expanduser().resolve()
        try: path.relative_to(root)
        except ValueError: raise SystemExit(f"Session must be under {root}: {path}")
        if not path.is_file() or path.suffix != ".jsonl": raise SystemExit(f"Not a readable Codex session: {path}")
        selected.append(path)
    out = Path(args.out).expanduser() if args.out else OUT / f"profile-sources-{datetime.now():%Y%m%d-%H%M%S}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Collaboration Profile — Selected Conversation Evidence", "", "> Generated locally from explicitly selected sessions. Review redactions before sharing.", "", f"- created: {datetime.now().isoformat(timespec='seconds')}", f"- selected sessions: {len(selected)}", ""]
    for number, path in enumerate(selected, 1):
        stamp, cwd, *_ = summary(path)
        lines += [f"## Session {number}", "", f"- source: `{path}`", f"- time: {stamp or '-'}", f"- cwd: `{cwd or '-'}`", ""]
        for item in events(path):
            if item.get("type") != "response_item": continue
            payload = item.get("payload") or {}
            role = payload.get("role") if isinstance(payload, dict) else ""
            if role not in {"user", "assistant"} or (role == "assistant" and not args.include_assistant): continue
            body = redact("\n".join(texts(payload))).strip()
            if body: lines += [f"### {'User' if role == 'user' else 'Assistant'}", "", body, ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)

parser = argparse.ArgumentParser(description="Prepare consent-based Codex conversation evidence.")
parser.add_argument("--source", default=str(ROOT))
sub = parser.add_subparsers(dest="command", required=True)
p = sub.add_parser("index"); p.add_argument("--limit", type=int, default=20)
p = sub.add_parser("pack"); p.add_argument("--session", action="append", required=True); p.add_argument("--out"); p.add_argument("--include-assistant", action="store_true")
args = parser.parse_args()
index(args) if args.command == "index" else pack(args)
