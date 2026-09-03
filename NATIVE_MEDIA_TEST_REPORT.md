# Evidências da rota nativa de mídia localizada

Data de corte: **2026-09-03**

Estado: **implementação experimental aprovada em CI / reprodução dentro do jogo pendente**

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

O artefato Windows MinGW x64 do CI foi iniciado durante 12 segundos numa cópia isolada do Caesar III, com diretórios de preferência separados. Ele permaneceu ativo até o encerramento deliberado, criou janela e renderizador e inicializou áudio sem crash nem solicitação de diretório. Nenhum arquivo da instalação Steam foi utilizado ou alterado.

## Limites honestos

- ainda não foi acionada uma mensagem dentro do jogo para confirmar auditivamente fala, música e fallback;
- o carregamento de campanha em diretório e `.campaign` usa a infraestrutura já existente do Augustus e compilou em todas as plataformas, mas o caminho `.campaign` ainda não foi exercitado interativamente;
- esta rota não substitui o instalador da `v1.0.0-rc.2` enquanto o suporte não estiver estabilizado;
- a prova funcional interativa deverá usar somente uma cópia de teste, sem alterar a instalação Steam principal.
