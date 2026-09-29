$ErrorActionPreference = "Stop"

$profiles = @(
    @{ Name="cwt-ads-manager"; Role="Ads Manager. Research Meta ads with Apify, identify recent creative patterns, pains, ICPs and hooks. Save JSON artifacts." },
    @{ Name="cwt-script-agent"; Role="Script Agent. Use fresh Tavily research and proprietary CrowdWisdom data to create three cinematic 30-60 second storyboards." },
    @{ Name="cwt-video-agent"; Role="Video Agent. Turn the selected storyboard into an OpenMontage cinematic production and verify the final MP4." }
)

foreach ($p in $profiles) {
    try {
        hermes profile create $p.Name --description $p.Role
    } catch {}

    $home = Join-Path $HOME ".hermes\profiles\$($p.Name)"
    New-Item -ItemType Directory -Force -Path $home | Out-Null

    Copy-Item "profiles\$($($p.Name))\SOUL.md" "$home\SOUL.md" -Force
    Copy-Item "profiles\$($($p.Name))\config.yaml" "$home\config.yaml" -Force
    Copy-Item ".env" "$home\.env" -Force
}

hermes kanban init
Write-Host "Hermes profiles and Kanban initialized."
Write-Host "Run: hermes dashboard"
