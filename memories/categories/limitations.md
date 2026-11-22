# Limitations — known constraints and workarounds

Load when: a tool behaves unexpectedly, or before using a tool listed below.
Format: `- [YYYY-MM-DD] <limit>. Workaround: <what to do>.` Newest first.

- [2026-11-22] Built-in browser: a tab showing a local file can't navigate to localhost. Workaround: use the new tabId the tool returns, or `preview_start` with a launch.json entry. "Policy check in progress" → retry once.
- [2026-11-22] Claude Code hooks/settings changes may only take effect in a new session. Workaround: test hook scripts directly with fixtures (see `procedures.md`), then confirm in the next session.
