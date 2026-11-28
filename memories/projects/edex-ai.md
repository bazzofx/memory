# Project: eDEX AI

- Repo: `C:\_web_apps_2025\eDexUI_AI\edex-ai` (fork of archived GitSquared/edex-ui 2.2.8, GPL-3.0), local branch `edex-ai`, no remote.
- Goal: eDEX-UI + embedded browser + tool-calling LLM + push-to-talk voice. The eDEX visual style must stay the same (user requirement).
- **Status and next steps: `docs/HANDOFF.md` in the repo — read it first.** M0–M3 done (initial deliverable); pushed to github.com/bazzofx/edex-ai main. Next: wake word, streaming TTS, renderer contextIsolation.
- Decisions: LLM = OpenRouter free models (env `apiOpenRouterEDEXAI`, default `nvidia/nemotron-3.5-lightning:free`), Ollama gemma4 as offline fallback; STT faster-whisper + TTS Piper in a Python sidecar (reuse Kairo, R-002); legacy renderer keeps Node for now, web content fully sandboxed.
- Cross-project lessons from here: I-024, I-025, I-026, I-028, S-009, S-001 (dev-run CDP + safe process stop), I-016 (user-scope env var).
