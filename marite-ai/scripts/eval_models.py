"""Evaluate installed Ollama models for Mārīte: Latvian quality, JSON schema compliance, latency.

Usage:  python scripts/eval_models.py [model ...]
Writes nothing; prints a report. Copy results into docs/BENCHMARKS.md.
"""
import json
import subprocess
import sys
import time

import httpx

OLLAMA = "http://127.0.0.1:11434"

SCHEMA = {
    "type": "object",
    "properties": {
        "emotion": {"type": "string", "enum": ["neutral", "happy", "encouraging", "thinking", "confused"]},
        "latvian": {"type": "string"},
        "english": {"type": "string"},
        "correction": {
            "type": "object",
            "properties": {
                "required": {"type": "boolean"},
                "original": {"type": "string"},
                "corrected": {"type": "string"},
                "explanation": {"type": "string"},
            },
            "required": ["required", "original", "corrected", "explanation"],
        },
    },
    "required": ["emotion", "latvian", "english", "correction"],
}

SYSTEM = (
    "You are Mārīte, a friendly ladybird who teaches Latvian to English speakers (level A1). "
    "Reply in JSON. 'latvian' is your short reply in correct Latvian (max 2 sentences). "
    "'english' is its English translation. If the learner's Latvian has a mistake, set correction.required=true "
    "and give the corrected sentence and a one-sentence English explanation; otherwise required=false "
    "and empty strings. Never invent Latvian words."
)

CASES = [
    ("greet", "Labdien! Kā tev iet?"),
    ("mistake", "Es esmu labi."),  # should be "Man iet labi" / "Man ir labi" style correction
    ("teach", "How do I say 'I would like a coffee, please' in Latvian?"),
    ("numbers", "Teach me the numbers one to five in Latvian."),
]


def gpu_mem() -> str:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        return out
    except Exception:
        return "?"


def run(model: str) -> None:
    print(f"\n===== {model} =====")
    with httpx.Client(timeout=300) as c:
        t0 = time.perf_counter()
        c.post(f"{OLLAMA}/api/generate", json={"model": model, "prompt": "", "keep_alive": "5m"})
        print(f"load: {time.perf_counter() - t0:.1f}s  gpu: {gpu_mem()}")
        ps = c.get(f"{OLLAMA}/api/ps").json()
        for m in ps.get("models", []):
            print(f"  size={m.get('size', 0) / 1e9:.1f}GB vram={m.get('size_vram', 0) / 1e9:.1f}GB")
        for name, text in CASES:
            body = {
                "model": model,
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
                "format": SCHEMA,
                "stream": False,
                "think": False,
                "keep_alive": "5m",
                "options": {"temperature": 0.3, "num_ctx": 4096, "num_predict": 400},
            }
            t0 = time.perf_counter()
            r = c.post(f"{OLLAMA}/api/chat", json=body)
            dt = time.perf_counter() - t0
            if r.status_code != 200:
                print(f"[{name}] HTTP {r.status_code}: {r.text[:200]}")
                continue
            data = r.json()
            content = data["message"]["content"]
            toks = data.get("eval_count", 0)
            tps = toks / (data.get("eval_duration", 1) / 1e9)
            try:
                obj = json.loads(content)
                ok = all(k in obj for k in SCHEMA["required"])
            except json.JSONDecodeError:
                obj, ok = content, False
            print(f"[{name}] {dt:.1f}s {toks} tok {tps:.1f} tok/s valid={ok}")
            print("   ", json.dumps(obj, ensure_ascii=False)[:600])
        c.post(f"{OLLAMA}/api/generate", json={"model": model, "prompt": "", "keep_alive": 0})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for m in sys.argv[1:] or ["qwen3.5:latest", "gemma4:latest", "ornith:9b"]:
        run(m)
