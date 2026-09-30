import sys
import json
from datetime import datetime, timedelta, timezone

from .apify_client import run_meta_ads, normalize_ad
from .tavily_client import search_month
from .llm import ask
from .io import save_json, list_unique_data, read_text_file
from .settings import ARTIFACTS

NICHES = [
    "AI trading",
    "stock market prediction",
    "trading signals",
    "market intelligence",
    "investor prediction",
]

def ads():
    raw = run_meta_ads(NICHES, limit=1)
    save_json(ARTIFACTS / "ads/meta_ads_raw.json", raw)

    ads = [normalize_ad(x) for x in raw]
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    recent = []

    for ad in ads:
        value = ad.get("start_date")
        if not value:
            ad["date_status"] = "undated"
            recent.append(ad)
            continue

        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt >= cutoff:
                recent.append(ad)
        except Exception:
            ad["date_status"] = "unparseable"
            recent.append(ad)

    save_json(ARTIFACTS / "ads/working_ads.json", recent)

    prompt = """
Analyze these recent/active Meta ads in the trading and market-intelligence niche.

Return JSON with:
- niche_patterns
- recurring_pains
- ICPs
- hook_patterns
- creative_concepts
- offer_patterns
- what_to_avoid
- ranked_ad_patterns

Do not claim actual conversion success unless performance evidence exists in the source.
Do not copy wording. Extract patterns only.

ADS:
""" + json.dumps(recent[:60], ensure_ascii=False)

    insights = ask(prompt, temperature=0.7)
    save_json(ARTIFACTS / "ads/ad_insights.json", insights)
    print("Ads research complete.")

def pains():
    queries = [
        "retail traders information overload prediction market signals pain points",
        "trader decision fatigue market uncertainty investor psychology",
        "how retail traders use crowd sentiment prediction signals",
        "trading mistakes caused by noise conflicting market signals",
    ]
    output = []
    for q in queries:
        output.append({"query": q, "response": search_month(q, max_results=5)})
    save_json(ARTIFACTS / "scripts/research.json", output)
    print("Fresh Tavily research complete.")

def unique_context():
    docs = []
    for p in list_unique_data():
        docs.append({"file": p.name, "content": read_text_file(p)})
    save_json(ARTIFACTS / "scripts/unique_data_context.json", docs)
    return docs

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "ads"
    if command == "ads":
        ads()
    elif command == "pains":
        pains()
    elif command == "unique":
        unique_context()
    else:
        raise SystemExit("Use: ads | pains | unique")
