"""Encode the real DREAM-001 story as a VML diagram + capsule, plus the Markdown equivalent."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vml

N = lambda i, label, kind, status=None: {"id": i, "label": label, "kind": kind, "status": status}
g = {"nodes": [
    N("L", "Bash tool halves \\\\", "issue", "verified"),
    N("Q", "quoted-heredoc advice", "fact", "rejected"),
    N("S", "'\\' SyntaxError", "issue", "verified"),
    N("J", "C:\\ai invalid JSON", "issue", "verified"),
    N("P", "byte-level probe", "action", "verified"),
    N("R", "issues.md rule v2", "fact", "verified"),
    N("W", "Write file, run by path", "action", "verified"),
    N("H", "inline-script guard", "tool", "pending"),
    N("C", "409-call corpus test", "action", "verified"),
    N("O", "fewer retry loops", "outcome", "hypothesis"),
],
"edges": [
    {"src": "L", "dst": "S", "rel": "causes"},
    {"src": "L", "dst": "J", "rel": "causes"},
    {"src": "P", "dst": "L", "rel": "evidence_for"},
    {"src": "L", "dst": "Q", "rel": "contradicts"},
    {"src": "R", "dst": "Q", "rel": "supersedes"},
    {"src": "R", "dst": "W", "rel": "requires"},
    {"src": "W", "dst": "S", "rel": "fixes"},
    {"src": "W", "dst": "J", "rel": "fixes"},
    {"src": "C", "dst": "H", "rel": "evidence_for"},
    {"src": "W", "dst": "O", "rel": "causes"},
]}
# P->L would point upward in a layered layout; order nodes so layering is natural.
facts = {
    "L": "Claude Code 2.1.329 / Windows Git Bash: a run of N backslashes becomes ceil(N/2) unless followed by '\"', even in '...' and <<'EOF'. Verified 2026-11-23.",
    "Q": "Old belief: quoted heredocs protect backslashes. Refuted by L.",
    "S": "Corpus id 361: f.split('\\\\') arrived as f.split('\\') -> SyntaxError.",
    "J": "Corpus ids 55/376: printf fixture C:\\\\ai -> C:\\ai -> invalid JSON (silent, exit 0).",
    "P": "printf '%s' 'A\\\\B' | od -An -tx1 -> 41 5c 42 (one backslash).",
    "R": "C:/ai/memories/categories/issues.md -> Shell & scripting, entry 1 (2026-11-22, corrected 2026-11-23).",
    "W": "Write the script/fixture with the Write tool, then run it by path.",
    "H": "Sandbox prototype, not deployed: dreams/experiments/DREAM-001/run-20261123-01/sandbox/inline-script-guard.cjs",
    "C": "Recall 4/4, warnings on good calls 4.0% vs 23.1% naive; p95 150 ms.",
    "O": "Expected benefit, not yet measured in the field.",
}
refs = {"report": "C:/ai/memories/dreams/experiments/DREAM-001/run-20261123-01/report.md",
        "archive": "C:/ai/memories/dreams/archive.md#DREAM-001"}
here = os.path.dirname(os.path.abspath(__file__))
png = os.path.join(here, "dream001.png")
vml.render(g, png, capsule={"vml": 1, "graph": g, "facts": facts, "refs": refs})
md = vml.to_markdown(g) + "\n## Facts\n" + "\n".join(f"- {k}: {v}" for k, v in facts.items()) + "\n## Refs\n" + "\n".join(f"- {k}: {v}" for k, v in refs.items()) + "\n"
open(os.path.join(here, "dream001.md"), "w", encoding="utf-8").write(md)
print(json.dumps(vml.decode_capsule(png)["facts"]["L"]))
t, raw, sent = vml.image_tokens(png)
print(f"image ~{t} tokens {raw}; markdown (graph+facts+refs) {len(md)} chars ~{len(md)//4} tokens; graph-only md ~{len(vml.to_markdown(g))//4} tokens")
