# Memory index

Root: `C:\ai\memories\`. Read this, then load only the file or entries you need. Look up by topic in **Topics** below, or grep an ID (`I-001`) or `#tag`.

| File | Holds | Load when |
| --- | --- | --- |
| `global.md` | Essential rules + realized-dream list | Always (imported for every project by `~/.claude/CLAUDE.md`) |
| `categories/issues.md` (`I-`) | Past errors, root causes, fixes | A command/edit/build/test fails — grep the error text; before a risky step in a listed topic |
| `categories/successes.md` (`S-`) | What worked well and should be repeated | Choosing an approach for something that was hard before |
| `categories/decisions.md` (`D-`) | Cross-project decisions and their reasoning | Changing shared tooling, memory layout or conventions |
| `categories/preferences.md` (`P-`) | User preferences, conventions, working style | Writing anything user-facing, committing, choosing how to work or which service to use |
| `categories/environments.md` (`E-`) | OS, shells, tools, versions, config, dependencies | Running commands, installing, debugging "works elsewhere" problems |
| `categories/procedures.md` (`PR-`) | Validated, reusable step-by-step workflows | Starting a task type that has a procedure listed |
| `categories/limitations.md` (`L-`) | Known constraints of tools/platforms + workarounds | A tool behaves unexpectedly; before using a tool with a listed limit |
| `categories/references.md` (`R-`) | How-to notes, known commands, pointers to docs and toolbox scripts | You need a command, doc or script for a tool or service |
| `categories/pending.md` (`T-`) | Unresolved tasks and follow-ups | Session start, task end, or "what's left?" |
| `projects/<name>.md` | Project goals, architecture, tech, constraints, project-only decisions | Working in that project: `kairo`, `zenwarrior` (ZenWarriorSounds), `voice2text` |
| `dreams/dreams.md` | Improvement proposals, experiments, approvals, implemented capabilities | Session review, or when asked about dreams (`dream-manager` skill) |
| `dreams/archive.md` | Closed dreams with resolution and "resurface if" conditions | Before proposing a dream (avoid reviving a closed one), or when a matching failure recurs |
| `dreams/experiments/<DREAM-ID or EXP-slug>/<run-id>/` | Experiment plans, reports and sandbox prototypes (`EXP-` = experiment with no dream, e.g. `EXP-vml`) | Realizing, resuming or reviewing a dream (`dream-realizer` skill) |
| `subconscious/index.md` + `DREAM-NNN-<slug>.md/.png` | Realized dreams: the discovery, the verified correct way, and a VML diagram of how it connects (`.md` is the source of truth) | Before repeating work a realized dream already solved; at dream close-out (`update-subconscious` skill) |
| `C:\ai\toolbox\` | Reusable scripts that memory entries point to (`toolbox/README.md`) | A memory entry names a script, or a script you wrote is worth keeping |

`.ignore` hides experiment `sandbox/` folders from Grep (ripgrep); read them by path when needed.

Placement rules:
- Project-only knowledge goes in `projects/<name>.md`. A lesson learned in a project but useful elsewhere goes in a category, with the project only as the example, and the project file lists its ID under "Cross-project lessons".
- An error + its fix → `issues.md`. An approach that worked → `successes.md`. A reusable multi-step workflow → `procedures.md`. A tool limit you can't fix, only work around → `limitations.md`. A command, doc or script to remember → `references.md`.
- A pending item that gets done is deleted (lasting lesson → the right category).

## Entry format
```
- **I-014** [2026-11-24] #python #packaging — <the rule or fact, one line, ≤ ~200 chars>
  - Why: <evidence / what went wrong>
  - Evidence: <report path>   Related: S-003
```
- IDs are permanent and never reused, even after an entry is deleted or moved (a moved entry keeps its ID). Link entries by ID, never by position ("entry 1").
- Prefixes: `I` issues, `S` successes, `D` decisions, `P` preferences, `E` environments, `L` limitations, `R` references, `T` pending, `PR` procedures (`## PR-NNN — <task>` heading, tags on the next line).
- Tags (fixed list; add one here first, only when no existing tag fits): #shell #powershell #windows #python #packaging #gpu #llm #tts #stt #image-gen #json #browser #electron #ui #testing #git #claude-code #memory #secrets
- After adding, removing or retagging entries, run `python C:/ai/toolbox/memory_topics.py --write`. It rebuilds Topics, checks IDs and tags, and prints the next free ID per prefix.

## Topics
<!-- topics:start -->
| Tag | Entries |
| --- | --- |
| #browser | I-017, L-003, L-004 |
| #claude-code | D-001, D-002, E-003, E-004, I-001, I-008, I-009, I-018, I-022, L-001, L-002, L-005, PR-001, PR-002, S-005, S-006 |
| #electron | S-001 |
| #git | E-005 |
| #gpu | E-001, I-011, I-013, S-003 |
| #image-gen | E-001, P-001, S-003 |
| #json | I-001, I-004, S-007 |
| #llm | E-001, P-001, R-002, S-004 |
| #memory | D-001, D-002, D-003, L-001, P-002, P-003, PR-001, R-003 |
| #packaging | I-014, I-015 |
| #powershell | I-002, R-001 |
| #python | E-001, I-003, I-010, I-011, I-012, I-013, I-014, I-015, I-023, S-002, S-003, S-008 |
| #secrets | I-016 |
| #shell | E-003, I-001, I-003, I-005, I-006, I-007, I-008, I-016, I-020, S-005 |
| #stt | E-001, P-001, R-002, S-008 |
| #testing | I-020, I-021, PR-002, S-001, S-006, S-007 |
| #tts | E-001, E-002, I-013, P-001, R-002, S-002 |
| #ui | I-019 |
| #windows | E-002, E-003, E-005, I-001, I-002, I-003, I-005, I-006, I-012, I-022, I-023, R-001, S-001, S-008 |

Next free IDs: D-004, E-006, I-024, L-006, P-004, PR-003, R-004, S-009, T-008. Generated by `toolbox/memory_topics.py`; don't edit by hand.
<!-- topics:end -->
