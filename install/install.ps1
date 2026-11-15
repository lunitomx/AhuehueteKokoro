<#
.SYNOPSIS
    Install Kokoro globally on Windows for Claude Code, Codex, and .agents-compatible harnesses.

.DESCRIPTION
    Windows version of install/install.sh. No WSL or Git Bash needed.
    Needs Windows PowerShell 5.1 (included in Windows 10 and 11) and Python 3.10+.

    The easiest way to run it is install\install.cmd (double-click, or from cmd):
        install\install.cmd
        install\install.cmd -Target %USERPROFILE%\my-project

.PARAMETER Target
    Also initialize Kokoro's private Markdown/YAML memory (.kokoro) inside this project folder.
#>
[CmdletBinding()]
param(
    [string]$Target = '',
    [switch]$Help
)

# Keep this file ASCII-only (see lib.ps1).
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir 'lib.ps1')

if ($Help) {
    Write-Host 'Usage: install.cmd [-Target PROJECT]'
    Write-Host ''
    Write-Host 'Install Kokoro globally for Claude Code, Codex, and .agents-compatible harnesses.'
    Write-Host ''
    Write-Host '  -Target PROJECT  Also initialize Kokoro''s private Markdown/YAML memory'
    Write-Host '                   inside the selected work project.'
    exit 0
}

function Assert-KokoroFile {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Kokoro setup error: missing required file: $Path"
    }
}

