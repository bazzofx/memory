# Project: Voice2Text

Path: `C:\Users\joker\OneDrive\Documents\Github\Voice2Text`. Load when working in this project.
Windows system-tray voice-to-text app, similar to Whisper Flow: zero-cost offline transcription with local Whisper (P-001).
Cross-project lessons from here: S-008 (clipboard + Ctrl+V text injection). Same speech stack as kairo's Luci (faster-whisper, pynput, sounddevice); see R-002 and `projects/kairo.md` → Voice.

## Stack and architecture (recorded 2026-06-01)
- Python + PyQt6 (tray app), faster-whisper, sounddevice (mic capture at 16 kHz float32), pynput (global hotkeys), pyperclip + `pynput.Controller` (paste for text injection).
- `main.py` entry point; `config.py` JSON config at `~/.voice2text/config.json`.
- `core/recorder.py` mic capture; `core/transcriber.py` faster-whisper wrapper with `ModelLoader` / `TranscribeWorker` QThreads; `core/typer.py` paste via clipboard + Ctrl+V; `core/hotkey.py` global hotkey with toggle and push-to-talk modes.
- `ui/app.py` (`Voice2TextApp` QObject, orchestrates everything), `ui/tray.py` (QSystemTrayIcon with coloured-dot status icons), `ui/settings_dialog.py` (hotkey editor, model / language / device / mic selectors).
- Defaults: hotkey Ctrl+Shift+Space (toggle mode), model `base`.
- When extending it, keep the QThread-based async pattern and signal-based cross-thread communication.
