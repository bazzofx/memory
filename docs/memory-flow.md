# Memory → dream → subconscious flow

Current as of 2026-11-25. Renders in any Markdown viewer that supports Mermaid. (The old PNG render, with a "Dream Validator" stage that never existed as a skill, was removed; it is in git history.)

```mermaid
flowchart TD
    A["Session starts in any project"] --> B["~/.claude/CLAUDE.md imports global.md<br/>(rules + realized-dreams list)"]
    B --> C["index.md → Topics: tag → entry IDs<br/>load only matching entries + projects/&lt;name&gt;.md"]
    C --> D["Do the task<br/>(on error: grep issues.md / limitations.md first)"]
    D --> E{"Stop hook: 2+ tool errors<br/>or 20+ tool calls?"}
    E -->|No| Z["Nothing to record"]
    E -->|Yes| F["memory-optimizer"]

    F --> G{"Reusable lesson?"}
    G -->|No| Z
    G -->|Yes| H["Phase A: find existing entry by ID / tag<br/>edit it, or add with next free ID + #tags"]
    H --> I["Run toolbox/memory_topics.py --write<br/>(rebuild Topics, check IDs and tags)"]
    I --> J["Phase B: dream pass (dream-manager)<br/>check dreams.md + archive.md, dedupe"]
    J --> K{"Recurring problem with an<br/>actionable improvement?"}
    K -->|No| P["Phase C: generalize lessons<br/>project-only facts → projects/&lt;name&gt;.md"]
    K -->|Yes| L["Add or update a Proposed dream"]
    L --> P

    L --> M{"User approves an experiment?"}
    M -->|No| R["Defer / reject with reason<br/>(archive.md, 'Resurface if')"]
    M -->|Yes| N["dream-realizer: verify the problem still exists,<br/>plan, sandbox, baseline, prototype, evaluate"]
    N --> O{"Passed the predeclared gates?"}
    O -->|No| Q["Record what was learned<br/>(never as a verified fact)"]
    Q --> F
    O -->|Yes| S["Gate 9: correct the source entry,<br/>record successes / procedures"]
    S --> T["update-subconscious: DREAM-NNN .md + VML .png"]
    T --> U["Add a one-line reference to global.md<br/>→ loaded in every future session"]
    U --> V{"Separate deployment approval?"}
    V -->|No| W["Keep as a proposal<br/>(knowledge is already in memory)"]
    V -->|Yes| X["Backup, canary deploy, observe,<br/>rollback on stop conditions"]
    X --> Y["Archive the dream; rebuild the subconscious entry"]

    classDef load fill:#164e63,color:#fff,stroke:#0891b2
    classDef memory fill:#1e3a8a,color:#fff,stroke:#3b82f6
    classDef dream fill:#4c1d95,color:#fff,stroke:#8b5cf6
    classDef realise fill:#14532d,color:#fff,stroke:#16a34a
    classDef stop fill:#78350f,color:#fff,stroke:#d97706

    class A,B,C,D load
    class F,H,I,P memory
    class J,L dream
    class N,S,T,U,X,Y realise
    class R,W,Z,Q stop
```
