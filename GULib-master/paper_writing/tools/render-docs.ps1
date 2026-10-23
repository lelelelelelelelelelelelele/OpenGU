#Requires -Version 7.0
[CmdletBinding()]
param(
    [string[]]$SourcePaths = @('outline/OUTLINE.md', 'latex/ENVIRONMENT.md')
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$writingRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$rootPrefix = $writingRoot + [System.IO.Path]::DirectorySeparatorChar
$utf8 = [System.Text.UTF8Encoding]::new($false)

$style = @'
:root{color-scheme:light;--ink:#24313e;--muted:#667382;--line:#d7e0e7;--accent:#175b80}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f2f5f7;color:var(--ink);font:16px/1.85 system-ui,'Microsoft YaHei',sans-serif}.layout{max-width:1440px;margin:auto;padding:34px 28px 90px;display:grid;grid-template-columns:235px minmax(0,1fr);gap:34px}nav{position:sticky;top:30px;align-self:start;font-size:13px}nav strong{display:block;font-size:17px;line-height:1.5;margin-bottom:14px}nav a{display:block;padding:8px 0;border-bottom:1px solid var(--line);color:var(--muted);text-decoration:none}.meta{color:var(--muted);font-size:13px;overflow-wrap:anywhere}main{min-width:0;padding:40px 46px;background:white;border:1px solid var(--line)}h1{font-size:29px;line-height:1.4;margin:0 0 24px}h2{font-size:22px;line-height:1.5;margin:42px 0 18px;padding-top:16px;border-top:2px solid #b5cbd7;scroll-margin-top:20px}h3{font-size:18px;margin:27px 0 12px}h4{font-size:16px;color:var(--accent);margin:22px 0 10px}p{margin:13px 0}li{margin:8px 0}a{color:var(--accent);text-underline-offset:3px}code{font-size:.87em;background:#edf2f6;padding:2px 5px;border-radius:3px;overflow-wrap:anywhere}pre{padding:16px;background:#edf2f6;overflow:auto}pre code{padding:0;background:none;overflow-wrap:normal}blockquote{border-left:4px solid #b5cbd7;margin:20px 0;padding:1px 20px;color:#3b5263;background:#f5f8fa}.table-scroll{overflow:auto;margin:22px 0}table{border-collapse:collapse;min-width:610px;width:100%;font-size:14px;line-height:1.75}th,td{border:1px solid var(--line);padding:11px 13px;text-align:left;vertical-align:top}th{background:#eaf1f6}tr:nth-child(even) td{background:#f8fafb}img{max-width:100%;height:auto}footer{border-top:1px solid var(--line);padding-top:18px;margin-top:40px;color:var(--muted);font-size:12px;overflow-wrap:anywhere}@media(max-width:960px){.layout{display:block;padding:16px}nav{position:static;margin:0 0 20px}nav a{display:inline-block;margin-right:14px}main{padding:25px 20px}h1{font-size:25px}}@media print{body{background:white}.layout{display:block;padding:0}nav{display:none}main{border:0;padding:0}h2,h3,h4{break-after:avoid}table{font-size:10px;min-width:0}a{color:inherit}}
nav{max-height:calc(100vh - 60px);overflow-y:auto;padding-right:8px}@media(max-width:960px){nav{max-height:none;overflow:visible;padding-right:0}}
'@

foreach ($relativeSource in $SourcePaths) {
    $sourceCandidate = if ([System.IO.Path]::IsPathRooted($relativeSource)) {
        $relativeSource
    } else {
        Join-Path $writingRoot $relativeSource
    }
    $sourcePath = (Resolve-Path -LiteralPath $sourceCandidate).Path
    if (-not $sourcePath.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Source must be inside paper_writing: $sourcePath"
    }
    if ([System.IO.Path]::GetExtension($sourcePath) -ne '.md') {
        throw "Expected a Markdown source: $sourcePath"
    }
    $source = Get-Content -Raw -Encoding UTF8 -LiteralPath $sourcePath
    $rawTitle = ($source -split '\r?\n', 2)[0] -replace '^#\s+', ''
    $title = [System.Net.WebUtility]::HtmlEncode($rawTitle)
    $body = (ConvertFrom-Markdown -InputObject $source).Html
    $navLinks = [System.Collections.Generic.List[string]]::new()
    $body = [regex]::Replace($body, '<h2(?:\s+[^>]*)?>(.*?)</h2>', {
        param($match)
        $sectionId = 'pw-doc-section-' + ($navLinks.Count + 1)
        $navLinks.Add('<a href="#' + $sectionId + '">' + $match.Groups[1].Value + '</a>')
        return '<h2 id="' + $sectionId + '">' + $match.Groups[1].Value + '</h2>'
    }, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    $body = $body.Replace('<table>', '<div class="table-scroll"><table>').Replace('</table>', '</table></div>')
    $sourceName = [System.IO.Path]::GetFileName($sourcePath)
    $sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePath).Hash.ToLowerInvariant()
    $nav = $navLinks -join "`n"
    $html = @"
<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="source-sha256" content="$sourceHash"><title>$title</title><style>$style</style></head>
<body><div class="layout"><nav><strong>OpenGU · Paper Writing</strong><p class="meta">2026-10-24<br>由 Markdown 源文件生成</p>$nav<p><a href="$sourceName">编辑用源文件</a></p></nav><main>$body<footer>Source: $sourceName<br>SHA-256: $sourceHash<br>使用 paper_writing/tools/render-docs.ps1 重建此页面。</footer></main></div></body></html>
"@
    $outputPath = [System.IO.Path]::ChangeExtension($sourcePath, '.html')
    [System.IO.File]::WriteAllText($outputPath, $html, $utf8)
    [pscustomobject]@{ Source = $sourcePath; Output = $outputPath; Sections = $navLinks.Count; SourceSHA256 = $sourceHash }
}
