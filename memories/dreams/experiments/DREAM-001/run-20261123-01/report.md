# Dream Realization Experiment Report

- **Dream ID / Run ID:** DREAM-001 / run-20261123-01 (plan: `plan.md`; previous Gate 1 run: `../run-20261122-01/report.md`)
- **Date, environment and tool versions:** 2026-11-23. Windows 10 Pro 19045, Git Bash, Claude Code 2.1.329 (desktop app), Node v22.23.2, Python 3.12.6. No network access and no new dependencies.
- **Authorized experimental scope:** Sandbox only, as the user asked in chat ("run experiments within the dream 01"). Nothing in `settings.json` or `.claude/hooks` was touched, and nothing was installed.

## Evidence that the issue persists after the existing fix
- **In the field:** still unknown. Since the rule was written (2026-11-22T22:41Z), none of the 25 Bash calls failed this way. The 2026-11-23 → 12-07 monitoring window has only just started.
- **New verified finding, which changes the dream:** the memory rule's mental model is incomplete. On this host, **the Bash tool collapses backslashes before Bash runs, even inside single quotes and quoted heredocs (`<<'EOF'`)**. Observed rule: a run of N backslashes becomes ceil(N/2), unless the next character is `"`, in which case it's left alone.
  - Byte-level proof: the transcript recorded `printf '%s' 'A\\B'` with two backslashes, but it output hex `41 5c 42`, which is one backslash. The same happened with `cat <<'EOF'`.
  - Real-tool confirmation: neg09 (valid JSON `C:\\ai\\memories` written through a quoted heredoc) failed with `Invalid \escape` when sent through the Bash tool. The same file run with `bash file.sh` succeeded.
  - This explains the original `'\\'` → `'\'` SyntaxError (corpus id 361, which used a *quoted* heredoc) and the `C:\\ai` → invalid JSON incident (ids 55 and 376, `printf '...'` into `t4.jsonl`).
  - Where in the stack the collapse happens isn't known (tool transport or shell wrapper). This is a hypothesis about cause, not a verified fact.

## Baseline reproduction
- **Fixtures:** 22 case files (`sandbox/cases/*.sh`, written verbatim with the Write tool, each with a SHA-256 prefix in `results-rev3.txt`) and a corpus of 409 Bash calls from the kairo transcripts. The corpus has 11 errored calls and SHA-256 prefix `11e55f0d68ad2753`. It's kept in the session scratchpad only: the auto-mode classifier blocked copying transcript data into the memory folder, so it isn't archived here.
- **Positive labels (real failures caused by quoting/escaping):** ids 102, 176, 244, 361. ids 144 (bad JSON data) and 282 (PowerShell argument bug) errored for other reasons and were excluded.
- **Mechanism, plain `bash file.sh`:** all 8 `pos*` cases broke. Two of them failed *silently* with exit 0: pos07 lost its output to `${a}` expansion, and pos08 returned a wrong result from `$(x)` substitution. All `neg*` and `edge*` cases worked.
- **Mechanism, with the simulated tool layer (`sandbox/layer-sim.cjs`):** neg01, neg09 and edge03 *break*, and neg02 and edge02 silently *change output*. The ground truth was relabelled to match.
- **Baseline detectors:**
  - No hook: recall 0/4.
  - The dream's original broad trigger: recall 4/4, but it warns on **93 of 403 calls that didn't fail (23.1%)**.

## Candidate version and diff
`sandbox/inline-script-guard.cjs`, revision 3, SHA-256 prefix `54af35339e18718b`. It's a PreToolUse hook for Bash.
- It reads stdin JSON and scans `tool_input.command` with a quote-aware scanner that never runs the command.
- It models the tool's backslash layer, then Bash's own backslash processing, then checks what the target program will receive.
- Reasons it can report:
  - `tool-collapse`: code-bound text contains `\\` that the tool will collapse.
  - `substitution`: `${`, `$(` or a backtick inside a double-quoted or unquoted body.
  - `backslash-collapse`: Bash's own collapse of `\\`.
  - `lone-backslash-literal`: a `'\'` string literal, which is always a syntax error.
  - `invalid-json-escape`: an invalid escape in JSON written to a `.json`/`.jsonl` file.
