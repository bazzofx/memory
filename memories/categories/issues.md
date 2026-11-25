# Issues — previous errors, root causes and fixes

Load when: a command, edit, build or test fails (grep the error text, tool name or `#tag` first), or before a risky step in one of the topics below.
Format (see `index.md` → Entry format): `- **I-NNN** [YYYY-MM-DD] #tags — <rule, one line>` then indented `Why:` / `Evidence:` sub-bullets. IDs are permanent and never reused; the next free ID is in `index.md`. Add a `##` topic only when none fits.

## Shell & scripting (Windows + Git Bash)
- **I-001** [2026-11-22] #shell #claude-code #windows #json — Never pass code, JSON or fixtures containing backslashes, `${...}` or nested quotes inline through Bash (heredocs, `printf`/`echo`, `python -c`/`node -e`); write the file with the Write tool and run or use it by path.
  - Cause (verified on Claude Code 2.1.329, Windows/Git Bash, 2026-11-23): the Bash tool collapses each run of N backslashes to ceil(N/2) before bash runs, unless the next char is `"`, **even inside `'…'` and quoted heredocs (`<<'EOF'`)**. So `'A\\B'` arrives as `A\B`. Bash then applies its own `${`/`$(`/backtick/`\\` processing in double quotes and unquoted heredocs.
  - Why (seen repeatedly): `'\\'` arrived as `'\'` in a `<<'EOF'` heredoc (SyntaxError); a fixture's `C:\\ai` became `C:\ai` (invalid JSON, sometimes silently with exit 0); a template literal `${esc(k)}` broke bash command substitution; a big inline `s.replace(...)` script failed on line 25; inline Python edits silently wrote control characters, because `"\\b"` / `"\\v"` became backspace / vertical tab (a regex `\b` stopped matching; a doc path became `\Luci<VT>oices`; 2026-11-22/24).
  - Check: after any inline edit that touched backslashes, run `grep -c $'\x08'` / `$'\x0b'` on the file.
  - Evidence: `dreams/experiments/DREAM-001/run-20261123-01/report.md`; realized as DREAM-001 (`subconscious/DREAM-001-bash-tool-backslash-layer.md`). Related: S-005, S-006.
- **I-002** [2026-11-24] #powershell #windows — With `powershell -Command "<script>"`, anything after the script is appended to the script text, not passed as `$args`; put validated numbers into the script and send untrusted text on stdin (`[Console]::In.ReadToEnd()`).
  - Why: the Windows TTS fallback silently said nothing ("Unexpected token '0'"), because stderr went to DEVNULL.
- **I-003** [2026-11-22] #shell #windows #python — Build paths with `os.path` / `pathlib` or `.replace(chr(92), '/')`, never hard-coded `'\\'` splits; convert Git Bash paths for Windows node/python with `cygpath -m` (`/c/Users/…` → `C:/Users/…`).
  - Why: a hard-coded split hit a SyntaxError; node's `existsSync('/c/…')` returned false, so a hook test looked like it silently did nothing.
- **I-004** [2026-11-22] #json — Don't hand-edit JSON via string replace; load → modify → `json.dump`, then validate with `python -m json.tool file.json`.
  - Why: a manual edit left a missing comma ("Expected ',' or ']' … line 132").
- **I-005** [2026-11-22] #shell #windows — `mv`/rename/`rm -rf` (or a tool's rmtree) of a folder fails with "Device or resource busy" / WinError 32 when a process, the app **or the Bash tool's own cwd** is inside it; `cd` out, stop whatever uses it (or copy then delete), and check the result before continuing.
  - Why: a skill folder rename failed and later steps read a path that didn't exist; a PyInstaller rebuild couldn't clear `build/luci-dist/.../_internal` because a previous `cd` left the shell there (2026-11-24).
- **I-006** [2026-11-25] #shell #windows — Don't parse `grep -rn` output by splitting on `:`: absolute Windows paths start with a drive letter (`C:/…:12:text`), so `split(':', 1)` yields `C`; search inside the script, or grep relative paths / use `grep -l`.
  - Why: a memory-layout test reported 0/24 hits with exit 0 until grep was replaced with a Python search.
- **I-007** [2026-11-22] #shell — `ls` on several paths exits 2 if any one is missing; that's not a real failure. Use `ls … 2>/dev/null` or `[ -e path ]`.
- **I-008** [2026-11-22] #shell #claude-code — Check the working directory before using relative paths and prefer absolute ones.
  - Why: "File does not exist. Note: your current working directory is …".

## Editing files
- **I-009** [2026-11-22] #claude-code — Use the Read tool on a file (at least the target lines, `offset`/`limit` is enough) right before Edit/Write, and copy `old_string` from that fresh Read; viewing it with Bash (`cat`, `sed -n`, `grep`) does **not** count.
  - Also re-Read when anything (user, linter, a script, a shell `mv`/`cp`) may have touched or moved the file. Or make the change through Bash instead.
  - Why: "File has been modified since read", "String to replace not found", and "File has not been read yet" after moving files with `mv`; on 2026-11-25 two parallel Edits failed after `sed -n` views.
