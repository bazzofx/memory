# Issues — previous errors, root causes and fixes

Load when: a command, edit, build or test fails (grep the error text, tool name or `#tag` first), or before a risky step in one of the topics below.
Format (see `index.md` → Entry format): `- **I-NNN** [YYYY-MM-DD] #tags — <rule, one line>` then indented `Why:` / `Evidence:` sub-bullets. IDs are permanent and never reused; the next free ID is in `index.md`. Add a `##` topic only when none fits.

## Shell & scripting (Windows + Git Bash)
- **I-040** [2026-11-27] #shell #powershell #windows — From Bash, `powershell -Command "...$env:X..."` fails: Bash expands `$env` inside the double quotes, so PowerShell gets `:X\...`. Write a `.ps1` (Write tool) and run `powershell -NoProfile -ExecutionPolicy Bypass -File <path>`.
  - Why: the YuE2 Studio start command (R-001) failed with "Start-Process ... cannot find the file specified" on `":LOCALAPPDATA\YuE2 Studio\..."` in an unattended scheduled run (ZenWarriorSounds, 2026-11-27); the `.ps1` + `-File` route worked at once. Related: I-001, I-002.
- **I-001** [2026-11-22] #shell #claude-code #windows #json — Never pass code, JSON or fixtures containing backslashes, `${...}` or nested quotes inline through Bash (heredocs, `printf`/`echo`, `python -c`/`node -e`); write the file with the Write tool and run or use it by path.
  - Cause (verified on Claude Code 2.1.329, Windows/Git Bash, 2026-11-23): the Bash tool collapses each run of N backslashes to ceil(N/2) before bash runs, unless the next char is `"`, **even inside `'…'` and quoted heredocs (`<<'EOF'`)**. So `'A\\B'` arrives as `A\B`. Bash then applies its own `${`/`$(`/backtick/`\\` processing in double quotes and unquoted heredocs.
  - Why (seen repeatedly): `'\\'` arrived as `'\'` in a `<<'EOF'` heredoc (SyntaxError); a fixture's `C:\\ai` became `C:\ai` (invalid JSON, sometimes silently with exit 0); a template literal `${esc(k)}` broke bash command substitution; a big inline `s.replace(...)` script failed on line 25; inline Python edits silently wrote control characters, because `"\\b"` / `"\\v"` became backspace / vertical tab (a regex `\b` stopped matching; a doc path became `\Luci<VT>oices`; 2026-11-22/24).
  - Check: after any inline edit that touched backslashes, run `grep -c $'\x08'` / `$'\x0b'` on the file.
  - 2026-11-25 (CVE_Intel): an inline `python - <<'EOF'` edit with regex `\\d` broke with "unexpected EOF"; a `sed` pattern with `\\n` silently matched nothing (exit 1, file unchanged). Write-tool scripts and Edit worked first time.
  - 2026-11-26 (AutoJobSearch): two `cat > x.py <<'EOF'` patch scripts that wrote Python string literals containing `"\\n"` put real line breaks into `cli.py`/`drafter.py` (SyntaxError: unterminated string literal). Fixed with Edit; the next patch, written with the Write tool, worked first time. Any patch script whose *replacement text* contains `\n` counts.
  - Evidence: `dreams/experiments/DREAM-001/run-20261123-01/report.md`; realized as DREAM-001 (`subconscious/DREAM-001-bash-tool-backslash-layer.md`). Related: S-005, S-006.
- **I-033** [2026-11-25] #python #shell — Never name a scratch script after a stdlib module (`inspect.py`, `json.py`, `types.py`): Python puts the script's folder first on `sys.path`, so any later script run from that folder imports it instead (e.g. `dataclasses` → `import inspect` ran the scratch file and crashed).
  - Why: `scratchpad/inspect.py` broke an unrelated probe script in the same folder with `IndexError` from inside `dataclasses` (CVE_Intel, 2026-11-25). Fix: unique names (`inspect_snap.py`) or run with `python -I` when the folder holds other scripts.
- **I-027** [2026-11-25] #python #windows #shell — Python printing non-Latin-1 text (ē, ī, ū, Cyrillic) to the Git Bash console fails with `UnicodeEncodeError: 'charmap' codec` (cp1252); prefix `export PYTHONIOENCODING=utf-8;`.
  - Why: inspecting Baltic news headlines with `python -c "print(...)"` crashed on 'ē' until the variable was set (BalticIntel, 2026-11-25). Files written with `encoding="utf-8"` are unaffected.
