from tavily import TavilyClient
from .settings import TAVILY_API_KEY

def search_month(query, max_results=6):
    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is required")

    client = TavilyClient(api_key=TAVILY_API_KEY)
    return client.search(
        query=query,
        search_depth="advanced",
        time_range="month",
        max_results=max_results,
        include_answer=False,
        include_raw_content="markdown",
    )
