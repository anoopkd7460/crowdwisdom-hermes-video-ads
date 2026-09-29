import requests
from .settings import APIFY_API_TOKEN, APIFY_ACTOR_ID, APIFY_COUNTRY

BASE = "https://api.apify.com/v2"

def run_meta_ads(search_queries, limit=100):
    if not APIFY_API_TOKEN:
        raise RuntimeError("APIFY_API_TOKEN is required")

    payload = {
        "searchQueries": search_queries,
        "country": APIFY_COUNTRY,
        "proxyConfig": {"useApifyProxy": True},
    }

    url = f"{BASE}/acts/{APIFY_ACTOR_ID}/run-sync-get-dataset-items"
    r = requests.post(
        url,
        params={"token": APIFY_API_TOKEN},
        json=payload,
        timeout=180,
    )
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list):
        return data[:limit]
    return data.get("items", data)[:limit]

def normalize_ad(row):
    def first(*keys):
        for key in keys:
            value = row.get(key)
            if value not in (None, "", []):
                return value
        return None

    return {
        "id": first("adArchiveID", "adArchiveId", "id"),
        "page_name": first("pageName", "page_name", "advertiser"),
        "headline": first("headline", "title"),
        "body": first("body", "adText", "text", "copy"),
        "cta": first("cta", "callToAction"),
        "start_date": first("startDate", "start_date", "adDeliveryStartTime"),
        "end_date": first("endDate", "end_date"),
        "platforms": first("platforms", "platform"),
        "media": first("media", "snapshotUrl", "adSnapshotUrl"),
        "raw": row,
    }