try {
    $SourceRoot = Get-KokoroSourceRoot $ScriptDir
    $SourceCommandsDir = Get-KokoroSourceSubdir $SourceRoot 'commands'
    $SourceKnowledgeDir = Get-KokoroSourceSubdir $SourceRoot 'knowledge'
    $SourceManifest = Get-KokoroSourceManifest $SourceRoot
    $Paths = Get-KokoroPaths
    $PackageHome = $Paths.PackageHome
    $PackageAgentPath = Get-KokoroAgentPath $PackageHome

    Assert-KokoroFile (Join-Path $SourceRoot 'IDENTITY_kokoro.md')
    Assert-KokoroFile $SourceManifest
    Assert-KokoroFile (Join-Path $SourceCommandsDir 'kokoro.md')

    # Fail early, before copying anything, when Python is missing.
    $PythonLabel = Get-KokoroPythonLabel
    Write-Host "Python: $PythonLabel"

    New-Item -ItemType Directory -Force -Path $PackageHome, $Paths.CommandsTarget | Out-Null

    if (-not (Test-KokoroSamePath $SourceRoot $PackageHome)) {
        Copy-Item -LiteralPath (Join-Path $SourceRoot 'IDENTITY_kokoro.md') -Destination (Join-Path $PackageHome 'IDENTITY_kokoro.md') -Force
        Copy-Item -LiteralPath (Join-Path $SourceRoot 'AGENTS.md') -Destination (Join-Path $PackageHome 'AGENTS.md') -Force
        Copy-Item -LiteralPath (Join-Path $SourceRoot '.claude\CLAUDE.md') -Destination (Join-Path $PackageHome 'CLAUDE.md') -Force
        Copy-Item -LiteralPath $SourceManifest -Destination (Join-Path $PackageHome 'package.yaml') -Force
        Copy-KokoroDir $SourceCommandsDir (Join-Path $PackageHome 'commands')
        Copy-KokoroDir $SourceKnowledgeDir (Join-Path $PackageHome 'knowledge')
        Copy-KokoroDir (Join-Path $SourceRoot 'runtime') (Join-Path $PackageHome 'runtime')
        Copy-KokoroDir (Join-Path $SourceRoot 'connectors') (Join-Path $PackageHome 'connectors')

        if (-not (Test-KokoroSamePath $ScriptDir (Join-Path $PackageHome 'install'))) {
            Copy-KokoroDir $ScriptDir (Join-Path $PackageHome 'install')
        }

        $agentsSource = Join-Path $SourceRoot '.agents\skills\kokoro'
        if (Test-Path -LiteralPath $agentsSource -PathType Container) {
            Copy-KokoroDir $agentsSource (Join-Path $PackageHome '.agents\skills\kokoro')
        }
    }

    # Meta Ads credentials file (optional connector). The user profile folder is
    # already private on Windows, so no extra permissions are set here.
    $template = Join-Path $PackageHome 'connectors\meta-ads\config\meta-ads.env.template'
    Assert-KokoroFile $template
    $envFile = $Paths.MetaAdsEnvFile
    if (Test-Path -LiteralPath $envFile) {
        $item = Get-Item -LiteralPath $envFile -Force
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            throw "Kokoro setup error: credential file must not be a symlink: $envFile"
        }
        if ($item.PSIsContainer) {
            throw "Kokoro setup error: credential path is not a file: $envFile"
        }
    } else {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $envFile) | Out-Null
        Copy-Item -LiteralPath $template -Destination $envFile
    }

    # Replace only the wrappers Kokoro owns.
    foreach ($wrapper in (Get-KokoroWrapperFiles $Paths.CommandsTarget)) {
        if (Test-KokoroOwned $wrapper.FullName) {
            Remove-Item -LiteralPath $wrapper.FullName -Force
        }
    }

    $packageCommands = Join-Path $PackageHome 'commands'
    foreach ($source in @(Get-ChildItem -LiteralPath $packageCommands -File -Filter 'kokoro*.md' | Sort-Object Name)) {
        $commandName = $source.Name
        $slashName = [System.IO.Path]::GetFileNameWithoutExtension($commandName)
        $wrapper = @"
---
kokoro_owned: true
kokoro_source: "commands/$commandName"
kokoro_package_home: "$PackageAgentPath"
---

<!-- Generated by Kokoro installer. Do not edit directly. -->

# /$slashName

Before executing this command:

1. Use ``$PackageAgentPath`` as the Kokoro package root.
2. Read ``$PackageAgentPath/IDENTITY_kokoro.md``.
3. Read the source command: ``$PackageAgentPath/commands/$commandName``.
4. Resolve bare Kokoro knowledge references under ``$PackageAgentPath/knowledge/``,
   ``$PackageAgentPath/knowledge/google-ads/``, or ``$PackageAgentPath/knowledge/lux/``.
5. If identity, command source, or required knowledge is missing, stop and tell
   the user to run Kokoro verify/update.
6. Never assume the current working directory is the Kokoro package.

This computer runs Windows. When the source command runs Python as ``python3``,
use ``$PythonLabel`` instead if ``python3`` is not available. Wherever it says
``KOKORO_PACKAGE_HOME``, use ``$PackageAgentPath``. If it says to run a ``.sh``
script under ``install/``, run the ``.cmd`` script with the same name.
"@
        Write-KokoroTextFile (Join-Path $Paths.CommandsTarget $commandName) $wrapper
    }

    foreach ($skillDir in @($Paths.CodexSkillDir, $Paths.AgentsSkillDir)) {
        $skill = @"
---
name: kokoro
description: Route Kokoro requests to the installed package.
kokoro_owned: true
kokoro_package_home: "$PackageAgentPath"
---

# Kokoro Router

Kokoro package root: ``$PackageAgentPath``

Before responding:

1. Read ``$PackageAgentPath/IDENTITY_kokoro.md``.
2. Route command requests to ``$PackageAgentPath/commands/kokoro*.md``.
3. Resolve knowledge under ``$PackageAgentPath/knowledge/``,
   ``$PackageAgentPath/knowledge/google-ads/``, and
   ``$PackageAgentPath/knowledge/lux/``.
4. For a request to create a Meta Ads campaign from zero, read
   ``$PackageAgentPath/commands/kokoro-meta-campaign.md``. It creates a plan
   and manual Ads Manager playbook only; never request credentials or publish.
5. For bug reports or improvement suggestions, read
   ``$PackageAgentPath/commands/kokoro-feedback.md``. Prepare a sanitized draft
   and do not submit it or share data without the user's review and authorization.
6. If any required file is missing, stop and ask the user to run
   ``$PackageAgentPath/install/verify.cmd`` or reinstall Kokoro.

Never assume the current working directory is the Kokoro package.

This computer runs Windows. When a command runs Python as ``python3``, use
``$PythonLabel`` instead if ``python3`` is not available.
"@
        Write-KokoroTextFile (Join-Path $skillDir 'SKILL.md') $skill
    }

    & (Join-Path $PackageHome 'install\verify.ps1')
    if ($LASTEXITCODE -ne 0) {
        throw 'Kokoro setup error: verify failed.'
    }

    if ($Target -ne '') {
        $targetFull = Get-KokoroFullPath $Target
        $code = Invoke-KokoroPython @((Join-Path $PackageHome 'runtime\kokoro.py'), 'init', '--target', $targetFull)
        if ($code -ne 0) {
            throw "Kokoro setup error: could not initialize project memory in $targetFull"
        }
    }

    Write-Host 'Kokoro installed.'
    Write-Host "Package root: $(Get-KokoroDisplayPath $PackageHome)"
    Write-Host "Claude commands: $(Get-KokoroDisplayPath $Paths.CommandsTarget)"
    Write-Host "Codex skill: $(Get-KokoroDisplayPath $Paths.CodexSkillDir)"
    Write-Host "Agents skill: $(Get-KokoroDisplayPath $Paths.AgentsSkillDir)"
    Write-Host "Meta Ads connector: $(Get-KokoroDisplayPath (Join-Path $PackageHome 'connectors\meta-ads\run.ps1'))"
    Write-Host "Meta Ads credentials: $(Get-KokoroDisplayPath $Paths.MetaAdsEnvFile)"
    if ($Target -ne '') {
        Write-Host "Project memory: $(Get-KokoroDisplayPath (Join-Path (Get-KokoroFullPath $Target) '.kokoro'))"
    }
    Write-Host "Verify: $(Get-KokoroDisplayPath (Join-Path $PackageHome 'install\verify.cmd'))"
    exit 0
} catch {
    Write-Host ''
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 2
}
