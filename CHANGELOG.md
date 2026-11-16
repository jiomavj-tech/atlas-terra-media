# Histórico de mudanças

## 12.5 — 16/11/2026 — conexões dos personagens catalogadas (Tarefa 5) e mais acabamento
- **Conexões**: a auditoria mostrava 158 de 190 fichas com pendência. Em 150 delas o campo dizia só "A catalogar"; as outras 8 tinham nomes que não batiam com nenhuma ficha.
  - As 150 fichas ganharam as ligações principais com outros personagens do Atlas (família, aliados, inimigos), tiradas da obra citada em cada ficha.
  - Dos 8 nomes soltos, 5 foram ligados à ficha certa (Thorin; Idril e Morwen dos jogos). Os outros 3 são lugares (Gondor, Valfenda, Lothlórien) e ficaram só como texto.
  - Resultado: 0 pendências e nenhuma ligação apontando para ficha inexistente. A lista completa está em `tools/catalogar_conexoes.py`.
- **Valfenda**: as cachoeiras passaram para o modelo novo, com fios de água e névoa.
- **Fangorn**: a clareira do Valarcano ficou maior e mais clara, e os Ents mais claros, para aparecerem.

## 12.4 — 16/11/2026 — revisão de acabamento
- **Cachoeiras**: novo modelo, com fios de água que se abrem ao cair e névoa na base, no lugar da placa clara. Usado nas Quedas de Rauros e em Henneth Annûn.
- **Forte da Trombeta**: fortaleza 70% maior, com torre mais alta, mais torres na muralha e a Muralha do Abismo mais alta.
- **Fangorn**: Ents maiores, para aparecerem entre as árvores.
- **Barcos élficos** (Portos Cinzentos, Lothlórien e Parth Galen): casco branco em vez de escuro.
- **Colinas dos Túmulos**: os morros não se empilham mais num pico pontudo.

## 12.3 — 16/11/2026 — Barad-dûr, Floresta Velha, Thranduil, Beorn, Fano-da-Colina e Henneth Annûn de perto
- **Barad-dûr**: a Torre Negra em degraus, com três anéis de muralhas e torres, as pontas no alto com o Olho, janelas de fogo, a ponte de ferro, o fosso de lava em volta da rocha e as forjas do planalto. 6 lugares e a rota "A Torre Negra".
- **Floresta Velha e Colinas dos Túmulos**: o Velho Salgueiro-homem à beira do Voltavime, a casa de Tom Bombadil com janelas acesas, flores e o lago dos lírios, a pedra erguida e os túmulos com anéis de pedras sob a névoa. 7 lugares e a rota "Tom Bombadil".
- **Salões de Thranduil**: a ponte e os portões de pedra na colina, lanternas, o alçapão com os barris descendo o rio, a clareira das festas e as teias das aranhas. 6 lugares e a rota "Barris soltos".
- **Carrocha e casa de Beorn**: o rochedo no meio do Anduin com os degraus e o vau, o salão de madeira de Beorn com colmeias, cerca viva, carvalhos e campos de trevo, e o Ninho das Águias. 6 lugares e a rota "Da Carrocha à casa de Beorn".
- **Fano-da-Colina**: a estrada em zigue-zague com os homens-Púkel, o campo alto com o acampamento de Rohan, a fila de pedras erguidas, o Dimholt e a Porta Escura sob o Dwimorberg. 7 lugares e a rota "As Sendas dos Mortos".
- **Henneth Annûn**: a cachoeira com a caverna atrás, o Lago Proibido com Gollum, a emboscada aos Haradrim com um olifante, a fogueira de Sam e Ithilien florida. 6 lugares e a rota "A Janela do Poente".
- Quatro lugares novos no mapa geral: Floresta Velha, Salões de Thranduil, Fano-da-Colina e Henneth Annûn.

