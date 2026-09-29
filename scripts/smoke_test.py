import os
from dotenv import load_dotenv

load_dotenv()
required = ["OPENROUTER_API_KEY", "APIFY_API_TOKEN", "TAVILY_API_KEY"]
missing = [x for x in required if not os.getenv(x)]

if missing:
    raise SystemExit("Missing: " + ", ".join(missing))

print("All required environment variables are present.")
