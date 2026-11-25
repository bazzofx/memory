"""VML - Visual Memory Language prototype (experiment only).

18 symbols:
  6 node kinds (shape + tint), 7 relations (line style + head + colour), 5 status badges.
Capsule: exact facts as JSON in a PNG iTXt chunk (keyword 'vml-capsule'), zlib-compressed.

CLI:
  python vml.py legend OUT.png
  python vml.py gen SEED N OUTDIR NAME      -> NAME.png, NAME.md, NAME.questions.json, NAME.truth.json
  python vml.py decode PNG                  -> prints capsule JSON
  python vml.py score TRANSCRIPT.json TRUTH.json [ANSWERS.json]
  python vml.py cost PNG MD                 -> estimated tokens
"""
import json, math, random, struct, sys, zlib, hashlib, os
from PIL import Image, ImageDraw, ImageFont

KINDS = {  # kind: (shape, fill)
    "fact":     ("rect",     "#f1f5f9"),
    "action":   ("pill",     "#dcfce7"),
    "decision": ("diamond",  "#fef9c3"),
    "tool":     ("hexagon",  "#e0e7ff"),
    "issue":    ("octagon",  "#fee2e2"),
    "outcome":  ("ellipse",  "#f3e8ff"),
}
RELS = {  # rel: (colour, style, head)
    "causes":      ("#1f2937", "solid",  "triangle"),
    "fixes":       ("#15803d", "solid",  "tee"),
    "requires":    ("#1d4ed8", "dotted", "open"),
    "part_of":     ("#6b7280", "solid",  "diamond"),
    "supersedes":  ("#7c3aed", "double", "triangle"),
    "contradicts": ("#dc2626", "dashed", "cross"),
    "evidence_for":("#d97706", "dashed", "dot"),
}
STATUS = {  # status: (colour, glyph)
    "verified":   ("#16a34a", "\u2713"),
    "hypothesis": ("#ca8a04", "?"),
    "rejected":   ("#dc2626", "\u2717"),
    "pending":    ("#6b7280", "\u2026"),
    "risk":       ("#ea580c", "!"),
}
FONT_DIR = "C:/Windows/Fonts/"
def font(size, bold=False, sym=False):
    name = "seguisym.ttf" if sym else ("arialbd.ttf" if bold else "arial.ttf")
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()

# ---------------------------------------------------------------- drawing primitives
def node_poly(shape, cx, cy, w, h):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    if shape == "diamond":
        return [(cx, y0 - 8), (x1 + 14, cy), (cx, y1 + 8), (x0 - 14, cy)]
    if shape == "hexagon":
        return [(x0, cy), (x0 + 14, y0), (x1 - 14, y0), (x1, cy), (x1 - 14, y1), (x0 + 14, y1)]
    if shape == "octagon":
        c = 10
        return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]
    return None

def draw_node(d, shape, fill, cx, cy, w, h, label, status, f):
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    if shape == "rect":
        d.rectangle(box, fill=fill, outline="#111827", width=2)
    elif shape == "pill":
        d.rounded_rectangle(box, radius=h / 2, fill=fill, outline="#111827", width=2)
    elif shape == "ellipse":
        d.ellipse([box[0] - 10, box[1] - 4, box[2] + 10, box[3] + 4], fill=fill, outline="#111827", width=2)
    else:
        d.polygon(node_poly(shape, cx, cy, w, h), fill=fill, outline="#111827", width=2)
    d.text((cx, cy), label, fill="#111827", font=f, anchor="mm")
    if status:
        col, glyph = STATUS[status]
        bx, by, r = box[2] + 2, box[1] - 2, 11
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col, outline="white", width=2)
        d.text((bx, by + 1), glyph, fill="white", font=font(15, sym=True), anchor="mm")

def styled_line(d, pts, colour, style, width=2):
    segs = list(zip(pts, pts[1:]))
    if style == "double":
        for off in (-2.5, 2.5):
            for (x0, y0), (x1, y1) in segs:
                L = math.hypot(x1 - x0, y1 - y0) or 1
                nx, ny = -(y1 - y0) / L * off, (x1 - x0) / L * off
                d.line([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny)], fill=colour, width=2)
        return
    if style == "solid":
        d.line(pts, fill=colour, width=width, joint="curve")
        return
    on, off = (3, 5) if style == "dotted" else (10, 6)
    for (x0, y0), (x1, y1) in segs:
        L = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < L:
            t2 = min(t + on, L)
            d.line([(x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L), (x0 + (x1 - x0) * t2 / L, y0 + (y1 - y0) * t2 / L)], fill=colour, width=width + (1 if style == "dotted" else 0))
            t = t2 + off

