[CmdletBinding()]
param(
    [ValidateRange(5, 1440)]
    [int]$IntervalMinutes = 30,
    [ValidateRange(1, 10000)]
    [int]$MaxItems = 100,
    [string]$TaskName = 'XAI Studio Media Export'
)

$ErrorActionPreference = 'Stop'
$runner = Join-Path $PSScriptRoot 'run_drive_media_export.ps1'
if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) {
    throw "Runner not found: $runner"
}

$powerShell = Join-Path $PSHOME 'powershell.exe'
if (-not (Test-Path -LiteralPath $powerShell -PathType Leaf)) {
    $powerShell = (Get-Command powershell.exe -ErrorAction Stop).Source
}

$arguments = "-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$runner`" -MaxItems $MaxItems"
$action = New-ScheduledTaskAction -Execute $powerShell -Argument $arguments
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
$principal = New-ScheduledTaskPrincipal `
    -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings `
    -Description 'Copies new Gallery-registered image/video originals to the browsable Google Drive media tree.'

Register-ScheduledTask -TaskName $TaskName -InputObject $task -Force | Out-Null
Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, @{Name='IntervalMinutes';Expression={$IntervalMinutes}}, @{Name='MaxItems';Expression={$MaxItems}}
