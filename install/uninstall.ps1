<#
.SYNOPSIS
    Uninstall Kokoro on Windows. Mirrors install/uninstall.sh.
    Removes only what Kokoro owns. Keeps the Meta Ads credentials file.
#>
[CmdletBinding()]
param()

# Keep this file ASCII-only (see lib.ps1).
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir 'lib.ps1')

$Paths = Get-KokoroPaths
$PackageHome = $Paths.PackageHome
$removed = 0
$preserved = 0

foreach ($wrapper in (Get-KokoroWrapperFiles $Paths.CommandsTarget)) {
    if (Test-KokoroOwned $wrapper.FullName) {
        Remove-Item -LiteralPath $wrapper.FullName -Force
        Write-Host "Removed wrapper: $(Get-KokoroDisplayPath $wrapper.FullName)"
        $removed++
    } else {
        Write-Host "Preserved non-Kokoro command: $(Get-KokoroDisplayPath $wrapper.FullName)"
        $preserved++
    }
}

foreach ($pair in @(@('Codex skill', $Paths.CodexSkillDir), @('agents skill', $Paths.AgentsSkillDir))) {
    $skillFile = Join-Path $pair[1] 'SKILL.md'
    if (Test-Path -LiteralPath $skillFile -PathType Leaf) {
        if (Test-KokoroOwned $skillFile) {
            Remove-Item -LiteralPath $pair[1] -Recurse -Force
            Write-Host "Removed $($pair[0]): $(Get-KokoroDisplayPath $pair[1])"
            $removed++
        } else {
            Write-Host "Preserved non-Kokoro $($pair[0]): $(Get-KokoroDisplayPath $pair[1])"
            $preserved++
        }
    }
}

$manifest = Join-Path $PackageHome 'package.yaml'
if ((Test-Path -LiteralPath $manifest -PathType Leaf) -and
    (Select-String -LiteralPath $manifest -Pattern '^package: kokoro$' -Quiet)) {
    # The uninstaller may be running from inside the package; leave that folder first.
    Set-Location -LiteralPath $HOME
    Remove-Item -LiteralPath $PackageHome -Recurse -Force
    Write-Host "Removed package home: $(Get-KokoroDisplayPath $PackageHome)"
    $removed++
} elseif (Test-Path -LiteralPath $PackageHome) {
    Write-Host "Preserved package home without Kokoro marker: $(Get-KokoroDisplayPath $PackageHome)"
    $preserved++
}

if (Test-Path -LiteralPath $Paths.MetaAdsEnvFile) {
    Write-Host "Preserved Meta Ads credentials: $(Get-KokoroDisplayPath $Paths.MetaAdsEnvFile)"
    $preserved++
}

Write-Host "Kokoro uninstall complete. removed=$removed preserved=$preserved"
exit 0
