# Shared helpers for the Windows (PowerShell) Kokoro installer.
# Mirrors install/lib.sh. Keep this file ASCII-only: Windows PowerShell 5.1
# reads scripts without a BOM as the local ANSI code page.

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Get-KokoroFullPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    if ($Path -eq '~') {
        $Path = $HOME
    } elseif ($Path.StartsWith('~/') -or $Path.StartsWith('~\')) {
        $Path = Join-Path $HOME $Path.Substring(2)
    }
    if (-not [System.IO.Path]::IsPathRooted($Path)) {
        $Path = Join-Path (Get-Location).ProviderPath $Path
    }
    $full = [System.IO.Path]::GetFullPath($Path)
    if ($full.Length -gt 3) {
        $full = $full.TrimEnd('\', '/')
    }
    return $full
}

function Get-KokoroEnvOrDefault {
    param([string[]]$Names, [string]$Default)

    foreach ($name in $Names) {
        $value = [Environment]::GetEnvironmentVariable($name)
        if (-not [string]::IsNullOrEmpty($value)) {
            return $value
        }
    }
    return $Default
}

function Get-KokoroSourceRoot {
    param([string]$ScriptDir)

    $root = Get-KokoroFullPath (Join-Path $ScriptDir '..')
    if (-not (Test-Path -LiteralPath (Join-Path $root '.claude\commands') -PathType Container) -and
        -not (Test-Path -LiteralPath (Join-Path $root 'commands') -PathType Container)) {
        throw "Kokoro setup error: package source does not contain Kokoro commands: $root"
    }
    return $root
}

function Get-KokoroSourceSubdir {
    param([string]$Root, [string]$Name)

    $inClaude = Join-Path $Root (Join-Path '.claude' $Name)
    if (Test-Path -LiteralPath $inClaude -PathType Container) {
        return $inClaude
    }
    return (Join-Path $Root $Name)
}

function Get-KokoroSourceManifest {
    param([string]$Root)

    $manifest = Join-Path $Root 'kokoro-package.yaml'
    if (Test-Path -LiteralPath $manifest -PathType Leaf) {
        return $manifest
    }
    return (Join-Path $Root 'package.yaml')
}

function Get-KokoroPaths {
    $claudeHome = Get-KokoroFullPath (Get-KokoroEnvOrDefault @('KOKORO_CLAUDE_HOME') (Join-Path $HOME '.claude'))
    $packageHome = Get-KokoroFullPath (Get-KokoroEnvOrDefault @('KOKORO_PACKAGE_HOME') (Join-Path $claudeHome 'kokoro'))
    $codexHome = Get-KokoroFullPath (Get-KokoroEnvOrDefault @('KOKORO_CODEX_HOME', 'CODEX_HOME') (Join-Path $HOME '.codex'))
    $agentsHome = Get-KokoroFullPath (Get-KokoroEnvOrDefault @('KOKORO_AGENTS_HOME', 'AGENTS_HOME') (Join-Path $HOME '.agents'))

    $configHome = [Environment]::GetEnvironmentVariable('KOKORO_CONFIG_HOME')
    if ([string]::IsNullOrEmpty($configHome)) {
        $xdg = Get-KokoroEnvOrDefault @('XDG_CONFIG_HOME') (Join-Path $HOME '.config')
        $configHome = Join-Path $xdg 'kokoro'
    }
    $configHome = Get-KokoroFullPath $configHome
    $metaAdsEnv = Get-KokoroFullPath (Get-KokoroEnvOrDefault @('KOKORO_META_ADS_ENV_FILE') (Join-Path $configHome 'meta-ads.env'))

    return [pscustomobject]@{
        ClaudeHome      = $claudeHome
        PackageHome     = $packageHome
        CommandsTarget  = Join-Path $claudeHome 'commands'
        CodexSkillDir   = Join-Path $codexHome 'skills\kokoro'
        AgentsSkillDir  = Join-Path $agentsHome 'skills\kokoro'
        ConfigHome      = $configHome
        MetaAdsEnvFile  = $metaAdsEnv
    }
}

# Path written into wrappers and skills: absolute, with forward slashes, so it
# is valid inside YAML double quotes and readable by Claude Code and Codex.
function Get-KokoroAgentPath {
    param([string]$Path)
    return ($Path -replace '\\', '/')
}

# Short path for console messages.
function Get-KokoroDisplayPath {
    param([string]$Path)

    $homeFull = Get-KokoroFullPath $HOME
    if ($Path.StartsWith($homeFull + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
        return '~\' + $Path.Substring($homeFull.Length + 1)
    }
    return $Path
}

function Test-KokoroSamePath {
    param([string]$A, [string]$B)
    return [string]::Equals((Get-KokoroFullPath $A), (Get-KokoroFullPath $B), [System.StringComparison]::OrdinalIgnoreCase)
}

function Copy-KokoroDir {
    param([string]$Source, [string]$Destination)

    if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
        throw "Kokoro setup error: missing source directory: $Source"
    }
    if (Test-Path -LiteralPath $Destination) {
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }
    $parent = Split-Path -Parent $Destination
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

# UTF-8 without BOM and LF line endings, so front matter parses the same as on macOS.
function Write-KokoroTextFile {
    param([string]$Path, [string]$Content)

    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($Path, $normalized, (New-Object System.Text.UTF8Encoding($false)))
}

function Test-KokoroOwned {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $false
    }
    return [bool](Select-String -LiteralPath $Path -Pattern '^kokoro_owned: true$' -Quiet)
}

function Get-KokoroWrapperFiles {
    param([string]$CommandsTarget)
    if (-not (Test-Path -LiteralPath $CommandsTarget -PathType Container)) {
        return @()
    }
    return @(Get-ChildItem -LiteralPath $CommandsTarget -File -Filter 'kokoro*.md' | Sort-Object Name)
}

function Get-KokoroForbiddenPrefix {
    return 'rai'
}

function Get-KokoroForbiddenNamedPathCount {
    param([string]$Root)
    if (-not (Test-Path -LiteralPath $Root)) {
        return 0
    }
    $prefix = Get-KokoroForbiddenPrefix
    return @(Get-ChildItem -LiteralPath $Root -Recurse -Force -Filter "$prefix-*" -ErrorAction SilentlyContinue).Count
}

# --- Python -------------------------------------------------------------------
# Windows has no fixed "python3". Try the launcher first, then the usual names.
# The Microsoft Store alias "python.exe" prints a hint and fails; the version
# probe rejects it.

$script:KokoroPython = $null

function Find-KokoroPython {
    $candidates = @(
        , @('py', '-3')
        , @('python')
        , @('python3')
    )
    foreach ($candidate in $candidates) {
        $exe = $candidate[0]
        if (-not (Get-Command $exe -CommandType Application -ErrorAction SilentlyContinue)) {
            continue
        }
        $prefix = @($candidate | Select-Object -Skip 1)
        $previous = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            $probe = & $exe @prefix -c 'import sys; print(int(sys.version_info >= (3, 10)))' 2>$null
            $code = $LASTEXITCODE
        } catch {
            $probe = $null
            $code = 1
        } finally {
            $ErrorActionPreference = $previous
        }
        if ($code -eq 0 -and ("$probe").Trim() -eq '1') {
            return , $candidate
        }
    }
    return $null
}

