# Environments — OS, tools, configurations and dependencies

Load when: running commands, installing things, or debugging "works elsewhere" problems.
Format: `- [YYYY-MM-DD] <fact>.` Update in place when a version changes. Newest first.

- [2026-11-24] Main machine AI/audio stack:
  - GPU: NVIDIA GTX 1070 (8 GB).
  - Python 3.12.6 at `C:\Python312`, with packages in user site-packages (`%APPDATA%\Python\Python312`).
  - torch 2.8.0+cu128 and torchvision 0.23.0+cu128 (upgraded from a broken 0.20.1 on 2026-11-24).
  - Ollama on 127.0.0.1:11434 with `gemma4:latest` (9.6 GB).
  - Installed: faster-whisper 1.2.1, piper-tts 1.8, pynput, sounddevice.
  - Unused leftovers: kokoro, misaki, spacy.
  - Hugging Face cache: `~/.cache/huggingface/hub` (whisper base / medium / large-v3).
- [2026-11-24] Windows SAPI (System.Speech) voices on the main machine: only Hazel, Zira and Maria, all **female**. A Windows-voice TTS fallback can't be male here. Check with `GetInstalledVoices()`.
- [2026-11-22] Main machine: Windows 10 Pro; Claude Code's Bash tool is Git Bash (POSIX paths like `/c/...`; `cygpath` available). Commands given to the user run in PowerShell.
- [2026-11-22] Node v22 is installed and on PATH (used for project hooks).
- [2026-11-22] Git converts LF→CRLF on commit (`core.autocrlf`); the "LF will be replaced by CRLF" warning is expected and harmless.
