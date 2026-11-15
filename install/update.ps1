<#
.SYNOPSIS
    Update Kokoro on Windows. Mirrors install/update.sh.
#>
[CmdletBinding()]
param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $ScriptDir 'install.ps1')
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Write-Host 'Kokoro update complete.'
exit 0
