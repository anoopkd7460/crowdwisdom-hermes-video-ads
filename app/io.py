import json
from .settings import DATA_DIR

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def list_unique_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    allowed = {".txt", ".md", ".json", ".csv"}
    return sorted(p for p in DATA_DIR.rglob("*") if p.is_file() and p.suffix.lower() in allowed)

def read_text_file(path):
    return path.read_text(encoding="utf-8", errors="ignore")[:30000]
