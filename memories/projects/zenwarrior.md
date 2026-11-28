# Project: ZenWarriorSounds

Path: `Y:\13_YoutubeChannels\ZenWarriorSounds` (Git Bash: `/y/13_YoutubeChannels/ZenWarriorSounds`). Load when working in this project.
YouTube/Instagram music-video production: project skills `zenwarrior`, `video-create`, `short-create`, `song-create*`, `youtube-upload` in `.claude/skills/`; shared helpers in `_tools/`.
Cross-project lessons from here: S-003 (local SDXL), I-011 (torch in venvs), P-001 (local by default), R-001 (YuE2 Studio), I-016 (API keys), I-030 (HF Hub hang), I-031 (openrouter/auto empty content), L-008 (export loudness stops short), I-039 (ffmpeg GIF backgrounds), I-040 (Bash expands `$env` in powershell -Command), I-041 (text placement on generated images).

## Video builds
- [2026-11-26] `buildVideo.ps1` accepts animated backgrounds (.gif/.mp4/.mov/.webm/.mkv) via `-stream_loop -1` (I-039). Small GIFs are upscaled to 1920x1080 and look soft; warn the user. Video8 (5 min) and Video9 (1 hour `-Loop`) were the first GIF-background builds.
- [2026-11-25] I-031 is fixed in `generate.py` (2026-11-28): default spec model `openai/gpt-6-luna`, empty content is retried, then falls back to `openrouter/auto`.

## Scheduling
- [2026-11-28] Daily shorts run as the Claude desktop scheduled task `zenwarrior-daily-short` (cron `0 11,15,18 * * *`, prompt in `~/.claude/scheduled-tasks/zenwarrior-daily-short/SKILL.md`), not Windows Task Scheduler. PAUSED 2026-11-28 by the user while a new poster style is tested; re-enable with `update_scheduled_task enabled:true`.

## Image generation
- [2026-11-28] short-create now uses the "warrior collection" style (user-approved after a 2-poster test): any warrior culture/art style/palette per poster, quote ALWAYS in Palatino Linotype Bold (user preference), composited in the outer third (top y 190-570 or bottom y 1170-1560, x 80-920) on the calmer one (I-041). The old sumi-e panel + Bahnschrift layout is gone.
  - Bulk: `make_short.py --images N` queues posters in `finalVideos\ShortImages\`; `--videos N` turns the oldest queued posters into shorts (moves them) and paints any shortfall; `--no-generate`. Default music: `_library\shortsMusic\default.*`, else random there, else `_library\songs`. `local_image.generate` caches the pipeline, so a batch loads the model once.
- [2026-11-25] LOCAL is the default image engine in `make_short.py` (short-create) and `generate_bg.py` (video-create); `--cloud` / `--openrouter` uses OpenRouter. The shared engine is `_tools/local_image.py`, which also unloads Ollama models.
  - Never add `--cloud` unless the user asks for cloud / OpenRouter / Gemini / "not local GPU". If local fails, report it and offer `--cloud` rather than switching silently (P-001).
- [2026-11-24] Warrior's Path shorts: `.claude/skills/short-create/scripts/local_poster.py --spec <json> --out <dir> [--video]`. SDXL (Juggernaut XL v9) paints only the scene; Pillow adds the sumi-e panel and the exact Bahnschrift Condensed quote text. ~104 s per 768×1344 scene (S-003); venv and model in E-001.

## Music
- [2026-11-24] Songs are generated through the `yue2-studio` MCP server (song-create skills). If it fails with ECONNREFUSED, start YuE2 Studio headless (R-001), then reconnect.
