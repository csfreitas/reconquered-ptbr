param(
    [Parameter(Mandatory = $true)]
    [string]$CampaignDirectory
)

$ErrorActionPreference = 'Stop'
$campaign = (Resolve-Path -LiteralPath $CampaignDirectory -ErrorAction Stop).Path
if ((Split-Path -Leaf $campaign) -ne 'Reconquered Campaign') {
    throw 'Destino recusado: a pasta final deve se chamar Reconquered Campaign.'
}

$installManifestPath = Join-Path $campaign '.reconquered-ptbr-install.json'
if (-not (Test-Path -LiteralPath $installManifestPath)) {
    throw 'Manifesto de instalação PT-BR não encontrado.'
}
$manifest = Get-Content -LiteralPath $installManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$backupRoot = $manifest.BackupDirectory

foreach ($file in $manifest.Files) {
    $destination = Join-Path $campaign $file.RelativePath
    if ($file.HadOriginal) {
        $backup = Join-Path $backupRoot $file.RelativePath
        if (-not (Test-Path -LiteralPath $backup)) { throw "Backup ausente: $backup" }
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        Copy-Item -LiteralPath $backup -Destination $destination -Force
    } elseif (Test-Path -LiteralPath $destination) {
        Remove-Item -LiteralPath $destination -Force
    }
}

$archivedManifest = Join-Path $backupRoot 'uninstalled-install-manifest.json'
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
Copy-Item -LiteralPath $installManifestPath -Destination $archivedManifest -Force
Remove-Item -LiteralPath $installManifestPath -Force

Write-Output 'Reconquered PT-BR removido. Arquivos anteriores restaurados.'
Write-Output "Backup preservado em: $backupRoot"