## 12.2 — 16/11/2026 — correção do globo travando
- Causa encontrada: desde a 12.0 o globo fica dentro do palco do mapa 3D, e cada toque nele também chegava ao mapa de baixo. Arrastar o globo movia e redesenhava o mapa 3D inteiro, com todos os nomes, a cada movimento do dedo.
- Agora os toques no globo param no globo, e o mapa 3D não redesenha enquanto o globo está aberto.
- Uma região de detalhe que falhar ao carregar não é mais tentada de novo a cada quadro.

## 12.1 — 16/11/2026 — globo mais leve
- O globo travava no celular. Mudanças para aliviar:
  - Os nomes sobre o globo não recalculam mais a página a cada quadro (medidos uma vez, movidos com `transform`).
  - Ao arrastar, o globo é desenhado no máximo uma vez por quadro.
  - Com o globo aberto, o mapa 3D que fica por baixo é escondido.
  - O globo é carregado com antecedência, parado, para a primeira passagem não engasgar.
  - Resolução do desenho limitada a 1,5× e sem filtro anisotrópico. Em aparelhos com 4 GB de memória ou menos, a textura do globo cai para 2048 × 1024.

## 12.0 — 16/11/2026 — o mundo e a Terra-média viraram um mapa só; Mapa e Teia na mesma seção
- **Zoom contínuo de Arda até a Terra-média**: o globo agora mostra a Terra-média do próprio Atlas (o mesmo desenho do mapa 3D), no lugar certo do continente. Antes eram dois mapas diferentes, com uma troca de tela no meio.
  - Afastando o mapa até o fim (ou tocando em "Ver o mundo"), a câmera vai para a vista de cima e o globo aparece por cima, alinhado, e se afasta.
  - Aproximando o globo sobre a Terra-média (ou tocando em "Voltar à Terra-média"), o globo gira até ficar alinhado, some, e o mapa 3D continua dali.
  - O globo ficou com textura 4 vezes maior (4096 × 2048).
- **Arda no fim da Terceira Era**: Beleriand aparece afundada no mar, e os mares interiores foram redesenhados para não cobrir a Terra-média.
- **Seção "Explorar"**: Mapa, Teia e Grafo 3D ficam na mesma seção, com botões no topo para trocar. A aba "Arda (mundo)" saiu, porque o globo agora faz parte do mapa.
- A barra de baixo ficou: Início · Pessoas · Explorar · Famílias · História · Mais.
- O mapa passou a ser a primeira coisa da tela e ficou mais alto; os textos e as listas vêm embaixo.

## 11.5 — 16/11/2026 — Fangorn, Rauros, Portos Cinzentos, Fornost, Pelargir e Dol Amroth de perto
- **Fangorn**: a floresta densa, a colina de rocha de Barbárvore junto ao Entágua (com um Ent ao lado), a Gruta da Nascente, o Valarcano com os Ents em roda e o monte dos orcs queimados na borda. 5 lugares e a rota "Os Ents de Fangorn".
- **Rauros e Amon Hen**: o lago Nen Hithoel com a água nivelada, as estátuas gigantes do Argonath, Parth Galen com os três barcos, o Assento da Visão no alto de Amon Hen, Tol Brandir, Amon Lhaw, as quedas e o lugar onde Boromir caiu. 8 lugares e a rota "A dissolução da Sociedade".
- **Portos Cinzentos**: Mithlond nas duas margens do golfo, com casas e torres brancas, os cais, o Navio Branco, barcos élficos e o estaleiro de Círdan. 7 lugares e a rota "A última viagem".
- **Fornost**: as ruínas da capital do Norte (muralha quebrada, torres, cidadela, colunas caídas), o fosso em volta, o Caminho Verde e os montes do campo de batalha. 5 lugares e a rota "A queda do Reino do Norte".
- **Pelargir**: a cidade murada na margem do Anduin, com cerca de 130 casas, os cais, a frota negra dos Corsários e o rio Sirith. 5 lugares e a rota "Os navios negros".
- **Dol Amroth**: o promontório de rocha avançando no mar, com o castelo de torres azuis, a Torre do Mar na ponta, a cidade e o porto com navios-cisne. 5 lugares e a rota "Os cavaleiros do cisne".

