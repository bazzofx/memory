# Toolbox — reusable scripts referenced by memory

Scripts that a memory entry points to live here, so they survive the session scratchpad being cleared. One file per script; keep each one self-contained, with a usage docstring at the top.

Rules:
- Save a script here when a memory entry (`S-`, `PR-`, `R-`, …) relies on it, or when you wrote one that is likely to be needed again. Reference it from the entry (`C:\ai\toolbox\<file>`), and list it below.
- Write scripts with the Write tool, never inline through Bash (I-001). Run Python with `python -I`.
- No secrets, API keys or personal data in scripts; read keys from env vars (I-016).
- Only keep a script after it has run successfully at least once; note when it was validated.

| Script | What it does | Memory | Validated |
| --- | --- | --- | --- |
| `memory_topics.py` | Rebuilds the Topics table in `memories/index.md` (`--write`), checks entry IDs, prefixes, tags and ID references, and prints the next free ID per prefix | `index.md` → Entry format, D-001 | 2026-11-25: passed on the real memory (57 entries); caught 4/4 planted errors in a copy |

Wanted (lost with their session scratchpads; save them here next time they're written, see T-007):
- CDP driver for a packaged Electron app (S-001).
- Transcript error scanner (PR-001).
