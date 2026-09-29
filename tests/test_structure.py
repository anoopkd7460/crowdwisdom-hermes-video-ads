from pathlib import Path

ROOT = Path(__file__).parents[1]

def test_required_paths():
    for p in ["app", "profiles", "scripts", "data/unique_data", "artifacts"]:
        assert (ROOT / p).exists()

def test_env_example_has_no_real_keys():
    text = (ROOT / ".env.example").read_text()
    assert "your_openrouter_key" in text
    assert "your_apify_token" in text
    assert "your_tavily_key" in text
