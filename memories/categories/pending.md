# Pending — unresolved tasks and follow-up work

Load when: session start, task end, or the user asks what's left.
Format: `- [YYYY-MM-DD] [project] <item>. Next: <first step>.` Delete an item when done (move any lasting lesson to its category).

- [2026-11-22] [kairo] Memory Stop hook (`.claude/hooks/memory-check.cjs`) only tested with fixtures, not yet seen firing in a live session. Next: after a noisy task in a new session, confirm it asks for memory-optimizer once.
- [2026-11-22] [kairo] Memory Stop hook now also runs the dream pass (Phase B) — confirm in a live session that it adds/updates dreams without duplicates. Next: check `dreams/dreams.md` after the first hook-triggered run.
- [2026-11-22] [kairo] Dreams are captured at task end, but there's no SessionStart review (show up to 3 pending dreams). Next: ask the user whether to add a SessionStart hook.
