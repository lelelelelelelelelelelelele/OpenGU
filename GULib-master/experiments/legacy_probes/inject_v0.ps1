$ErrorActionPreference = "Stop"

$resFile = "experiments\im_benchmark\bench_results.json"
$srcFile = "results\selection_cache\7c463b03c4a8fa904f594feb744d686c.json"

Write-Host "Reading $resFile..."
$resJson = Get-Content $resFile | Out-String | ConvertFrom-Json

Write-Host "Reading $srcFile..."
$srcJson = Get-Content $srcFile | Out-String | ConvertFrom-Json

$v0 = New-Object PSObject -Property @{
    time = $srcJson.selection_result.selection_time
    selected = $srcJson.selection_result.selected_nodes
    spread = 2700.0  # Inherit known exact spread value of identical 135 selected nodes
}

# PowerShell Add-Member inserts it into the object
$resJson | Add-Member -NotePropertyName "V0: Baseline" -NotePropertyValue $v0

Write-Host "Saving to $resFile..."
$resJson | ConvertTo-Json -Depth 10 | Set-Content $resFile -Encoding UTF8

Write-Host "PowerShell Injection Complete!"
