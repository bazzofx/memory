# Dreams — Agent Improvement Proposals

Dreams are optional improvement proposals, not instructions or permissions. Review existing entries before adding new ones; merge related ideas. Present at most three relevant pending dreams at a session boundary or when requested.

Location: `C:\ai\memories\dreams\dreams.md` (central, shared by all projects; archive in `C:\ai\memories\dreams\archive.md`). Set each dream's `Scope` to the project name (e.g. `kairo`) or `cross-project`.

## Pending

### DREAM-001 — Warn before inline scripts that Bash will mangle
- Category: Quality
- Status: Proposed
- Origin: Observed
- Evidence: `categories/issues.md` — Shell & scripting: inline-script quoting (backslashes / `${}` mangled in heredoc, printf, `python -c`), seen 4× across kairo and memory setup
- Trigger: A Bash tool call contains a heredoc, `printf`/`echo` or `python -c`/`node -e` with backslashes or `${`
- Proposal: A PreToolUse hook on Bash that detects those patterns and returns a warning suggesting the Write tool + run-by-path instead (warn, not block)
- Benefit: Estimated — fewer SyntaxError / invalid-JSON retries; untested
- Validation: Count matching `is_error` results in transcripts for 2 weeks before vs after; check false-positive warnings
- Impact / Effort / Risk: Medium / Low / Low (estimates)
- Scope: cross-project
- Date: 2026-11-22

### DREAM-002 — Reusable script for mining transcript errors
- Category: Automation
- Status: Proposed
- Origin: Observed
- Evidence: `categories/procedures.md` — "Refresh memory from past sessions" was done with a one-off script written by hand, which itself first failed on a backslash
- Trigger: Refreshing memory or running a periodic memory review
- Proposal: Save the scanner as `C:\ai\memories\tools\mine-errors.py` (args: project filter, since-date) and point the procedure at it
- Benefit: Estimated — refresh in one command instead of rewriting the script; untested
- Validation: Run on current transcripts; output matches the manual pass and finishes in under a minute
- Impact / Effort / Risk: Low / Low / Low (estimates)
- Scope: cross-project
- Date: 2026-11-22

## Approved Experiments

## Ready for Approval

## Implemented

## Deferred or Rejected