## 11.4 — 16/11/2026 — Erebor e Valle, Cidade do Lago e Dol Guldur de perto
- **Erebor e Valle**:
  - A Montanha Solitária com os braços em estrela, o Portão da Frente (arco, estátuas e ameias) e o Rio Corrente saindo dele e dando a volta em Valle.
  - Valle reconstruída, com muralha, cerca de 75 casas de telhados coloridos e a torre dos sinos.
  - A Colina do Corvo com o posto de guarda, a porta secreta com o brilho da fechadura e a Desolação de Smaug com árvores queimadas.
  - 8 lugares e a rota "A Montanha Solitária".
- **Cidade do Lago**:
  - Esgaroth sobre estacas dentro do Lago Comprido, com cerca de 130 casas de madeira, o Salão do Mestre, a ponte até a margem e barcos.
  - As estacas queimadas da cidade velha, os ossos de Smaug no fundo raso e os barris dos anões chegando pelo Rio da Floresta.
  - 7 lugares e a rota "Smaug e a Cidade do Lago".
- **Dol Guldur**: a colina nua de Amon Lanc com a fortaleza escura (muralha quebrada, torres e torreão com luz vermelha), a boca das masmorras, árvores mortas em volta e a Floresta das Trevas fechada. 5 lugares e a rota "A sombra de Dol Guldur".

## 11.3 — 16/11/2026 — Topo do Vento, Portão Negro, Minas Morgul e Cirith Ungol de perto
- **Topo do Vento**: a colina de topo achatado com o anel de pedras em ruínas de Amon Sûl, a pedra com a marca de Gandalf, a clareira com a fogueira dos hobbits, a Grande Estrada e as Colinas do Vento. 5 lugares e a rota "O ataque no Topo do Vento".
- **Portão Negro**: a passagem de Cirith Gorgor entre as montanhas, a muralha com as portas de ferro, as duas Torres dos Dentes (Narchost e Carchost), os morros de escória, os lodaçais de Dagorlad e o vale de Udûn. 6 lugares e a rota "A batalha do Morannon".
- **Minas Morgul e Cirith Ungol** (uma região só):
  - A cidade pálida com muralhas, casas e a torre alta com brilho esverdeado; a ponte com estátuas sobre o Morgulduin e os campos de flores pálidas.
  - A Encruzilhada com o rei de pedra coroado de flores, as escadas Reta e Sinuosa, a boca da Toca de Laracna com teias e a Torre de Cirith Ungol em três andares.
  - 8 lugares e a rota "O caminho de Cirith Ungol".

## 11.2 — 15/11/2026 — Moria, Lothlórien e Bri de perto
- **Moria**:
  - As Portas de Durin brilham em ithildin no paredão (arco, pilares, coroa e estrela), entre dois azevinhos. Diante delas ficam o lago escuro com os tentáculos do Vigia e o leito seco do Sirannon com as ruínas de Azevim.
  - Do outro lado, o Portão Leste, a escada até o Lago Espelhado (com a coroa de estrelas refletida e a Pedra de Durin), o Veio de Prata, o Caradhras com o caminho do passo e a Torre de Durin no Zirakzigil.
  - 11 lugares e a rota "A travessia de Moria".
- **Lothlórien**:
  - Caras Galadhon tem mallorns gigantes de tronco prateado e copa dourada, plataformas (talans) com lanternas, a muralha verde e a ponte branca. O maior mallorn, no centro, é o de Celeborn e Galadriel.
  - Também: o Espelho de Galadriel, Cerin Amroth com os dois anéis de árvores e as flores elanor e niphredil, o talan de Haldir, o Nimrodel e a Margem com os barcos élficos e o barco-cisne.
  - 8 lugares e a rota "Em Lothlórien".
- **Bri**:
  - A colina com casas de Homens e tocas de hobbits, a estalagem do Pônei Saltitante, o dique com a sebe alta e os portões Oeste e Sul, e a casa de Bill Samambaia.
  - Também: Staddle, Combe, Archet, a Floresta Chet e a encruzilhada do Caminho Verde.
  - 10 lugares e a rota "Os hobbits em Bri".
