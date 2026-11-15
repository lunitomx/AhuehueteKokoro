<#
.SYNOPSIS
    Start the Meta Ads MCP connector on Windows. Mirrors run.sh.
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

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    [Console]::Error.WriteLine('Meta Ads connector requires uv: https://docs.astral.sh/uv/ (winget install -e --id astral-sh.uv)')
    exit 2
}
& uv run --project $ScriptDir kokoro-meta-ads-launch --env-file $EnvFile
exit $LASTEXITCODE