- "Code-bound" means one of: stdin to python/node, a `-c`/`-e` argument, `echo`/`printf` redirected to a code file, or a heredoc to a `.json/.js/.py/...` file.
- It fails open: malformed input, a non-Bash tool, an internal error or no findings all give empty output and exit 0. It never sets `permissionDecision`.

Revision history:
- **Revision 1:** a long-script rule (> 25 lines) gave a 7.2% false-warning rate, and it missed id 361.
- **Revision 2:** added the tool-layer model and removed long-script warnings. Line counts of the failures (27, 41) overlapped with successes (28–128).
- **Revision 3:** context cut at `;`/`&&`/`||`. Revision 2 had already reached the corpus metrics.

## Comparison results (revision 3, `results-rev3.txt`)
| Metric | Threshold | No hook | Broad trigger | Candidate |
|---|---|---|---|---|
| Synthetic + robustness cases | 100% | — | — | **28/28 pass** |
| Recall on labelled corpus failures | ≥ 90% | 0/4 | 4/4 | **4/4** |
| Warnings on corpus calls that didn't error | ≤ 5% | 0% | 23.1% | **4.0% (16/403)** |
| Hook runtime p95 (incl. Node startup) | ≤ 150 ms | — | — | 150 ms (max 445 ms) |
| Crashes / non-zero exits | 0 | — | — | 0 |

Two of the 16 warnings (ids 55 and 376) are **true silent failures**. Their `printf '{"file_path":"C:\\ai\\..."}' > t4.jsonl` fixture becomes invalid JSON through the verified layer. That leaves **14/403 (3.5%)** warnings on calls that genuinely worked. Most of them are `python - <<'EOF'` patch scripts containing `\\` inside nested strings. Some of those may have silently written different bytes than intended, but that wasn't verified.

The no-tool-layer mode (`INLINE_GUARD_NO_TOOL_LAYER=1`, for other hosts) also passed all of its synthetic and robustness cases (p95 132 ms).

## Threshold evaluation
All the predeclared thresholds are met. Runtime is right at the limit (p95 150 ms), and Node startup on Windows is most of that.

## Security and regressions
- The hook never executes command text and makes no network calls.
- The corpus was redacted with a secret regex (0 hits).
- The hook can't block a call, because it fails open and adds context only.
- Not verified: whether `hookSpecificOutput.additionalContext` for PreToolUse reaches the model in Claude Code 2.1.329. The prototype also emits `systemMessage`, which is shown to the user. This has to be checked in a canary before anyone relies on it.

## Limitations, uncertainty and deviations
- The corpus comes from one project over about one day (409 calls). The 1-false-warning-per-day field target can't be proven from it.
- The positive labels are my own judgement (4 real cases), so recall has a very wide confidence interval.
- The tool-layer rule is empirical and specific to this host. A Claude Code update could change or fix it. The `NO_TOOL_LAYER` switch exists for that reason.
- Deviation from the plan: the corpus was limited to kairo transcripts and kept in the scratchpad, because the classifier blocked the copy. Ground truth was revised after discovering the tool layer, before revision 2 was evaluated.
- Field recurrence after the memory rule is still unconfirmed.

## Conclusion
**passed**, for the sandbox experiment only. Synthetic success doesn't prove that a live recurrence is happening.

## Next action
- **Revise memory now:** the `issues.md` rule should say that quoted heredocs and single quotes don't protect backslashes in this Bash tool, so they must be written with the Write tool.
- **Keep the field monitor running** until 2026-12-07.
- **Ask for project-local canary approval** only if the user wants it. That would mean `kairo/.claude/settings.json` PreToolUse matcher `Bash` → `node .claude/hooks/inline-script-guard.cjs`, with a backup and the existing hooks preserved. Deployment is **not authorized** by this run.

## Artifact paths
`plan.md`, `report.md`, `sandbox/{inline-script-guard.cjs, run-tests.cjs, layer-sim.cjs, results-rev3.txt, cases/}`

## Memory updates proposed
One correction to `categories/issues.md` → Shell & scripting, entry 1 (now I-001): add the tool-layer backslash collapse (verified 2026-11-23, Claude Code 2.1.329, Windows).

## Reviewed/approved by
Pending user review.
