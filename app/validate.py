import json
from pathlib import Path
from .settings import ARTIFACTS

def validate_storyboard():
    p = ARTIFACTS / "scripts/selected_storyboard.json"
    data = json.loads(p.read_text(encoding="utf-8"))

    duration = int(data["duration_seconds"])
    assert 30 <= duration <= 60
    assert 6 <= len(data["scenes"]) <= 10

    for scene in data["scenes"]:
        assert scene["end_sec"] > scene["start_sec"]
        assert scene["visual"]
        assert scene["narration"]

    return True

if __name__ == "__main__":
    print("Storyboard valid:", validate_storyboard())
