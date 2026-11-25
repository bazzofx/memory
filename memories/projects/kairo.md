# Project: kairo

Path: `C:\_web_apps_2025\kairo` (Git, branch `main`). Load when working in this project.

## Overview
- Web app: TypeScript + Vite (`vite.config.ts`, `src/`, `server.ts`), Vitest tests, Firebase (`firestore.rules`, `firebase-applet-config.json`).
- `luci/`: Python voice assistant "Luci" (voice commands, spoken replies with Piper, task assistant); has its own `requirements.txt` / `.venv`.

## Voice (Luci)
- [2026-11-24] Stack and handoff:
  - Speech to text: faster-whisper `base` on the CPU.
  - Understanding: lexicon rules, then Ollama `gemma4:latest`.
  - Task assistant: `luci/luci/assistant.py`.
  - Text to speech: Piper, default voice `en_US-hifi_tts_92-medium`, with the Windows voice as fallback (`luci/luci/audio/speaker.py`).
  - Kairo writes the spoken words (`src/voice/speech.ts`).
  - Reusable summary for other TTS + Ollama projects: `docs/voice-tts-handoff.md`.
- [2026-11-24] Luci serves on ws://127.0.0.1:8765. Only one instance can hold the port; the user sometimes runs one from a terminal.
- [2026-11-24] End-to-end test without touching the user's settings:
  - Start Luci with `LUCI_HOME=<scratchpad>/home`, feeding it with `tail -f in.txt | python -m luci serve --no-mic` (run in the background).
  - Append commands to `in.txt`.
  - Connect the browser pane's Kairo with that home's token.
  - Free-mode data is lost on a Vite hot reload, so re-add test tasks after code edits.
- [2026-11-24] Testing projects in the browser pane while signed out (free mode): only one `+project` is allowed. `updateNoteContent` strips `+` from any second project name, and the check is case-sensitive (`+ops` ≠ `+Ops`). Use a single project (one spelling) in test data, or sign in. A duplicate-counting bug in that check was fixed on 2026-11-24.
- [2026-11-24] Task dates like `@today` and `@tomorrow` are resolved **relative to the containing note's `date`** (`parseMarkdown` → `resolveDateShortcut`), not the real today. Writing a task into another day's journal silently re-dates it, while `dueDate` still shows 'Today'. `quickAddTask` must target today's journal, and `createNote(..., background=true)` adds a journal without switching views (switching unmounts the To Do page and drops input focus).
- [2026-11-24] Every view App renders into `<main>` must own its scrolling (`flex-1 h-full overflow-y-auto`), because `<main>` is `overflow-hidden`. StatsView lacked this, and content below the window was unreachable.

## Constraints & decisions
- [2026-11-22] Node scripts outside `src/` (e.g. `.claude/hooks/`) use `.cjs` with `require`. Why: package.json has `"type": "module"`, so a `.js` file with `require` would fail to load.
- [2026-11-22] User chose to work directly on `main` for the memory/skill setup (declined a feature branch). For the voice work (2026-11-24), the user had feature branches merged into `main` and pushed on request (`git merge --no-ff`, then `git push origin main`).
- [2026-11-24] Windows desktop build: Electron (user chose it over Tauri) runs the esbuild-bundled `server.ts` in-process on a **fixed** `http://localhost:47821`. The port can't change, because IndexedDB is stored per origin, and localhost keeps the Firebase popup sign-in and Luci's Origin check working. The user chose to bundle Luci as a frozen PyInstaller `luci.exe` (`luci/packaging/luci.spec`, used via `LUCI_EXE`). `npm run package:win` builds everything under `build/` (electron-builder output goes to `build/package/`), then `scripts/collect-release.cjs` copies only the setup and portable `.exe` files into `release/` (committed f6a4475). The `/api/luci/*` routes need the header `x-kairo-luci: 1`.
- [2026-11-24] UI redesign ("KAIRO — UI Redesign" spec) runs in stages, with a commit offered after each. Stage 1 (top bar, `k-*` colour tokens in `src/index.css` `@theme`) is done. Planned next: 2 folder sidebar + Create menu, 3 task rows/groups/detail drawer, 4 `#`/`+`/`@`/`!` suggestions + focus mode, 5 restyle remaining views. Verify UI work in the web app only (`npm run dev`, tests, tsc). Why: the user said to skip rebuilding the .exe (`npm run package:win`) for UI changes. Still waiting on user answers: what the task drawer shows (tasks are markdown lines with no status/attachments), when user-created Notes folders land (`Note.folder` is a fixed union), and where Tags go. Decided by the user: Calendar is a top-bar button, and Upcoming has a List/Calendar switch. The sidebar has no Daily Journal item and no per-document list; journals and documents live in All Notes. To Do filters by Status and by Project (with a project, no project, or one project).

## Agent setup
- Skills: `.claude/skills/memory-optimizer`, `.claude/skills/dream-manager`.
- Stop hook: `.claude/hooks/memory-check.cjs` — asks for memory-optimizer after tasks with 2+ tool errors or 20+ tool calls (env: `MEMORY_HOOK_MIN_ERRORS`, `MEMORY_HOOK_MIN_TOOLS`).
