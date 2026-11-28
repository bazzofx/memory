# Project: BalticIntel (INTEL // FUSION)

Path: `C:\_web_apps_2025\BalticIntel` (local git, `main`, tag `v0.7`; no remote)
Purpose: local-first Baltic security intelligence graph; plan in `intel-fusion-development-plan.md` (P0–P4).

- **Status 2026-11-25:** v0.8 = P0 + P1 done: live metadata-only RSS feed, FastAPI + SQLite/FTS5, no AI calls. Next is P2 (local model extraction via Ollama 0.40.3, GTX 1060) and a Playwright browser suite (P0 item still open).
- Run: `python -m backend` → http://127.0.0.1:8765 (hourly scheduler); `python -m backend collect` for one run; `python -m pytest -q tests` (44 offline tests). README/CHANGELOG document everything.
- **UI rule:** `frontend/index.html` is generated from the approved `intel-fusion-v07-retry.html` by `tools/patch_frontend_v08.py` (exact-match replacements). Edit the script, never index.html; the user requires the v0.7 look (Latvian carmine/ivory/charcoal, centered dialogs, one-image hover preview, depth 10).
- Feeds checked 2026-11-25: working = LSM eng.lsm.lv/rss, LRT, Postimees, Consilium, BBC Europe, Guardian Europe, DW, Kyiv Independent, Ukrinform. Not usable: ERR news.err.ee/rss (403 to bots — don't bypass), mod.gov.lv rss (static pages), LETA (SSL EOF), Baltic Times (403), NATO/mfa.gov.lv/president.lv (no RSS).
- Honesty rules from the plan: never present samples as live, no substitute photos, eventDate null in metadata mode, groupings labelled unreviewed.
- Cross-project lessons from here: L-006, I-027, I-029, R-004, S-010, L-007.
- v0.8.1 + v0.8.2 (2026-11-25, committed 3e41fb1): live lookup on Expand intelligence (Google News RSS + stored FTS, review-before-merge), feed retries, scheduler clock fix, `Start-IntelFusion.cmd` launcher, 56 tests. v0.8.2: nodes show 3–4 keyword notes (`labelKeywords`); Expand = new keyword + previous keywords (trail then label), strict AND query then broad OR; `Stop-IntelFusion.ps1` stops by recorded PID; 64 tests. Open the app at http://127.0.0.1:8765/ — opening frontend/index.html from disk shows only the offline sample.
- v0.8.3 (2026-11-25, uncommitted): drag nodes to move them (offsets `n.dx/n.dy` added in a wrapped `pos()`, so branches follow); a moved graph blocks the 60 s auto-reload; Reset graph restores the layout. Positions are not persisted.
- v0.8.4 (2026-11-25, uncommitted): Full screen button (wrapper `#canvasWrap.fs` + requestFullscreen when allowed); in full screen the details panel docks right and a blank-canvas click closes it and deselects.
