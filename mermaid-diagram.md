
# Dream Mermaid Diagram

flowchart TD

    A["Agent starts task"] --> B["Load global memory and relevant indexed lessons"]
    B --> C["Execute task"]
    C --> D["Task completion / reflection"]

    D --> E["Memory Optimizer"]
    E --> F{"Reusable lesson?"}
    F -->|No| Z["No memory changes"]
    F -->|Yes| G["Check existing memories"]
    G --> H["Merge or save in category Markdown file"]
    H --> I["Update memory index"]
    I --> J["Dream Manager"]

    J --> K{"Actionable improvement?"}
    K -->|No| Z
    K -->|Yes| L["Check existing dreams and deduplicate"]
    L --> M["Create or update dream proposal"]
    M --> N["Dream Validator"]

    N --> O["Review evidence, recurrence, impact and feasibility"]
    O --> P["Log validation findings"]
    P --> Q{"Dream justified?"}
    Q -->|No| R["Reject or defer with reason"]
    Q -->|Yes| S["Request experiment approval"]

    S --> T{"User approves?"}
    T -->|No| R
    T -->|Yes| U["Dream Realiser"]

    U --> V["Plan bounded experiment and rollback"]
    V --> W["Implement and test experiment"]
    W --> X["Log results and compare success metrics"]
    X --> Y{"Successful?"}

    Y -->|No| AA["Record failure and learn"]
    AA --> E

    Y -->|Yes| AB["Request implementation approval"]
    AB --> AC{"Approved?"}
    AC -->|No| R
    AC -->|Yes| AD["Deploy validated capability"]
    AD --> AE["Document capability and archive dream"]
    AE --> E

    R --> AF["Preserve decision in dream archive"]

    classDef memory fill:#164e63,color:#fff,stroke:#0891b2
    classDef dream fill:#4c1d95,color:#fff,stroke:#8b5cf6
    classDef validate fill:#78350f,color:#fff,stroke:#d97706
    classDef realise fill:#14532d,color:#fff,stroke:#16a34a

    class E,G,H,I memory
    class J,L,M dream
    class N,O,P validate
    class U,V,W,X,AD,AE realise
