import sys,json;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import integrate,route_js
pl=lambda n:json.load(open(f'/tmp/claude-0/b2/{n}.json'))['places']
SUB=[['Portas de Durin','PortasDurin','O Portão Oeste de Moria, invisível na rocha até brilhar à luz da lua. A inscrição dizia: "Fale, amigo, e entre". A senha era a palavra élfica para amigo: mellon.','Gandalf, Frodo, Celebrimbor, Narvi'],
 ['Lago do Vigia','LagoVigia','O lago escuro formado pelo Sirannon represado. Dele saiu o Vigia da Água, que agarrou Frodo e depois fechou as portas atrás da Sociedade.','Frodo, Sam, Gandalf'],
 ['Portão Leste','PortaoLeste','O Portão do Riacho Escuro, saída de Moria para o vale de Azanulbizar.','Aragorn, Legolas, Gimli'],
 ['Escada do Riacho Escuro','EscadaRiachoEscuro','A trilha de degraus que desce do Portão Leste até o vale e o Lago Espelhado.',''],
 ['Lago Espelhado','LagoEspelhado','Kheled-zâram: um lago escuro e parado onde Durin viu uma coroa de estrelas refletida sobre sua cabeça. Gimli levou Frodo e Sam para olhar.','Gimli, Frodo, Sam, Durin'],
 ['Pedra de Durin','PedraDurin','Coluna quebrada que marca o lugar de onde Durin olhou pela primeira vez o Lago Espelhado.','Gimli, Durin'],
 ['Ponte de Khazad-dûm','PonteKhazadDum','Lá dentro, perto do Portão Leste: a ponte estreita sobre o abismo onde Gandalf enfrentou o Balrog. "Você não vai passar!"','Gandalf, Balrog, Aragorn, Boromir'],
 ['Caradhras','Caradhras','O Chifre Vermelho, montanha cruel. A neve e o vento derrotaram a Sociedade no Passo do Chifre Vermelho e a obrigaram a entrar em Moria.','Gandalf, Boromir, Aragorn'],
 ['Zirakzigil','Zirakzigil','O pico de Celebdil, com a Torre de Durin no alto da Escada Sem Fim. Ali Gandalf venceu o Balrog e morreu.','Gandalf, Balrog'],
 ['Azevim','Azevim','Eregion, a antiga terra dos elfos ferreiros, cheia de azevinhos e ruínas. Ali foram forjados os Anéis de Poder.','Celebrimbor'],
 ['Veio de Prata','VeioPrata','O Celebrant, que nasce no Lago Espelhado e corre para Lothlórien.','']]
integrate(pl('moria'),SUB,'Moria',16,'moria',route_js('A travessia de Moria','⛏️',26,[
 ['Caradhras','Caradhras','Janeiro de 3019. A Sociedade tenta o Passo do Chifre Vermelho, mas a neve a derrota.'],
 ['Azevim','Azevim','De volta às terras de Azevim, Gandalf decide passar por baixo das montanhas, por Moria.'],
 ['Lago do Vigia','LagoVigia','Diante do lago escuro, o Vigia da Água agarra Frodo pelo tornozelo.'],
 ['Portas de Durin','PortasDurin','Gandalf decifra a inscrição: a senha é mellon. A Sociedade entra, e o Vigia fecha as portas atrás dela.'],
 ['Ponte de Khazad-dûm','PonteKhazadDum','15 de janeiro. Na ponte, Gandalf enfrenta o Balrog e cai no abismo com ele.'],
 ['Portão Leste','PortaoLeste','Aragorn guia os outros para fora, sob o sol, chorando por Gandalf.'],
 ['Lago Espelhado','LagoEspelhado','Gimli leva Frodo e Sam para olhar o Lago Espelhado, junto à Pedra de Durin.'],
 ['Veio de Prata','VeioPrata','A Sociedade segue o Veio de Prata rumo a Lothlórien.']]),'A travessia de Moria')