def head(d, tip, frm, colour, kind):
    (tx, ty), (fx, fy) = tip, frm
    a = math.atan2(ty - fy, tx - fx)
    ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    if kind == "triangle":
        d.polygon([(tx, ty), (tx - 14 * ux + 6 * px, ty - 14 * uy + 6 * py), (tx - 14 * ux - 6 * px, ty - 14 * uy - 6 * py)], fill=colour)
    elif kind == "open":
        d.line([(tx - 13 * ux + 7 * px, ty - 13 * uy + 7 * py), (tx, ty), (tx - 13 * ux - 7 * px, ty - 13 * uy - 7 * py)], fill=colour, width=3)
    elif kind == "tee":
        d.line([(tx - 2 * ux + 10 * px, ty - 2 * uy + 10 * py), (tx - 2 * ux - 10 * px, ty - 2 * uy - 10 * py)], fill=colour, width=4)
    elif kind == "diamond":
        d.polygon([(tx, ty), (tx - 9 * ux + 6 * px, ty - 9 * uy + 6 * py), (tx - 18 * ux, ty - 18 * uy), (tx - 9 * ux - 6 * px, ty - 9 * uy - 6 * py)], fill=colour)
    elif kind == "dot":
        d.ellipse([tx - 6 * ux - 6, ty - 6 * uy - 6, tx - 6 * ux + 6, ty - 6 * uy + 6], fill=colour)

def midpoint(pts):
    tot = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    acc = 0
    for a, b in zip(pts, pts[1:]):
        L = math.dist(a, b)
        if acc + L >= tot / 2:
            t = (tot / 2 - acc) / (L or 1)
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        acc += L
    return pts[0]

# ---------------------------------------------------------------- layout (simple Sugiyama)
def layout(g):
    ids = [n["id"] for n in g["nodes"]]
    layer = {i: 0 for i in ids}
    for _ in ids:
        for e in g["edges"]:
            layer[e["dst"]] = max(layer[e["dst"]], layer[e["src"]] + 1)
    chains = []
    for k, e in enumerate(g["edges"]):
        chain = [e["src"]]
        for L in range(layer[e["src"]] + 1, layer[e["dst"]]):
            dummy = f"_d{k}_{L}"
            layer[dummy] = L
            chain.append(dummy)
        chain.append(e["dst"])
        chains.append(chain)
    nl = max(layer.values()) + 1
    rows = [[v for v in layer if layer[v] == L] for L in range(nl)]
    parents = {}
    for c in chains:
        for a, b in zip(c, c[1:]):
            parents.setdefault(b, []).append(a)
            parents.setdefault(a, [])
    pos = {}
    for sweep in range(4):
        for L, row in enumerate(rows):
            for i, v in enumerate(row):
                pos.setdefault(v, i)
            if L:
                row.sort(key=lambda v: sum(pos[p] for p in parents.get(v, [])) / len(parents[v]) if parents.get(v) else pos[v])
            for i, v in enumerate(row):
                pos[v] = i
    return layer, rows, chains

def render(g, path, capsule=None, scale=1.0):
    f = font(15)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    size = {}
    for n in g["nodes"]:
        w = tmp.textlength(n["label"], font=f) + 34
        size[n["id"]] = (max(w, 90), 36)
    layer, rows, chains = layout(g)
    gapx, gapy, dummy_w = 46, 120, 16
    rowW = [sum(size.get(v, (dummy_w, 0))[0] for v in r) + gapx * (len(r) - 1) for r in rows]
    W = int(max(rowW) + 120)
    H = int(len(rows) * gapy + 60)
    xy = {}
    for L, r in enumerate(rows):
        x = (W - rowW[L]) / 2
        for v in r:
            w = size.get(v, (dummy_w, 0))[0]
            xy[v] = (x + w / 2, 60 + L * gapy)
            x += w + gapx
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    nodes = {n["id"]: n for n in g["nodes"]}
    # ports: spread outgoing/incoming along bottom/top edges
    outs, ins = {}, {}
    for k, c in enumerate(chains):
        outs.setdefault(c[0], []).append(k)
        ins.setdefault(c[-1], []).append(k)
    def port(v, k, lst, top):
        cx, cy = xy[v]
        w, h = size[v]
        ks = sorted(lst[v], key=lambda kk: xy[chains[kk][1 if not top else -2]][0])
        i = ks.index(k)
        span = min(w * 0.7, 24 * (len(ks) - 1))
        dx = -span / 2 + (span / (len(ks) - 1) if len(ks) > 1 else 0) * i
        dy = -h / 2 - (8 if nodes[v]["kind"] == "decision" else 0) if top else h / 2 + (8 if nodes[v]["kind"] == "decision" else 0)
        return (cx + dx, cy + dy)
    for k, (e, c) in enumerate(zip(g["edges"], chains)):
        colour, style, hd = RELS[e["rel"]]
        pts = [port(c[0], k, outs, False)] + [xy[v] for v in c[1:-1]] + [port(c[-1], k, ins, True)]
        if hd != "cross":
            tip = pts[-1]
            pts_line = pts[:-1] + [(tip[0], tip[1] - 3)]
        else:
            pts_line = pts
        styled_line(d, pts_line, colour, style)
        if hd == "cross":
            mx, my = midpoint(pts)
            d.line([(mx - 7, my - 7), (mx + 7, my + 7)], fill=colour, width=4)
            d.line([(mx - 7, my + 7), (mx + 7, my - 7)], fill=colour, width=4)
        else:
            head(d, pts[-1], pts[-2], colour, hd)
    for n in g["nodes"]:
        shape, fill = KINDS[n["kind"]]
        cx, cy = xy[n["id"]]
        draw_node(d, shape, fill, cx, cy, *size[n["id"]], n["label"], n.get("status"), f)
    if scale != 1.0:
        img = img.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    img.save(path)
    if capsule is not None:
        embed_capsule(path, capsule)
    return img.size