- Câmera: quando uma montanha fica entre a câmera e o lugar olhado, a câmera sobe sozinha até enxergar.

## 11.1 — 15/11/2026 — Rohan e Isengard de perto
- **Isengard**: o Anel de rocha com o portão arrebentado e uma brecha, e Orthanc com quatro pilares negros e chifres no alto.
  - Dentro do Anel: estradas de pedra com pilares e a metade norte inundada pelos Ents. Na metade sul, os poços de Saruman com brilho de fogo e vapor.
  - Em volta: a represa dos Ents no Isen, o Vale do Mago devastado (tocos de árvores), os Vaus do Isen com o Túmulo dos Cavaleiros cercado de lanças e a borda de Fangorn. 9 lugares e a rota "A queda de Isengard".
- **Abismo de Helm**: o Forte da Trombeta no esporão (muralha, torres e a torre alta) e a Muralha do Abismo com o bueiro arrombado.
  - Também: as Cavernas Cintilantes com brilhos, o Dique de Helm, a Floresta dos Huorns, a Colina da Morte e o Thrihyrne atrás. 9 lugares e a rota "A batalha do Abismo de Helm".
- **Edoras**: a colina com cerca de 110 casas de madeira e palha, e Meduseld com telhado dourado no alto, sobre um terraço com escadaria e o canal da fonte.
  - Também: a paliçada com o portão, os 16 túmulos dos reis com flores brancas, o rio Snowbourn com ponte e cavalos nos campos. 7 lugares e a rota "A chegada a Edoras".
- Tocar em "Isengard", "Abismo de Helm" ou "Edoras" mergulha a câmera no lugar.
- Os geradores agora usam uma biblioteca comum (`tools/relevo/regioes/reg.py`), o que acelera as próximas regiões.

## 11.0 — 15/11/2026 — regiões de detalhe sem limite
- O mapa 3D aceita quantas regiões de detalhe forem criadas. Antes o limite era 4.
- Só as regiões perto da câmera (até 4 ao mesmo tempo) ficam carregadas na placa de vídeo. As outras são carregadas quando você se aproxima e liberadas quando se afasta, o que poupa memória no celular.
- De longe aparece o mapa normal, com os marcos em 3D (Minas Tirith, Barad-dûr etc.). Ao chegar perto, a região detalhada entra no lugar.

## 10.9 — 15/11/2026 — a Montanha da Perdição de perto
- Nova região de detalhe no mapa 3D: a Montanha da Perdição (Orodruin) e o planalto de Gorgoroth.
- A montanha tem o cone sobre uma base larga de cinzas, ravinas, a cratera com lago de fogo e a porta do Sammath Naur brilhando na face leste.
- A Estrada de Sauron chega do lado de Barad-dûr como uma calçada elevada e sobe em espiral até a porta.
- Três rios de lava descem as encostas e se espalham pelo planalto.
- O planalto tem fendas incandescentes, fumarolas, rochas, troncos secos, acampamentos de orcs com fogueiras, torres de vigia e a trilha por onde os hobbits chegaram.
- 7 lugares com descrição, que aparecem ao aproximar: Sammath Naur, Cratera do Orodruin, Estrada de Sauron, Planalto de Gorgoroth, A subida de Sam, Colina de cinzas e Rios de lava.
- Nova rota passo a passo, "A Montanha da Perdição", com 6 paradas, de Gorgoroth ao resgate pelas águias.
- Tocar em "Monte da Perdição" mergulha a câmera na montanha.
- O motor aceita no máximo 4 regiões de detalhe, e com esta chegou ao limite.

