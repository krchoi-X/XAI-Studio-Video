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
$productionsStateDirectory = 'D:\AI_Studio\workspace\productions-drive-export'
$productionsStatusPath = Join-Path $productionsStateDirectory 'last-run.json'
$driveRoot = 'G:\'
$knownPython = 'D:\codex\personal-prompt-studio\personal-prompt-studio\backend\.venv\Scripts\python.exe'

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$startedAt = Get-Date
$logPath = Join-Path $logDirectory ("sync-{0:yyyyMMdd-HHmmss}.log" -f $startedAt)
$productionsFailed = $false
$productionsProblem = $null

function Write-ProductionsStatus {
    param(
        [bool]$Ok,
        [string]$Problem,
        [string]$LogPath
    )
    New-Item -ItemType Directory -Path $productionsStateDirectory -Force | Out-Null
    $temporary = "$productionsStatusPath.tmp.$PID"
    [ordered]@{
        ok = $Ok
        checked_at = (Get-Date).ToString('o')
        problem = $Problem
        log = $LogPath
    } | ConvertTo-Json | Set-Content -LiteralPath $temporary -Encoding UTF8
    Move-Item -LiteralPath $temporary -Destination $productionsStatusPath -Force
}

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

    # Character-independent productions: a separate exporter with its own ledger and log. It must never change
    # the media export's result above, so a failure here is only reported.
    $productionsExporter = Join-Path $PSScriptRoot 'productions_drive_export.py'
    $productionsLog = Join-Path $logDirectory ("productions-{0:yyyyMMdd-HHmmss}.log" -f $startedAt)
    try {
        Push-Location $repositoryRoot
        try {
            & $pythonPath $productionsExporter sync --all --limit $MaxItems 2>&1 | Tee-Object -FilePath $productionsLog | Out-Null
            $productionsExitCode = $LASTEXITCODE
        } finally {
            Pop-Location
        }
        if ($productionsExitCode -ne 0) {
            $productionsFailed = $true
            $productionsProblem = "exit $productionsExitCode; see $productionsLog"
            Write-Warning "Productions export reported a problem ($productionsProblem)"
            Write-ProductionsStatus -Ok $false -Problem $productionsProblem -LogPath $productionsLog
        } else {
            Write-ProductionsStatus -Ok $true -Problem $null -LogPath $productionsLog
        }
    } catch {
        $productionsFailed = $true
        $productionsProblem = $_.Exception.Message
        Write-Warning "Productions export failed: $($_.Exception.Message)"
        try {
            Write-ProductionsStatus -Ok $false -Problem $productionsProblem -LogPath $productionsLog
        } catch {
            Write-Warning "Could not persist Productions backup status: $($_.Exception.Message)"
        }
    }

    if ($exitCode -ne 0) {
        throw "Media export failed with exit code $exitCode. See $logPath"
    }

    # Keep roughly three months of small execution logs.
    Get-ChildItem -LiteralPath $logDirectory -Filter 'sync-*.log' -File |
        Where-Object LastWriteTime -lt (Get-Date).AddDays(-90) |
        Remove-Item -Force
    Get-ChildItem -LiteralPath $logDirectory -Filter 'productions-*.log' -File |
        Where-Object LastWriteTime -lt (Get-Date).AddDays(-90) |
        Remove-Item -Force

    if ($productionsFailed) {
        [Console]::Error.WriteLine("Media export completed, but Productions export failed: $productionsProblem")
        exit 2
    }

    Write-Output "Media export completed. Log: $logPath"
} catch {
    $_ | Out-String | Set-Content -LiteralPath $logPath -Encoding UTF8
    Write-Error "Media export failed. See $logPath"
    exit 1
}
