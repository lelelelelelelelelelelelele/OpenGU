#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$source = Join-Path $PSScriptRoot 'REPORT.md'
$text = Get-Content -Raw -Encoding UTF8 -LiteralPath $source
$hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLowerInvariant()
$body = (ConvertFrom-Markdown -InputObject $text).Html
$body = $body.Replace('<table>', '<div class="table-scroll"><table>').Replace('</table>', '</table></div>')
$html = @"
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="source-sha256" content="$hash"><title>EXP-014 · Paper appendix: request-generation cost</title><style>body{margin:0;background:#f2f5f7;color:#203144;font:16px/1.8 system-ui,'Microsoft YaHei',sans-serif}main{max-width:1120px;margin:30px auto;padding:34px;background:white}h1{font-size:27px}h2{font-size:22px;border-top:1px solid #ced8e1;padding-top:20px;margin-top:30px}a{color:#1b6285}p{overflow-wrap:anywhere}.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:680px;font-size:14px}th,td{border:1px solid #ced8e1;padding:10px;text-align:left}th{background:#eaf1f6}code{font-size:12px;overflow-wrap:anywhere}footer{border-top:1px solid #ced8e1;margin-top:30px;font-size:12px;overflow-wrap:anywhere}@media(max-width:800px){main{margin:0;padding:20px}}</style></head><body><main>$body<footer><a href="REPORT.md">Markdown source</a><br>Source SHA-256: $hash</footer></main></body></html>
"@
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot 'REPORT.html'), $html, [System.Text.UTF8Encoding]::new($false))
[pscustomobject]@{ SourceSHA256=$hash; Tables=([regex]::Matches($body,'<table>')).Count }
