# Memory index

Root: `C:\ai\memories\`. Read this, then load only the file you need.

| File | Holds | Load when |
| --- | --- | --- |
| `global.md` | Essential rules | Always (imported by each project's CLAUDE.md) |
| `categories/issues.md` | Past errors, root causes, fixes | A command/edit/build/test fails — grep the error text; before a risky step in a listed topic |
| `categories/successes.md` | What worked well and should be repeated | Choosing an approach for something that was hard before |
| `categories/decisions.md` | Cross-project decisions and their reasoning | Changing shared tooling, memory layout or conventions |
| `categories/preferences.md` | User preferences, conventions, working style | Writing anything user-facing, committing, choosing how to work |
| `categories/environments.md` | OS, shells, tools, versions, config, dependencies | Running commands, installing, debugging "works elsewhere" problems |
| `categories/procedures.md` | Validated, reusable step-by-step workflows | Starting a task type that has a procedure listed |
| `categories/limitations.md` | Known constraints of tools/platforms + workarounds | A tool behaves unexpectedly; before using a tool with a listed limit |
| `categories/pending.md` | Unresolved tasks and follow-ups | Session start, task end, or "what's left?" |
| `projects/<name>.md` | Project goals, architecture, tech, constraints, project-only decisions | Working in that project (e.g. `projects/kairo.md`) |
| `dreams/dreams.md` | Improvement proposals, experiments, approvals, implemented capabilities | Session review, or when asked about dreams (`dream-manager` skill) |
| `dreams/archive.md` | Closed dreams with resolution and "resurface if" conditions | Before proposing a dream (avoid reviving a closed one), or when a matching failure recurs |
| `dreams/experiments/<DREAM-ID>/<run-id>/` | Experiment plans, reports and sandbox prototypes | Realizing, resuming or reviewing a dream (`dream-realizer` skill) |

Placement rules:
- Project-only knowledge goes in `projects/<name>.md`, not tagged into a category file.
- An error + its fix → `issues.md`. A reusable multi-step workflow → `procedures.md`. A tool limit you can't fix, only work around → `limitations.md`.
- A pending item that gets done is deleted (lasting lesson → the right category).
