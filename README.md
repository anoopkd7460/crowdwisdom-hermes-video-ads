# CrowdWisdomTrading — Hermes Video Ads Agent

Python + Hermes Agent multi-agent system for the CrowdWisdomTrading internship assessment.

## Pipeline

`Ads Manager -> Script Agent -> Video Agent`

Hermes Kanban cards use parent dependencies, so the next worker starts only after the previous worker completes.

### 1. Ads Manager
- Apify Meta Ads Library scraper
- last-30-day research window
- OpenRouter analysis
- saves raw ads, recent ads and creative insights as JSON

### 2. Script Agent
Creates exactly 3 original 30–60 sec cinematic concepts:
- `pain_icp`
- `unique_data`
- `solution`

Uses:
- fresh Tavily research with `time_range="month"`
- CrowdWisdom proprietary files in `data/unique_data/`
- Apify-derived creative patterns
- OpenRouter for structured storyboard generation

### 3. Video Agent
- creates an OpenMontage cinematic production brief
- uses the OpenMontage `cinematic` pipeline
- expects a real 30–60 sec MP4
- final render goes to `artifacts/video/final/`

## Setup

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Install Hermes Agent using the official Hermes Agent installer/documentation, then:

```powershell
hermes --version
hermes kanban init
```

Put the permitted proprietary CrowdWisdom examples from the assessment under:

```text
data/unique_data/
```

Do NOT commit confidential files to a public repository.

Create the Hermes profiles:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_hermes.ps1
```

Create the Kanban pipeline:

```powershell
python scripts\create_kanban.py
```

Open the board:

```powershell
hermes dashboard
```

## Service smoke test

```powershell
python scripts\smoke_test.py
```

Run research manually if you want to inspect artifacts before dispatch:

```powershell
python -m app.research ads
python -m app.research pains
```

## Important interpretation

The system deliberately does NOT claim that "most successful" ads were identified unless the scraper provides performance evidence. It calls the output "working/recent ads" when the available source supports recency/activity, and the LLM extracts patterns from them.

## Submission artifacts

```text
artifacts/
├── ads/
│   ├── meta_ads_raw.json
│   ├── working_ads.json
│   └── ad_insights.json
├── scripts/
│   ├── research.json
│   ├── unique_data_context.json
│   ├── all_scripts.json
│   └── selected_storyboard.json
└── video/
    ├── openmontage_prompt.txt
    └── final/
        └── <final-video>.mp4
```

## Creative direction

Default creative direction: **"The Signal" — a market-intelligence thriller.**

Cold open:
A trader is seconds away from a decision while multiple screens flash conflicting signals.

Escalation:
The screens become an overwhelming wall of noise.

Visual metaphor:
The noise collapses into one coherent signal.

Reveal:
CrowdWisdomTrading is introduced as the intelligence layer helping traders see collective prediction signals rather than simply adding another noisy dashboard.

End:
A restrained brand reveal and CTA.

The final video should work even if the viewer ignores on-screen text.

## GitHub submission

Do not publish API tokens in `.env`, README, source files, or git history.

The company asked for the tokens so they can rerun the code. Put them in the submission email or another private channel agreed with the company. Never commit them to GitHub.
