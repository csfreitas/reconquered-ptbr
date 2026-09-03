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
if (Test-Path -LiteralPath $installManifestPath) {
    throw 'A integração audiovisual PT-BR já está registrada. Desinstale-a antes de reinstalar.'
}
if (Test-Path -LiteralPath (Join-Path $campaign '.reconquered-ptbr-music-install.json')) {
    throw 'A integração musical isolada está instalada. Remova-a antes de instalar o pacote audiovisual completo.'
}
if (Test-Path -LiteralPath (Join-Path $campaign '.reconquered-ptbr-install.json')) {
    throw 'A beta PT-BR antiga está instalada. Remova-a antes de instalar o pacote completo.'
}

$musicPlanPath = Join-Path $PSScriptRoot 'MEDIA_INTEGRATION_PLAN.json'
$speechPlanPath = Join-Path $PSScriptRoot 'SPEECH_INTEGRATION_PLAN.json'
$payloadAudio = Join-Path $PSScriptRoot 'Reconquered Campaign\audio'
$payloadLocalization = Join-Path $PSScriptRoot 'Reconquered Campaign\localization'
$musicPlan = Get-Content -LiteralPath $musicPlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
$speechPlan = Get-Content -LiteralPath $speechPlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
$speechByMission = @{}
foreach ($mission in $speechPlan.missions) { $speechByMission[$mission.id] = $mission }
$musicHashes = @{}
foreach ($asset in $musicPlan.assets) { $musicHashes[$asset.file] = $asset.sha256 }

$expectedLocalization = @('locales.xml')
foreach ($mission in $musicPlan.missions) {
    $overlayName = $mission.xml -replace ' corrected\.xml$', '.xml'
    $expectedLocalization += (Join-Path 'pt-BR\messages' $overlayName)
}
$localizationFiles = @(Get-ChildItem -LiteralPath $payloadLocalization -File -Recurse)
$actualLocalization = @($localizationFiles | ForEach-Object { $_.FullName.Substring($payloadLocalization.Length + 1) })
$missingLocalization = @($expectedLocalization | Where-Object { $_ -notin $actualLocalization })
$unexpectedLocalization = @($actualLocalization | Where-Object { $_ -notin $expectedLocalization })
if ($missingLocalization.Count -gt 0 -or $unexpectedLocalization.Count -gt 0) {
    throw "Payload de localização inválido. Ausentes: $($missingLocalization -join ', '); inesperados: $($unexpectedLocalization -join ', ')."
}

# Valide completamente baseline, XML e payload antes da primeira escrita.
$audioNames = @()
foreach ($mission in $musicPlan.missions) {
    if (-not $speechByMission.ContainsKey($mission.id)) { throw "Plano de fala ausente para $($mission.id)." }
    $speechMission = $speechByMission[$mission.id]
    if ($speechMission.xml -ne $mission.xml -or $speechMission.baseline_sha256 -ne $mission.sha256) {
        throw "Planos de mídia divergentes para $($mission.id)."
    }
    $xml = Join-Path $campaign (Join-Path 'xmls' $mission.xml)
    if (-not (Test-Path -LiteralPath $xml)) { throw "XML ausente: $($mission.xml)" }
    $actual = (Get-FileHash -LiteralPath $xml -Algorithm SHA256).Hash
    if ($actual -ne $mission.sha256) {
        throw "Baseline incompatível em $($mission.xml). Esperado $($mission.sha256); encontrado $actual."
    }
    $document = [Xml.XmlDocument]::new()
    $document.PreserveWhitespace = $true
    $document.Load($xml)
    $briefing = @($document.messages.message.background_music | Where-Object { $_.filename -ieq $musicPlan.briefing_original })
    $victory = @($document.messages.message.background_music | Where-Object { $_.filename -ieq $musicPlan.victory_original })
    if ($briefing.Count -ne 1 -or $victory.Count -ne 1) {
        throw "Referências musicais únicas não encontradas em $($mission.xml)."
    }
    foreach ($speech in $speechMission.speech) {
        $nodes = @($document.messages.message | Where-Object { $_.uid -ceq $speech.uid })
        if ($nodes.Count -ne 1) { throw "UID de fala ausente ou duplicado em $($mission.xml): $($speech.uid)" }
        $audioNames += $speech.file
    }
    $audioNames += $mission.briefing
    $audioNames += $mission.victory
}

