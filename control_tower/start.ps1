param(
    [string] $Python = "",
    [int] $Port = 8790
)

# Starts the Control Tower under a supervisor that restarts it if it exits.
# Idempotent: does nothing when the port is already served or a supervisor is already running.
# Registered to run at logon by register-autostart.ps1; safe to run by hand.

$ErrorActionPreference = "Stop"

$stateRoot = "D:\AI_Studio\control-tower"
$supervisorScript = Join-Path $PSScriptRoot "supervisor.ps1"
$stopMarker = Join-Path $stateRoot "control-tower.stop"

if (-not (Test-Path -LiteralPath $supervisorScript)) {
    throw "supervisor.ps1 not found: $supervisorScript"
}

New-Item -ItemType Directory -Force -Path $stateRoot | Out-Null
Remove-Item -LiteralPath $stopMarker -Force -ErrorAction SilentlyContinue

# The tailnet address of a served port is the origin of the `tailscale serve status` block whose root
# path proxies to it - scheme and port included, and always the FQDN, because a raw tailnet IP with the
# wrong scheme answers "Client sent an HTTP request to an HTTPS server". control_tower/tailscale.py is
# the reference implementation; this mirrors it so the banner never prints an address that does not work.
function Get-TailnetUrl {
    param([int] $LocalPort)
    if (-not (Get-Command tailscale.exe -ErrorAction SilentlyContinue)) { return $null }
    $output = & tailscale.exe serve status
    if ($LASTEXITCODE -ne 0 -or -not $output) { return $null }
    $origin = $null
    foreach ($raw in $output) {
        $line = "$raw".Trim()
        if (-not $line) { continue }
        if ($line -notlike '|--*' -and $line -match '^(https?://\S+)') {
            $origin = $Matches[1].TrimEnd('/')
            continue
        }
        if ($origin -and $line -match '^\|--\s+(\S+)\s+proxy\s+(\S+)') {
            $servedPath = $Matches[1]
            $target = $Matches[2].TrimEnd('/')
            if ($servedPath -eq '/' -and $target -like "*:$LocalPort" -and
                ($target -like '*127.0.0.1*' -or $target -like '*localhost*')) {
                return "$origin/"
            }
        }
    }
    return $null
}

function Write-Addresses {
    param([int] $LocalPort)
    Write-Host "Local:   http://127.0.0.1:$LocalPort/"
    $tailnet = Get-TailnetUrl -LocalPort $LocalPort
    if ($tailnet) {
        Write-Host "Tailnet: $tailnet"
    } else {
        Write-Host 'Tailnet: not published; run tailscale serve to reach this from the tablet.'
    }
}

# Ask the service itself rather than looking at the port: `tailscale serve` also listens on this port to
# proxy the tablet, so a raw listener check reports a running server when there is none.
try {
    $health = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/api/health" -TimeoutSec 3 -UseBasicParsing
    if ($health.StatusCode -eq 200) {
        Write-Host "Control Tower is already answering."
        Write-Addresses -LocalPort $Port
        exit 0
    }
} catch {
    # not answering: fall through and start it
}

$existing = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessId -ne $PID -and $_.CommandLine -and
    $_.CommandLine.IndexOf($supervisorScript, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
}
if ($existing) {
    Write-Host "A Control Tower supervisor is already running (pid $($existing[0].ProcessId)); it will restart the server."
    exit 0
}

$arguments = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $supervisorScript, "-Port", "$Port")
if ($Python) { $arguments += @("-Python", $Python) }
$process = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -ArgumentList $arguments -PassThru -WindowStyle Hidden

Write-Host "Control Tower supervisor started (pid $($process.Id))."
Write-Addresses -LocalPort $Port
Write-Host "Logs:    $stateRoot\supervisor.log"
