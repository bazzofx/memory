# Project: ZenWarriorSounds

Path: `Y:\13_YoutubeChannels\ZenWarriorSounds` (Git Bash: `/y/13_YoutubeChannels/ZenWarriorSounds`). Load when working in this project.
YouTube/Instagram music-video production: project skills `zenwarrior`, `video-create`, `short-create`, `song-create*`, `youtube-upload` in `.claude/skills/`; shared helpers in `_tools/`.
Cross-project lessons from here: S-003 (local SDXL), I-011 (torch in venvs), P-001 (local by default), R-001 (YuE2 Studio), I-016 (API keys).

## Image generation
- [2026-11-25] LOCAL is the default image engine in `make_short.py` (short-create) and `generate_bg.py` (video-create); `--cloud` / `--openrouter` uses OpenRouter. The shared engine is `_tools/local_image.py`, which also unloads Ollama models.
  - Never add `--cloud` unless the user asks for cloud / OpenRouter / Gemini / "not local GPU". If local fails, report it and offer `--cloud` rather than switching silently (P-001).
- [2026-11-24] Warrior's Path shorts: `.claude/skills/short-create/scripts/local_poster.py --spec <json> --out <dir> [--video]`. SDXL (Juggernaut XL v9) paints only the scene; Pillow adds the sumi-e panel and the exact Bahnschrift Condensed quote text. ~104 s per 768×1344 scene (S-003); venv and model in E-001.

## Music
- [2026-11-24] Songs are generated through the `yue2-studio` MCP server (song-create skills). If it fails with ECONNREFUSED, start YuE2 Studio headless (R-001), then reconnect.