- **I-029** [2026-11-25] #powershell #windows — To launch a long-lived local server from a PowerShell/.cmd launcher, use `Start-Process <exe> -WindowStyle Minimized` with **no** `-RedirectStandard*` (log to a file from inside the app) and `-PassThru` to keep its PID; stop it by that PID, never by image name.
  - Why: with only `-RedirectStandardError`, the server stayed attached to the launcher's console (its access log printed there) and would die when that window closed. `tasklist IMAGENAME eq python.exe | taskkill` to restart it was blocked by the auto-mode classifier (could hit unrelated processes). BalticIntel launcher, 2026-11-25. Related: S-001, I-018.
  - Verified pattern: launcher writes `$proc.Id` to `data\server.pid`; a stop script checks `Get-CimInstance Win32_Process -Filter "ProcessId = $pid"` has the expected CommandLine (`-m\s+backend`) before `Stop-Process`. For a server started before PID files, find it by CommandLine filter (allowed by auto mode), not by image name.
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
- **I-024** [2026-11-25] #git #windows #shell — Scripted exact-string patches (node/python `replace`) fail on a fresh clone because `core.autocrlf=true` checks files out CRLF; add `.gitattributes` with `* text=auto eol=lf`, run `sed -i 's/\r$//'` on the tree (index stays LF, no real diff), or use the Edit tool.
  - Why: a patch script reported "MISSING" for every multi-line block in a cloned upstream repo (eDEX AI, 2026-11-25). Related: E-005.

## LLM APIs
- **I-031** [2026-11-25] #llm #python — OpenRouter `openrouter/auto` can return `message.content = None` for a structured-JSON prompt (it may route to a reasoning model that spends `max_tokens` on reasoning); guard None as a retryable error and pin a concrete model for unattended runs.
  - Why: a scheduled ZenWarriorSounds short run crashed twice with `AttributeError: 'NoneType' object has no attribute 'strip'` in `generate.py` (max_tokens 700); the retry loop only caught ValueError. A tiny probe to `openrouter/auto` worked (routed to `openai/gpt-6-luna`), and `--model openai/gpt-6-luna` fixed the real run (2026-11-25). Log `data['model']` and `finish_reason` when content is empty.
  - Recurred 2026-11-26 (same scheduled run, same crash on the first try). Until the code is fixed, pass `--model openai/gpt-6-luna` up front in unattended runs instead of discovering it after the crash. Related: DREAM-003.

- **I-036** [2026-11-26] #llm — Ollama serves models with a 4096-token context by default and rejects longer prompts (`400 request (7139 tokens) exceeds the available context size (4096 tokens)`, surfaced by litellm as `APIConnectionError: OllamaException`); for agent frameworks build a variant: Modelfile `FROM <model>` + `PARAMETER num_ctx 16384`, then `ollama create <model>-16k -f Modelfile`.
  - Why: Skyvern's action prompt was ~7k tokens; all 5 retries failed in ~24 s and Skyvern only reported "Max retries per step (5) exceeded … context window, LLM service errors…". The real cause was only in the litellm traceback (AutoJobSearch, 2026-11-26). Grep agent logs for `OllamaException` / `RateLimitError` before tuning anything.
- **I-037** [2026-11-26] #llm — OpenRouter `:free` models are often `429 … temporarily rate-limited upstream`; before a long agent run, send each free model a tiny JSON request and pick one that answers (6 of 11 answered on 2026-11-26; both Gemma 4 `:free` were 429).
  - How: list `GET https://openrouter.ai/api/v1/models` (no key) → ids ending `:free`, sort by `context_length`; probe `POST /api/v1/chat/completions` with `max_tokens` 200. `nvidia/nemotron-3-ultra-550b-a55b:free` then drove a full Skyvern form fill (AutoJobSearch `formtest/probe_openrouter_free.py`). Related: I-031.

- **I-038** [2026-11-26] #python — In `re.M` regexes anchored at line start, use `^[ \t]*`, not `^\s*`: `\s` also matches newlines, so the pattern swallows the blank line before a heading or list item (Markdown → plain text lost paragraph breaks).
  - Why: `re.sub(r"^\s*[*+]\s+", "- ", text, flags=re.M)` joined "…detections.\n\n* fast" into "…detections.\n- fast"; `^[ \t]*[*+][ \t]+` kept the blank line (AutoJobSearch `formtest/applicant_fields.py`, 2026-11-26).

