# Evidências da v1.0.0-rc.2

Data de corte: **2026-09-03**

Estado: **prerelease técnica aprovada / QA comunitário dentro do jogo pendente**

## Cobertura

- 20 missões e 198 mensagens PT-BR;
- 197 falas vinculadas por UID;
- `RC02/epithets` deliberadamente texto-only;
- dez músicas próprias, separadas das vozes;
- nenhuma mídia ou XML completo original distribuído.

## Testes automatizados e estruturais

- suíte local: **21/21 testes aprovados**;
- compilação do integrador Python e do construtor de release: aprovada;
- sintaxe dos instaladores PowerShell: aprovada;
- hashes do baseline público `fileid=2243`: 20/20;
- correspondência de UIDs e campos localizáveis: integral;
- quatro ZIPs com uma raiz comum, 240 arquivos e zero caminho duplicado;
- leitura integral e CRC: aprovados nos quatro volumes.

## Testes funcionais dos instaladores

Os dois caminhos foram exercitados em fixture limpa no host Windows:

- Python portátil: 21 arquivos de localização, 20 XMLs modificados, 197 falas e dez músicas;
- PowerShell: a mesma cobertura;
- manifesto: 248 registros por instalação;
- desinstalação: 20/20 hashes dos XMLs restaurados;
- zero overlay e zero áudio PT-BR residual;
- o ciclo Python foi repetido usando os arquivos realmente extraídos dos quatro ZIPs da `rc.2`.

## Hashes da release

| Arquivo | SHA-256 |
|---|---|
| `Reconquered-PTBR-v1.0.0-rc.2-core.zip` | `DC2EF6EE20D46CDE9B10E9FD1D48613B93B49249F3954F6A13BB1217EDB0AD5F` |
| `Reconquered-PTBR-v1.0.0-rc.2-music.zip` | `861F35E6315399BE569423465422708747488AC0DF18A3B86822F86E881E7896` |
| `Reconquered-PTBR-v1.0.0-rc.2-voices-RC01-RC10.zip` | `B70718377F435695C9D22A9C72FE678E15035E3F0D44631A6765520E0B75AA7F` |
| `Reconquered-PTBR-v1.0.0-rc.2-voices-RC11-RC20.zip` | `ED837C127CA3E2FC74A93BE6C4B056C717E54B55D7C13561ADEC2B54B31429C0` |
| `RELEASE_MANIFEST.json` | `1C9260DD063388C0B4EC729EEE74742F9BBF0E275BBCC073B313B7E6D1C4E9A3` |

## Limites honestos

- não houve teste dentro do Augustus, conforme a dispensa aprovada para a versão 1.0;
- Linux e macOS ainda não tiveram execução nativa, embora o integrador use somente Python padrão e preserve caminhos sensíveis a maiúsculas/minúsculas;
- Android, Nintendo Switch e PS Vita dependem por enquanto de preparação em computador e transferência manual;
- fanfarra seguida de fala e interrupção ao fechar briefing/evento foram aprovadas em RC01 no Windows SDL2; vitória, demais missões, glifos e equilíbrio final permanecem no QA comunitário.

## Correção sobre a rc.1

A `v1.0.0-rc.1` continha os overlays nos ZIPs, mas não os copiava automaticamente para a campanha. A `rc.2` corrige os dois instaladores, inclui os overlays no manifesto e foi validada ponta a ponta. A tag antiga não foi reescrita.
