param(
    [string] $Python = "",
    [int] $Port = 8790
)

# Keeps the Control Tower server running: restarts it if it exits, stops when the stop marker appears.
# Started by start.ps1; not meant to be run directly.

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$stateRoot = "D:\AI_Studio\control-tower"
$stopMarker = Join-Path $stateRoot "control-tower.stop"
$logPath = Join-Path $stateRoot "supervisor.log"
$stdoutPath = Join-Path $stateRoot "server.stdout.log"
$stderrPath = Join-Path $stateRoot "server.stderr.log"

New-Item -ItemType Directory -Force -Path $stateRoot | Out-Null

function Write-SupervisorLog {
    param([string] $Message)
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
    Add-Content -LiteralPath $logPath -Encoding utf8 -Value "$timestamp $Message"
}

function Resolve-Python {
    param([string] $Explicit)
    $candidates = @()
    if ($Explicit) { $candidates += $Explicit }
    if ($env:XAI_CT_PYTHON) { $candidates += $env:XAI_CT_PYTHON }
    # The interpreter Control Tower has always used on this PC; it carries fastapi, uvicorn, sse-starlette, psutil.
    $candidates += "$env:LOCALAPPDATA\hermes\hermes-agent\venv\Scripts\python.exe"
    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) { return $candidate }
    }
    $onPath = (Get-Command python.exe -ErrorAction SilentlyContinue)
    if ($onPath) { return $onPath.Source }
    throw "no Python interpreter found; pass -Python or set XAI_CT_PYTHON"
}

$interpreter = Resolve-Python -Explicit $Python
Write-SupervisorLog "supervisor started pid=$PID python=$interpreter port=$Port"

while (-not (Test-Path -LiteralPath $stopMarker)) {
    try {
        Write-SupervisorLog "starting control tower"
        $process = Start-Process -FilePath $interpreter -ArgumentList @(
            "-X", "utf8", "-m", "control_tower", "--port", "$Port"
        ) -WorkingDirectory $repoRoot -PassThru -Wait -WindowStyle Hidden `
            -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
        Write-SupervisorLog "control tower exited code=$($process.ExitCode)"
    } catch {
        Write-SupervisorLog "control tower failed to start: $($_.Exception.Message)"
    }
    if (Test-Path -LiteralPath $stopMarker) { break }
    Start-Sleep -Seconds 5
}

Write-SupervisorLog "supervisor stopping (stop marker present)"
