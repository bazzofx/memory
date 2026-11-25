# Dreams — Agent Improvement Proposals

Dreams are optional improvement proposals, not instructions or permissions. Review existing entries before adding new ones; merge related ideas. Present at most three relevant pending dreams at a session boundary or when requested.

Location: `C:\ai\memories\dreams\dreams.md` (central, shared by all projects; archive in `C:\ai\memories\dreams\archive.md`). Set each dream's `Scope` to the project name (e.g. `kairo`) or `cross-project`.

## Pending

### DREAM-001 — Warn before inline scripts that Bash will mangle
- Status: Proposed (resurfaced 2026-11-24 from `archive.md`; it was archived 2026-11-23 as resolved_by_memory, provisional)
- Origin: Observed. Scope: cross-project. Dated 2026-11-22.
- Why it resurfaced: the archive condition ("any Bash call after 2026-11-23 … silently writes broken output") was met. The memory rule existed and was still broken: in the Kairo voice session, inline `python - <<'PYEOF'` edits wrote control characters without any error:
  - `"\\v"` became a vertical tab in `README.md`, `luci/requirements.txt` and `docs/luci-voice-plan.md` (`%LOCALAPPDATA%\Luci<VT>oices`)
  - `"\\b"` became a backspace in `luci/luci/nlu/rules.py`, so a word-boundary regex silently stopped matching
  - A Python `SyntaxError` from a `'that's'` quote.

  Each was caught only by later checks or tests. Evidence: `categories/issues.md` → Shell & scripting, entry 1 (2026-11-24 addition).
- Proposal: deploy the already-tested sandbox hook (`dreams/experiments/DREAM-001/run-20261123-01/sandbox/inline-script-guard.cjs`) as a **project-local canary** PreToolUse warning in kairo. It must not block anything. Also consider a cheap PostToolUse check that flags new `\x08` / `\x0b` bytes in files touched by a Bash call.
- Success measure: across 2 weeks, zero silent control-character writes or backslash-mangling failures, with at most 5% warnings on Bash calls that would have worked (the sandbox measured 4%).
- Needs: separate user approval before anything is installed (dream-realizer).
- Reusable artifacts: `dreams/experiments/DREAM-001/run-20261123-01/sandbox/`, plus the reports for `run-20261122-01` and `run-20261123-01`.

## Approved Experiments

## Ready for Approval

## Implemented

## Deferred or Rejected

### DREAM-002 — Reusable script for mining transcript errors
- Status: Rejected (2026-11-22)
- Reason: Below the policy bar. It happened once, there's no recurring failure or bottleneck, and `procedures.md` → "Refresh memory from past sessions" already covers it. The backslash failure cited as evidence belongs to DREAM-001 (archived; see `archive.md`).
- Resurface only if: memory refreshes become periodic (for example monthly) and rewriting the scanner takes real time or fails again.
