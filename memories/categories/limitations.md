# Limitations — known constraints and workarounds

Load when: a tool behaves unexpectedly, or before using a tool listed below.
Format: `- [YYYY-MM-DD] <limit>. Workaround: <what to do>.` Newest first.

- [2026-11-23] In auto mode, the permission classifier blocks bulk-extracting transcripts from **all** projects (`~/.claude/projects/*/*.jsonl`) into the shared memory folder ("Unauthorized Access"). Workaround: read only the current project's transcripts and keep extracts in the session scratchpad. Store just hashes and counts in memory.

- [2026-11-22] `claude -p` run from inside a Claude desktop session doesn't load CLAUDE.md (not even text written directly in it, with or without the app's session env vars), so it can't verify `@` imports. Unverified: an `@` import path probably ends at the first space, so give files you import names without spaces. Workaround: check what loaded with `/memory` in a fresh interactive session.
- [2026-11-22] Built-in browser: a tab showing a local file can't navigate to localhost. Workaround: use the new tabId the tool returns, or `preview_start` with a launch.json entry. "Policy check in progress" → retry once.
- [2026-11-24] Built-in browser: `read_console_messages` keeps errors from older hot-reloaded module versions, even after navigating or reloading. Workaround: compare the `?t=` timestamp in the stack trace with the current module, and if it is old, confirm the fix with the type check and the rendered page.
- [2026-11-22] Claude Code hooks/settings changes may only take effect in a new session. Workaround: test hook scripts directly with fixtures (see `procedures.md`), then confirm in the next session.
