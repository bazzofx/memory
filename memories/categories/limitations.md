# Limitations — known constraints and workarounds

Load when: a tool behaves unexpectedly, or before using a tool listed below.
Format (see `index.md` → Entry format): `- **L-NNN** [YYYY-MM-DD] #tags — <limit, one line>` then an indented `Workaround:` sub-bullet. Newest first.

- **L-001** [2026-11-23] #claude-code #memory — In auto mode, the permission classifier blocks bulk-extracting transcripts from **all** projects (`~/.claude/projects/*/*.jsonl`) into the shared memory folder ("Unauthorized Access").
  - Workaround: read only the current project's transcripts and keep extracts in the session scratchpad. Store just hashes and counts in memory.
- **L-002** [2026-11-22] #claude-code — `claude -p` run from inside a Claude desktop session doesn't load CLAUDE.md (not even text written directly in it, with or without the app's session env vars), so it can't verify `@` imports.
  - Unverified: an `@` import path probably ends at the first space, so give imported files names without spaces.
  - Workaround: check what loaded in a fresh interactive session (`/memory` in a terminal, or ask the agent to quote a line from `global.md`).
- **L-003** [2026-11-22] #browser — Built-in browser: a tab showing a local file can't navigate to localhost.
  - Workaround: use the new tabId the tool returns, or `preview_start` with a launch.json entry. "Policy check in progress" → retry once.
- **L-004** [2026-11-24] #browser — Built-in browser: `read_console_messages` keeps errors from older hot-reloaded module versions, even after navigating or reloading.
  - Workaround: compare the `?t=` timestamp in the stack trace with the current module; if it is old, confirm the fix with the type check and the rendered page.
- **L-005** [2026-11-22] #claude-code — Claude Code hook, settings and CLAUDE.md changes may only take effect in a new session.
  - Workaround: test hook scripts directly with fixtures (PR-002), then confirm in the next session.
