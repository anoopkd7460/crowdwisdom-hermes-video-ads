import json
import subprocess

def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode:
        print(p.stderr)
        raise SystemExit(p.returncode)
    return p.stdout

run(["hermes", "kanban", "init"])

ads = run([
    "hermes", "kanban", "create", "Research winning trading ads",
    "--assignee", "cwt-ads-manager",
    "--priority", "1",
    "--body",
    "Run python -m app.research ads. Analyze recent Meta ads in the trading/market-intelligence niche. Save artifacts/ads/meta_ads_raw.json, working_ads.json and ad_insights.json. Do not claim conversion success without performance evidence.",
    "--json"
])
ads_id = json.loads(ads)["id"]

script = run([
    "hermes", "kanban", "create", "Create three cinematic ad storyboards",
    "--assignee", "cwt-script-agent",
    "--parent", ads_id,
    "--priority", "1",
    "--body",
    "Run python -m app.research pains, then python -m app.script_agent. Use data/unique_data. Save all_scripts.json and selected_storyboard.json. Run python -m app.validate.",
    "--json"
])
script_id = json.loads(script)["id"]

video = run([
    "hermes", "kanban", "create", "Produce final cinematic video",
    "--assignee", "cwt-video-agent",
    "--parent", script_id,
    "--priority", "1",
    "--body",
    "Run python -m app.video_agent. Then use OpenMontage's cinematic pipeline to render the selected storyboard. Save final MP4 under artifacts/video/final/ and verify it."
])
print("Hermes pipeline:", ads_id, "->", script_id, "-> final video task")
print(video)