function Initialize-KokoroPython {
    if ($null -ne $script:KokoroPython) {
        return
    }
    $found = Find-KokoroPython
    if ($null -eq $found) {
        Write-Host ''
        Write-Host 'Kokoro necesita Python 3.10 o mas nuevo. / Kokoro needs Python 3.10 or newer.' -ForegroundColor Yellow
        Write-Host 'Instalalo con / Install it with:'
        Write-Host '    winget install -e --id Python.Python.3.12'
        Write-Host 'o descargalo de / or download it from: https://www.python.org/downloads/windows/'
        Write-Host 'Despues cierra esta ventana, abre una nueva y vuelve a correr el instalador.'
        Write-Host 'Then close this window, open a new one, and run the installer again.'
        throw 'Kokoro setup error: Python 3.10+ not found.'
    }
    $script:KokoroPython = $found
}

function Get-KokoroPythonLabel {
    Initialize-KokoroPython
    return ($script:KokoroPython -join ' ')
}

# Runs Python with the found interpreter. Returns the exit code only.
function Invoke-KokoroPython {
    param([string[]]$Arguments, [switch]$Quiet)

    Initialize-KokoroPython
    $exe = $script:KokoroPython[0]
    $prefix = @($script:KokoroPython | Select-Object -Skip 1)
    $previousEap = $ErrorActionPreference
    $previousUtf8 = $env:PYTHONUTF8
    $ErrorActionPreference = 'Continue'
    $env:PYTHONUTF8 = '1'
    try {
        if ($Quiet) {
            & $exe @prefix @Arguments *> $null
        } else {
            & $exe @prefix @Arguments 2>&1 | ForEach-Object { Write-Host $_ }
        }
        return $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousEap
        $env:PYTHONUTF8 = $previousUtf8
    }
}
