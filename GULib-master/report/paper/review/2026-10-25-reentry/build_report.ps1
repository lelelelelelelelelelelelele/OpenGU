#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$utf8 = [Text.UTF8Encoding]::new($false)
$sourcePaths = @(
    'C:/Users/ADMIN/.codex/visualizations/2026/10/24/01a16ea7-c8f2-7ba2-bbf1-06bd2e7649f2/review-preparation-20261025/REPORT.md',
    'E:/project/OpenGU-DocMap/40_论文写作/40_论文写作.md',
    'E:/project/OpenGU-DocMap/40_论文写作/06_结果.md',
    (Join-Path $repo 'report/paper/overleaf/main.tex'),
    (Join-Path $repo 'report/paper/overleaf/sections/results.tex'),
    (Join-Path $repo 'report/paper/figures/exp080-ratio-response-20261025/REPORT.md'),
    (Join-Path $repo 'report/paper/figures/exp080-ratio-response-20261025/verification.json'),
    (Join-Path $repo 'report/paper/overleaf/figures/citeseer_selector_responses.pdf'),
    (Join-Path $repo 'self/research/analyses/EXP-079/e79r5/RESPONSE_PATTERN_REPORT.md'),
    (Join-Path $repo 'paper_writing/outline/OUTLINE.v8.md'),
    'C:/Users/ADMIN/.codex/worktrees/paper-v1-figures/OpenGU/GULib-master/paper_writing/outline/OUTLINE.v9.md',
    'C:/Users/ADMIN/.codex/worktrees/paper-v1-figures/OpenGU/GULib-master/paper_writing/review/2026-10-25-pre-v1/REPORT.md',
    (Join-Path $repo 'paper_writing/review/2026-10-24-round3/REVIEW_INPUTS.json')
)
$sources = foreach ($path in $sourcePaths) {
    $exists = Test-Path -LiteralPath $path -PathType Leaf
    [ordered]@{path=$path; exists=$exists; sha256=$(if($exists){(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()}else{$null})}
}
function Read-GitObservation([string]$root, [string[]]$gitArguments) {
    $output = @(& git -c "safe.directory=$root" -C $root @gitArguments 2>&1 | ForEach-Object { "$($_)" })
    return [ordered]@{exit_code=$LASTEXITCODE; output=$output}
}
$roots = @(
    (Split-Path -Parent $repo),
    'C:/Users/ADMIN/.codex/worktrees/paper-v1-figures/OpenGU',
    'C:/Users/ADMIN/.codex/worktrees/response-figure-study/OpenGU',
    'C:/Users/ADMIN/.codex/worktrees/round4-integration/OpenGU',
    'E:/project/OpenGU-DocMap'
)
$workspaces = foreach ($root in $roots) {
    if (Test-Path -LiteralPath $root -PathType Container) {
        [ordered]@{path=$root; exists=$true; head=(Read-GitObservation $root @('rev-parse','HEAD')); branch=(Read-GitObservation $root @('branch','--show-current')); tracked_status=(Read-GitObservation $root @('status','--short','--untracked-files=no'))}
    } else { [ordered]@{path=$root; exists=$false} }
}
$inventory = [ordered]@{
    observed_at=[DateTimeOffset]::UtcNow.ToOffset([TimeSpan]::FromHours(8)).ToString('o')
    purpose='入口来源与构建时Git观察，不是冻结论文包；REPORT工作区表为入口编辑前观察。'
    review_input_frozen=$false
    sources=$sources
    workspaces=$workspaces
}
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'SOURCE_INVENTORY.json'), ($inventory | ConvertTo-Json -Depth 12), $utf8)
$style = @'
*{box-sizing:border-box}body{margin:0;background:#f4f5f7;color:#20262d;font:16px/1.85 system-ui,'Microsoft YaHei',sans-serif}main{max-width:1100px;margin:30px auto;padding:40px 48px;background:white;border:1px solid #dce0e5}h1{font-size:28px;line-height:1.5}h2{font-size:21px;margin-top:38px;border-top:1px solid #dce0e5;padding-top:22px}h3{font-size:18px}a{color:#245d87;overflow-wrap:anywhere}blockquote{margin:18px 0;padding:5px 20px;border-left:3px solid #456c8b;background:#f4f7fa}.table-scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px;min-width:650px}td,th{border:1px solid #dce0e5;padding:10px 12px;text-align:left;vertical-align:top}th{background:#edf2f6}li{margin:8px 0}footer{margin-top:36px;color:#626b76;font-size:12px;overflow-wrap:anywhere}code{font-size:.9em;background:#edf2f6;overflow-wrap:anywhere}img{max-width:100%}@media(max-width:700px){main{margin:0;border:0;padding:22px 18px}h1{font-size:24px}}@media print{main{margin:0;padding:0;border:0}body{background:white}table{min-width:0}}
'@
$documents = @((Join-Path $PSScriptRoot 'REPORT.md'), (Join-Path $repo '.claude/handoffs/2026-10-25-062327-paper-session-restart.md'))
foreach ($document in $documents) {
    $markdown = Get-Content -Raw -Encoding UTF8 -LiteralPath $document
    $body = (ConvertFrom-Markdown -InputObject $markdown).Html
    $body = [regex]::Replace($body, 'href="([A-Z]:/[^\"]+)"', 'href="file:///$1"')
    $body = $body.Replace('<table>','<div class="table-scroll"><table>').Replace('</table>','</table></div>')
    $title = [Net.WebUtility]::HtmlEncode((($markdown -split '\r?\n',2)[0] -replace '^#\s+',''))
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $document).Hash.ToLowerInvariant()
    $sourceName = [IO.Path]::GetFileName($document)
    $html = @"
<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="source-sha256" content="$hash"><title>$title</title><style>$style</style></head><body><main>$body<footer>2026-10-25 · <a href="$sourceName">Markdown源</a><br>源SHA-256：$hash<br>由report/paper/review/2026-10-25-reentry/build_report.ps1生成。</footer></main></body></html>
"@
    [IO.File]::WriteAllText([IO.Path]::ChangeExtension($document,'.html'), $html, $utf8)
    Write-Output ([IO.Path]::ChangeExtension($document,'.html'))
}