# ---------------------------------------------------------------- capsule (PNG iTXt)
def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

def embed_capsule(path, obj):
    raw = open(path, "rb").read()
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")
    obj_hash = hashlib.sha256(payload).hexdigest()
    data = b"vml-capsule\x00" + b"\x01\x00" + b"\x00" + b"\x00" + zlib.compress(payload, 9)
    iend = raw.rfind(b"IEND") - 4
    open(path, "wb").write(raw[:iend] + _chunk(b"iTXt", data) + raw[iend:])
    return obj_hash

def decode_capsule(path):
    raw = open(path, "rb").read()
    i = 8
    while i < len(raw):
        (n,) = struct.unpack(">I", raw[i:i + 4])
        tag, data = raw[i + 4:i + 8], raw[i + 8:i + 8 + n]
        if tag == b"iTXt" and data.startswith(b"vml-capsule\x00"):
            body = data[len(b"vml-capsule\x00"):]
            comp, body = body[0], body[2:]
            lang_end = body.index(b"\x00"); body = body[lang_end + 1:]
            kw_end = body.index(b"\x00"); body = body[kw_end + 1:]
            return json.loads(zlib.decompress(body) if comp else body)
        i += 12 + n
    return None

# ---------------------------------------------------------------- markdown baseline
def to_markdown(g):
    lab = {n["id"]: n["label"] for n in g["nodes"]}
    out = ["## Nodes"]
    for n in g["nodes"]:
        out.append(f"- {n['label']} [{n['kind']}]" + (f" ({n['status']})" if n.get("status") else ""))
    out.append("## Relations")
    for e in g["edges"]:
        out.append(f"- {lab[e['src']]} --{e['rel']}--> {lab[e['dst']]}")
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- random graphs + questions
WORDS = ("cache index token hook queue parser schema router fixture shell quote socket voice timer budget "
         "kernel driver sensor ledger import export render buffer cursor matrix vector signal filter batch "
         "worker session prompt corpus memory dream policy layer bridge portal anchor beacon cipher delta "
         "ember falcon garnet harbor island jungle lantern meadow nectar orbit pebble quartz raven summit").split()

