# Reconquered PT-BR — beta comunitário não oficial

Versão: **v0.1.0-beta.1**

Baseline: **Reconquered Current público (`fileid=2243`)**

Data: **2026-09-01**

Este pacote permite à comunidade testar a localização PT-BR da campanha Reconquered no Caesar III/Augustus. Não é uma versão oficial do Reconquered e não contém mapas, músicas, imagens, vídeos, falas ou outros assets originais da campanha.

## Conteúdo desta beta

- textos completos de RC01 Óstia, RC02 Brundisium e RC03 Capua;
- configuração do locale `pt-BR`;
- áudio PT-BR próprio e opcional da vitória de RC01, Rei de Roma V01/G05;
- instalador com validação por hash e backup automático;
- desinstalador que restaura os arquivos anteriores;
- checksums e evidências de QA.

RC04–RC20 ainda não estão incluídas. Briefing e eventos intermediários de RC01 também não são publicados nesta beta porque ainda possuem gates artísticos ou funcionais pendentes.

## Requisitos

1. Uma instalação legítima de Caesar III.
2. A versão pública atual do Reconquered compatível com o baseline `fileid=2243`.
3. Um build do Augustus com suporte a overlays de mensagens customizadas:
   - [PR #1893 no Augustus](https://github.com/Keriew/augustus/pull/1893);
   - [branch de desenvolvimento no fork](https://github.com/csfreitas/augustus/tree/feature/custom-campaign-localization-overlays).

O instalador recusa versões diferentes do baseline para evitar aplicar textos ou mídia sobre cenários incompatíveis.

## Instalação

Abra o PowerShell na pasta extraída e execute:

```powershell
.\Install-Reconquered-PTBR.ps1 -CampaignDirectory "C:\caminho\para\Reconquered Campaign"
```

Para testar também a vitória PT-BR aprovada de RC01:

```powershell
.\Install-Reconquered-PTBR.ps1 -CampaignDirectory "C:\caminho\para\Reconquered Campaign" -InstallRc01VictoryAudio
```

O áudio opcional substitui localmente `audio\Ostia2.mp3`, depois de criar backup. O original não está presente neste pacote.

No Augustus, selecione o locale `pt-BR`. Se o locale do jogo estiver configurado como português compatível, o alias também poderá ser detectado conforme a configuração do overlay.

## Desinstalação

```powershell
.\Uninstall-Reconquered-PTBR.ps1 -CampaignDirectory "C:\caminho\para\Reconquered Campaign"
```

Os arquivos anteriores são restaurados a partir do backup criado durante a instalação. O backup é preservado para recuperação manual.

## Como testar

Ao relatar problemas, informe:

- versão e commit do Augustus;
- origem da instalação do Caesar III: Steam, GOG, CD-ROM ou outra;
- locale configurado;
- missão e UID/evento da mensagem;
- screenshot;
- se o problema é tradução, layout/glifo, áudio, volume, gatilho ou travamento.

Use o modelo de issue do repositório. Não envie assets originais do Reconquered.

## Estado de aprovação

Esta release está **aprovada para beta comunitário**. Isso não equivale a `approved final`:

- textos RC01–RC03 passaram pelos validadores automatizados;
- vitória G05 de RC01 foi aprovada artisticamente, masterizada e verificada tecnicamente;
- testes funcionais adicionais, glifos, mídia e playthrough continuam abertos;
- RC02 e RC03 ainda não possuem vozes finais nesta beta.

## Direitos e atribuição

Consulte [LICENSE-NOTICE.md](LICENSE-NOTICE.md). Este pacote não concede autorização para redistribuir assets de Caesar III ou Reconquered.
