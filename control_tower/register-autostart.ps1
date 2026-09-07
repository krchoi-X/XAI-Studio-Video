param(
    [switch] $Unregister
)

# Registers a per-user scheduled task that starts the Control Tower at logon and after a standby resume.
# Mirrors the Gallery's task ("XAI Personal Studio") but is a separate task on a separate port; neither
# touches the other. Least privilege, interactive token, no elevation.

$ErrorActionPreference = "Stop"

$taskName = "XAI Control Tower"
$launcher = Join-Path $PSScriptRoot "start.ps1"
$powershell = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"

if ($Unregister) {
    & schtasks.exe /Delete /TN $taskName /F
    if ($LASTEXITCODE -ne 0) { throw "schtasks.exe failed with exit code $LASTEXITCODE" }
    Write-Host "Scheduled task removed: $taskName"
    exit 0
}

if (-not (Test-Path -LiteralPath $launcher)) { throw "start.ps1 not found: $launcher" }

$escapedLauncher = [System.Security.SecurityElement]::Escape($launcher)
$escapedPowerShell = [System.Security.SecurityElement]::Escape($powershell)
$escapedWorkingDir = [System.Security.SecurityElement]::Escape($PSScriptRoot)
$userId = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$escapedUserId = [System.Security.SecurityElement]::Escape($userId)
$taskXmlPath = Join-Path $env:TEMP "xai-control-tower-task.xml"

$taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>Start the XAI Control Tower job observability service at logon and after Modern Standby resume.</Description></RegistrationInfo>
  <Triggers>
    <LogonTrigger><Enabled>true</Enabled><UserId>$escapedUserId</UserId></LogonTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and EventID=1]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
    </EventTrigger>
  </Triggers>
  <Principals><Principal id="Author"><UserId>$escapedUserId</UserId><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author"><Exec><Command>$escapedPowerShell</Command><Arguments>-NoProfile -ExecutionPolicy Bypass -File &quot;$escapedLauncher&quot;</Arguments><WorkingDirectory>$escapedWorkingDir</WorkingDirectory></Exec></Actions>
</Task>
"@

Set-Content -LiteralPath $taskXmlPath -Encoding Unicode -Value $taskXml
try {
    & schtasks.exe /Create /TN $taskName /XML $taskXmlPath /F
    if ($LASTEXITCODE -ne 0) { throw "schtasks.exe failed with exit code $LASTEXITCODE" }
} finally {
    Remove-Item -LiteralPath $taskXmlPath -Force -ErrorAction SilentlyContinue
}

Write-Host "Scheduled task registered: $taskName"
Write-Host "Triggers: user logon, Modern Standby resume"
Write-Host "Remove with: powershell -NoProfile -ExecutionPolicy Bypass -File `"$PSScriptRoot\register-autostart.ps1`" -Unregister"
