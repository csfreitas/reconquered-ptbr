# Limitações conhecidas — v0.1.0-beta.1

- Requer um build do Augustus com o suporte do PR #1893 enquanto ele não estiver incorporado ao upstream.
- O pacote textual cobre RC01–RC03; RC04–RC20 ainda não estão incluídas.
- Somente a vitória de RC01 está disponível como áudio opcional nesta beta.
- O áudio opcional usa substituição local com backup porque overlays de mídia por locale ainda não integram o MVP do Augustus.
- Caracteres PT-BR podem apresentar problemas de glifo em algumas telas/fontes; relate separadamente de problemas de tradução.
- Briefing, eventos intermediários e vitória ainda precisam de validação funcional completa dentro do jogo.
- O bug de cancelamento na sequência fanfarra → fala permanece um follow-up separado e não deve ser confundido com falha do texto.
- Trilhas próprias de briefing e vitória ainda estão em curadoria e não fazem parte desta release.
- Títulos e metadados gerais da campanha fora das Custom Messages ainda podem permanecer no idioma original.
