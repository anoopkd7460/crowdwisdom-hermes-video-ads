import json
from pathlib import Path
from .io import load_json
from .settings import ARTIFACTS, OPENMONTAGE_DIR

def build_openmontage_brief():
    storyboard = load_json(ARTIFACTS / "scripts/selected_storyboard.json")

    prompt = f"""
Create a 30–60 second CINEMATIC advertisement for CrowdWisdomTrading.

Use the OpenMontage CINEMATIC pipeline.

The result must feel like a premium movie trailer:
- real motion where appropriate
- cinematic sound design
- strong pacing
- restrained on-screen text
- no slideshow feeling
- no text-ad structure

Brand:
CrowdWisdomTrading

URL:
https://crowdwisdomtrading.com

Storyboard:
{json.dumps(storyboard, indent=2, ensure_ascii=False)}

Production rules:
- Preserve the storyboard narrative beats.
- Make the visual hook land in the first 2–3 seconds.
- Do not invent product statistics.
- Keep runtime between 30 and 60 seconds.
- Master in 16:9.
- Verify audio, duration, captions, scene continuity and final visual quality.
- Save the final MP4 under artifacts/video/final/.

Read OpenMontage's AGENT_GUIDE.md and the cinematic pipeline definition before execution.
"""

    target = ARTIFACTS / "video/openmontage_prompt.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(prompt, encoding="utf-8")

    print(f"Brief written: {target}")
    print(f"OpenMontage directory: {Path(OPENMONTAGE_DIR).resolve()}")
    print("Next: run the OpenMontage cinematic pipeline using the brief.")

if __name__ == "__main__":
    build_openmontage_brief()
