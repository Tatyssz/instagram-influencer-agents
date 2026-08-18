# Publica output/mediakit no repo Tatyssz/portifolio (pasta ugc/) e faz push.
# Depois: deploy no Netlify tatyssz-portifolio (painel ou scripts/deploy-netlify.ps1 no repo portifolio).
# Uso: .\scripts\sync_portfolio_netlify.ps1
# Requer: gh auth + clone em ..\portifolio

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Src = Join-Path $Root "output\mediakit"
$Repo = Join-Path (Split-Path -Parent $Root) "portifolio"
$Dst = Join-Path $Repo "ugc"

if (-not (Test-Path $Src)) {
    Write-Error "Build nao encontrado: $Src"
}
if (-not (Test-Path $Repo)) {
    Write-Error "Clone o repo portifolio ao lado deste projeto: gh repo clone Tatyssz/portifolio `"$Repo`""
}

$Portfolio = Join-Path $Src "portfolio.html"
$Index = Join-Path $Src "index.html"
if ((Test-Path $Portfolio) -and -not (Test-Path $Index)) {
    Copy-Item $Portfolio $Index -Force
}

if (Test-Path $Dst) { Remove-Item $Dst -Recurse -Force }
New-Item -ItemType Directory -Path $Dst | Out-Null
robocopy $Src $Dst /E /XF estimativa-metricas.json estimativa-metricas.md canva-conteudo-pronto.txt media-kit.html media-kit.pdf Tatiana-Zacharias-Media-Kit.pdf _redirects /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null

Push-Location $Repo
try {
    git add ugc README.md
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Nada novo para publicar."
        exit 0
    }
    git commit -m "Publica portfólio UGC Beauty (media kit)"
    git push origin main
    Write-Host "GitHub atualizado. Dispare deploy em:"
    Write-Host "  https://app.netlify.com/projects/tatyssz-portifolio/deploys"
    Write-Host "URL final: https://tatyssz-portifolio.netlify.app/ugc/"
}
finally {
    Pop-Location
}