$audioNames = @($audioNames | Sort-Object -Unique)
foreach ($name in $audioNames) {
    $source = Join-Path $payloadAudio $name
    if (-not (Test-Path -LiteralPath $source)) { throw "Áudio ausente no payload: $name" }
    $plannedSpeech = @($speechPlan.missions.speech | Where-Object { $_.file -eq $name })
    if ($plannedSpeech.Count -gt 0) {
        $actual = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
        if ($plannedSpeech[0].sha256 -ne $actual) { throw "Hash de fala divergente: $name" }
    } elseif ($musicHashes.ContainsKey($name)) {
        $actual = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
        if ($musicHashes[$name] -ne $actual) { throw "Hash de música divergente: $name" }
    } else {
        throw "Áudio sem hash registrado nos planos: $name"
    }
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $campaign ".reconquered-ptbr-media-backup\$stamp"
$records = @()

foreach ($source in $localizationFiles) {
    $payloadRelative = $source.FullName.Substring($payloadLocalization.Length + 1)
    $relative = Join-Path 'localization' $payloadRelative
    $destination = Join-Path $campaign $relative
    $hadOriginal = Test-Path -LiteralPath $destination
    if ($hadOriginal) {
        $backup = Join-Path $backupRoot $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
        Copy-Item -LiteralPath $destination -Destination $backup
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Copy-Item -LiteralPath $source.FullName -Destination $destination -Force
    $records += [ordered]@{
        Kind = 'localization'
        RelativePath = $relative
        HadOriginal = $hadOriginal
        InstalledSha256 = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    }
}

foreach ($mission in $musicPlan.missions) {
    $speechMission = $speechByMission[$mission.id]
    $relative = Join-Path 'xmls' $mission.xml
    $xml = Join-Path $campaign $relative
    $backup = Join-Path $backupRoot $relative
    New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
    Copy-Item -LiteralPath $xml -Destination $backup

    $document = [Xml.XmlDocument]::new()
    $document.PreserveWhitespace = $true
    $document.Load($xml)
    (@($document.messages.message.background_music | Where-Object { $_.filename -ieq $musicPlan.briefing_original }))[0].SetAttribute('filename', $mission.briefing)
    (@($document.messages.message.background_music | Where-Object { $_.filename -ieq $musicPlan.victory_original }))[0].SetAttribute('filename', $mission.victory)

    foreach ($speech in $speechMission.speech) {
        $message = (@($document.messages.message | Where-Object { $_.uid -ceq $speech.uid }))[0]
        $speechNodes = @($message.media | Where-Object { $_.type -ieq 'speech' })
        if ($speechNodes.Count -gt 1) { throw "Mais de uma fala já vinculada ao UID $($speech.uid)." }
        if ($speechNodes.Count -eq 1) {
            $speechNodes[0].SetAttribute('filename', $speech.file)
        } else {
            $node = $document.CreateElement('media')
            $node.SetAttribute('type', 'speech')
            $node.SetAttribute('filename', $speech.file)
            [void]$message.AppendChild($node)
        }
    }

    $settings = [Xml.XmlWriterSettings]::new()
    $settings.Encoding = [Text.UTF8Encoding]::new($false)
    $settings.Indent = $false
    $settings.NewLineHandling = [Xml.NewLineHandling]::None
    $writer = [Xml.XmlWriter]::Create($xml, $settings)
    try { $document.Save($writer) } finally { $writer.Dispose() }

    $records += [ordered]@{
        Kind = 'xml'
        RelativePath = $relative
        HadOriginal = $true
        InstalledSha256 = (Get-FileHash -LiteralPath $xml -Algorithm SHA256).Hash
    }
}

foreach ($name in $audioNames) {
    $relative = Join-Path 'audio' $name
    $source = Join-Path $payloadAudio $name
    $destination = Join-Path $campaign $relative
    $hadOriginal = Test-Path -LiteralPath $destination
    if ($hadOriginal) {
        $backup = Join-Path $backupRoot $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
        Copy-Item -LiteralPath $destination -Destination $backup
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Force
    $records += [ordered]@{
        Kind = 'audio'
        RelativePath = $relative
        HadOriginal = $hadOriginal
        InstalledSha256 = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    }
}

$manifest = [ordered]@{
    Component = 'Reconquered PT-BR audiovisual integration'
    InstalledUtc = [DateTime]::UtcNow.ToString('o')
    CampaignDirectory = $campaign
    BackupDirectory = $backupRoot
    Missions = $musicPlan.missions.Count
    LocalizationFiles = $localizationFiles.Count
    SpeechFiles = ($speechPlan.missions.speech | Measure-Object).Count
    MusicFiles = 10
    Files = $records
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $installManifestPath -Encoding UTF8

Write-Output "Integração audiovisual PT-BR instalada em: $campaign"
Write-Output "21 arquivos de localização instalados; 20 XMLs atualizados; 197 falas e 10 músicas próprias instaladas. Backup: $backupRoot"
