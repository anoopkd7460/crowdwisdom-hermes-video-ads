import json

from .io import load_json, save_json
from .llm import ask
from .settings import ARTIFACTS
from .research import unique_context


def build():
    # Load the completed Ads research.
    insights = load_json(
        ARTIFACTS / "ads/ad_insights.json"
    )

    # Load Tavily/fresh research if it exists.
    # The research module may save this under one of these names.
    research_candidates = [
        ARTIFACTS / "ads/research.json",
        ARTIFACTS / "research.json",
        ARTIFACTS / "scripts/research.json",
    ]

    research = {}

    for path in research_candidates:
        if path.exists():
            research = load_json(path)
            print(f"Loaded fresh research from: {path}")
            break

    # CrowdWisdom-specific data.
    unique = unique_context()

    # Keep the prompt small enough for the free model.
    context = {
        "ad_insights": insights,
        "fresh_research": research,
        "proprietary_data": unique,
    }

    context_text = json.dumps(
        context,
        ensure_ascii=False,
        indent=2,
    )

    # Limit context size to avoid very large free-model requests.
    context_text = context_text[:30000]

    prompt = f"""
Create THREE differentiated 30-60 second cinematic video-ad
storyboards for CrowdWisdomTrading.

Product:
https://crowdwisdomtrading.com

Audience:
Retail traders/investors dealing with information overload
and uncertainty.

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
- scenes
- cta
- factual_claims_used
- unsupported_claims_to_avoid

Each ad must contain 6-10 scenes.

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

- The first 2-3 seconds must be a strong visual hook.
- This is a movie-style video, not a text-heavy advertisement.
- Use cinematic tension, human stakes and visual metaphors.
- Make all three concepts genuinely different.
- Do not invent CrowdWisdom numbers.
- Use proprietary numbers only when explicitly present
  in the supplied data.
- Never copy competitor wording.
- Keep narration concise and natural for a 30-60 second video.
- Make scenes visually practical for AI/video generation.
- Do not make unsupported financial promises.
- Do not guarantee profits or investment returns.

Concept requirements:

pain_icp:
Focus on the trader's real information overload,
uncertainty and difficulty separating useful signals
from noise.

unique_data:
Use only CrowdWisdom-specific information explicitly
present in the supplied proprietary data.

solution:
Show how CrowdWisdom can help the target audience
make sense of market information. Avoid unsupported
claims about guaranteed performance.

Return ONLY valid JSON in this exact structure:

{{
  "ads": [
    {{
      "type": "pain_icp",
      "title": "...",
      "strategic_angle": "...",
      "target_icp": "...",
      "core_pain": "...",
      "visual_hook": "...",
      "promise": "...",
      "duration_seconds": 45,
      "scenes": [],
      "cta": "...",
      "factual_claims_used": [],
      "unsupported_claims_to_avoid": []
    }},
    {{
      "type": "unique_data",
      "title": "...",
      "strategic_angle": "...",
      "target_icp": "...",
      "core_pain": "...",
      "visual_hook": "...",
      "promise": "...",
      "duration_seconds": 45,
      "scenes": [],
      "cta": "...",
      "factual_claims_used": [],
      "unsupported_claims_to_avoid": []
    }},
    {{
      "type": "solution",
      "title": "...",
      "strategic_angle": "...",
      "target_icp": "...",
      "core_pain": "...",
      "visual_hook": "...",
      "promise": "...",
      "duration_seconds": 45,
      "scenes": [],
      "cta": "...",
      "factual_claims_used": [],
      "unsupported_claims_to_avoid": []
    }}
  ]
}}

RESEARCH CONTEXT:

{context_text}
"""

    print("Generating three cinematic storyboards...")
    print("Using the free OpenRouter model. This may take a few minutes.")

    result = ask(prompt, temperature=0.8)

    if not isinstance(result, dict):
        raise RuntimeError(
            "LLM did not return a JSON object."
        )

    if "ads" not in result:
        raise RuntimeError(
            "LLM response does not contain an 'ads' field."
        )

    if len(result["ads"]) != 3:
        raise RuntimeError(
            f"Expected 3 ads, got {len(result['ads'])}."
        )

    # Create output directory.
    scripts_dir = ARTIFACTS / "scripts"
    scripts_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_json(
        scripts_dir / "all_scripts.json",
        result,
    )

    for ad in result["ads"]:
        safe = "".join(
            c.lower() if c.isalnum() else "_"
            for c in ad["type"]
        )[:40]

        save_json(
            scripts_dir / f"script_{safe}.json",
            ad,
        )

    # First storyboard is used as the selected storyboard.
    save_json(
        scripts_dir / "selected_storyboard.json",
        result["ads"][0],
    )

    print()
    print("SUCCESS: Three storyboards saved.")
    print()
    print("Generated:")
    print("  artifacts/scripts/all_scripts.json")
    print("  artifacts/scripts/script_pain_icp.json")
    print("  artifacts/scripts/script_unique_data.json")
    print("  artifacts/scripts/script_solution.json")
    print("  artifacts/scripts/selected_storyboard.json")


if __name__ == "__main__":
    build()