def random_graph(seed, n):
    r = random.Random(seed)
    labels = set()
    while len(labels) < n:
        labels.add(f"{r.choice(WORDS)} {r.choice(WORDS)}")
    labels = sorted(labels)
    r.shuffle(labels)
    nodes = []
    for i, lab in enumerate(labels):
        st = r.choice(list(STATUS)) if r.random() < 0.5 else None
        nodes.append({"id": f"N{i}", "label": lab, "kind": r.choice(list(KINDS)), "status": st})
    m = round(1.3 * n)
    pairs = set()
    edges = []
    relw = ["causes"] * 4 + ["fixes"] * 2 + ["requires"] * 2 + ["part_of", "supersedes", "contradicts", "evidence_for", "evidence_for"]
    while len(edges) < m:
        a, b = sorted(r.sample(range(n), 2))
        if abs(a - b) > max(3, n // 3) or (a, b) in pairs:
            continue
        pairs.add((a, b))
        edges.append({"src": f"N{a}", "dst": f"N{b}", "rel": r.choice(relw)})
    return {"nodes": nodes, "edges": edges}

def questions(g, seed):
    r = random.Random(seed + 999)
    lab = {n["id"]: n["label"] for n in g["nodes"]}
    out_by = lambda v, rel: sorted(lab[e["dst"]] for e in g["edges"] if e["src"] == v and e["rel"] == rel)
    in_by = lambda v, rel: sorted(lab[e["src"]] for e in g["edges"] if e["dst"] == v and e["rel"] == rel)
    qs, ans = [], {}
    e = r.choice(g["edges"])
    qs.append({"id": "q1", "q": f"What is the relation between '{lab[e['src']]}' and '{lab[e['dst']]}'? Answer {{rel, src, dst}}."})
    ans["q1"] = {"rel": e["rel"], "src": lab[e["src"]], "dst": lab[e["dst"]]}
    cands = [n["id"] for n in g["nodes"] if out_by(n["id"], "causes")]
    v = r.choice(cands)
    qs.append({"id": "q2", "q": f"List everything '{lab[v]}' directly causes."}); ans["q2"] = out_by(v, "causes")
    for rel in ("fixes", "requires", "evidence_for"):
        cands = [n["id"] for n in g["nodes"] if in_by(n["id"], rel)]
        if cands:
            v = r.choice(cands)
            qs.append({"id": "q3", "q": f"List every node with a '{rel}' relation pointing to '{lab[v]}'."}); ans["q3"] = in_by(v, rel)
            break
    present = sorted({n["status"] for n in g["nodes"] if n["status"]})
    s = r.choice(present)
    qs.append({"id": "q4", "q": f"List every node whose status is '{s}'."}); ans["q4"] = sorted(n["label"] for n in g["nodes"] if n["status"] == s)
    v = r.choice(g["nodes"])
    qs.append({"id": "q5", "q": f"What kind is '{v['label']}'?"}); ans["q5"] = v["kind"]
    causes = {}
    for e in g["edges"]:
        if e["rel"] == "causes":
            causes.setdefault(e["src"], []).append(e["dst"])
    def reach(a):
        seen, stack = set(), list(causes.get(a, []))
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x); stack += causes.get(x, [])
        return seen
    multi = [(a, b) for a in causes for b in reach(a) if b not in causes.get(a, [])]
    if multi:
        a, b = r.choice(multi); yes = True
    else:
        ids = [n["id"] for n in g["nodes"]]; a, b = r.sample(ids, 2); yes = b in reach(a)
    qs.append({"id": "q6", "q": f"Does '{lab[a]}' lead to '{lab[b]}' through a chain of 2+ 'causes' arrows? Answer true/false."}); ans["q6"] = yes
    return qs, ans

# ---------------------------------------------------------------- scoring
def norm(s):
    return " ".join(str(s).lower().split())

def score(trans, truth, answers=None):
    g = truth["graph"]
    lab = {n["id"]: norm(n["label"]) for n in g["nodes"]}
    tn = {norm(k): v for k, v in trans.get("nodes", {}).items()}
    kind_ok = sum(1 for n in g["nodes"] if tn.get(norm(n["label"]), {}).get("kind") == n["kind"])
    stat_ok = sum(1 for n in g["nodes"] if (tn.get(norm(n["label"]), {}).get("status") or None) == (n["status"] or None))
    def key(s, rel, d):
        return (rel, *sorted((s, d))) if rel == "contradicts" else (rel, s, d)
    T = {key(lab[e["src"]], e["rel"], lab[e["dst"]]) for e in g["edges"]}
    P = {key(norm(e[0]), e[1], norm(e[2])) for e in trans.get("edges", [])}
    Tc = {tuple(sorted((lab[e["src"]], lab[e["dst"]]))) for e in g["edges"]}
    Pc = {tuple(sorted((norm(e[0]), norm(e[2])))) for e in trans.get("edges", [])}
    tp = len(T & P)
    res = {
        "nodes": len(g["nodes"]), "edges": len(T),
        "kind_acc": round(kind_ok / len(g["nodes"]), 3), "status_acc": round(stat_ok / len(g["nodes"]), 3),
        "edge_precision": round(tp / (len(P) or 1), 3), "edge_recall": round(tp / len(T), 3),
        "connection_recall": round(len(Tc & Pc) / len(Tc), 3),
        "edge_errors": {"missed": sorted(map(list, T - P)), "wrong": sorted(map(list, P - T))},
    }
    if answers:
        a, ok = truth["answers"], {}
        for q, want in a.items():
            got = answers.get(q)
            if isinstance(want, list):
                ok[q] = sorted(map(norm, got or [])) == sorted(map(norm, want))
            elif isinstance(want, dict):
                ok[q] = got is not None and norm(got.get("rel")) == norm(want["rel"]) and (
                    (norm(got.get("src")), norm(got.get("dst"))) == (norm(want["src"]), norm(want["dst"]))
                    or want["rel"] == "contradicts")
            else:
                ok[q] = (str(got).lower() == str(want).lower())
        res["questions"] = ok
        res["question_acc"] = round(sum(ok.values()) / len(ok), 3)
    return res

