# Evidências da v0.1.0-beta.1

Data de corte: **2026-09-01**

## Overlay textual

- suíte automatizada: **12/12 testes aprovados**;
- RC01: 6/6 UIDs, zero erros e seis avisos esperados de mídia não representável no overlay textual;
- RC02: 10/10 UIDs, zero erros e zero avisos;
- RC03: 12/12 UIDs, zero erros e dois avisos esperados de áudio ainda pendente;
- caracteres de substituição UTF-8: nenhum encontrado.

## Vitória RC01 G05

- Voice ID V01: `XScFJJnNp0BwI1Kt6Ets`;
- modelo: Eleven v3;
- estado: `approved artistic / in-game QA pending`;
- duração: 22,32 s;
- loudness: -16,2 LUFS;
- LRA: 1,6 LU;
- true peak: -1,5 dBFS;
- MP3: estéreo, 44,1 kHz, 192 kbps;
- decodificação integral: aprovada;
- SHA-256 do áudio distribuído: `8E4D99B813418B9C351B61E2A9656C53B6F7B30AD07C3FCE7BBC27C7E469B208`.

## Compatibilidade do baseline

O instalador exige os seguintes hashes dos cenários públicos atuais:

| Cenário | SHA-256 |
|---|---|
| `RC01 Ostia.mapx` | `B4CA9D04C2D94CB1AEA3E7BBA1E1E3AB01F6904BD382EEBAFF60B3006AD43ACF` |
| `RC02 Brundisium.mapx` | `F7E50095D2790F303ECA7651B99E9F4827E19DBFDFD5E47B920D74E3FFD2BC00` |
| `RC03 Capua.mapx` | `F4297ECFE96CCFE211AC02EC6E520F0418B7C610127FA58EFF7A27FBDDA05C84` |

## Instalações já exercitadas no desenvolvimento

- Caesar III PT-BR original em CD-ROM;
- instalação Steam verificada por integridade;
- cópia isolada baseada no CD-ROM com build do Augustus do PR;
- instalação da vitória G05 validada por hash na cópia isolada;
- instalação Steam não alterada durante a integração G05.

## Instalador da release

- baseline RC01–RC03 correto: aceito;
- três overlays instalados: confirmado;
- áudio opcional G05 instalado: hash `8E4D99B813418B9C351B61E2A9656C53B6F7B30AD07C3FCE7BBC27C7E469B208` confirmado;
- manifesto e backup automático: confirmados;
- desinstalação: áudio original restaurado pelo mesmo hash;
- overlays sem versão anterior: removidos durante a desinstalação;
- manifesto ativo: removido e arquivado no backup;
- baseline incompatível: recusado antes de qualquer instalação;
- cenário modificado usado no teste negativo: hash `C393E5F22BFBADE9ADEA40A9DF2910DA81B9ED8592F04EE94A35770D495D3EE8`.

Esta evidência aprova a release para teste comunitário, não como versão final da campanha completa.