SUB=[['Caras Galadhon','CarasGaladhon','A cidade das árvores: talans sobre mallorns gigantes, cercados por uma muralha verde. No maior deles moravam Celeborn e Galadriel.','Galadriel, Celeborn, Haldir'],
 ['Espelho de Galadriel','EspelhoGaladriel','Uma bacia de prata num vale escondido, que mostra coisas que foram, que são e que talvez ainda sejam. Ali Frodo ofereceu o Anel a Galadriel, e ela recusou.','Galadriel, Frodo, Sam'],
 ['Cerin Amroth','CerinAmroth','O coração do antigo reino élfico: uma colina com dois anéis de árvores, coberta de elanor dourada e niphredil branca. Ali Aragorn e Arwen se prometeram.','Aragorn, Arwen, Frodo'],
 ['Nimrodel','Nimrodel','O riacho de águas claras onde Legolas cantou a canção de Nimrodel. A Sociedade o atravessou ao entrar em Lórien.','Legolas'],
 ['Talan de Haldir','TalanHaldir','A plataforma no alto de um mallorn onde os hobbits passaram a primeira noite, guardados pelos elfos de Haldir.','Haldir, Frodo, Sam, Merry, Pippin'],
 ['A Margem','Margem','O ancoradouro no Veio de Prata. Dali a Sociedade partiu em barcos élficos, depois da despedida de Galadriel no barco-cisne.','Galadriel, Celeborn'],
 ['Muralha Verde','MuralhaVerde','A muralha alta e verde que cerca Caras Galadhon, com um fosso e uma ponte branca no portão sul.',''],
 ['Naith','Naith','A Língua de Lórien, a ponta de terra entre o Veio de Prata e o Anduin.','']]
integrate(pl('lorien'),SUB,'Lothlorien',16,'lorien',route_js('Em Lothlórien','🍂',30,[
 ['Nimrodel','Nimrodel','Janeiro de 3019. A Sociedade atravessa o Nimrodel, e Legolas canta a canção da donzela élfica.'],
 ['Talan de Haldir','TalanHaldir','Os elfos de Haldir os recebem. Os hobbits dormem num talan, no alto de um mallorn.'],
 ['Cerin Amroth','CerinAmroth','Em Cerin Amroth, Aragorn se lembra do dia em que prometeu se casar com Arwen.'],
 ['Caras Galadhon','CarasGaladhon','Na cidade das árvores, Celeborn e Galadriel recebem a Sociedade.'],
 ['Espelho de Galadriel','EspelhoGaladriel','No Espelho, Frodo e Sam veem visões. Frodo oferece o Anel; Galadriel resiste à tentação e recusa.'],
 ['A Margem','Margem','16 de fevereiro. Depois dos presentes e da despedida, a Sociedade desce o rio em barcos élficos.']]),'Em Lothlórien')
SUB=[['Pônei Saltitante','PoneiSaltitante','A estalagem de Cevado Carrapicho, onde os hobbits conheceram Passolargo e onde Frodo pôs o Anel sem querer, na frente de todos.','Cevado Carrapicho, Aragorn, Frodo, Nob'],
 ['Portão Oeste de Bri','PortaoOesteBri','O portão na sebe onde a Grande Estrada Leste entra em Bri. O porteiro desconfiou dos hobbits que chegaram à noite.','Frodo, Sam, Merry, Pippin'],
 ['Portão Sul de Bri','PortaoSulBri','Por onde a estrada sai de Bri, rumo ao leste.',''],
 ['Colina de Bri','ColinaBri','A colina em cujas encostas fica Bri: casas de Homens embaixo e tocas de hobbits mais acima.',''],
 ['Casa de Bill Samambaia','CasaFerny','A casa do espião de Bri, aliado dos Cavaleiros Negros. Ele vendeu à Sociedade o pônei Bill, que Sam adotou.','Bill Samambaia, Sam'],
 ['Encruzilhada','Encruzilhada','Onde o antigo Caminho Verde, do norte ao sul, cruza a Grande Estrada Leste.',''],
 ['Staddle','Staddle','Vila na encosta sudeste da colina, onde vivem muitos hobbits.',''],
 ['Archet','Archet','Vila na borda da Floresta Chet.',''],
 ['Combe','Combe','Vila num vale fundo a leste da colina.',''],
 ['Floresta Chet','FlorestaChet','A floresta a nordeste de Bri. Passolargo levou os hobbits por ela para escapar dos Cavaleiros.','Aragorn']]
integrate(pl('bri'),SUB,'Bri',18,'bri',route_js('Os hobbits em Bri','🍺',40,[
 ['Portão Oeste de Bri','PortaoOesteBri','29 de setembro de 3018. À noite, os hobbits chegam ao portão de Bri pela Grande Estrada Leste.'],
 ['Pônei Saltitante','PoneiSaltitante','Na estalagem, conhecem Passolargo. Cantando sobre a mesa, Frodo escorrega e o Anel vai parar no seu dedo.'],
 ['Casa de Bill Samambaia','CasaFerny','Os pôneis são roubados durante a noite; Bill Samambaia vende à Sociedade um pônei magro, o Bill.'],
 ['Portão Sul de Bri','PortaoSulBri','30 de setembro. A Sociedade sai pelo portão sul, sob os olhares do povo de Bri.'],
 ['Floresta Chet','FlorestaChet','Passolargo deixa a estrada e guia os hobbits pela Floresta Chet, rumo ao Topo do Vento.']]),'Os hobbits em Bri')