## 10.8 — 15/11/2026 — Valfenda de perto
- Nova região de detalhe no mapa 3D: Valfenda, no vale escondido do Bruinen, ao pé das Montanhas Sombrias.
- A Última Casa Amiga tem salão principal, alas, torres, o Salão do Fogo, a biblioteca, a varanda do Conselho com colunata, terraços, pavilhões e jardins com flores.
- O vale tem escarpas em degraus, cachoeiras que descem dos paredões, a nascente do rio e árvores com cores de outono (Frodo chegou em outubro).
- A ponte estreita de pedra, sem parapeito, e a trilha em zigue-zague que desce do planalto.
- O Vau do Bruinen tem pedras no leito, e a Grande Estrada Leste segue rumo ao Passo Alto.
- 9 lugares com descrição, que aparecem ao aproximar: Última Casa Amiga, Salão do Fogo, Varanda do Conselho, Ponte de Valfenda, Descida para Valfenda, Cachoeiras, Rio Bruinen, Vau do Bruinen e Grande Estrada Leste.
- Nova rota passo a passo, "A chegada a Valfenda", com 8 paradas, do Vau do Bruinen à partida da Sociedade.
- Tocar em "Valfenda" mergulha a câmera no vale.

## 10.7 — 15/11/2026 — Minas Tirith de perto
- Nova região de detalhe no mapa 3D: Minas Tirith. Dá para aproximar até 15 vezes mais que no resto do mapa.
- A cidade tem os 7 círculos de muralha, a proa de pedra voltada para o leste, os portões alternados e cerca de 520 casas nos terraços.
- Na Cidadela ficam a Torre de Ecthelion, o Salão dos Reis, a fonte e a Árvore Branca. Também aparecem as Casas de Cura e as cúpulas de Rath Dínen.
- O Mindolluin fica atrás da cidade, ligado a ela por um esporão. Em volta estão:
  - os Campos do Pelennor, com fazendas;
  - o Rammas Echor, com os Fortes da Calçada;
  - o cais do Harlond, com os navios negros dos Corsários;
  - as ruínas de Osgiliath, com a ponte partida.
- 12 lugares com descrição, que aparecem ao aproximar: Grande Portão, Cidadela, Árvore Branca, Casas de Cura, Rath Dínen, Mindolluin, Campos do Pelennor, Batalha do Pelennor, Rammas Echor, Fortes da Calçada, Harlond e Ponte de Osgiliath.
- Nova rota passo a passo, "O cerco de Minas Tirith", com 9 paradas, de Osgiliath à Árvore Branca.
- Tocar em "Minas Tirith" mergulha a câmera na cidade.
- O motor do relevo agora aceita várias regiões de detalhe e novos tipos de modelo (torres, muralhas curvas, cúpulas, barcos).

## 10.6 — 15/11/2026 — o Condado de perto
- Nova "região de detalhe" no mapa 3D: dentro do Condado dá para aproximar até 15 vezes mais que no resto do mapa.
- O Condado foi pintado em alta resolução: colcha de plantações e pastos com sebes, trigais com sulcos, flores, hortas, estradas e caminhos, o rio O Água, a lagoa de Beirágua, o Pântano, a Ponta do Bosque, a Sebe Alta e a borda da Floresta Velha.
- Mais de 180 construções em 3D: tocas de hobbit com porta redonda colorida, janelas acesas e chaminé; Bolsão no alto da Colina; casas, o moinho, a estalagem Dragão Verde, a Árvore da Festa, a Pedra das Três Quartas, as Grandes Smials, a Sede do Brandevin, a Ponte do Brandevin com arcos, a balsa com cais, Cricôncavo, a Sebe Alta com o túnel, montes de feno e ovelhas — e cerca de 1.000 árvores (salgueiros nas margens, pomares, árvores das sebes).
- 19 lugares do Condado com descrição, que aparecem ao aproximar: Bolsão, Vila dos Hobbits, Árvore da Festa, Moinho, Beirágua, Dragão Verde, Pedra das Três Quartas, Grã Cava, Grandes Smials, Ponta do Bosque, Pântano, Fazenda do Magote, Tronco, Balsa de Buqueburgo, Sede do Brandevin, Cricôncavo, Ponte do Brandevin, Sebe Alta e Túnel da Sebe.
- Nova rota passo a passo "A fuga do Condado" (Bolsão → Túnel da Sebe), com a câmera bem próxima.
- Tocar em "Condado" mergulha a câmera no Condado.
- Mapa inteiro: os rios deixaram de parecer cânions (vales mais largos e rasos).
- A câmera nunca entra no chão ao aproximar em encostas.

