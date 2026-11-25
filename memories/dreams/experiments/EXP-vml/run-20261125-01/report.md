# VML cyber look — legibility test (run-20261125-01)

Date: 2026-11-25. Question: can the diagram be restyled (dark neon, glow, scanlines, seeded jitter) without losing information?
Change under test: `look="cyber"` in `update-subconscious/scripts/vml.py`. Symbols are unchanged; `causes` goes from black to white. Decoration is seeded.

## Method
Random graphs from the earlier VML generator (graph and answers saved to files, not shown). One reader (me), no legend changes. Each image was transcribed (node kind and status, every edge), then scored by script and quizzed with 6 questions.

## Results
| Round | Graph (nodes / edges) | Node kind and status | Edges recalled / precision | Questions |
| --- | --- | --- | --- | --- |
| 1, seed 77 | 10 / 13 | 100% | 13/13, 100% | 6/6 |
| 1, seed 78 | 16 / 21 | 100% | 19/21 (90.5%), 95% | 5/6 |
| after fix, seed 91 | 14 / 18 | 100% | 18/18, 100% | 6/6 |
| after fix, seed 92 | 20 / 26 | 100% | 26/26, 100% | 6/6 |

## Defect found and fixed
Round 1, seed 78: two chained green "fixes" arrows (raven driver → cipher vector → lantern delta) read as one long arrow passing behind the node. The first tee was drawn before the node, and the ellipse covered it. This is not specific to the cyber look: the plain look had the same draw order.
Fix (two changes): (1) arrowheads are drawn after all nodes, (2) top ports of `outcome` ellipses sit 4 px higher. Re-tested on fresh seeds (rounds after fix); no misses.

## Other checks
- DREAM-001 entry rebuilt in cyber look; two rebuilds produced identical PNG bytes (seeded decoration).
- `check` passes (capsule matches the spec).

## Limits
- One reader who also wrote the vocabulary; the seed-78 misread shows the test can fail.
- Small sample: 4 graphs, 59 edges; the 2 missed edges were before the fix and the fixed rounds were different graphs, not a re-read of seed 78.
- Glow and scanlines at the sizes used were fine; very dense graphs (over 25 nodes) were not tested. The skill caps entries at 16 nodes.
- Image scaling by a viewer was not tested.
- The legend is still drawn in the plain look.

Artifacts: `sandbox/` (generator script, images, transcriptions, answers).
