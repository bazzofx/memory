# Preferences — user preferences, conventions and working style

Load when: writing anything user-facing, committing, or choosing how to work.
Format (see `index.md` → Entry format): `- **P-NNN** [YYYY-MM-DD] #tags — <preference, one line>` then indented `Why:` (where the user said or showed it). Newest first. Only record what the user stated or clearly chose.

- **P-001** [2026-11-25] #llm #image-gen #stt #tts — Local and offline AI by default (image generation, speech to text, LLMs); use paid cloud APIs (OpenRouter, Gemini, …) only when the user explicitly asks. If the local path fails, report it and offer cloud rather than switching silently.
  - Why: ZenWarriorSounds made local the default image engine on 2026-11-25 (`--cloud` / `--openrouter` only on request); Voice2Text was built for zero-cost offline transcription because the user wants no API costs.
- **P-002** [2026-11-22] #memory — Record only noteworthy memories (long-horizon tasks, real issues), not every task; check whether a memory already exists and update, merge or delete it before adding.
  - Why: the user's explicit instruction when creating memory-optimizer.
- **P-003** [2026-11-22] #memory — Keep loaded context small: memory is loaded by category or topic at the moment it's needed.
  - Why: the user asked for the per-category split for this reason.
