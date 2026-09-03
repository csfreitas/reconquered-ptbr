# Como contribuir

Obrigado por testar a localização brasileira do Reconquered.

## Relatos de teste

Siga o [checklist de QA comunitário](COMMUNITY_QA_CHECKLIST.md). Abra uma issue e informe missão, UID/evento, versão do Augustus, origem da instalação, locale, resultado esperado e resultado observado. Screenshots são bem-vindos; não anexe assets originais da campanha.

## Sugestões de tradução

- preserve intenção e contexto do texto público atual;
- diferencie texto oficial, comentário público do autor e dicas gerais de Augustus;
- use o Caesar III original PT-BR como referência terminológica;
- cidades presentes no `c3.eng` devem manter a grafia ali usada, como `Brundisium`, `Capua` e `Tarentum`;
- sinalize correções históricas separadamente;
- não altere decisões aprovadas silenciosamente.

## Conteúdo proibido

- material de canais privados de Tester;
- mapas, músicas, imagens, vídeos ou vozes originais do Reconquered;
- arquivos completos do Caesar III;
- imitação deliberada de voz real existente.

Ao enviar uma contribuição, você declara que possui direito de fornecê-la ao projeto para avaliação e inclusão. A licença definitiva do projeto ainda será definida antes de uma versão estável.

## Companions de mídia nativa

Não edite manualmente os 20 arquivos em `Reconquered Campaign/localization/pt-BR/media/`. Altere os planos aprovados e execute:

```sh
python3 generate_native_media_overlays.py
python3 generate_native_media_overlays.py --check
```

Cada UID precisa existir no overlay textual correspondente. Somente nomes simples de arquivo são aceitos; diretórios, prefixos de drive e travessia de caminho são proibidos. A mídia deve ser criação própria ou possuir autorização de distribuição comprovável.
