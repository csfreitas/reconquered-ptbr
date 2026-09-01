param(
    [Parameter(Mandatory = $true)]
    [string]$CampaignDirectory,
    [switch]$InstallRc01VictoryAudio
)

$ErrorActionPreference = 'Stop'
$campaign = (Resolve-Path -LiteralPath $CampaignDirectory -ErrorAction Stop).Path
if ((Split-Path -Leaf $campaign) -ne 'Reconquered Campaign') {
    throw 'Destino recusado: a pasta final deve se chamar Reconquered Campaign.'
}

$installManifestPath = Join-Path $campaign '.reconquered-ptbr-install.json'
if (Test-Path -LiteralPath $installManifestPath) {
    throw 'Uma instalação PT-BR já está registrada. Desinstale-a antes de instalar novamente.'
}

$expectedScenarioHashes = [ordered]@{
    'scenario\RC01 Ostia.mapx' = 'B4CA9D04C2D94CB1AEA3E7BBA1E1E3AB01F6904BD382EEBAFF60B3006AD43ACF'
    'scenario\RC02 Brundisium.mapx' = 'F7E50095D2790F303ECA7651B99E9F4827E19DBFDFD5E47B920D74E3FFD2BC00'
    'scenario\RC03 Capua.mapx' = 'F4297ECFE96CCFE211AC02EC6E520F0418B7C610127FA58EFF7A27FBDDA05C84'
}

foreach ($entry in $expectedScenarioHashes.GetEnumerator()) {
    $path = Join-Path $campaign $entry.Key
    if (-not (Test-Path -LiteralPath $path)) { throw "Cenário ausente: $($entry.Key)" }
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if ($actual -ne $entry.Value) {
        throw "Baseline incompatível em $($entry.Key). Esperado $($entry.Value); encontrado $actual."
    }
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $campaign ".reconquered-ptbr-backup\$stamp"
$payloadRoot = Join-Path $PSScriptRoot 'payload\Reconquered Campaign'
$files = @(
    @{ Source = (Join-Path $payloadRoot 'localization\locales.xml'); Relative = 'localization\locales.xml' },
    @{ Source = (Join-Path $payloadRoot 'localization\pt-BR\messages\RC01 Ostia.xml'); Relative = 'localization\pt-BR\messages\RC01 Ostia.xml' },
    @{ Source = (Join-Path $payloadRoot 'localization\pt-BR\messages\RC02 Brundisium.xml'); Relative = 'localization\pt-BR\messages\RC02 Brundisium.xml' },
    @{ Source = (Join-Path $payloadRoot 'localization\pt-BR\messages\RC03 Capua.xml'); Relative = 'localization\pt-BR\messages\RC03 Capua.xml' }
)
if ($InstallRc01VictoryAudio) {
    $files += @{ Source = (Join-Path $PSScriptRoot 'payload\optional-audio\Ostia2.mp3'); Relative = 'audio\Ostia2.mp3' }
}

$records = @()
foreach ($file in $files) {
    if (-not (Test-Path -LiteralPath $file.Source)) { throw "Payload ausente: $($file.Source)" }
    $destination = Join-Path $campaign $file.Relative
    $hadOriginal = Test-Path -LiteralPath $destination
    if ($hadOriginal) {
        $backup = Join-Path $backupRoot $file.Relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
        Copy-Item -LiteralPath $destination -Destination $backup
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Copy-Item -LiteralPath $file.Source -Destination $destination -Force
    $records += [ordered]@{
        RelativePath = $file.Relative
        HadOriginal = $hadOriginal
        InstalledSha256 = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    }
}

$manifest = [ordered]@{
    Version = '0.1.0-beta.1'
    InstalledUtc = [DateTime]::UtcNow.ToString('o')
    CampaignDirectory = $campaign
    BackupDirectory = $backupRoot
    VictoryAudioInstalled = [bool]$InstallRc01VictoryAudio
    Files = $records
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $installManifestPath -Encoding UTF8

Write-Output "Reconquered PT-BR v0.1.0-beta.1 instalado em: $campaign"
Write-Output "Backup preservado em: $backupRoot"
Write-Output "Áudio de vitória RC01 instalado: $([bool]$InstallRc01VictoryAudio)"
