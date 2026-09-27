param(
    [string]$SourceVersion = "3.0",
    [string]$TargetVersion,
    [string]$GimpRoot = (Join-Path $env:APPDATA "GIMP"),
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

function Get-ScriptRoot {
    if ($PSScriptRoot) {
        return $PSScriptRoot
    }

    return Split-Path -Parent $MyInvocation.MyCommand.Path
}

function Get-VersionFolders {
    param([string]$Root)

    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        return @()
    }

    Get-ChildItem -LiteralPath $Root -Directory -Force |
        Where-Object { $_.Name -match '^\d+\.\d+$' } |
        Sort-Object { [version]$_.Name }
}

function Get-TargetConfigDirectory {
    param(
        [string]$Root,
        [string]$RequestedVersion,
        [string]$SourceVersion
    )

    if ($RequestedVersion) {
        $requestedPath = Join-Path $Root $RequestedVersion
        if (-not (Test-Path -LiteralPath $requestedPath -PathType Container)) {
            throw "Requested GIMP config folder does not exist: $requestedPath. Start GIMP $RequestedVersion once, close it, then run this installer again."
        }

        return (Get-Item -LiteralPath $requestedPath)
    }

    $versionFolders = @(Get-VersionFolders -Root $Root)
    if ($versionFolders.Count -eq 0) {
        throw "No GIMP config folders were found under $Root. Start GIMP once, close it, then run this installer again."
    }

    $newerThanSource = @(
        $versionFolders |
            Where-Object { [version]$_.Name -gt [version]$SourceVersion }
    )

    if ($newerThanSource.Count -gt 0) {
        return $newerThanSource[-1]
    }

    return $versionFolders[-1]
}

function Copy-DirectoryContents {
    param(
        [string]$Source,
        [string]$Destination,
        [switch]$Preview
    )

    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        $destinationPath = Join-Path $Destination $_.Name

        if ($Preview) {
            Write-Host "Would copy: $($_.FullName) -> $destinationPath"
            return
        }

        Copy-Item -LiteralPath $_.FullName -Destination $destinationPath -Recurse -Force
    }
}

$scriptRoot = Get-ScriptRoot
$sourceDir = Join-Path $scriptRoot $SourceVersion

Write-Host "PhotoGIMP Windows Installer"
Write-Host "==========================="

if (-not $env:APPDATA -and -not $PSBoundParameters.ContainsKey("GimpRoot")) {
    throw "APPDATA is not set. Pass -GimpRoot with the path to your GIMP config root."
}

if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
    throw "Source UI config folder was not found: $sourceDir"
}

$targetDir = Get-TargetConfigDirectory -Root $GimpRoot -RequestedVersion $TargetVersion -SourceVersion $SourceVersion

Write-Host "Source UI config: $sourceDir"
Write-Host "Target GIMP config: $($targetDir.FullName)"

if ($targetDir.FullName -eq (Resolve-Path -LiteralPath $sourceDir).Path) {
    throw "Source and target are the same folder. Pass -TargetVersion 3.2 or install from a folder outside the target config directory."
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = "$($targetDir.FullName).backup-$timestamp"

if ($WhatIf) {
    Write-Host "Would back up: $($targetDir.FullName) -> $backupDir"
    Copy-DirectoryContents -Source $sourceDir -Destination $targetDir.FullName -Preview
    Write-Host ""
    Write-Host "Preview complete. No files were changed."
    exit 0
}

Write-Host "Backing up current config to: $backupDir"
Copy-Item -LiteralPath $targetDir.FullName -Destination $backupDir -Recurse -Force

Write-Host "Installing $SourceVersion UI config into GIMP $($targetDir.Name)..."
Copy-DirectoryContents -Source $sourceDir -Destination $targetDir.FullName

Write-Host ""
Write-Host "Done. Start GIMP $($targetDir.Name) to use the installed UI config."
Write-Host "To restore your previous settings, copy the backup contents from:"
Write-Host $backupDir
