# Limitations — known constraints and workarounds

Load when: a tool behaves unexpectedly, or before using a tool listed below.
Format (see `index.md` → Entry format): `- **L-NNN** [YYYY-MM-DD] #tags — <limit, one line>` then an indented `Workaround:` sub-bullet. Newest first.

- **L-008** [2026-11-26] #audio — YuE2 Studio `song_export` loudness normalization is one gain with no limiter; a dynamic track hits the true-peak ceiling before the LUFS target and stops short (note code `ceiling_short`, not an error).
  - Why: `loudness {target_lufs:-14, ceiling_dbtp:-1}` on a zen ambient track (-19.5 LUFS, -2.9 dBTP) gave only -17.6 LUFS (+1.9 dB).
  - Workaround: accept it (quieter, unclipped) or limit/compress first (e.g. ffmpeg `loudnorm`/`alimiter`) when the exact target matters.
- **L-001** [2026-11-23] #claude-code #memory — In auto mode, the permission classifier blocks bulk-extracting transcripts from **all** projects (`~/.claude/projects/*/*.jsonl`) into the shared memory folder ("Unauthorized Access").
  - Workaround: read only the current project's transcripts and keep extracts in the session scratchpad. Store just hashes and counts in memory.
- **L-002** [2026-11-22] #claude-code — `claude -p` run from inside a Claude desktop session doesn't load CLAUDE.md (not even text written directly in it, with or without the app's session env vars), so it can't verify `@` imports.
  - Unverified: an `@` import path probably ends at the first space, so give imported files names without spaces.
  - Workaround: check what loaded in a fresh interactive session (`/memory` in a terminal, or ask the agent to quote a line from `global.md`).
- **L-003** [2026-11-22] #browser — Built-in browser: a tab showing a local file can't navigate to localhost.
  - Workaround: use the new tabId the tool returns, or `preview_start` with a launch.json entry. "Policy check in progress" → retry once.
- **L-007** [2026-11-25] #browser #testing — Built-in browser: the screenshot coordinate frame (e.g. 800×600) is not the page's CSS viewport (e.g. 1024×768), and the screenshot can lag the page; reading click/drag targets off a scaled screenshot misses.
  - Workaround: get the target from JS (`el.getBoundingClientRect()` centre, check `document.elementFromPoint`), multiply by frame/`innerWidth` (here 0.78), then `left_click_drag`. Verify the effect in JS state, not by eye. Why: a node-drag test hit empty canvas and panned it instead (BalticIntel v0.8.3). Recurred the same day (v0.8.4) when scaling by hand: a "blank canvas" click hit a docked panel — always confirm the target with `elementFromPoint` before clicking.
  - Also: `element.requestFullscreen()` does not take effect in the built-in browser (no `document.fullscreenElement`); give full-screen UIs a CSS-class fallback (`position:fixed;inset:0`) and test that.
- **L-006** [2026-11-25] #browser #claude-code — Built-in browser: `preview_start(name)` reads `.claude/launch.json` only from the session's *original* working directory, and silently reassigns a busy port while the server's hardcoded `runtimeArgs` port stays put → blank `chrome-error://` page, no console errors.
  - Workaround that worked (2026-11-25): add the entry to the *original* dir's launch.json with `"autoPort": false` and a free port, running the other project via `python -c "import sys,runpy;sys.path.insert(0,r'<project>');sys.argv=['backend','--port','<port>'];runpy.run_module('backend',run_name='__main__')"`. File/`file://` pages outside the project open only as static snapshots; test offline modes with a `?offline` switch instead.
  - Fallback: skip `preview_start(name)` for an added dir: start the server with Bash `run_in_background` on a port checked free (`netstat -ano | grep :<port>`), then `navigate` to `http://127.0.0.1:<port>/`. A blank page with no console output → check `location.href` in JS for `chrome-error`. `navigate` can report "denied or failed" though the page loaded: screenshot before retrying.
  - Why: BalticIntel (2026-11-25) — launch.json in project dir not found. Traffic Lens (2026-11-25) — 8765 held by another process, tool moved to 8766 but `http.server 8765` kept the arg; a retry with edited launch.json was then denied by the auto-mode classifier, background Bash server worked. CVE_Intel (2026-11-25) — runpy entry in `C:\ai\.claude\launch.json` on 8766 worked. Related: L-003, I-018.
- **L-004** [2026-11-24] #browser — Built-in browser: `read_console_messages` keeps errors from older hot-reloaded module versions, even after navigating or reloading.
  - Workaround: compare the `?t=` timestamp in the stack trace with the current module; if it is old, confirm the fix with the type check and the rendered page.
- **L-005** [2026-11-22] #claude-code — Claude Code hook, settings and CLAUDE.md changes may only take effect in a new session.
  - Workaround: test hook scripts directly with fixtures (PR-002), then confirm in the next session.
