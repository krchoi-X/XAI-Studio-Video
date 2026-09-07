param(
    [int] $Port = 8790
)

# Stops the Control Tower and its supervisor. Writes a stop marker first so the supervisor does not restart it.
# Observation only stops; no job, record or media is touched.

$ErrorActionPreference = "Stop"

$stateRoot = "D:\AI_Studio\control-tower"
$stopMarker = Join-Path $stateRoot "control-tower.stop"
$supervisorScript = Join-Path $PSScriptRoot "supervisor.ps1"

New-Item -ItemType Directory -Force -Path $stateRoot | Out-Null
Set-Content -LiteralPath $stopMarker -Encoding utf8 -Value (Get-Date -Format "yyyy-MM-ddTHH:mm:ssK")

$stopped = 0
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessId -ne $PID -and $_.CommandLine -and (
        $_.CommandLine.IndexOf($supervisorScript, [System.StringComparison]::OrdinalIgnoreCase) -ge 0 -or
        ($_.Name -like "python*" -and $_.CommandLine -match "-m\s+control_tower")
    )
} | ForEach-Object {
    try {
        Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop
        $stopped++
    } catch {
        Write-Host "could not stop pid $($_.ProcessId): $($_.Exception.Message)"
    }
}

Write-Host "Control Tower stopped ($stopped process(es)). Remove $stopMarker or run start.ps1 to start again."
