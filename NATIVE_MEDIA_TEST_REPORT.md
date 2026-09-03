# Evidências da rota nativa de mídia localizada

Data de corte: **2026-09-03**

Estado: **implementação experimental aprovada em CI / reprodução do briefing RC01 aprovada em campanha por diretório / rota `.campaign` pendente**

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

## Limites honestos

- fala e música do briefing RC01 foram confirmadas auditivamente em campanha por diretório; fallback, eventos intermediários, vitória e interrupção antecipada do áudio ainda não receberam evidência interativa específica;
- o carregamento de campanha em diretório está exercitado; o caminho `.campaign` usa a infraestrutura já existente do Augustus e compilou em todas as plataformas, mas ainda não foi exercitado interativamente;
- esta rota não substitui o instalador da `v1.0.0-rc.2` enquanto o suporte não estiver estabilizado;
- a prova funcional interativa deverá usar somente uma cópia de teste, sem alterar a instalação Steam principal.
