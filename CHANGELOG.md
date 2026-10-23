# Histórico de mudanças

## 7.8 — 23/10/2026
- Corrigido: o Grafo principal não abria. Itens adicionados por outras partes do app (livros, filmes, famílias) não entravam na lista do grafo; agora o grafo se atualiza sozinho antes de desenhar.
- Corrigido: relações que apontam para itens inexistentes agora são ignoradas, com um único aviso no console, sem travar o desenho.
- Corrigido: os botões "Explorar no mapa" da Cronologia e os botões das seções Obras e Genealogias também deixam de dar erro (era o mesmo problema do grafo).
- Cronologia: eventos sem data ficam de fora e aparece o aviso "N acontecimentos sem data definida".
- Versão unificada: o número 7.8 fica em um só lugar (ATLAS_VERSAO) e o título e o cabeçalho leem dele.
- Genealogias completas: a árvore rola dentro da própria caixa e a página não rola mais para o lado no celular.

## 7.7 — 23/10/2026
- Busca por voz 🎙️: abre a ficha do personagem, marca o lugar no mapa, pesquisa na Teia e muda de seção ("abrir famílias").
- Leitura em voz alta 🔊 da ficha aberta, dividida em frases curtas para o Chrome do Android não cortar a fala.
- Corrigido: a auditoria de conexões quebrava ao abrir a página ("people is not defined").
- Corrigido: aparecia um "\n" escrito na tela inicial, e o mesmo erro anulava parte do estilo visual.
- Corrigido: a busca da Teia agora dá prioridade ao nome exato ("Mordor" abre o lugar, não o jogo *Shadow of Mordor*).

## 7.1 — base anterior
- Tela inicial, galeria de retratos, mapa ilustrado com jornadas, seção de jogos e mapa em tela cheia.
