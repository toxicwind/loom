#!/usr/bin/env python3
"""Read-only latency audit: recompute from ALL segments, never first-N."""
import json, pathlib, re, argparse, sys

def load(path):
    d = json.loads(pathlib.Path(path).read_text())
    return next((v for v in d.values() if isinstance(v, list)), [])

def stats(name, segs):
    rows = []
    for s in segs:
        if str(s.get("role", "assistant")).lower() != "assistant":
            continue
        dur_raw = s.get("dur")
        if dur_raw is None:
            continue
        rows.append(float(str(dur_raw).replace("s", "")))
    b = {
        "<2s": sum(1 for x in rows if x < 2),
        "2-5s": sum(1 for x in rows if 2 <= x < 5),
        "5-19s": sum(1 for x in rows if 5 <= x < 19),
        ">19s": sum(1 for x in rows if x >= 19),
    }
    return {
        "name": name,
        "n": len(rows),
        "total_s": round(sum(rows), 1),
        "avg_s": round(sum(rows)/len(rows), 2) if rows else 0,
        "max_s": max(rows) if rows else 0,
        "buckets": b,
    }

ap = argparse.ArgumentParser(description="Latency audit from fleet/audit JSON + MD")
ap.add_argument("--fleet", required=True, help="Fleet session JSON")
ap.add_argument("--audit", required=True, help="Audit session JSON")
ap.add_argument("--md", required=True, help="Session export MD")
args = ap.parse_args()

f = stats("fleet", load(args.fleet))
u = stats("audit", load(args.audit))
md = pathlib.Path(args.md).read_text(errors="ignore")
md_n = len(re.findall(r"^#{1,6}\s+.*assistant", md, re.I | re.M))

result = {
    "fleet": f,
    "audit": u,
    "md_headers": md_n,
    "md_minus_json": md_n - u["n"],
    "avg_ratio": round(u["avg_s"] / f["avg_s"], 2) if f["avg_s"] else 0,
}
print(json.dumps(result, indent=2))
sys.exit(0)
