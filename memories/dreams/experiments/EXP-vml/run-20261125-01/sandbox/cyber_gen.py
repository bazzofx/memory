"""Render blind cyber-look graphs (truth saved, not printed) and the DREAM-001 spec in cyber look."""
import importlib.util, json, os, sys

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

new = load("newvml", "C:/_web_apps_2025/kairo/.claude/skills/update-subconscious/scripts/vml.py")
old = load("oldvml", "C:/ai/memories/dreams/experiments/EXP-vml/run-20261124-01/sandbox/vml.py")
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for seed, n, name in ((91, 14, "d1"), (92, 20, "d2")):
    g = old.random_graph(seed, n)
    qs, ans = old.questions(g, seed)
    size = new.render(g, os.path.join(out, name + ".png"), look="cyber", seed=seed)
    json.dump(qs, open(os.path.join(out, name + ".questions.json"), "w"), indent=1)
    json.dump({"graph": g, "answers": ans}, open(os.path.join(out, name + ".truth.json"), "w"))
    print(name, "rendered", size, "(truth saved, not shown)")
spec = json.load(open(sys.argv[2], encoding="utf-8"))
size = new.render({"nodes": spec["nodes"], "edges": spec["edges"]}, os.path.join(out, "dream001-cyber.png"),
                  title=spec["id"] + " - " + spec["title"], look="cyber", seed=1)
print("dream001-cyber", size)