## 10.5 — 15/11/2026 — nova Terra-média
- Mapa da Terra-média redesenhado do zero, em estilo cartográfico, com toda a Terceira Era: de Lindon e das Montanhas Azuis até Rhûn, do Forochel até Harad e Umbar. Litoral, golfos e baías, 18 rios (Anduin, Brandevin, Fontegris, Isen, Entágua…), lagos, 12 cordilheiras, florestas com cerca de 3.300 árvores 3D, desertos, neve e o planalto de Mordor.
- 16 lugares novos nos alfinetes: Portos Cinzentos, Fornost, Topo do Vento, Gundabad, Dol Guldur, Rauros, Dol Amroth, Pelargir, Umbar, Mar de Rhûn, Colinas de Ferro, Harad, Khand, Abismo de Helm, Osgiliath e Carrocha.
- O mapa ilustrado antigo saiu; no lugar do "Mapa plano" ficam os botões "Vista inclinada" e "Vista de cima".
- Ligação com Arda: ao ampliar a Terra-média no globo (ou tocar em "Entrar na Terra-média") o app voa para o mapa; ao afastar bastante o mapa (ou tocar em "Ver Arda") volta ao globo.
- Os nomes dos alfinetes não se sobrepõem mais: quando dois se encostam, aparece só o mais próximo.

## 10.4 — 15/11/2026
- Retratos trocados por versões novas: Círdan, Dwalin, Elrond.

## 10.3 — 15/11/2026
- Retrato novo: Elrohir (com arco, para diferenciar do irmão Elladan).

## 10.2 — 15/11/2026
- Nova aba Mapa → Arda (mundo): globo 3D de Arda com base desenhada para o Atlas (Aman, Belegaer, Terra-média, Terra Escura, Terras do Leste), relevo, 19 lugares com descrição.

## 10.1 — 15/11/2026 — mapa 3D refeito
- Câmera em perspectiva de verdade (corrige a faixa que cortava a tela ao inclinar), céu e névoa no horizonte.
- Construções em 3D no lugar dos desenhos colados no chão: Barad-dûr com o Olho em chamas, Orthanc no anel de Isengard, Minas Tirith em sete anéis, Minas Morgul com brilho verde, Portão Negro, Carn Dûm, Cirith Ungol, Meduseld em Edoras, Valfenda, tocas do Condado, Bri e o portão de Erebor.
- Cerca de 3.500 árvores 3D nas florestas; lava na Montanha da Perdição; relevo com o dobro de detalhe, cristas nas montanhas, sombras projetadas, neve e água assadas em resolução cheia.
- Os alfinetes ficam no topo de cada construção.

## 10.0 — 15/11/2026
- Nova versão do retrato do Dori.

## 9.9 — 15/11/2026 — retratos
- Retratos novos: Déagol, Elanor Brandyfoot, Durin, o Imortal, Durin IV (série), Elladan, Dís, Elendil, Durin, o Flagelo.

## 9.8 — 15/11/2026
- Retrato novo: Drogo Bolseiro.

## 9.7 — 15/11/2026
- Retrato novo: Dori.

## 9.6 — 15/11/2026 — retratos, lote 8
- Retratos novos ou trocados por versões em busto: Círdan, Curufin, Bombur, Bronwyn, Celegorm, Bregalad, Disa, Bárd, o Arqueiro, Caranthir, Dior Eluchíl, Celebrían.

## 9.5 — 15/11/2026 — retratos, lote 7
- 5 retratos novos, recortados em busto a partir de imagens de corpo inteiro: Bárd, o Arqueiro, Bombur, Bregalad, Bronwyn, Caranthir.

## 9.4 — 15/11/2026
- Novo retrato do Beregond (mais velho, cabelo curto e grisalho), para não ficar parecido com o Beren.

## 9.3 — 15/11/2026 — retratos, lote 6
- 2 retratos novos: Azog, Beleg Cúthalion.

