# Pending — unresolved tasks and follow-up work

Load when: session start, task end, or the user asks what's left.
Format (see `index.md` → Entry format): `- **T-NNN** [YYYY-MM-DD] [project] <item, one line>` then an indented `Next:` sub-bullet. Delete an item when done (move any lasting lesson to its category); its ID is not reused.

- **T-001** [2026-11-25] [global] Confirm that `global.md` now loads in projects other than kairo through `~/.claude/CLAUDE.md`.
  - Next: in a new session in another project (e.g. ZenWarriorSounds or Voice2Text), check that the agent knows the `## Realized dreams` list without reading any file. If not, see L-002.
- **T-002** [2026-11-22] [global] The Stop hook's dream pass (Phase B) hasn't yet been seen adding or updating a dream from a live run. Its first live run (2026-11-25) checked `dreams.md`, added nothing and made no duplicates.
  - Next: after a hook-triggered run that proposes a dream, check `dreams/dreams.md` for duplicates.
- **T-003** [2026-11-25] [global] The global `dream-realizer` skill's folder name and frontmatter name (`dream-realization`) differ; `~/.claude/CLAUDE.md` names both.
  - Next: ask the user which name to keep, then make both match.
- **T-004** [2026-11-25] [kairo] Leftover project-local copies of the memory skills (`.claude/skills/`) and hook (`.claude/hooks/memory-check.cjs`) can drift from the global ones. Kairo's `CLAUDE.md` no longer points at them (2026-11-25).
  - Next: ask the user whether to delete the copies.
- **T-005** [2026-11-24] [kairo] Luci's spoken path (Ctrl+1 → Whisper, a spoken yes/no to a proposal, barge-in) was only tested with typed input; the microphone was never tested live.
  - Next: ask the user to try it, and check the Luci log.
- **T-006** [2026-11-22] [global] Dreams are captured at task end, but there's no SessionStart review (show up to 3 pending dreams).
  - Next: ask the user whether to add a SessionStart hook.
- **T-007** [2026-11-25] [global] `S-001`'s CDP script and `PR-001`'s transcript scanner were lost with their session scratchpads.
  - Next: the next time either is needed, save the script to `C:\ai\toolbox\` and list it in `toolbox/README.md`.
