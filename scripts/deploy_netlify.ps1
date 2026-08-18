# Publica output/mediakit no Netlify (equivalente ao Drop, com link fixo).
# Uso: .\scripts\deploy_netlify.ps1
# Na primeira vez, abre o browser para login Netlify (grátis).

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Dir = Join-Path $Root "output\mediakit"

if (-not (Test-Path $Dir)) {
    Write-Error "Pasta nao encontrada: $Dir`nRode o build do media kit antes."
}

# Abre direto na raiz do site
$Portfolio = Join-Path $Dir "portfolio.html"
$Index = Join-Path $Dir "index.html"
if ((Test-Path $Portfolio) -and -not (Test-Path $Index)) {
    Copy-Item $Portfolio $Index -Force
}

Push-Location $Root
try {
    npx --yes netlify-cli status 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Login Netlify (autorize no browser)..."
        npx --yes netlify-cli login
    }

    Write-Host "Enviando $Dir ..."
    npx --yes netlify-cli deploy --prod --dir $Dir --create-site tatiana-zacharias-mediakit
    Write-Host "Pronto. Copie a URL 'Website URL' acima."
}
finally {
    Pop-Location
}
