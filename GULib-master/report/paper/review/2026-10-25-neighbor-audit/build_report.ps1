$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$sourcePath = Join-Path $PSScriptRoot 'REPORT.md'
$markdown = Get-Content -LiteralPath $sourcePath -Raw -Encoding UTF8
$sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
$body = (ConvertFrom-Markdown -InputObject $markdown).Html
$body = $body -replace '<table>', '<div class="table-scroll"><table>' -replace '</table>', '</table></div>'
$template = @'
<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="report-source-sha256" content="__HASH__"><title>近邻原文独立核对 · Q1–Q3与Fig.3/4</title>
<style>
:root{color-scheme:light;--ink:#182536;--muted:#526578;--line:#d9e2ea;--accent:#145f76}
*{box-sizing:border-box}body{margin:0;background:#eff3f6;color:var(--ink);font:16px/1.85 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1160px;margin:28px auto;padding:40px 46px 60px;background:#fff;border:1px solid var(--line);border-radius:12px}h1{font-size:30px;line-height:1.45;margin:0 0 22px}h2{font-size:24px;margin:44px 0 16px;padding-top:14px;border-top:2px solid var(--line)}h3{font-size:20px;margin:30px 0 10px}p{margin:12px 0}a{color:var(--accent);text-underline-offset:3px}strong{font-weight:680}li{margin:8px 0}.table-scroll{overflow-x:auto;margin:20px 0;border:1px solid var(--line);border-radius:7px}table{width:100%;border-collapse:collapse;min-width:690px;font-size:14px;line-height:1.7}th{background:#eaf1f5;text-align:left;vertical-align:top}th,td{padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border:0}tr:nth-child(even) td{background:#f8fafb}code{font-size:.88em;overflow-wrap:anywhere}footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);font-size:13px;color:var(--muted);overflow-wrap:anywhere}body>main>p:nth-of-type(2){padding:18px 20px;background:#edf5f6;border-left:4px solid var(--accent)}
@media(max-width:760px){main{margin:0;padding:24px 18px;border-radius:0;overflow-wrap:anywhere}h1{font-size:25px}h2{font-size:21px}table{min-width:680px}}@media print{body{background:#fff}main{border:0;margin:0;max-width:none;padding:0}table{min-width:0;font-size:10px}.table-scroll{overflow:visible}h2,h3{break-after:avoid}tr{break-inside:avoid}}
</style></head><body><main>__BODY__<footer>由 REPORT.md 生成。源 SHA-256：__HASH__。原文覆盖与统计解释以可编辑源稿和来源回执为准。</footer></main></body></html>
'@
$html = $template.Replace('__HASH__', $sourceHash).Replace('__BODY__', $body)
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot 'REPORT.html'), $html, [System.Text.UTF8Encoding]::new($false))
Write-Output "Generated REPORT.html from source SHA-256 $sourceHash"
