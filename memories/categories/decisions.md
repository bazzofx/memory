# Decisions — important decisions and their reasoning (cross-project)

Load when: changing shared tooling, the memory layout or conventions. Project-only decisions go in `projects/<name>.md`.
Format: `- [YYYY-MM-DD] <decision>. Why: <constraint or rationale>.` Newest first.

- [2026-11-22] Agent memory is central at `C:\ai\memories\` with the layout `global.md`, `index.md`, `categories/`, `projects/`, `dreams/`. Projects reference it from their CLAUDE.md; no project-local memory folders. Only `global.md` is always loaded; other files are loaded on demand via `index.md`. Why: user wants one memory shared by kairo and other projects, loading only the relevant file to keep context small.
