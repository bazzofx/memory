# Project: kairo

Path: `C:\_web_apps_2025\kairo` (Git, branch `main`). Load when working in this project.

## Overview
- Web app: TypeScript + Vite (`vite.config.ts`, `src/`, `server.ts`), Vitest tests, Firebase (`firestore.rules`, `firebase-applet-config.json`).
- `luci/`: Python voice assistant "Luci" (voice commands, spoken replies with Piper, task assistant); has its own `requirements.txt` / `.venv`.

## Constraints & decisions
- [2026-11-22] Node scripts outside `src/` (e.g. `.claude/hooks/`) use `.cjs` with `require`. Why: package.json has `"type": "module"`, so a `.js` file with `require` would fail to load.
- [2026-11-22] User chose to work directly on `main` for the memory/skill setup (declined a feature branch).

## Agent setup
- Skills: `.claude/skills/memory-optimizer`, `.claude/skills/dream-manager`.
- Stop hook: `.claude/hooks/memory-check.cjs` — asks for memory-optimizer after tasks with 2+ tool errors or 20+ tool calls (env: `MEMORY_HOOK_MIN_ERRORS`, `MEMORY_HOOK_MIN_TOOLS`).
