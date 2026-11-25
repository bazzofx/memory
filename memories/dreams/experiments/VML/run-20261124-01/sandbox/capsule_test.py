"""Capsule tests: exact round-trip, hash match, overhead, and survival through common re-encodes."""
import json, hashlib, os, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vml

run = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run")
for g in ("g1", "g2", "g3", "g4"):
    p = os.path.join(run, g + ".png")
    truth = json.load(open(os.path.join(run, g + ".truth.json")))
    cap = vml.decode_capsule(p)
    h = hashlib.sha256(json.dumps(cap, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    graph_ok = cap["graph"] == truth["graph"]
    raw_size = os.path.getsize(p)
    # size without capsule: re-render to temp
    tmp = p + ".nocap.png"
    vml.render(truth["graph"], tmp)
    nocap = os.path.getsize(tmp)
    os.remove(tmp)
    print(f"{g}: decode={'OK' if cap else 'NONE'} hash_match={h == truth['capsule_sha']} graph_exact={graph_ok} "
          f"facts={len(cap['facts'])} png={raw_size}B capsule_overhead={raw_size - nocap}B")

p = os.path.join(run, "g3.png")
out = os.path.join(run, "_survival")
os.makedirs(out, exist_ok=True)
cases = {}
shutil.copy(p, os.path.join(out, "copy.png")); cases["plain file copy"] = "copy.png"
Image.open(p).save(os.path.join(out, "pil_resave.png")); cases["re-save with Pillow (default)"] = "pil_resave.png"
im = Image.open(p); im.save(os.path.join(out, "pil_resave_pnginfo.png"), pnginfo=None); cases["re-save, pnginfo=None"] = "pil_resave_pnginfo.png"
Image.open(p).resize((400, 531)).save(os.path.join(out, "resized.png")); cases["resize + save"] = "resized.png"
Image.open(p).convert("RGB").save(os.path.join(out, "as.jpg"), quality=90); cases["convert to JPEG"] = "as.jpg"
for name, f in cases.items():
    fp = os.path.join(out, f)
    try:
        ok = vml.decode_capsule(fp) is not None if fp.endswith(".png") else False
    except Exception as e:
        ok = f"error {e}"
    print(f"survives {name:32s}: {ok}")
