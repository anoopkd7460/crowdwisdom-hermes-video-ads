import json
import re
import requests
from .settings import OPENROUTER_API_KEY, OPENROUTER_MODEL, CROWDWISDOM_URL

SYSTEM = """
You are the senior creative strategist for CrowdWisdomTrading.
Extract marketing patterns, not wording. Never copy competitor ads.
The final work must be cinematic, original, emotionally compelling and visual.
Never invent proprietary CrowdWisdom numbers.
Return valid JSON whenever JSON is requested.
""".strip()

def _json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}|\[.*\]", text, re.S)
        if not m:
            raise
        return json.loads(m.group(0))

def ask(prompt, temperature=0.8):
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is required")
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": CROWDWISDOM_URL,
            "X-OpenRouter-Title": "CrowdWisdomTrading Video Ads Agent",
        },
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    return _json(r.json()["choices"][0]["message"]["content"])
