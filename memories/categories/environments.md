# Environments — OS, tools, configurations and dependencies

Load when: running commands, installing things, or debugging "works elsewhere" problems.
Format (see `index.md` → Entry format): `- **E-NNN** [YYYY-MM-DD] #tags — <fact, one line>` with details as sub-bullets. Update in place when a version changes. Newest first.

- **E-006** [2026-11-25] #windows #browser — The main machine's network resolves some hosts to fake-IP range `198.18.x.x` (proxy/TUN DNS), e.g. `www.bleepingcomputer.com` → 198.18.8.39, so SSRF guards that require public addresses refuse them; don't loosen the guard, mark the source disabled.
  - Same day from Python/httpx: CISA RSS feeds return HTTP 403 (KEV JSON at cisa.gov works), mitel/danfoss/n-able/wso2 home pages 403.
- **E-001** [2026-11-24] #python #gpu #llm #tts #stt #image-gen — Main machine AI/audio stack: GTX 1070 (8 GB), 64 GB RAM, Python 3.12.6, torch 2.8.0+cu128, Ollama `gemma4:latest`.
  - Python at `C:\Python312`, packages in user site-packages (`%APPDATA%\Python\Python312`).
  - torch 2.8.0+cu128 and torchvision 0.23.0+cu128 (upgraded from a broken 0.20.1 on 2026-11-24; see I-013).
  - Ollama on 127.0.0.1:11434 with `gemma4:latest` (9.6 GB).
  - Installed: faster-whisper 1.2.1, piper-tts 1.8, pynput, sounddevice. Unused leftovers: kokoro, misaki, spacy.
  - Local image venv: `C:\Users\joker\localimage\.venv` (uv, `--system-site-packages`, diffusers 0.43, reuses the system torch; see I-011).
  - Hugging Face cache `~/.cache/huggingface/hub`: whisper base / medium / large-v3, `RunDiffusion/Juggernaut-XL-v9` fp16 (~6.5 GB).
  - YuE2 Studio (music generation, backs the `yue2-studio` MCP server): `%LOCALAPPDATA%\YuE2 Studio\YuE2-Studio.exe` (headless start: R-001).
- **E-002** [2026-11-24] #tts #windows — Windows SAPI (System.Speech) voices on the main machine are only Hazel, Zira and Maria, all **female**, so a Windows-voice TTS fallback can't be male here. Check with `GetInstalledVoices()`.
- **E-003** [2026-11-22] #windows #shell #claude-code — Main machine: Windows 10 Pro. Claude Code's Bash tool is Git Bash (POSIX paths like `/c/...`, `cygpath` available); commands given to the user run in PowerShell.
- **E-004** [2026-11-22] #claude-code — Node v22 is installed and on PATH (used for hooks).
- **E-005** [2026-11-22] #git #windows — Git converts LF→CRLF on commit (`core.autocrlf`); the "LF will be replaced by CRLF" warning is expected and harmless.
