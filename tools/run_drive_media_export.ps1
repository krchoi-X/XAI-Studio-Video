[CmdletBinding()]
param(
    [ValidateRange(1, 10000)]
    [int]$MaxItems = 100
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$exporter = Join-Path $PSScriptRoot 'drive_media_export.py'
$stateDirectory = 'D:\AI_Studio\workspace\drive-media-export'
$logDirectory = Join-Path $stateDirectory 'logs'
$driveRoot = 'G:\'
$knownPython = 'D:\codex\personal-prompt-studio\personal-prompt-studio\backend\.venv\Scripts\python.exe'

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$startedAt = Get-Date
$logPath = Join-Path $logDirectory ("sync-{0:yyyyMMdd-HHmmss}.log" -f $startedAt)

try {
    if (-not (Test-Path -LiteralPath $driveRoot -PathType Container)) {
        throw "Google Drive is not available at $driveRoot. The sync was not started."
    }

    if (Test-Path -LiteralPath $knownPython -PathType Leaf) {
        $pythonPath = $knownPython
    } else {
        $pythonPath = (Get-Command python.exe -ErrorAction Stop).Source
    }

    Push-Location $repositoryRoot
    try {
        & $pythonPath $exporter sync --all --limit $MaxItems 2>&1 | Tee-Object -FilePath $logPath
        $exitCode = $LASTEXITCODE
    } finally {
        Pop-Location
    }

    if ($exitCode -ne 0) {
        throw "Media export failed with exit code $exitCode. See $logPath"
    }

    # Keep roughly three months of small execution logs.
    Get-ChildItem -LiteralPath $logDirectory -Filter 'sync-*.log' -File |
        Where-Object LastWriteTime -lt (Get-Date).AddDays(-90) |
        Remove-Item -Force

    Write-Output "Media export completed. Log: $logPath"
} catch {
    $_ | Out-String | Set-Content -LiteralPath $logPath -Encoding UTF8
    Write-Error "Media export failed. See $logPath"
    exit 1
}