## 9.2 — 15/11/2026 — retratos, lote 5
- 8 retratos novos: Alfrid Lickspittle, Aulë, Barbárvore, Bandobras Tûk, Beren, Beregond, Bifur, Bofur.

## 9.1 — 15/11/2026 — retratos, lote 4
- 9 retratos novos: Arondir, Anárion, Ancalagon, o Negro, Ar-Pharazôn, Aredhel, Alatar, Aldarion, Amras, Amrod.

## 9.0 — 14/11/2026 — retratos, lote 3
- 10 imagens novas no lugar dos desenhos simples: Dirhael, Marwen, Ioreth, Lithariel, Torvin, Hirgon, Adar, Senhor Luminoso, os Orcs do sistema Nêmesis e a região de Seregost.

## 8.9 — 14/11/2026 — retratos, lote 2
- 5 retratos novos: Eaoden, Idrial, Morwen (The Third Age), Elegost e The Tower of Sauron. Nenhum personagem mostra mais silhueta vazia.

## 8.8 — 14/11/2026 — retratos, lote 1
- 10 retratos novos no lugar das silhuetas vazias: Castamir, Ranger (Olog-hai), The Black Hand of Sauron, The Hammer of Sauron, Eradan, Farin, e as versões de Battle for Middle-earth II de Arwen, Eärnur, Glorfindel e Haldir. Originais em `retratos/`.

## 8.7 — 14/11/2026 — mapa 3D caprichado e app instalável
- O mapa 3D usa uma versão da ilustração sem os nomes, ícones redondos e botões pintados: cada lugar aparece uma vez só, no alfinete em pé.
- Relevo melhorado: sombras projetadas pelas montanhas, oclusão nos vales, luz quente e sombra fria, neve só nos picos claros, água com tom de reflexo do céu, névoa no horizonte e laterais de terra como uma maquete.
- Mordor agora tem as cordilheiras nas bordas (Ered Lithui e Ephel Dúath), o planalto de Gorgoroth no meio e a Montanha da Perdição em destaque.
- O painel "Auditoria de conexões" saiu do Grafo e foi para "🛠 Ferramentas do editor".
- O Atlas pode ser instalado no Android (Chrome → ⋮ → Instalar app): ícone próprio, abre em tela cheia e funciona sem internet.

## 8.6 — 14/11/2026 — relevo no mapa 3D
- Mapa 3D com relevo de verdade: as Montanhas Sombrias, Ered Luin, Angmar, as Montanhas Brancas, as cordilheiras de Mordor, Erebor e a Montanha da Perdição se levantam do mapa, com luz e sombra vindas do noroeste e névoa no horizonte.
- Feito em WebGL puro, sem bibliotecas: o app continua offline e cresceu só ~25 KB (o mapa de altitude é uma imagem pequena de 246×220).
- Alfinetes, rotas passo a passo e o viajante acompanham o relevo (as rotas "sobem e descem" as montanhas).
- Botão 🏔 liga/desliga o relevo (fica lembrado). Se o celular não tiver WebGL, o mapa 3D anterior (sem relevo) continua funcionando.
- O relevo só é montado na primeira vez que o Mapa é aberto, para não atrasar a abertura do app.

## 8.5 — 14/11/2026 — reorganização das seções
- De 20 seções para 9, com abas: Início · Personagens (Galeria, Fichas) · Teia (Grafo 3D, Teia Viva, Comparar dois) · Mapa (Mapa 3D, Geografia por eras, Jornadas) · Famílias (Árvores completas, Árvores clássicas) · História (Linha do tempo, Acontecimentos, Primeira Era) · Obras (Livros, Filmes e séries, Comparar) · Jogos · Fontes.
- Nenhum conteúdo foi apagado: as seções antigas viraram abas. Os dois comparadores ficaram juntos na aba "Comparar".
- Nova barra inferior: Início · Pessoas · Teia · Mapa · História · ☰ Mais (Famílias, Obras, Jogos, Fontes).
- Cada seção lembra a última aba aberta.

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
