# References — how-to notes, commands and pointers to docs or scripts

Load when: you need a known command, doc or script for a tool or service, rather than a lesson from a failure. Errors go in `issues.md`, approaches that worked in `successes.md`.
Format (see `index.md` → Entry format): `- **R-NNN** [YYYY-MM-DD] #tags — <what it is and where, one line>` then indented `How:` / `Use when:` sub-bullets. Newest first. Reusable scripts live in `C:\ai\toolbox\`; reference them here.

- **R-001** [2026-11-24] #windows #powershell — Start YuE2 Studio (backs the `yue2-studio` MCP server for music generation) headless when the MCP server refuses connections (ECONNREFUSED).
  - How: `Start-Process "$env:LOCALAPPDATA\YuE2 Studio\YuE2-Studio.exe" -ArgumentList '--headless' -WindowStyle Hidden` (from Bash, via `powershell -Command`; see I-002). Wait a little, then reconnect with ToolSearch.
  - Use when: song-create skills or unattended scheduled runs need the server (ZenWarriorSounds).
- **R-002** [2026-11-24] #tts #stt #llm — Reusable handoff for local voice + Ollama projects: `C:\_web_apps_2025\kairo\docs\voice-tts-handoff.md` (Piper streaming, faster-whisper, the Ollama JSON-schema pattern).
  - Use when: adding speech in or out, or a local LLM, to any project (see S-002, S-004).
- **R-003** [2026-11-25] #memory — Memory policies: `C:\ai\policies\agent-reflection-policy.md` (short) and `agent-reflection-full-policy.md` (full). The policy wins over conflicting skill guidance.
