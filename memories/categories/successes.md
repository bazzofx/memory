# Successes — what worked well and should be repeated

Load when: choosing an approach for something that was hard before. Multi-step reusable workflows belong in `procedures.md` instead.
Format (see `index.md` → Entry format): `- **S-NNN** [YYYY-MM-DD] #tags — <approach, one line>` then indented `Why:` (evidence it worked) sub-bullets. Newest first.

- **S-001** [2026-11-24] #electron #testing #windows — Verify a packaged Electron app without desktop control: launch the `.exe` with `--remote-debugging-port=9333`, then drive it over CDP from a Node script.
  - Script: global `fetch` + `WebSocket`; read `http://127.0.0.1:9333/json`, send `Runtime.evaluate` (page text, `fetch` to its APIs) and `Page.captureScreenshot`. Close with `window.close()`, then check `tasklist` for leftovers.
  - Before launching, check no copy is already running (`Get-CimInstance Win32_Process` shows path and start time). With a single-instance lock a second launch hands over to the running copy and exits, so the port never opens. Don't kill the user's copy.
  - A portable build unpacks itself first, so wait longer than 60 s.
  - Why: verified the Kairo portable exe end to end (UI rendered, bundled Luci started, nothing left running).
  - Script: the original `cdp-luci.mjs` was lost with its session scratchpad. Save the next version to `C:\ai\toolbox\` (see `toolbox/README.md`).
- **S-002** [2026-11-24] #tts #python — Choose a local text-to-speech engine by measuring **startup time** and **time to first sentence** on the target machine; stream sentence by sentence and stop with a generation counter.
  - Streaming: a producer thread fills a small queue while the current sentence plays.
  - Why, on the GTX 1070 PC: Piper (`piper-tts`, ONNX, CPU) started in ~5 s, first sentence ~1 s, stopped within 0.2 s. Kokoro took ~35 s to start and 3–5 s to the first word on CPU (0.3 s on GPU, 840 MB).
  - Code and API notes: R-002.
- **S-003** [2026-11-24] #image-gen #gpu #python — Local SDXL works on the 8 GB GTX 1070: Juggernaut XL v9 fp16 with model CPU offload, ~104 s per 768×1344 image at 28 steps. Free VRAM first with `ollama stop gemma4:latest`.
  - Ollama plus yue-server hold ~5 GB of VRAM if left running.
  - Let the model paint only the scene and add exact text (quotes, titles) with Pillow afterwards; diffusion models can't render exact text.
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
