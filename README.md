# Reconquered PT-BR v1.0.0-rc.2

Este candidato comunitário localiza as 20 missões da versão pública atual do Reconquered (`fileid=2243`) para português brasileiro. Ele contém 198 mensagens, 197 falas e dez músicas próprias. Não contém mapas, XMLs completos, imagens, vídeos, sons ou músicas originais de Caesar III/Reconquered.

Release oficial do candidato: <https://github.com/csfreitas/reconquered-ptbr/releases/tag/v1.0.0-rc.2>. A `v1.0.0-rc.1` foi substituída porque seus instaladores não copiavam automaticamente os overlays textuais.

## Downloads necessários

Baixe e extraia os quatro ZIPs na mesma pasta:

1. `Reconquered-PTBR-v1.0.0-rc.2-core.zip`;
2. `Reconquered-PTBR-v1.0.0-rc.2-music.zip`;
3. `Reconquered-PTBR-v1.0.0-rc.2-voices-RC01-RC10.zip`;
4. `Reconquered-PTBR-v1.0.0-rc.2-voices-RC11-RC20.zip`.

Todos usam a mesma pasta raiz. O instalador verificará a presença e os hashes de todos os volumes antes de alterar a campanha. Ele instala automaticamente os 21 arquivos de localização, além das falas e músicas; não é necessária cópia manual da pasta `localization`.

## Windows

```powershell
.\Install-Reconquered-PTBR-Media.ps1 -CampaignDirectory "C:\caminho\para\Reconquered Campaign"
```

## Linux e macOS

```sh
python3 reconquered_ptbr_media.py install "/caminho/para/Reconquered Campaign"
```

Ou, após conceder permissão de execução ao atalho:

```sh
./install-reconquered-ptbr-media.sh "/caminho/para/Reconquered Campaign"
```

## Android, Nintendo Switch e PS Vita

Prepare a pasta `Reconquered Campaign` em Windows, Linux ou macOS usando um dos instaladores acima. Depois transfira a pasta já preparada para o diretório de dados do Caesar III/Augustus no dispositivo. Preserve o backup criado pelo instalador no computador.

## Desinstalação

Use o desinstalador da mesma família utilizada na instalação:

```powershell
.\Uninstall-Reconquered-PTBR-Media.ps1 -CampaignDirectory "C:\caminho\para\Reconquered Campaign"
```

```sh
python3 reconquered_ptbr_media.py uninstall "/caminho/para/Reconquered Campaign"
```

## Requisitos e limites

- requer a versão pública atual do Reconquered correspondente aos hashes do pacote;
- requer o suporte textual do Augustus PR #1893 ou build compatível;
- a integração audiovisual modifica somente os XMLs públicos presentes no computador do usuário e cria backup;
- o instalador recusa baseline divergente ou volume ausente antes da primeira alteração;
- o QA dentro do jogo será comunitário, conforme decisão do projeto para a versão 1.0.

## Conteúdo deste repositório

A árvore Git contém os 20 overlays PT-BR, planos de integração, instaladores e documentação. Os WAVs não são versionados devido ao tamanho; estão somente nos assets da release. Contribuições e relatos devem seguir [CONTRIBUTING.md](CONTRIBUTING.md), sem anexar conteúdo original do Reconquered ou Caesar III.

## Evolução experimental: mídia localizada nativa

A branch `feature/native-localized-media-package` prepara uma rota futura para builds do Augustus que ofereçam mídia localizada nativa. Ela não altera a `v1.0.0-rc.2` publicada.

Nessa rota, o pacote instala somente arquivos próprios em:

```text
localization/pt-BR/messages/
localization/pt-BR/media/
localization/pt-BR/audio/
```

Os XMLs canônicos do Reconquered são validados, mas não são modificados. Os 20 companions são gerados de modo reproduzível com `generate_native_media_overlays.py`. O instalador experimental é `reconquered_ptbr_native_media.py`; consulte [NATIVE_MEDIA_TEST_REPORT.md](NATIVE_MEDIA_TEST_REPORT.md) para o estado real da validação.
