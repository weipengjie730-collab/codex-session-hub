---
name: collaboration-profile
description: Build a user-approved AI collaboration profile from explicitly selected local Codex conversations. Never silently scan all conversation history or make personality, mental-health, or capability judgments.
---

# Collaboration Profile

Create a practical, user-owned `AI_WORKING_PROFILE.md` that tells future AI conversations how to work well with this person.

## Boundary

- Do not read every historical chat automatically. First run `index`, show the user candidates, and only process sessions they explicitly select.
- Warn that the helper redacts common secret formats but cannot guarantee complete redaction. Exclude private third-party, credential, health, legal, and financial chats.
- Treat conclusions as hypotheses. Cite interaction evidence and ask the user to approve or correct the final profile.
- Do not infer personality, diagnosis, intelligence, politics, or protected traits.

## Workflow

1. List local session candidates: `python3 scripts/collaboration_profile.py index --limit 20`.
2. Ask the user to select 3-10 representative paths.
3. Create a local evidence pack from only those paths: `python3 scripts/collaboration_profile.py pack --session /absolute/path/one.jsonl --session /absolute/path/two.jsonl --include-assistant`.
4. Read the pack and draft `${COLLABORATION_PROFILE_ROOT:-~/Documents/Codex/collaboration-profile}/AI_WORKING_PROFILE.md` from `templates/ai-working-profile.md`.
5. Ask the user to confirm the 5-8 most important defaults before treating the profile as approved.

## Profile content

Include only actionable observations: communication defaults, execution/approval defaults, decision and quality bar, useful response formats, likely friction points, and evidence/confidence. Keep the default profile under 900 Chinese characters.

## Reuse

When the approved profile exists, read it as a preference layer in future tasks. It never overrides the current request or authorizes irreversible actions.
