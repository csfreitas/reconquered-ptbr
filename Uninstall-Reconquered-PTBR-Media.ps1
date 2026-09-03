param(
    [Parameter(Mandatory = $true)]
    [string]$CampaignDirectory
)

$ErrorActionPreference = 'Stop'
$campaign = (Resolve-Path -LiteralPath $CampaignDirectory -ErrorAction Stop).Path
if ((Split-Path -Leaf $campaign) -ne 'Reconquered Campaign') {
    throw 'Destino recusado: a pasta final deve se chamar Reconquered Campaign.'
}

$installManifestPath = Join-Path $campaign '.reconquered-ptbr-media-install.json'
if (-not (Test-Path -LiteralPath $installManifestPath)) {
    throw 'Manifesto da integração audiovisual PT-BR não encontrado.'
}
$manifest = Get-Content -LiteralPath $installManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$backupRoot = $manifest.BackupDirectory

foreach ($file in $manifest.Files) {
    $destination = Join-Path $campaign $file.RelativePath
    if (-not (Test-Path -LiteralPath $destination)) {
        throw "Arquivo instalado ausente; desinstalação interrompida: $($file.RelativePath)"
    }
    $actual = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    if ($actual -ne $file.InstalledSha256) {
        throw "Arquivo alterado após a instalação; desinstalação recusada para preservar mudanças: $($file.RelativePath)"
    }
}

foreach ($file in $manifest.Files) {
    $destination = Join-Path $campaign $file.RelativePath
    if ($file.HadOriginal) {
        $backup = Join-Path $backupRoot $file.RelativePath
        if (-not (Test-Path -LiteralPath $backup)) { throw "Backup ausente: $backup" }
        Copy-Item -LiteralPath $backup -Destination $destination -Force
    } else {
        Remove-Item -LiteralPath $destination -Force
    }
}

$archivedManifest = Join-Path $backupRoot 'uninstalled-media-install-manifest.json'
Copy-Item -LiteralPath $installManifestPath -Destination $archivedManifest -Force
Remove-Item -LiteralPath $installManifestPath -Force

Write-Output 'Integração audiovisual PT-BR removida. Os XMLs e arquivos anteriores foram restaurados.'
Write-Output "Backup preservado em: $backupRoot"
