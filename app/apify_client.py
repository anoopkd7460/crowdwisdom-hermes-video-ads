import requests

from .settings import APIFY_API_TOKEN, APIFY_ACTOR_ID, APIFY_COUNTRY

BASE = "https://api.apify.com/v2"


def run_meta_ads(search_queries, limit=10):
    """
    Run the Meta Ad Library scraper through Apify.

    Args:
        search_queries: List of keywords to search.
        limit: Maximum number of ads to return.

    Returns:
        List of raw ad records.
    """

    if not APIFY_API_TOKEN:
        raise RuntimeError("APIFY_API_TOKEN is required")

    payload = {
        "searchQueries": search_queries,
        "country": APIFY_COUNTRY,
        "maxAds": limit,
        "activeStatus": "all",
        "sortMode": "newest",
    }

    url = (
        f"{BASE}/acts/{APIFY_ACTOR_ID}"
        "/run-sync-get-dataset-items"
    )

    response = requests.post(
        url,
        params={"token": APIFY_API_TOKEN},
        json=payload,
        timeout=180,
    )

    if not response.ok:
        print("Apify response:")
        print(response.text)

    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data[:limit]

    if isinstance(data, dict):
        items = data.get("items", [])

        if isinstance(items, list):
            return items[:limit]

    return []


def normalize_ad(row):
    def first(*keys):
        for key in keys:
            value = row.get(key)

            if value not in (None, "", []):
                return value

        return None

    return {
        "id": first(
            "adArchiveID",
            "adArchiveId",
            "ad_archive_id",
            "id",
        ),

        "page_name": first(
            "pageName",
            "page_name",
            "advertiser",
        ),

        "headline": first(
            "headline",
            "title",
        ),

        "body": first(
            "bodyText",
            "body",
            "adText",
            "text",
            "copy",
        ),

        "description": first(
            "description",
        ),

        "cta": first(
            "ctaText",
            "cta",
            "callToAction",
        ),

        "start_date": first(
            "startDate",
            "start_date",
            "adDeliveryStartTime",
        ),

        "end_date": first(
            "endDate",
            "end_date",
            "adDeliveryStopTime",
        ),

        "platforms": first(
            "platforms",
            "publisherPlatforms",
            "platform",
        ),

        "media": first(
            "media",
            "videoUrls",
            "imageUrls",
            "snapshotUrl",
            "adSnapshotUrl",
        ),

        "ad_url": first(
            "adUrl",
        ),

        "landing_page_url": first(
            "landingPageUrl",
        ),

        "is_active": first(
            "isActive",
        ),

        "raw": row,
    }