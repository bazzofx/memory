# VML (Visual Memory Language) — Experiment Report

- **Run ID:** EXP-vml / run-20261124-01 (folder named `VML` until 2026-11-25). There's no dream entry; the user asked for this test directly in chat.
- **Date / environment:** 2026-11-24. Windows 10, Python 3.12.6, Pillow 12.3.0. No new dependencies and no network access. Read by Claude Opus 5.5 through the Read tool's vision.
- **Scope:** sandbox only. Nothing in the memory system was converted or changed.

## What was built (prototype)
- **Vocabulary (18 symbols):**
  - **6 node shapes for kinds**, with a tint: fact = rectangle, action = pill, decision = diamond, tool = hexagon, issue = octagon, outcome = ellipse.
  - **7 relation styles** (line + head + colour): causes = solid black triangle, fixes = solid green tee, requires = dotted blue open head, part_of = grey diamond head, supersedes = purple double line, contradicts = red dashed with an X, evidence_for = orange dashed with a dot.
  - **5 status badges:** verified ✓, hypothesis ?, rejected ✗, pending …, risk !.
  - See `sandbox/legend.png`.
- **Renderer:** a layered layout with dummy nodes for long edges, written in Pillow (`sandbox/vml.py`).
- **Capsule:** exact facts and refs as JSON in a PNG `iTXt` chunk (`vml-capsule`, zlib). It's metadata, not steganography.

## Method
- **Blind random graphs:** 4 of them (6/8, 10/13, 16/21 and 24/31 nodes/edges), with random labels, kinds, statuses and relations. Ground truth and answers went to separate files that I didn't open until scoring.
- **Order of work:** I read the legend, then each image, wrote a full transcription, then answered 6 generated questions per graph: relation type, direct effects, incoming relation, status filter, kind, and a multi-hop causal chain.
- **Scoring:** by script.
- **Markdown arm:** the same graph as a `## Nodes` / `## Relations` list. Reading it is exact by construction, so the comparison is cost and practicality, not accuracy.
- **Capsule:** round-trip with a hash check, overhead, and survival through common re-encodes.
- **Real memory:** the DREAM-001 story as a diagram with a capsule (`sandbox/dream001.png`, `.md`).

## Results
| Graph | Nodes / edges | Kinds + statuses read right | Edges read right (type + direction) | Questions | Image tokens* | Markdown tokens* | Image ÷ MD |
|---|---|---|---|---|---|---|---|
| g1 | 6 / 8 | 12/12 | 8/8 | 6/6 † | 336 | 138 | 2.4× |
| g2 | 10 / 13 | 20/20 | 13/13 | 6/6 | 554 | 227 | 2.4× |
| g3 | 16 / 21 | 32/32 | 21/21 | 6/6 | 1045 | 335 | 3.1× |
| g4 | 24 / 31 | 48/48 | 31/31 | 6/6 | 1532 | 518 | 3.0× |
| DREAM-001 (real) | 10 / 10 | — | — | — | 485 | 248 graph-only | 2.0× |

\* Estimates. Image tokens ≈ w×h/750 after the API resizes it (g4 was sent downscaled to 1188×967). Markdown tokens ≈ characters/4.

† The script scored g1's q6 as wrong, but this was a generator bug: g1 has no chain of two or more "causes" arrows, and the fallback counted a single direct arrow as "true". My answer (false) matches the question.

**Capsule:**
- Decoded exactly in 4/4 images, hashes matched, and the graph equals the ground truth. Overhead was 390–862 bytes.
- It survives a plain file copy only. It is **stripped** by a Pillow re-save, a resize or a JPEG conversion.
- Vision can't see it, so getting the facts back always takes a decode command.

## Findings
1. **Relationships drawn as symbols are highly legible.** 79/79 edges and 112/112 node attributes were read correctly, including the 24-node graph with many crossings that was downscaled before I saw it. Your core idea, arrows for relationships instead of symbols for sentences, works for vision.
2. **There's no accuracy gain over Markdown for the agent, and it costs 2–3× the tokens.** The Markdown version carries the same information exactly and more cheaply. The cost ratio grows with graph size.
3. **The capsule works but adds friction and fragility.** Each exact fact needs a tool call to decode, and the data vanishes on any re-encode. Markdown already has the facts inline, and a Markdown link back to the source is sturdier than hidden metadata.
4. **Real value: a human overview.** The DREAM-001 diagram shows cause → fix → superseded → contradiction at a glance, which a text list doesn't. That's the strongest use case found here.
5. **Vocabulary fixes needed:** the "pending" glyph (…) is nearly invisible (it was read from the grey colour alone), and long edges in dense graphs make the reader trace lines.

## Limitations / bias
- **The reader isn't independent.** I designed the vocabulary and had the legend fresh in mind, so a cold reader might do worse.
- **Small sample:** n = 4 synthetic graphs + 1 real one, a single reader, and no timing or latency measurement.
- **Not tested:** whether images help with *recall across sessions* (the "subconscious" idea), and how a human reader does with this vocabulary.
- **Not built:** the "subconscious" step that translates Markdown memory into diagrams.

## Conclusion
- **As the agent's primary memory format:** not beneficial for this setup. Accuracy is equal, cost is 2–3× higher, and the capsule is fragile.
- **As a generated, read-only overview for humans, with Markdown as the source of truth:** promising.

## Suggested next step (not done)
If wanted, propose a dream: generate a VML overview image *from* the Markdown memory (e.g. per project or per dream) for human review. Keep the Markdown as the source of truth and link to it instead of using a capsule. Fix the pending glyph first.

## Artifacts
`sandbox/vml.py` (renderer, capsule, generator, scorer), `sandbox/capsule_test.py`, `sandbox/real_dream001.py`, `sandbox/legend.png`, `sandbox/dream001.png|.md`, `sandbox/run/g1–g4.{png,md,questions,truth,trans,answers}.json`
