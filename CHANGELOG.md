# Histórico de mudanças

## 8.4 — 14/11/2026 — correções de usabilidade (verificação UX)
- Nada mais flutua por cima do conteúdo: 🎙️ e 🔊 foram para a barra do topo (e o 🎙️ também ao lado da busca do Início). O botão "Auditoria visual" saiu da tela.
- Ferramentas de curadoria (Auditoria visual, auditorias das imagens e editorial, exportar CSV, contagem de retratos em produção) ficam juntas num bloco recolhido "🛠 Ferramentas do editor", no fim de Personagens.
- Títulos sem números de versão internos (ex.: "Biblioteca de personagens — v2.3" → "Biblioteca de personagens").
- Início: busca e atalhos vêm antes da esfera.
- Toques mais fáceis: nomes da Genealogia completa em tamanho de leitura (com rolagem dentro da caixa), pontos do "Comparar dois elementos" com área de toque de 44 px, botões "Mostrar tudo / Somente conexões" maiores, pontos do mapa 3D afastado mais fáceis de acertar.
- Genealogias clássicas: os nomes quebram linha em vez de sumir na direita.
- Letras pequenas de Personagens e Jogos aumentadas.
- Jornadas: o texto falava em "mapa fotografado", que não existe mais; agora diz mapa 3D.

## 8.3 — 14/11/2026
- Corrigido: o Grafo 3D ficava em branco quando o app já abria direto na tela do grafo (ao recarregar a página ou voltar ao link). Agora ele desenha sempre que a área do grafo aparece ou muda de tamanho. A mesma proteção foi aplicada ao Mapa 3D e à esfera do Início.
- Corrigido: no Grafo plano, os botões ＋ － Centralizar ficavam por cima dos botões "Grafo 3D / Grafo plano".
- O Grafo 3D ficou com altura ajustada à parte visível da tela do celular, sem ficar escondido atrás da barra de atalhos.

## 8.2 — 14/11/2026
- Grafo principal em 3D (modo padrão; o "Grafo plano" continua no botão ao lado). Os 118 elementos ficam distribuídos no espaço, com os itens ligados mais próximos uns dos outros. Arraste para girar (com embalo), dois dedos para aproximar, botões ＋ － ↻ (girar sozinho) e ◎.
- Tocar num ponto acende as conexões e abre a ficha completa ao lado (ou abaixo, no celular, pelo botão "Detalhes ↓"). Escolher um item na lista, nas conexões da ficha ou vindo da esfera do Início gira o grafo até ele.
- A busca e os filtros de categoria e era destacam os itens correspondentes no 3D.

## 8.1 — 14/11/2026
- Mapa 3D no estilo Google Earth (agora é o modo padrão; o "Mapa plano" continua disponível no botão ao lado). O mapa fica inclinado com horizonte e céu; 1 dedo move, 2 dedos aproximam e giram, 2 dedos para cima/baixo inclinam. Botões de aproximar, inclinar, bússola (volta para o norte), ver tudo e tela cheia.
- Alfinetes em pé com o nome de cada lugar; tocar num alfinete faz a câmera voar até ele e abre a ficha. Novos lugares: Fangorn, Gondor, Minas Morgul, Barad-dûr, Floresta das Trevas, Cidade do Lago, Lindon e Angmar.
- Rotas passo a passo (Sociedade do Anel, Frodo e Sam, Bilbo): a câmera acompanha o viajante parada por parada, com o texto do que aconteceu em cada lugar. Botões Anterior, Próximo, Reproduzir/Pausar e Sair da rota. A rota de Frodo e Sam ganhou Ithilien e Minas Morgul.
- Corrigido: os pontos das rotas no mapa plano estavam deslocados em relação aos desenhos do mapa; foram recalibrados.

## 8.0 — 23/10/2026
- Tela de Início: a Teia virou uma esfera 3D. Arraste com o dedo para girar (com embalo), use dois dedos para aproximar e toque num ponto para ver as conexões.
- Ao tocar num ponto aparece um cartão com a descrição e as conexões. Tocar numa conexão gira a esfera até ela; "Ver no grafo completo" abre o Grafo principal já selecionado.
- Botões "↻ Girar sozinha" e "◎ Centralizar". A esfera para de girar quando sai da tela, para economizar bateria.

## 7.9 — 23/10/2026
- Tela de Início: a Teia completa (Grafo principal, 118 elementos e 202 relações) aparece no topo. Tocar num ponto abre o grafo já com aquele elemento selecionado; o botão "⛶ Abrir" abre o grafo inteiro.
- O toque pega o ponto mais próximo do dedo, mesmo que ele não acerte o círculo exato.

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
