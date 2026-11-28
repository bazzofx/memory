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

  Each was caught only by later checks or tests. Evidence: I-001 in `categories/issues.md` (2026-11-24 addition).
- New evidence 2026-11-25 (BalticIntel): despite I-001 being loaded, two more inline `python - <<'EOF'` edits carried regex backslashes (`r"\\s*,\\s*"`), each giving `SyntaxWarning: invalid escape sequence '\s'`. The output happened to be correct only because the run had one backslash. The agent then switched to Write-tool scripts for the rest of the session. This supports the canary warning hook.
- New evidence 2026-11-26 (AutoJobSearch): two heredoc patch scripts again turned `"\\n"` into real newlines (SyntaxError in 2 files), with I-001 and the realized-dream line in `global.md` both loaded. Memory alone is not preventing it, which strengthens the case for the warning hook. Evidence: I-001.
- New evidence 2026-11-25 (CVE_Intel): two more failures despite I-001 being loaded: an inline `python - <<'EOF'` with `\\d` regexes ended in "unexpected EOF", and a `sed` with `\\n` silently changed nothing (exit 1). Both were redone with Write-tool scripts / Edit. A canary warning would have caught both before they ran. Evidence: I-001.
- Proposal: deploy the already-tested sandbox hook (`dreams/experiments/DREAM-001/run-20261123-01/sandbox/inline-script-guard.cjs`) as a **project-local canary** PreToolUse warning in kairo. It must not block anything. Also consider a cheap PostToolUse check that flags new `\x08` / `\x0b` bytes in files touched by a Bash call.
- Success measure: across 2 weeks, zero silent control-character writes or backslash-mangling failures, with at most 5% warnings on Bash calls that would have worked (the sandbox measured 4%).
- Needs: separate user approval before anything is installed (dream-realizer).
- Reusable artifacts: `dreams/experiments/DREAM-001/run-20261123-01/sandbox/`, plus the reports for `run-20261122-01` and `run-20261123-01`.
- Subconscious: `subconscious/DREAM-001-bash-tool-backslash-layer.md` (+ `.png`) covers the verified discovery and correct way from the sandbox run. Rebuild it if the deployment is validated.

### DREAM-004 — Toolbox helper to register any project for preview_start
- Status: Proposed
- Origin: Observed. Scope: cross-project (built-in browser previews). Dated 2026-11-25.
- Evidence: L-006, hit in 3 sessions on 2026-11-25 (BalticIntel, Traffic Lens, CVE_Intel). Each lost several tool calls finding that `preview_start` reads only the original dir's launch.json and that busy ports get reassigned. Recurred 2026-11-26 (AutoJobSearch mock form): wrote the project's own `.claude/launch.json` first, `preview_start` failed with "No server named … found", then worked from `C:\ai\.claude\launch.json`. L-006 was in memory but not looked up before the first try.
- Proposal: `C:\ai\toolbox\preview_entry.py <name> <project_dir> <module|cmd>`: picks a free port (netstat), upserts an entry with `"autoPort": false` into the session's original `.claude\launch.json` (runpy/sys.path form for Python modules), and prints the port. Proposal only; nothing installed.
- Success measure: the next 3 sessions that preview an added-directory project reach a rendered page on the first `preview_start` call.

### DREAM-003 — Load cached local image models offline by default
- Status: Proposed
- Origin: Observed. Scope: ZenWarriorSounds (`_tools/local_image.py`), pattern reusable for any local HF pipeline. Dated 2026-11-25.
- Evidence: I-030. An unattended scheduled short run hung 10+ min on the Hub check until it was rerun with `HF_HUB_OFFLINE=1`.
- Proposal: in `run_local()` set `HF_HUB_OFFLINE=1` in the child env when the model folder exists in the HF cache, and fall back to online only if the offline load raises. Optionally add a watchdog that aborts if there is no progress for N minutes.
- New evidence 2026-11-26: the scheduled short hung again for about 20 min (I-030). On the rerun, `generate.py` hit the I-031 None-content crash again. Both memory rules existed but were applied only after each failure. Proposed extension: in the same change, guard None content in `generate.py` and pin a concrete default model. Optionally also add `HF_HUB_OFFLINE=1` / `--model` to the `zenwarrior-daily-short` scheduled-task prompt as a stopgap. A "Harden short-create" task chip was suggested to the user.
- Evidence 2026-11-26 (2nd run): I-031 None-content crash recurred on the first `make_short.py` call (3rd occurrence); `--model openai/gpt-6-luna` fixed it at once. No HF hang this run. Stopgap `--model` in the scheduled-task prompt would have saved one failed run.
- Evidence 2026-11-27: HF hang recurred (3rd time, ~10 min lost, I-030) in the scheduled run; also the prompt's inline YuE2 start command failed under Git Bash (I-040). Stopgap for the `zenwarrior-daily-short` prompt now covers three things: `HF_HUB_OFFLINE=1`, `--model openai/gpt-6-luna`, and starting YuE2 via a `.ps1` with `-File`. Recommended to the user in the run report.
- Success measure: the next 10 scheduled shorts finish the poster step with no hang; the load stays at about 3 s.
- Needs: user approval (dream-realizer) before code changes.

## Approved Experiments

## Ready for Approval

## Implemented

## Deferred or Rejected

### DREAM-002 — Reusable script for mining transcript errors
- Status: Rejected (2026-11-22)
- Reason: Below the policy bar. It happened once, there's no recurring failure or bottleneck, and PR-001 in `procedures.md` ("Refresh memory from past sessions") already covers it. The backslash failure cited as evidence belongs to DREAM-001 (archived; see `archive.md`).
- Resurface only if: memory refreshes become periodic (for example monthly) and rewriting the scanner takes real time or fails again.
