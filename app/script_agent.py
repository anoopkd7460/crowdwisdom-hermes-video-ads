import json
from .io import load_json, save_json
from .llm import ask
from .settings import ARTIFACTS
from .research import unique_context

def build():
    insights = load_json(ARTIFACTS / "ads/ad_insights.json")
    research = load_json(ARTIFACTS / "scripts/research.json")
    unique = unique_context()

    context = {
        "ad_insights": insights,
        "fresh_research": research,
        "proprietary_data": unique,
    }

    prompt = """
Create THREE differentiated 30–60 second cinematic video-ad storyboards for CrowdWisdomTrading.

Product:
https://crowdwisdomtrading.com

Audience:
Retail traders/investors dealing with information overload and uncertainty.

Create exactly these concepts:
1. pain_icp
2. unique_data
3. solution

Each ad must contain:
- type
- title
- strategic_angle
- target_icp
- core_pain
- visual_hook
- promise
- duration_seconds
- scenes: 6–10 scene objects
- cta
- factual_claims_used
- unsupported_claims_to_avoid

Every scene object must contain:
- start_sec
- end_sec
- visual
- camera
- narration
- on_screen_text
- sound_design
- transition

Creative rules:
- The first 2–3 seconds must be a visual hook.
- This is a movie-style video, not a text ad.
- Use cinematic tension, human stakes and visual metaphors.
- Make the three concepts genuinely different.
- Do not invent CrowdWisdom numbers.
- Use proprietary numbers only if explicitly present in the provided files.
- Never copy competitor wording.

Return:
{"ads":[...three objects...]}

CONTEXT:
""" + json.dumps(context, ensure_ascii=False)[:90000]

    result = ask(prompt, temperature=0.9)
    save_json(ARTIFACTS / "scripts/all_scripts.json", result)

    for ad in result["ads"]:
        safe = "".join(c.lower() if c.isalnum() else "_" for c in ad["type"])[:40]
        save_json(ARTIFACTS / f"scripts/script_{safe}.json", ad)

    save_json(ARTIFACTS / "scripts/selected_storyboard.json", result["ads"][0])
    print("Three storyboards saved.")

if __name__ == "__main__":
    build()
