# Evidências da rota nativa de mídia localizada

Data de corte: **2026-09-03**

Estado: **implementação experimental aprovada em CI / reprodução do briefing RC01 aprovada em campanha por diretório e pacote `.campaign`**

## Augustus

- branch: [`feature/custom-campaign-localized-media-overlays`](https://github.com/csfreitas/augustus/tree/feature/custom-campaign-localized-media-overlays);
- commit inicial: [`3b0fce9c1`](https://github.com/csfreitas/augustus/commit/3b0fce9c11fa922a33163ddd8be7a9017b629529);
- CI: [18/18 alvos aprovados](https://github.com/csfreitas/augustus/actions/runs/33713629827);
- nenhuma segunda PR foi aberta no upstream.

A matriz aprovada inclui Windows MinGW/MSVC, Linux x64/ARM64/SDL2/SDL3, Flatpak, AppImage, macOS, iOS, Android/SDL3, Emscripten, Nintendo Switch e PS Vita.

## Estrutura validada

```text
localization/<locale>/messages/<scenario>.xml
localization/<locale>/media/<scenario>.xml
localization/<locale>/audio/<filename>
```

O companion aceita `speech` e `background_music`. Entradas ou arquivos ausentes retornam à mídia canônica de forma independente. Companion inválido não invalida o overlay textual.

## Geração do pacote

- CI do pacote: [Windows, Linux e macOS aprovados](https://github.com/csfreitas/reconquered-ptbr/actions/runs/33756063857);
- 20 companions gerados a partir dos planos aprovados;
- 20/20 companions reproduzíveis em modo `--check`;
- UIDs conferidos contra os overlays textuais;
- formas reais de UID preservadas, inclusive `Victory` e `victory`;
- nomes de arquivo validados contra diretório, drive e travessia de caminho;
- nenhuma mídia ou XML canônico original adicionado ao Git.

## Teste do instalador nativo

Uma cópia local do baseline público `fileid=2243` recebeu o pacote completo:

- 20 missões;
- 41 arquivos de localização: um manifesto de locales, 20 overlays textuais e 20 companions de mídia;
- 197 falas;
- dez músicas;
- 207 arquivos de áudio próprios;
- 248 registros reversíveis;
- 20/20 hashes dos XMLs canônicos permaneceram iguais ao baseline durante a instalação.

O comando de verificação confirmou todos os arquivos e hashes instalados. Após a desinstalação:

- 20/20 hashes dos XMLs permaneceram restaurados;
- zero divergência de hash;
- manifesto nativo ausente;
- diretório nativo de mídia ausente;
- diretório nativo de áudio ausente;
- overlays anteriores foram restaurados quando já existiam.

O teste unitário usa payload sintético próprio e cobre instalação, verificação, preservação do XML canônico, backup, desinstalação e remoção de diretórios vazios.

O artefato Windows MinGW x64 do CI foi iniciado durante 12 segundos numa cópia isolada do Caesar III e recebeu explicitamente essa cópia como diretório de dados. Ele permaneceu ativo até o encerramento deliberado, criou janela e renderizador e inicializou áudio sem crash nem solicitação de diretório. Nenhum arquivo da instalação Steam foi utilizado ou alterado.

## Teste funcional interativo — RC01 Ostia

Em 2026-09-03, o mesmo artefato foi aberto contra a cópia isolada e a campanha em diretório. Antes da execução, os 32 arquivos existentes no diretório global de preferências do Augustus foram copiados e inventariados por SHA-256. O teste alterou somente `augustus-log.txt` e `augustus-log-backup.txt`; ambos foram restaurados a partir da cópia, e a comparação final confirmou 32/32 arquivos idênticos ao estado anterior.

O log confirmou, na mesma sessão:

```text
Loading custom campaign scenario  RC01 Ostia.mapx
Loaded custom message localization  localization/pt-BR/messages/RC01 Ostia.xml
Loaded custom message media localization  localization/pt-BR/media/RC01 Ostia.xml
```

O responsável pelo projeto iniciou RC01 Ostia e aprovou o briefing como “impecável”. Texto, voz PT-BR e música foram reproduzidos juntos com equilíbrio artístico aprovado. A fixture não correspondia ao patch 1.0.1.0 e não continha o pacote completo de assets do build; por isso o log registrou avisos de assets ausentes e falhas ao gravar save/configuração. Essas limitações não impediram o carregamento dos dois overlays nem a reprodução do briefing e não foram atribuídas à feature de mídia localizada.

### Pacote `.campaign`

A mesma campanha instalada foi empacotada localmente como ZIP com extensão `.campaign`, sem o backup e sem o manifesto do instalador. A inspeção anterior à execução confirmou 658 entradas, 647 arquivos, zero nome duplicado e presença de `Settings.xml`, mapa RC01, overlay textual, companion de mídia, fala e música do briefing. O arquivo de teste possui SHA-256 `C463ED750938F7FD39DA38C7D897450C2A0581645604EC3205CCD01F7E813A6B` e não foi publicado.

Com a campanha em diretório removida temporariamente da lista, Augustus reconheceu o `.campaign`, exibiu seus metadados e iniciou RC01 Ostia. O log registrou duas vezes o carregamento conjunto do cenário, do overlay textual e do companion de mídia. O responsável confirmou novamente que o briefing estava correto. A [captura da seleção da campanha](docs/evidence/2026-09-03-rc01-campaign-package-selection.png) registra o pacote reconhecido pela interface.

O botão **Seleção de cenários** apareceu desativado porque esse nome de pacote ainda possuía `current_mission = 0`. O comportamento é intencional: o código habilita a lista somente quando `current_mission > 0`, depois que existe progresso na campanha. **Iniciar campanha** permaneceu disponível e abriu Ostia normalmente.

Depois do teste, o `.campaign` foi retirado da pasta ativa e preservado somente no scratch local; a campanha em diretório foi restaurada. Nenhum arquivo da Steam foi tocado.

### Matriz de fallback de mídia

Quatro variações temporárias do companion de RC01 foram exercitadas na campanha em diretório. O arquivo aprovado foi copiado antes da rodada e restaurado ao final com igualdade exata de SHA-256: `5E990DBD056CDE78539D5969C461C3438A44013889681481F7E7FB52E57DCBB7`.

| Caso | Companion | Resultado confirmado |
|---|---|---|
| fala localizada aponta para arquivo ausente | válido; música localizada presente | texto PT-BR, fala canônica em inglês e música localizada |
| música localizada aponta para arquivo ausente | válido; fala localizada presente | texto e fala PT-BR, música canônica `ROME2.wav` |
| versão do companion incompatível | inválido (`version="2"`) | texto PT-BR preservado; fala e música canônicas |
| entrada `intro` ausente | válido; outras entradas preservadas | texto PT-BR; fala e música canônicas |

Nos casos válidos, o log confirmou o carregamento do overlay textual e do companion. No caso inválido, confirmou primeiro o overlay textual e depois registrou `Unsupported custom message media localization version` e `Unable to load custom message media localization`, sem descartar a tradução. Todos os quatro resultados auditivos foram confirmados pelo responsável.

As preferências globais foram preservadas antes de cada execução. Depois da última rodada, a comparação retornou 32 arquivos, zero divergência e zero ausência. A instalação Steam não participou dos testes.

## Limites honestos

- fala, música, os quatro fallbacks e a interrupção antecipada do briefing RC01 foram confirmados auditivamente em campanha por diretório; ao iniciar a missão imediatamente, fala e música pararam corretamente;
- a tentativa de alcançar o primeiro evento ficou inconclusiva porque o Mapa do Império travou na fixture sem o conjunto completo de assets. O log registrou ausência maciça de grupos `UI`, `Terrain_Maps`, `Industry` e outros; esse resultado não foi atribuído ao overlay;
- o commit [`993bcaa5c`](https://github.com/csfreitas/augustus/commit/993bcaa5c75233df2ad89bfa9ee865e29d2ae7c1) limpa callbacks pendentes antes da parada explícita em briefing, eventos e vitória pela API comum SDL2/SDL3. A [matriz multiplataforma](https://github.com/csfreitas/augustus/actions/runs/33774971291) passou em 18/18 alvos; o teste interativo específico fanfarra → fala continua pendente em uma instalação de teste completa;
- carregamento por diretório e `.campaign` está exercitado no artefato Windows; a execução funcional nativa nas demais plataformas continua dependente de QA comunitário;
- esta rota não substitui o instalador da `v1.0.0-rc.2` enquanto o suporte não estiver estabilizado;
- a prova funcional interativa deverá usar somente uma cópia de teste, sem alterar a instalação Steam principal.
