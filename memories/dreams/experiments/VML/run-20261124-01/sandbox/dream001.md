## Nodes
- Bash tool halves \\ [issue] (verified)
- quoted-heredoc advice [fact] (rejected)
- '\' SyntaxError [issue] (verified)
- C:\ai invalid JSON [issue] (verified)
- byte-level probe [action] (verified)
- issues.md rule v2 [fact] (verified)
- Write file, run by path [action] (verified)
- inline-script guard [tool] (pending)
- 409-call corpus test [action] (verified)
- fewer retry loops [outcome] (hypothesis)
## Relations
- Bash tool halves \\ --causes--> '\' SyntaxError
- Bash tool halves \\ --causes--> C:\ai invalid JSON
- byte-level probe --evidence_for--> Bash tool halves \\
- Bash tool halves \\ --contradicts--> quoted-heredoc advice
- issues.md rule v2 --supersedes--> quoted-heredoc advice
- issues.md rule v2 --requires--> Write file, run by path
- Write file, run by path --fixes--> '\' SyntaxError
- Write file, run by path --fixes--> C:\ai invalid JSON
- 409-call corpus test --evidence_for--> inline-script guard
- Write file, run by path --causes--> fewer retry loops

## Facts
- L: Claude Code 2.1.329 / Windows Git Bash: a run of N backslashes becomes ceil(N/2) unless followed by '"', even in '...' and <<'EOF'. Verified 2026-11-23.
- Q: Old belief: quoted heredocs protect backslashes. Refuted by L.
- S: Corpus id 361: f.split('\\') arrived as f.split('\') -> SyntaxError.
- J: Corpus ids 55/376: printf fixture C:\\ai -> C:\ai -> invalid JSON (silent, exit 0).
- P: printf '%s' 'A\\B' | od -An -tx1 -> 41 5c 42 (one backslash).
- R: C:/ai/memories/categories/issues.md -> Shell & scripting, entry 1 (2026-11-22, corrected 2026-11-23).
- W: Write the script/fixture with the Write tool, then run it by path.
- H: Sandbox prototype, not deployed: dreams/experiments/DREAM-001/run-20261123-01/sandbox/inline-script-guard.cjs
- C: Recall 4/4, warnings on good calls 4.0% vs 23.1% naive; p95 150 ms.
- O: Expected benefit, not yet measured in the field.
## Refs
- report: C:/ai/memories/dreams/experiments/DREAM-001/run-20261123-01/report.md
- archive: C:/ai/memories/dreams/archive.md#DREAM-001