- **I-022** [2026-11-25] #claude-code #windows — Overwriting an existing file with the Write tool keeps its original encoding (e.g. UTF-16 LE), so check `file <path>` afterwards and re-encode if needed: read as `utf-16`, write as `utf-8`.
  - Why: `C:\ai\README.md` stayed UTF-16 after a full rewrite with Write; only `file` showed it.
- **I-023** [2026-11-25] #python #windows — `Path.write_text()` / `open(..., 'w')` on Windows turn `\n` into `\r\n`; pass `newline="\n"` when a generated file must stay LF.
  - Why: `toolbox/memory_topics.py --write` turned `index.md` into CRLF until `newline="\n"` was added.

## Python environments & secrets
- **I-010** [2026-11-22] #python — Run project scripts with the project's own interpreter/venv (check for `.venv`, `venv`, `requirements.txt`) before assuming a package is missing.
  - Why: an upload script crashed importing `googleapiclient` under the wrong Python.
- **I-011** [2026-11-24] #python #gpu — Don't let pip install torch into a new venv for GPU work; it pulls a CPU-only build. Reuse the system CUDA torch with `uv venv --system-site-packages` (see E-001 for the versions).
  - Why: ZenWarriorSounds' local SDXL venv (`C:\Users\joker\localimage\.venv`) only works on the GPU because it reuses system torch 2.8+cu128. Related: S-003.
- **I-012** [2026-11-24] #python #windows — While one thread blocks reading a **stdin pipe** (Node `spawn(..., {stdio: 'pipe'})`, `tail -f file | python`), another thread importing a compiled extension (numpy, onnxruntime, ctranslate2/faster-whisper) can hang forever; import those on the main thread before starting the stdin reader or background loaders.
  - Why: Luci's voice stayed "loading" forever only with piped stdin. `python -X faulthandler` showed the thread stuck in numpy's `create_module`; a 0.6 s main-thread preload fixed it.
- **I-013** [2026-11-24] #python #gpu #tts — `transformers` "Could not import module 'X'" hides the real error: import the submodule directly (e.g. `import transformers.models.albert.modeling_albert`). "operator torchvision::nms does not exist" means torchvision doesn't match torch.
  - Fix for torch 2.8: `torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128 --no-deps`.
  - Why: Kokoro TTS failed to load because torchvision 0.20.1 sat next to torch 2.8.
- **I-014** [2026-11-24] #python #packaging — Before documenting an install, check that `requirements.txt` lists every non-stdlib import.
  - Why: Luci's file had `faster-whisper` and `pynput` commented out while the code imported them, so a fresh install would have had no mic or hotkey.
- **I-015** [2026-11-24] #python #packaging — PyInstaller: don't `collect_all()` big packages (onnxruntime, ctranslate2, faster_whisper) from a crowded/global Python; use `collect_data_files` + `collect_dynamic_libs` and `excludes` (numba/llvmlite, pandas, scipy, PIL, sqlalchemy, fsspec, torch).
  - Check `du -sh _internal/*` after building. A frozen exe ignores `python -u`, so add `[("u", None, "OPTION")]` as EXE's options when a parent reads its piped output.
  - Why: Luci's bundle went 440 → 313 MB (llvmlite alone was 115 MB), and Kairo's Luci log view stayed empty until the unbuffered option was added.
- **I-016** [2026-11-22] #secrets #shell — If a script needs an env var (API key), check it exists first (`[ -n "$VAR" ]`) and ask the user; never invent or hard-code a key.
  - Why: `OPENROUTER_API_KEY` / `apiZenWarriorOpenRouter` were unset and scripts exited.

## Built-in browser & terminal tools
- **I-017** [2026-11-22] #browser — Call `read_page` or `find` before clicking by `ref`.
  - Why: "ref map not initialized".
- **I-018** [2026-11-22] #claude-code — Long-running servers go in `run_in_background` (or launch.json + `preview_start`), not typed `run_in_terminal` lines that may be read as unfinished.

## UI & CSS
- **I-019** [2026-11-24] #ui — Stray page scrollbars can come from an absolutely positioned element (e.g. a Tailwind `sr-only` table) with no positioned ancestor; put `relative` on its wrapper.
  - Diagnose with JS: compare `document.documentElement.scrollHeight` with `innerHeight`, then check `el.offsetParent` of absolute elements.
  - Why: a chart's `sr-only` table was placed against `<body>` and made the document taller than the viewport.

## Testing
- **I-020** [2026-11-24] #testing #shell — A CLI that reads stdin exits at once when backgrounded (`exe &` / `( … &)`) from the Bash tool, because stdin is at EOF, so an empty log looks like a crash; test it in the foreground with piped stdin: `(sleep 30; echo ":quit") | timeout 60 app.exe …`.
  - Why: two silent "failed" runs of the frozen `luci.exe serve` were really clean EOF exits.
- **I-021** [2026-11-22] #testing — When a test script prints all cases and exits 1, find *which* case failed (print only failures with expected vs got) before changing code.
