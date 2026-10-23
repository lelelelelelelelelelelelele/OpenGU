[CmdletBinding()]
param(
    [switch]$ValidateOverleaf
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$writingRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Join-Path $writingRoot 'latex'
$buildRoot = Join-Path $projectRoot 'build'
$latexmk = (Get-Command latexmk -ErrorAction Stop).Source
foreach ($program in @('pdflatex', 'bibtex', 'kpsewhich')) {
    $null = Get-Command $program -ErrorAction Stop
}
foreach ($required in @('acmart.cls', 'ACM-Reference-Format.bst')) {
    $resolved = & kpsewhich $required
    if ($LASTEXITCODE -ne 0 -or -not $resolved) {
        throw "Missing TeX dependency: $required"
    }
}

function Build-Project {
    param([string]$SourceDirectory, [string]$OutputDirectory)
    $null = New-Item -ItemType Directory -Path $OutputDirectory -Force
    $savedLocale = [Environment]::GetEnvironmentVariable('LC_ALL', 'Process')
    try {
        # Use a locale recognized by Perl on Windows without changing user settings.
        $env:LC_ALL = 'C'
        Push-Location -LiteralPath $SourceDirectory
        try {
            & $latexmk '-pdf' '-interaction=nonstopmode' '-halt-on-error' '-file-line-error' '-no-shell-escape' "-outdir=$OutputDirectory" 'main.tex' 2>&1 |
                Out-File -LiteralPath (Join-Path $OutputDirectory 'build-command.txt') -Encoding utf8
            if ($LASTEXITCODE -ne 0) {
                throw "LaTeX build failed; see $OutputDirectory/build-command.txt and main.log"
            }
        }
        finally {
            Pop-Location
        }
    }
    finally {
        [Environment]::SetEnvironmentVariable('LC_ALL', $savedLocale, 'Process')
    }
    $pdf = Join-Path $OutputDirectory 'main.pdf'
    if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) {
        throw "Build did not produce $pdf"
    }
    $log = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $OutputDirectory 'main.log')
    if ($log -match 'There were undefined references|There were undefined citations|Citation .+ undefined|Reference .+ undefined|Rerun to get cross-references right') {
        throw "Unresolved citations or cross-references; see $OutputDirectory/main.log"
    }
    Write-Output "Built: $pdf"
}

Build-Project -SourceDirectory $projectRoot -OutputDirectory $buildRoot
if ($ValidateOverleaf) {
    $repositoryRoot = Split-Path -Parent $writingRoot
    $overleafRoot = Join-Path $repositoryRoot 'report/paper/overleaf'
    Build-Project -SourceDirectory $overleafRoot -OutputDirectory (Join-Path $buildRoot 'overleaf-validation')
}
