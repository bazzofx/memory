# Global memory rules (always loaded)

Memory root: `C:\ai\memories\` (Git Bash: `/c/ai/memories/`), shared by all projects. Keep this file short — it is loaded into every session.

1. **Load on demand.** Don't read every memory file up front. Use `index.md` to pick the one file that matches the moment, and prefer `Grep` on a keyword over reading a whole file.
2. **On any non-trivial error:** grep `categories/issues.md` (and `limitations.md`) for the error text or tool before retrying. Don't rerun the same command unchanged or stack guesses.
3. **Before a large or long-horizon task:** check `categories/procedures.md` and `successes.md`, and the project file in `projects/`.
4. **Record only what's noteworthy** — non-obvious failures, hard-won fixes, validated workflows, lasting decisions, stated user preferences. Skip typos and routine work.
5. **Every memory change goes through the `memory-optimizer` skill:** check existing entries first; if the memory exists, edit it, otherwise add it; one entry lives in exactly one file.
6. **End of a noteworthy task/session:** run `memory-optimizer`'s end-of-task workflow — Phase A upserts memories, then Phase B checks `dreams/dreams.md` and turns issues, limitations or successes into new or updated dream proposals.
7. **Untested ideas** go to `dreams/` via the `dream-manager` skill, never into `categories/`.
8. Never store secrets, API keys, passwords or personal data in memory.