def image_tokens(path):
    w, h = Image.open(path).size
    s = min(1.0, 1568 / max(w, h), math.sqrt(1_150_000 / (w * h)))
    w2, h2 = int(w * s), int(h * s)
    return math.ceil(w2 * h2 / 750), (w, h), (w2, h2)

# ---------------------------------------------------------------- legend
def legend(path):
    g = {"nodes": [], "edges": []}
    W, H = 1180, 470
    img = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(img); f = font(15); fb = font(17, bold=True)
    d.text((20, 14), "VML legend - nodes (kind)", font=fb, fill="#111827")
    for i, (k, (shape, fill)) in enumerate(KINDS.items()):
        draw_node(d, shape, fill, 100 + i * 185, 75, 120, 36, k, None, f)
    d.text((20, 125), "Relations (arrow points from cause/part/fixer to effect/whole/target)", font=fb, fill="#111827")
    for i, (rel, (col, style, hd)) in enumerate(RELS.items()):
        y = 165 + i * 30
        a, b = (40, y), (240, y)
        styled_line(d, [a, (b[0] - 3, y)] if hd != "cross" else [a, b], col, style)
        if hd == "cross":
            mx = 140; d.line([(mx - 7, y - 7), (mx + 7, y + 7)], fill=col, width=4); d.line([(mx - 7, y + 7), (mx + 7, y - 7)], fill=col, width=4)
        else:
            head(d, b, a, col, hd)
        d.text((260, y), f"{rel}  ({style} {col_name(col)}, {hd} head)" if hd != "cross" else f"{rel}  (dashed red, X in middle, no direction)", font=f, fill="#111827", anchor="lm")
    d.text((720, 125), "Status badges (top-right of node)", font=fb, fill="#111827")
    for i, (s, (col, glyph)) in enumerate(STATUS.items()):
        y = 170 + i * 40
        d.ellipse([730, y - 11, 752, y + 11], fill=col, outline="white", width=2)
        d.text((741, y + 1), glyph, fill="white", font=font(15, sym=True), anchor="mm")
        d.text((765, y), s, font=f, fill="#111827", anchor="lm")
    img.save(path)

def col_name(c):
    return {"#1f2937": "black", "#15803d": "green", "#1d4ed8": "blue", "#6b7280": "grey", "#7c3aed": "purple", "#dc2626": "red", "#d97706": "orange"}[c]

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "legend":
        legend(sys.argv[2])
    elif cmd == "gen":
        seed, n, outdir, name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
        os.makedirs(outdir, exist_ok=True)
        g = random_graph(seed, n)
        qs, ans = questions(g, seed)
        cap = {"vml": 1, "graph": g, "facts": {n["id"]: f"exact fact for {n['label']} (seed {seed})" for n in g["nodes"]}}
        p = os.path.join(outdir, name)
        size = render(g, p + ".png", capsule=cap)
        open(p + ".md", "w", encoding="utf-8").write(to_markdown(g))
        json.dump(qs, open(p + ".questions.json", "w"), indent=1)
        json.dump({"graph": g, "answers": ans, "capsule_sha": hashlib.sha256(json.dumps(cap, ensure_ascii=False, sort_keys=True).encode()).hexdigest()},
                  open(p + ".truth.json", "w"), indent=1)
        print(f"{name}: {n} nodes, {len(g['edges'])} edges, image {size}")
    elif cmd == "decode":
        print(json.dumps(decode_capsule(sys.argv[2]), indent=1)[:2000])
    elif cmd == "score":
        tr, tt = json.load(open(sys.argv[2])), json.load(open(sys.argv[3]))
        an = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else None
        print(json.dumps(score(tr, tt, an), indent=1))
    elif cmd == "cost":
        t, raw, sent = image_tokens(sys.argv[2])
        md = open(sys.argv[3], encoding="utf-8").read()
        print(f"image ~{t} tokens (raw {raw}, sent as {sent}); markdown {len(md)} chars ~{math.ceil(len(md) / 4)} tokens")
