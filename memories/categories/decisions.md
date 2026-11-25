# Decisions — important decisions and their reasoning (cross-project)

Load when: changing shared tooling, the memory layout or conventions. Project-only decisions go in `projects/<name>.md`.
Format (see `index.md` → Entry format): `- **D-NNN** [YYYY-MM-DD] #tags — <decision, one line>` then indented `Why:` sub-bullets. Newest first.

- **D-001** [2026-11-25] #memory #claude-code — Central memory is the only source of truth, and it loads for every project through `~/.claude/CLAUDE.md` (`@C:/ai/memories/global.md`). Project CLAUDE.md files hold only their project pointer, and Claude Code's per-project auto-memory (`~/.claude/projects/<proj>/memory/`) holds only a pointer line.
  - Entries carry permanent IDs (`I-`, `S-`, `D-`, `P-`, `E-`, `L-`, `R-`, `PR-`, `T-`) and `#tags` from the fixed list in `index.md`; `index.md` → Topics maps each tag to its IDs across all files. Reusable scripts live in `C:\ai\toolbox\`, how-to notes and pointers in `categories/references.md`.
  - Why: `global.md` had only loaded in kairo, and ZenWarriorSounds and Voice2Text kept lessons in their own auto-memory where no other project could see them. The user approved the restructure on 2026-11-25.
- **D-002** [2026-11-25] #memory #claude-code — Memory tooling is global, not per project: the skills `memory-optimizer`, `dream-manager`, `dream-realizer` (frontmatter name `dream-realization`) and `update-subconscious` live in `C:\Users\joker\.claude\skills\`, and the Stop hook is registered once in `C:\Users\joker\.claude\settings.json`.
  - Hook command: `node "C:/Users/joker/.claude/hooks/memory-check.cjs"`, timeout 30. Projects must not register it again, or it fires twice.
  - Why: the user moved them so every project gets the memory and dream workflow; kairo's own Stop entry was removed for this reason.
- **D-003** [2026-11-22] #memory — Agent memory is central at `C:\ai\memories\` (`global.md`, `index.md`, `categories/`, `projects/`, `dreams/`, `subconscious/`), with no project-local memory folders. Only `global.md` is always loaded; everything else is loaded on demand via `index.md`.
  - [2026-11-25] `global.md` also holds a short `## Realized dreams` list (one line per realized dream, pointing to `subconscious/`), written by `dream-realizer` Gate 9 step 5. Why: the user asked for past realized work to be always in context.
  - Why: the user wants one memory shared by every project, loading only the relevant file to keep context small.