## E-mail sending
- **I-035** [2026-11-26] #python #secrets — Outlook.com/Hotmail SMTP rejects App Passwords (`535 5.7.139 basic authentication is disabled`); send with OAuth2 XOAUTH2 instead: `msal` PublicClientApplication, authority `https://login.microsoftonline.com/consumers`, scope `https://outlook.office.com/SMTP.Send`, `smtp-mail.outlook.com:587` STARTTLS, then `AUTH XOAUTH2 base64("user=<addr>\x01auth=Bearer <token>\x01\x01")` → expect 235.
  - Entra app registration (user does it): Manifest first `"requestedAccessTokenVersion": 2` (else switching account types fails with "Property api.requestedAccessTokenVersion is invalid"), then `"signInAudience": "AzureADandPersonalMicrosoftAccount"`; add platform Mobile & desktop with redirect `http://localhost` for browser sign-in; set "Allow public client flows" = Yes for device-code sign-in.
  - Error map: `AADSTS700016 ... not found in the directory '9188040d-…'` = app is single-tenant (not for personal accounts; that GUID is the consumers tenant); `AADSTS50059` on `/common` = same; `AADSTS70002 client not supported for this feature` = public client flows off. Changes took ~1–2 min to apply. Probe audiences cheaply with `app.initiate_device_flow(...)` against consumers / common / the tenant id.
  - Why: AutoJobSearch (2026-11-26): app-password SMTP failed; three app registrations were needed before personal sign-in worked; `acquire_token_interactive` (browser, localhost redirect) then succeeded and a test mail with a PDF attachment was delivered. Cache the token with `msal.SerializableTokenCache` in a git-ignored file and use `acquire_token_silent` for later sends. Gmail still accepts App Passwords on `smtp.gmail.com:465`.

## Python environments & secrets
- **I-030** [2026-11-25] #python #image-gen #gpu — If a cached Hugging Face model is loading (diffusers/transformers `from_pretrained`) and it sits at 0% CPU with an idle GPU and no output, it is blocked on the Hub network check; kill it and run with `HF_HUB_OFFLINE=1`.
  - Why: an unattended SDXL (Juggernaut XL v9) poster run hung for 10+ min with no output; with `HF_HUB_OFFLINE=1` the pipeline loaded from `~/.cache/huggingface/hub` in ~3 s (ZenWarriorSounds short-create, 2026-11-25). Diagnose with `Get-Process <pid>` CPU staying flat plus `nvidia-smi` showing ~1% use. Related: E-001, S-003, DREAM-003.
  - Recurred 2026-11-26: another 20 min was lost before the hang was noticed. For unattended runs, set `HF_HUB_OFFLINE=1` before launching (e.g. `HF_HUB_OFFLINE=1 python make_short.py ...`; the env is inherited by the venv child), not only after a hang.
  - Recurred 2026-11-27 (3rd time, ~10 min lost; nvidia-smi showed ~1 GB used / idle): the rule was not checked before launching. Rerun with `HF_HUB_OFFLINE=1` drew the poster in 114 s. Check this entry before any unattended local-image run.
- **I-010** [2026-11-22] #python — Run project scripts with the project's own interpreter/venv (check for `.venv`, `venv`, `requirements.txt`) before assuming a package is missing.
  - Why: an upload script crashed importing `googleapiclient` under the wrong Python.
- **I-028** [2026-11-25] #python #windows — `python -I` (isolated mode) also disables user site-packages, so on this machine (packages in `%APPDATA%\Python\Python312`, see E-001) it raises `ModuleNotFoundError` for sounddevice, piper, etc.; use plain `python -u` for your own scripts, `-I` only for untrusted dirs.
  - Why: a voice sidecar test failed on `import sounddevice` with `-I` and passed without it (eDEX AI, 2026-11-25).
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
  - A variable the user set at Windows user scope is invisible to processes started earlier (this Claude session, its children). Check with `[Environment]::GetEnvironmentVariable('NAME','User')`; an app can fall back to `reg query HKCU\Environment /v NAME` (never log the value). Seen 2026-11-25 with `apiOpenRouterEDEXAI`.

## Built-in browser & terminal tools
- **I-017** [2026-11-22] #browser — Call `read_page` or `find` before clicking by `ref`.
  - Why: "ref map not initialized".
- **I-018** [2026-11-22] #claude-code — Long-running servers go in `run_in_background` (or launch.json + `preview_start`), not typed `run_in_terminal` lines that may be read as unfinished.

