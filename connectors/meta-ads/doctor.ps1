<#
.SYNOPSIS
    Meta Ads connector readiness check on Windows. Mirrors doctor.sh.
#>
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigHome = $env:KOKORO_CONFIG_HOME
if ([string]::IsNullOrEmpty($ConfigHome)) {
    $base = $env:XDG_CONFIG_HOME
    if ([string]::IsNullOrEmpty($base)) { $base = Join-Path $HOME '.config' }
    $ConfigHome = Join-Path $base 'kokoro'
}
$EnvFile = $env:KOKORO_META_ADS_ENV_FILE
if ([string]::IsNullOrEmpty($EnvFile)) { $EnvFile = Join-Path $ConfigHome 'meta-ads.env' }

$python = $null
foreach ($candidate in @(, @('py', '-3'), @('python'), @('python3'))) {
    if (Get-Command $candidate[0] -CommandType Application -ErrorAction SilentlyContinue) {
        $python = $candidate
        break
    }
}
if ($null -eq $python) {
    Write-Error 'Meta Ads connector requires Python 3.10+: winget install -e --id Python.Python.3.12'
    exit 2
}
$env:PYTHONUTF8 = '1'
$prefix = @($python | Select-Object -Skip 1)
& $python[0] @prefix (Join-Path $ScriptDir 'src\kokoro_meta_ads\doctor.py') --env-file $EnvFile --json
exit $LASTEXITCODE
