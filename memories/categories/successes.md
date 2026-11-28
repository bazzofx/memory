# Successes — what worked well and should be repeated

Load when: choosing an approach for something that was hard before. Multi-step reusable workflows belong in `procedures.md` instead.
Format (see `index.md` → Entry format): `- **S-NNN** [YYYY-MM-DD] #tags — <approach, one line>` then indented `Why:` (evidence it worked) sub-bullets. Newest first.

- **S-011** [2026-11-25] #browser #testing — Test a file-upload/import UI headlessly: build the file in page JS, `const dt = new DataTransfer(); dt.items.add(new File([text], 'x.json')); input.files = dt.files; input.dispatchEvent(new Event('change'))`, then assert on resulting DOM/state.
  - Never call `location.reload()` inside `javascript_tool`: the reload cuts the script off and its return value is lost. Use `navigate` with a cache-busting `?v=N` as its own step, then run the checks.
  - Why: verified rule-file import, Reset-to-file and localStorage override persistence in a static dashboard without a native file dialog (Traffic Lens, 2026-11-25). Related: L-007.
- **S-010** [2026-11-25] #python #llm — No-AI short keyword labels for news headlines: score words by IDF over the stored headline corpus, +3 for category-rule terms (keep multi-word ones like "air raid" whole), +1 for proper names, drop stopwords/common news verbs and -ed/-ing/-ly words; take 2 topic words + the entities named first.
  - Also strip all-caps kickers/bylines first ("WATCH:", "NAME ⟩", "… | Author" — test all-caps with `head == head.upper()`, since `[^a-zà-ž]` treats Š as lowercase) and possessives ("China's"). In a teaser fallback, skip capitalised words (mostly people's names).
  - Why: gave usable graph-node notes like "airBaltic · Guarantee · Latvia", "Air raid · Operation · Kaliningrad · Lithuania" on 41 live developments; some verbs still slip in ("Weaken"), so an LLM is the upgrade path (BalticIntel v0.8.2, `backend/intelligence/classify.py`).
- **S-009** [2026-11-25] #electron #stt #tts #python — For local speech in an Electron/Node app, run a Python sidecar over stdin/stdout JSON lines (no port): commands `ptt_start/ptt_stop/speak/stop/mute/quit`, events `status/recording/transcript/speak_start/speak_done`; stdout = protocol only, logs to stderr, spawn with `python -u`.
  - Import numpy/sounddevice on the main thread before the stdin reader (I-012). Barge-in = `stop` before recording; test without a mic by transcribing Piper-synthesized speech resampled to 16 kHz.
  - Why: eDEX AI M3 passed 8 sidecar + 10 in-app checks first try; Whisper base int8 CPU 1.5 s per 3 s audio, Piper first audio 0.5 s. Related: R-002.

- **S-001** [2026-11-24] #electron #testing #windows — Verify a packaged Electron app without desktop control: launch the `.exe` with `--remote-debugging-port=9333`, then drive it over CDP from a Node script.
  - Script: global `fetch` + `WebSocket`; read `http://127.0.0.1:9333/json`, send `Runtime.evaluate` (page text, `fetch` to its APIs) and `Page.captureScreenshot`. Close with `window.close()`, then check `tasklist` for leftovers.
  - Before launching, check no copy is already running (`Get-CimInstance Win32_Process` shows path and start time). With a single-instance lock a second launch hands over to the running copy and exits, so the port never opens. Don't kill the user's copy.
  - A portable build unpacks itself first, so wait longer than 60 s.
  - Also works for a dev run (`electron src --remote-debugging-port=9333 --remote-debugging-address=127.0.0.1`) with a temp settings dir; embedded WebContentsViews show up as their own CDP page targets. Stop only your own process tree (`taskkill /pid <pid> /T /F`, or filter `Win32_Process` by CommandLine) — never `taskkill /IM electron.exe`, which hits other Electron apps (blocked by the auto-mode classifier, 2026-11-25).
  - Why: verified the Kairo portable exe end to end (UI rendered, bundled Luci started, nothing left running).
  - Script: the original `cdp-luci.mjs` was lost with its session scratchpad. Save the next version to `C:\ai\toolbox\` (see `toolbox/README.md`).
- **S-002** [2026-11-24] #tts #python — Choose a local text-to-speech engine by measuring **startup time** and **time to first sentence** on the target machine; stream sentence by sentence and stop with a generation counter.
  - Streaming: a producer thread fills a small queue while the current sentence plays.
  - Why, on the GTX 1070 PC: Piper (`piper-tts`, ONNX, CPU) started in ~5 s, first sentence ~1 s, stopped within 0.2 s. Kokoro took ~35 s to start and 3–5 s to the first word on CPU (0.3 s on GPU, 840 MB).
  - Code and API notes: R-002.
- **S-003** [2026-11-24] #image-gen #gpu #python — Local SDXL works on the 8 GB GTX 1070: Juggernaut XL v9 fp16 with model CPU offload, ~104 s per 768×1344 image at 28 steps. Free VRAM first with `ollama stop gemma4:latest`.
  - Ollama plus yue-server hold ~5 GB of VRAM if left running.
  - Let the model paint only the scene and add exact text (quotes, titles) with Pillow afterwards; diffusion models can't render exact text.
  - Condensed poster type with no extra font: Windows' variable `bahnschrift.ttf` + Pillow `font.set_variation_by_name('Bold Condensed')`; shrink the size until the longest word fits the column, and let hyphenated words break after the hyphen so one long word doesn't shrink all lines (2026-11-25).
  - Why: ZenWarriorSounds shorts run fully local this way (see `projects/zenwarrior.md`). Setup: E-001, I-011.
- **S-004** [2026-11-24] #llm — When an LLM acts on user data, use "model proposes, code decides".
  - Send items as compact lines with short refs.
  - Force a JSON schema reply (`{say, actions[]}`, Ollama `format` = schema, temperature 0, `think: false`).
  - Have the model copy date words; the app's own code resolves them.
  - Validate every action with the normal command contract; drop unknown refs and impossible changes.
  - Ask the user to confirm before applying.
  - Why: in Kairo/Luci it worked end to end (answers, a bulk reschedule, a breakdown into steps, cancel), and no invalid change reached the store.
- **S-005** [2026-11-23] #shell #claude-code — To find *which layer* mangles a command, compare what the transcript recorded as sent with the output's bytes, using a tiny harmless probe, then vary the quoting one factor at a time.
  - Sent: `~/.claude/projects/<proj>/<session>.jsonl` → `"command"`. Bytes: `od -An -tx1` (not `od -c` or `echo`). Vary `'…'`, `<<'EOF'`, `"…"`.
  - Why: it showed the Bash tool, not bash, halves `\\` — the real cause behind failures blamed on heredoc quoting (I-001). Evidence: `dreams/experiments/DREAM-001/run-20261123-01/report.md`.
- **S-006** [2026-11-23] #claude-code #testing — Before building a warning hook or checker, measure its trigger on real past calls from the transcripts: recall on hand-labelled failures, warning rate on calls that succeeded, compared with the naive trigger.
  - Why: the dream's proposed trigger would have warned on 23% of good calls; the tested one caught 4/4 real failures and warned on 4%, and the measurement found 2 silent failures (exit 0, invalid JSON) no error scan had found.
- **S-007** [2026-11-23] #testing #json — Keep shell test cases as one file per case, written verbatim with the Write tool, and generate hook stdin with `JSON.stringify` in a runner script; never hand-escape commands inside a JSON fixture.
  - Why: it avoided another escaping layer while testing escaping bugs; 22 cases plus 6 robustness checks ran reproducibly on the first try.
- **S-008** [2026-06-01] #windows #python #stt — To inject dictated text into whatever app has focus on Windows, copy it to the clipboard and send Ctrl+V (`pyperclip` + `pynput.Controller`) rather than typing it key by key.
  - Why: Voice2Text settled on it as the most reliable method (`core/typer.py`; see `projects/voice2text.md`).