## UI & CSS
- **I-034** [2026-11-25] #ui — When appending code to an existing single-`<script>` page, a new top-level `function`/`const` whose name matches an existing global (e.g. `active`) is a SyntaxError ("Identifier … has already been declared") that kills the *whole* script; prefix new names or check `grep -o "let [a-z]*\|function [a-z]*"` first.
  - Why: a feed layer's `function active()` collided with the page's `let active` (selected node) → blank graph, `data is not defined`. Renamed to `activeSrc`. CVE_Intel, 2026-11-25.
- **I-032** [2026-11-25] #ui #json — An offline/embedded fallback dataset derived from live data must not keep the live data's change-detection hash/version, or the page treats the live load as "unchanged" and keeps showing the fallback.
  - Why: a sample built from `latest.json` copied its `contentHash`; the app's `apply()` skipped the live snapshot (18 sample nodes shown instead of 95, live=false). Fix: set the sample's hash to a fixed marker (`"offline-sample"`). CVE_Intel, 2026-11-25.
- **I-019** [2026-11-24] #ui — Stray page scrollbars can come from an absolutely positioned element (e.g. a Tailwind `sr-only` table) with no positioned ancestor; put `relative` on its wrapper.
  - Diagnose with JS: compare `document.documentElement.scrollHeight` with `innerHeight`, then check `el.offsetParent` of absolute elements.
  - Why: a chart's `sr-only` table was placed against `<body>` and made the document taller than the viewport.

## Electron apps
- **I-025** [2026-11-25] #electron #ui #gpu — xterm.js 5 `@xterm/addon-webgl` can draw a grey background and too-wide cells (GTX 1070, Electron 45, `ignore-gpu-blocklist`); default to the DOM renderer, make WebGL opt-in, and also load `@xterm/xterm/css/xterm.css`.
  - Diagnose: viewport `getComputedStyle().backgroundColor` was correct, so the canvas was at fault; disposing the WebGL addon live fixed the look. Seen upgrading eDEX-UI (xterm 4 → 5).
- **I-026** [2026-11-25] #electron #windows — systeminformation 5.x on Windows spawns PowerShell/WMI per call; parallel callers (e.g. one worker per core) pin the CPU at 100% (~30 powershell.exe, WUDFHost busy). Use one process, de-duplicated in-flight calls and per-function min intervals. Do NOT use `si.powerShellStart()`: its persistent session hangs `processes()` and every call queued after it.
  - Why: upgrading eDEX-UI (si 5.9 → 5.33) with its per-core cluster read 100% CPU even from outside; a single cached service measured 10–35%. Symptom also: `currentLoad` always 100 and stats calls timing out. With `powerShellStart()` the CPU and process widgets stayed empty (verified standalone: `processes()` never resolved).

## Media & ffmpeg
- **I-041** [2026-11-28] #image-gen — Don't place overlay text on a generated image by edge/detail energy alone: a dark subject on a dark background (head against night sky) scores as calm and gets covered. Reserve a fixed outer band (top or bottom third) and only use detail to choose which one.
  - Why: auto-placing a quote by lowest gradient energy put it over a Viking's head (rows 600-680 scored 3.5 vs sky 1-2, image median 5.3); fixed bands top y 190-570 / bottom y 1170-1560 on a 1080x1920 poster, plus "calm empty sky in upper third" in the scene prompt, fixed it (ZenWarriorSounds short-create, 2026-11-28).

- **I-039** [2026-11-26] #video #shell — ffmpeg `-loop 1 -i x.gif` fails ("Option loop not found"): `-loop` is an image2 option the gif demuxer lacks. Loop animated backgrounds (gif/mp4) with `-stream_loop -1 -i`; keep `-loop 1` for stills; force fps (`-r 30`) since GIF timing is variable.
  - Why: a video builder that always used `-loop 1` failed on a 553×309 9-frame GIF; switching by extension fixed it (ZenWarriorSounds `buildVideo.ps1`, 2026-11-26). Check animation with `-vf mpdecimate -f null -` (22 distinct frames in 3 s = moving).

## Testing
- **I-020** [2026-11-24] #testing #shell — A CLI that reads stdin exits at once when backgrounded (`exe &` / `( … &)`) from the Bash tool, because stdin is at EOF, so an empty log looks like a crash; test it in the foreground with piped stdin: `(sleep 30; echo ":quit") | timeout 60 app.exe …`.
  - Why: two silent "failed" runs of the frozen `luci.exe serve` were really clean EOF exits.
- **I-021** [2026-11-22] #testing — When a test script prints all cases and exits 1, find *which* case failed (print only failures with expected vs got) before changing code.
