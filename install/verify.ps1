<#
.SYNOPSIS
    Verify a Kokoro installation on Windows. Mirrors install/verify.sh.
#>
[CmdletBinding()]
param()

# Keep this file ASCII-only (see lib.ps1).
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir 'lib.ps1')

$script:Errors = 0

function Add-KokoroFailure {
    param([string]$Message)
    Write-Host "Kokoro verify error: $Message" -ForegroundColor Red
    $script:Errors++
}

function Assert-File {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Add-KokoroFailure "missing file: $Path"
    }
}

function Assert-Dir {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        Add-KokoroFailure "missing directory: $Path"
    }
}

try {
    $Paths = Get-KokoroPaths
    $PackageHome = $Paths.PackageHome
    $Runtime = Join-Path $PackageHome 'runtime\kokoro.py'

    Assert-File (Join-Path $PackageHome 'package.yaml')
    Assert-File (Join-Path $PackageHome 'IDENTITY_kokoro.md')
    Assert-File (Join-Path $PackageHome 'AGENTS.md')
    Assert-File (Join-Path $PackageHome 'CLAUDE.md')
    Assert-Dir (Join-Path $PackageHome 'commands')
    Assert-Dir (Join-Path $PackageHome 'knowledge')
    Assert-File (Join-Path $PackageHome 'commands\kokoro.md')
    foreach ($module in @('kokoro', 'clients', 'evidence', 'evidence_ledger', 'projections', 'freshness',
            'ideas', 'learning', 'creative', 'grounding', 'voice', 'routines')) {
        Assert-File (Join-Path $PackageHome "runtime\$module.py")
    }
    Assert-File (Join-Path $PackageHome 'knowledge\kokoro-evidence-model.md')
    Assert-File (Join-Path $PackageHome 'knowledge\kokoro-open-questions.md')
    foreach ($knowledge in @('hypothesis-contract', 'revalidation', 'creative-iteration',
            'creative-winner-selection', 'idea-bank', 'idea-evaluation', 'context-freshness',
            'dependency-staleness', 'grounding-standard', 'voice-review-standard',
            'learning-traces', 'learning-promotion')) {
        Assert-File (Join-Path $PackageHome "knowledge\kokoro-$knowledge.md")
    }
    $connector = Join-Path $PackageHome 'connectors\meta-ads'
    Assert-Dir $connector
    Assert-File (Join-Path $connector 'run.ps1')
    Assert-File (Join-Path $connector 'doctor.ps1')
    Assert-File (Join-Path $connector 'pyproject.toml')
    Assert-File (Join-Path $PackageHome 'install\privacy_scan.py')
    Assert-File $Paths.MetaAdsEnvFile

    if ((Invoke-KokoroPython @($Runtime, 'doctor') -Quiet) -ne 0) {
        Add-KokoroFailure 'Kokoro runtime doctor failed'
    }
    $doctor = Join-Path $connector 'src\kokoro_meta_ads\doctor.py'
    if ((Invoke-KokoroPython @($doctor, '--env-file', $Paths.MetaAdsEnvFile, '--json') -Quiet) -ne 0) {
        Add-KokoroFailure 'Meta Ads connector doctor failed'
    }

    # Guest registry and evidence ledger must work in a fresh private workspace.
    $smoke = Join-Path ([System.IO.Path]::GetTempPath()) ('kokoro-verify.' + [guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Force -Path (Join-Path $smoke '.kokoro') | Out-Null
    Write-KokoroTextFile (Join-Path $smoke '.kokoro\.gitignore') "local/`n"
    $smokeChecks = @(
        @{ Args = @('client', 'list', '--target', $smoke); Label = 'guest registry smoke test failed' },
        @{ Args = @('evidence', 'verify', '--target', $smoke); Label = 'evidence ledger smoke test failed' },
        @{ Args = @('evidence', 'summary', '--target', $smoke); Label = 'evidence summary smoke test failed' },
        @{ Args = @('freshness', 'report', '--target', $smoke); Label = 'freshness report smoke test failed' },
        @{ Args = @('routine', 'list'); Label = 'routine recipes smoke test failed' }
    )
    foreach ($check in $smokeChecks) {
        if ((Invoke-KokoroPython (@($Runtime) + $check.Args) -Quiet) -ne 0) {
            Add-KokoroFailure $check.Label
        }
    }
    Remove-Item -LiteralPath $smoke -Recurse -Force -ErrorAction SilentlyContinue

    if ((Invoke-KokoroPython @((Join-Path $PackageHome 'install\privacy_scan.py'), $PackageHome)) -ne 0) {
        Add-KokoroFailure 'release privacy scan failed'
    }

    $wrapperCount = 0
    foreach ($wrapper in (Get-KokoroWrapperFiles $Paths.CommandsTarget)) {
        $wrapperCount++
        $text = [System.IO.File]::ReadAllText($wrapper.FullName)
        if ($text -notmatch '(?m)^kokoro_owned: true$') {
            Add-KokoroFailure "wrapper is missing Kokoro ownership marker: $($wrapper.FullName)"
        }
        if ($text -notmatch '(?m)^kokoro_package_home:') {
            Add-KokoroFailure "wrapper is missing package home: $($wrapper.FullName)"
        }
        $match = [regex]::Match($text, '(?m)^kokoro_source: *"?([^"\r\n]+)"?')
        if (-not $match.Success) {
            Add-KokoroFailure "wrapper is missing source metadata: $($wrapper.FullName)"
        } else {
            $sourcePath = Join-Path $PackageHome ($match.Groups[1].Value -replace '/', '\')
            if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
                Add-KokoroFailure "wrapper source does not exist: $sourcePath"
            }
        }
    }
    if ($wrapperCount -le 0) {
        Add-KokoroFailure "no Kokoro Claude wrappers found in $($Paths.CommandsTarget)"
    }

    foreach ($pair in @(@('Codex skill', $Paths.CodexSkillDir), @('Agents skill', $Paths.AgentsSkillDir))) {
        $skillFile = Join-Path $pair[1] 'SKILL.md'
        Assert-File $skillFile
        if (Test-Path -LiteralPath $skillFile -PathType Leaf) {
            $text = [System.IO.File]::ReadAllText($skillFile)
            if ($text -notmatch '(?m)^kokoro_owned: true$') {
                Add-KokoroFailure "$($pair[0]) missing ownership marker"
            }
            if ($text -notmatch '(?m)^kokoro_package_home:') {
                Add-KokoroFailure "$($pair[0]) missing package home"
            }
        }
    }

    foreach ($path in @($PackageHome, $Paths.CommandsTarget, $Paths.CodexSkillDir, $Paths.AgentsSkillDir)) {
        if ((Get-KokoroForbiddenNamedPathCount $path) -ne 0) {
            Add-KokoroFailure "forbidden package path names found under $path"
        }
    }

    foreach ($privateDir in @('.raise', '.rai', '.kokoro', 'clients', 'clientes', 'private', 'exports',
            'reports', 'generated', 'deliverables')) {
        if (Test-Path -LiteralPath (Join-Path $PackageHome $privateDir)) {
            Add-KokoroFailure "private/runtime directory copied into package: $(Join-Path $PackageHome $privateDir)"
        }
    }

    $sensitive = @(Get-ChildItem -LiteralPath $PackageHome -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {
            $_.Name -eq '.DS_Store' -or $_.Name -like '*.csv' -or $_.Name -like '*.xls' -or
            $_.Name -like '*.xlsx' -or $_.Name -like '.env*' -or $_.Name -like 'client_secret_*.json'
        })
    foreach ($file in $sensitive) {
        Add-KokoroFailure "sensitive or OS file copied into package: $($file.FullName)"
    }
} catch {
    Add-KokoroFailure $_.Exception.Message
}

if ($script:Errors -gt 0) {
    exit 1
}

Write-Host 'Kokoro verify OK.'
Write-Host "Package root: $(Get-KokoroDisplayPath $PackageHome)"
Write-Host "Python: $(Get-KokoroPythonLabel)"
Write-Host "Claude wrappers: $wrapperCount"
Write-Host "Codex skill: $(Get-KokoroDisplayPath $Paths.CodexSkillDir)"
Write-Host "Agents skill: $(Get-KokoroDisplayPath $Paths.AgentsSkillDir)"
Write-Host 'Meta Ads connector: optional'
exit 0
