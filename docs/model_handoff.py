"""Log model handoff reasons on every turn — never log keys or secrets."""
import json
import time
import os

LOG = os.environ.get("MODEL_HANDOFF_LOG", "logs/model-handoff.jsonl")

def log_turn(*, turn_id, model, prev_model, fallback_reason,
             upstream_status, dur_s, tool, aborted, session_id):
    """Log a handoff record. Always writes; caller must supply safe values."""
    rec = {
        "ts": time.time(),
        "session_id": session_id,
        "turn_id": turn_id,
        "model": model,
        "prev_model": prev_model,
        "model_changed": model != prev_model,
        "fallback_reason": fallback_reason,
        "upstream_status": upstream_status,
        "dur_s": round(float(dur_s), 2),
        "tool": tool,
        "aborted": bool(aborted),
    }
    log_dir = os.path.dirname(LOG)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    if rec["model_changed"]:
        print(
            f"[HANDOFF] {prev_model} -> {model} "
            f"reason={fallback_reason} status={upstream_status} "
            f"turn={turn_id} dur={dur_s}s",
            flush=True,
        )
    return rec
