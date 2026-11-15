import sys,json;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import integrate,route_js
pl=lambda n:json.load(open(f'/tmp/claude-0/ro/{n}.json'))['places']
SUB=[['Forte da Trombeta','ForteTrombeta','A fortaleza sobre o esporão de rocha na boca do Abismo, com a torre alta e a grande trombeta de Helm.','Théoden, Aragorn, Gamling'],
 ['Muralha do Abismo','MuralhaAbismo','A muralha que fecha a boca do Abismo, do Forte da Trombeta até a escarpa do outro lado. O riacho passa por baixo, num bueiro.','Aragorn, Éomer, Legolas, Gimli'],
 ['Bueiro','Bueiro','A passagem do riacho sob a muralha. Os orcs a explodiram com o fogo de Orthanc e abriram uma brecha.','Gimli, Éomer'],
 ['Cavernas Cintilantes','CavernasCintilantes','Aglarond: cavernas cheias de cristais no fundo do Abismo. Gimli ficou maravilhado e depois voltou com outros anões para viver nelas.','Gimli'],
 ['Dique de Helm','DiqueHelm','Uma vala com aterro que atravessa o vale abaixo do Forte. Foi a primeira linha de defesa.','Erkenbrand, Gamling'],
 ['Floresta dos Huorns','FlorestaHuorns','Na manhã seguinte à batalha, uma floresta surgiu na saída do vale. Os orcs fugiram para ela e nenhum saiu.','Huorns, Barbárvore'],
 ['Colina da Morte','ColinaMorte','O monte de pedras onde foram enterrados os inimigos mortos na batalha.',''],
 ['Chegada de Gandalf','ColinaGandalf','Ao amanhecer, Gandalf, o Cavaleiro Branco, desceu a encosta com Erkenbrand e os homens do Westfolde.','Gandalf, Erkenbrand'],
 ['Vale do Abismo','ValeAbismo','O vale verde e estreito que leva do Dique de Helm até a muralha e o Forte.','']]
integrate(pl('helm'),SUB,'AbismoHelm',20,'abismo',route_js('A batalha do Abismo de Helm','🛡️',36,[
 ['Dique de Helm','DiqueHelm','Noite de 3 de março de 3019. Os defensores do Dique de Helm recuam diante do exército de Saruman.'],
 ['Muralha do Abismo','MuralhaAbismo','Sob chuva, orcs e Terrapardenses atacam a muralha com escadas. Aragorn e Éomer lutam lado a lado.'],
 ['Bueiro','Bueiro','Com o fogo de Orthanc, os orcs explodem o bueiro do riacho e abrem uma brecha na muralha.'],
 ['Cavernas Cintilantes','CavernasCintilantes','Gimli e os que recuaram resistem no fundo do Abismo, junto às Cavernas Cintilantes.'],
 ['Forte da Trombeta','ForteTrombeta','Ao amanhecer, a trombeta de Helm soa, e Théoden cavalga para fora com Aragorn e seus homens.'],
 ['Chegada de Gandalf','ColinaGandalf','Gandalf aparece na encosta com Erkenbrand e os homens do Westfolde.'],
 ['Floresta dos Huorns','FlorestaHuorns','Os orcs fogem para a floresta que surgiu durante a noite. Nenhum deles sai de lá.'],
 ['Colina da Morte','ColinaMorte','Os inimigos mortos são enterrados sob um monte de pedras: a Colina da Morte.']]),'A batalha do Abismo de Helm')
SUB=[['Meduseld','Meduseld','O Paço Dourado, no alto da colina: um grande salão com telhado coberto de ouro, que se via de longe. Ali morava o rei de Rohan.','Théoden, Éowyn, Gríma'],
 ['Portão de Edoras','PortaoEdoras','O portão da paliçada. Os guardas exigiam que os visitantes deixassem as armas antes de entrar no Paço.','Háma'],
 ['Túmulos dos Reis','TumulosReis','Dos dois lados da estrada, os montes dos reis de Rohan: nove de um lado e sete do outro, cobertos de flores brancas de simbelmynë.','Théoden, Éomer'],
 ['Escadaria de Meduseld','EscadariaMeduseld','A escadaria de pedra que sobe até o terraço do Paço, ao lado de uma fonte que jorra de uma pedra em forma de cabeça de cavalo.','Háma'],
 ['Rio Snowbourn','RioSnowbourn','O rio que desce das Montanhas Brancas e passa ao lado de Edoras.',''],
 ['Paliçada de Edoras','PalicadaEdoras','Edoras era cercada por um fosso, uma muralha de terra e uma cerca alta de estacas.',''],
 ['Estrada para o Oeste','EstradaOeste','A estrada que leva de Edoras ao Westfolde e ao Abismo de Helm.','Théoden, Éomer']]
integrate(pl('edoras'),SUB,'Edoras',22,'edoras',route_js('A chegada a Edoras','🐎',40,[
 ['Túmulos dos Reis','TumulosReis','2 de março de 3019. Gandalf, Aragorn, Legolas e Gimli sobem a estrada entre os túmulos dos reis, cobertos de flores brancas.'],
 ['Portão de Edoras','PortaoEdoras','No portão, os guardas não os deixam passar armados. Mais adiante, Háma pede que deixem as armas à porta do Paço.'],
 ['Escadaria de Meduseld','EscadariaMeduseld','Eles sobem a escadaria de pedra ao lado da fonte em forma de cabeça de cavalo.'],
 ['Meduseld','Meduseld','No Paço Dourado, Gandalf liberta Théoden do feitiço de Saruman, e Gríma Língua de Cobra é expulso.'],
 ['Estrada para o Oeste','EstradaOeste','Théoden reúne os Cavaleiros e parte para o oeste, rumo ao Abismo de Helm.']]),'A chegada a Edoras')
