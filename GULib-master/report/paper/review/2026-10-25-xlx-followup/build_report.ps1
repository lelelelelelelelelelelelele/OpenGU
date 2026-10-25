$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'REPORT.md'
$hash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
$body = (ConvertFrom-Markdown -InputObject (Get-Content -LiteralPath $source -Raw -Encoding UTF8)).Html
$body = $body -replace '<table>','<div class="scroll"><table>' -replace '</table>','</table></div>'
$template = @'
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="report-source-sha256" content="__HASH__"><title>XLX进展核查与Weak Accept路线</title><style>
*{box-sizing:border-box}body{margin:0;background:#eff3f6;color:#182536;font:16px/1.85 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1120px;margin:28px auto;padding:38px 44px 56px;background:white;border:1px solid #d9e2ea;border-radius:12px;overflow-wrap:anywhere}h1{font-size:30px;line-height:1.45;margin:0 0 20px}h2{font-size:23px;margin-top:36px;padding-top:16px;border-top:2px solid #d9e2ea}a{color:#145f76;text-underline-offset:3px}.scroll{overflow-x:auto;margin:20px 0;border:1px solid #d9e2ea;border-radius:7px}table{width:100%;min-width:680px;border-collapse:collapse;font-size:14px;line-height:1.75}th,td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid #d9e2ea}th{background:#eaf1f5}tr:nth-child(even) td{background:#f8fafb}p{margin:12px 0}li{margin:9px 0}main>p:nth-of-type(2){padding:18px 20px;background:#edf5f6;border-left:4px solid #145f76}footer{margin-top:38px;padding-top:16px;border-top:1px solid #d9e2ea;font-size:12px;color:#526578}code{font-size:.9em}@media(max-width:760px){main{margin:0;border-radius:0;padding:24px 18px}h1{font-size:25px}h2{font-size:21px}}@media print{body{background:white}main{border:0;margin:0;padding:0;max-width:none}table{min-width:0;font-size:10px}.scroll{overflow:visible}tr{break-inside:avoid}}
</style></head><body><main>__BODY__<footer>REPORT.md为源；源SHA-256：__HASH__。本页是进展核查，不是科学验收。</footer></main></body></html>
'@
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'REPORT.html'),$template.Replace('__HASH__',$hash).Replace('__BODY__',$body),[Text.UTF8Encoding]::new($false))
Write-Output "Generated REPORT.html; source $hash"
