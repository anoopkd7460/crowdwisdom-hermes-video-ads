from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

ARTIFACTS = ROOT / "artifacts"
DATA_DIR = ROOT / "data" / "unique_data"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID","webdatalabs~meta-ad-library-scraper")
APIFY_COUNTRY = os.getenv("APIFY_COUNTRY", "US")
CROWDWISDOM_URL = os.getenv("CROWDWISDOM_URL", "https://crowdwisdomtrading.com")
OPENMONTAGE_DIR = os.getenv("OPENMONTAGE_DIR", "../OpenMontage")

def require(*names):
    missing = [n for n in names if not globals().get(n)]
    if missing:
        raise RuntimeError("Missing configuration: " + ", ".join(missing))
