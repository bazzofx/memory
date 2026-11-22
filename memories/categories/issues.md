# Issues — previous errors, root causes and fixes

Load when: a command, edit, build or test fails (grep for the error text or tool first), or before a risky step in one of the topics below.
Format: `- [YYYY-MM-DD] <rule>. Why: <root cause / what went wrong>.` Newest first within each topic; add a `##` topic only when none fits.

## Shell & scripting (Windows + Git Bash)
- [2026-11-22] Never write Python/JS — or JSON/test fixtures — containing backslashes, `${...}` or nested quotes inline in Bash heredocs, `printf`/`echo` or `python -c`. Write the file with the Write tool, then run/use it. Why (seen repeatedly): `'\\'` arrived as `'\'` (SyntaxError); a fixture's `C:\\ai` became `C:\ai` (invalid JSON); a template literal `${esc(k)}` broke bash command substitution; a big inline `s.replace(...)` script failed on line 25.
- [2026-11-22] Build paths with `os.path` / `pathlib` or `.replace(chr(92), '/')`, never hard-coded `'\\'` splits. When passing a path from Git Bash to Windows node/python, convert it with `cygpath -m` (`/c/Users/…` → `C:/Users/…`). Why: hard-coded split hit a SyntaxError; node's `existsSync('/c/…')` returned false, so a hook test looked like it silently did nothing.
- [2026-11-22] Don't hand-edit JSON via string replace; load → modify → `json.dump`. Then validate with `python -m json.tool file.json`. Why: a manual edit left a missing comma ("Expected ',' or ']' … line 132").
- [2026-11-22] `mv`/rename of a folder can fail with "Device or resource busy" on Windows when a process or the app has it open. Close/stop whatever uses it, or copy then delete, and check the result before continuing. Why: skill folder rename failed and later steps read a path that didn't exist.
- [2026-11-22] `ls` on several paths exits 2 if any one is missing — that's not a real failure; use `ls … 2>/dev/null` or test with `[ -e path ]`.
- [2026-11-22] Check the working directory before relative paths ("File does not exist. Note: your current working directory is …"). Prefer absolute paths.

## Editing files
- [2026-11-22] Re-Read a file right before Edit/Write if anything (user, linter, a script I ran, a shell `mv`/`cp`) may have touched or moved it, and copy `old_string` from that fresh Read, not from memory. Why: "File has been modified since read", "String to replace not found", and "File has not been read yet" after moving files with `mv`.

## Python environments & secrets
- [2026-11-22] Run project scripts with the project's own interpreter/venv (check for `.venv`, `venv`, `requirements.txt`) before assuming a package is missing. Why: an upload script crashed importing `googleapiclient` under the wrong Python.
- [2026-11-22] If a script needs an env var (API key), check it exists first (`[ -n "$VAR" ]`) and ask the user — never invent or hard-code a key. Why: OPENROUTER_API_KEY / apiZenWarriorOpenRouter were unset; scripts exited.

## Built-in browser & terminal tools
- [2026-11-22] Call `read_page` or `find` before clicking by `ref`. Why: "ref map not initialized".
- [2026-11-22] Long-running servers go in `run_in_background` (or launch.json + preview_start), not `run_in_terminal` typed lines that may be read as unfinished.

## Testing
- [2026-11-22] When a test script prints all cases and exits 1, find *which* case failed (print only failures + expected vs got) before changing code.
