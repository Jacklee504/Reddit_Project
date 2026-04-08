import json
from pathlib import Path
from datetime import datetime, timezone


def load_processed_post_ids(state_path):
    path = Path(state_path)
    if not path.exists():
        return set()

    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("processed_post_ids", []))


def mark_processed(state_path, post_id):
    path = Path(state_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"processed_post_ids": [], "updated_at": None}

    processed = set(data.get("processed_post_ids", []))
    processed.add(str(post_id))
    data["processed_post_ids"] = sorted(processed)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
