# Limitações conhecidas — v1.0.0-rc.2

- Requer um build do Augustus com o suporte do PR #1893 enquanto ele não estiver incorporado ao upstream.
- O instalador aceita somente o baseline público Reconquered `fileid=2243`; a próxima grande atualização exigirá reconciliação e novos hashes.
- Caracteres PT-BR podem apresentar problemas de glifo em algumas telas/fontes; isso deve ser relatado separadamente da tradução.
- Sequência fanfarra → fala, interrupção ao fechar mensagens e equilíbrio dos controles de voz/música aguardam QA comunitário dentro do jogo.
- `RC02/epithets` é deliberadamente texto-only por ser um tutorial mecânico.
- As músicas são derivadas das prévias MP3 fornecidas pela EasyMusic e entregues em WAV após ajuste de nível; uma futura fonte WAV oficial poderá substituí-las.
- O pacote não localiza ainda todos os metadados externos às Custom Messages, como certos títulos gerais da campanha.
- Android, Nintendo Switch e PS Vita não executam o instalador incluído; prepare a campanha em um computador antes de transferi-la.
- A rota nativa de mídia permanece experimental e depende da branch correspondente no fork do Augustus; ela ainda não possui uma segunda PR upstream.
- A instalação/desinstalação nativa já passou em fixture completa, mas a seleção e reprodução dentro do jogo e o caminho `.campaign` ainda exigem prova funcional interativa.
