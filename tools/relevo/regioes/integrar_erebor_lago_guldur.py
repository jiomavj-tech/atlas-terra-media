import sys,json;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import integrate,route_js
pl=lambda n:json.load(open(f'/tmp/claude-0/b4/{n}.json'))['places']
SUB=[['Portão da Frente','PortaoErebor','A grande entrada de Erebor, de onde nasce o Rio Corrente. Por ela Smaug saiu para atacar a Cidade do Lago, e diante dela Thorin ergueu um muro.','Thorin, Bilbo, Smaug, Dáin'],
 ['Valle','ValleCidade','A cidade dos Homens ao pé da Montanha, famosa pelos sinos e brinquedos. Smaug a destruiu; Bard a reconstruiu depois da morte do dragão.','Bard, Girion, Brand'],
 ['Colina do Corvo','ColinaCorvo','O antigo posto de guarda dos anões num braço da Montanha. Lá vivia o corvo Roäc, e lá Bilbo assistiu à Batalha dos Cinco Exércitos.','Bilbo, Roäc, Gandalf'],
 ['Porta secreta','PortaSecreta','A porta escondida no flanco oeste. A fechadura só aparece com a última luz do Dia de Durin; por ela Bilbo desceu até Smaug.','Bilbo, Thorin, Smaug'],
 ['Rio Corrente','RioCorrente','Nasce no Portão da Frente, dá uma volta em Valle e corre para o Lago Comprido.',''],
 ['Desolação de Smaug','DesolacaoSmaug','As terras queimadas e sem vida em volta da Montanha, nos anos em que o dragão dormia sobre o tesouro.','Smaug'],
 ['Batalha dos Cinco Exércitos','CampoCincoExercitos','No vale diante do Portão, anões, elfos e homens enfrentaram orcs e wargs. Thorin, Fíli e Kíli morreram ali.','Thorin, Dáin, Bard, Thranduil, Beorn, Bolg'],
 ['Pico de Erebor','PicoErebor','A Montanha Solitária, com seus braços em estrela. Sob ela ficava o Reino sob a Montanha, de Thrór a Dáin.','Thrór, Thorin, Dáin']]
integrate(pl('erebor'),SUB,'Erebor',14,'erebor',route_js('A Montanha Solitária','🐉',26,[
 ['Desolação de Smaug','DesolacaoSmaug','Outono de 2941. Thorin e companhia atravessam a Desolação de Smaug rumo à Montanha.'],
 ['Colina do Corvo','ColinaCorvo','Do alto da Colina do Corvo, veem o Portão da Frente e as ruínas de Valle.'],
 ['Porta secreta','PortaSecreta','No Dia de Durin, a última luz mostra a fechadura. Bilbo desce pelo túnel e conversa com Smaug.'],
 ['Portão da Frente','PortaoErebor','Furioso, Smaug sai pelo Portão e voa para destruir a Cidade do Lago. Lá, Bard o mata.'],
 ['Batalha dos Cinco Exércitos','CampoCincoExercitos','Anões, elfos e homens, prestes a lutar entre si, unem-se contra orcs e wargs. Thorin é ferido de morte.'],
 ['Valle','ValleCidade','Dáin torna-se Rei sob a Montanha, e Bard reconstrói Valle.']]),'A Montanha Solitária')
SUB=[['Esgaroth','Esgaroth','A Cidade do Lago, construída sobre estacas dentro do Lago Comprido e ligada à margem por uma ponte de madeira.','Bard, Mestre da Cidade do Lago'],
 ['Salão do Mestre','SalaoMestre','O grande salão no centro, onde o Mestre recebeu Thorin com festa.','Mestre da Cidade do Lago, Thorin'],
 ['Ponte da Cidade','PonteLago','A longa ponte de madeira. Foi derrubada às pressas quando Smaug atacou.',''],
 ['Ossos de Smaug','OssosSmaug','O dragão caiu sobre a cidade velha, morto pela Flecha Negra de Bard. Seus ossos ficaram no fundo raso, e ninguém ousava tocar nas joias.','Smaug, Bard'],
 ['Cidade velha','CidadeVelha','As estacas queimadas da cidade destruída por Smaug. A nova foi construída mais ao norte.',''],
 ['Rio da Floresta','RioFloresta','Por onde os anões chegaram, escondidos em barris, depois de fugir dos salões do Rei Élfico.','Bilbo, Thorin'],
 ['Lago Comprido','LagoComprido','O grande lago ao sul da Montanha Solitária, onde deságuam o Rio Corrente e o Rio da Floresta.','']]
integrate(pl('lago'),SUB,'CidadeLago',16,'lago',route_js('Smaug e a Cidade do Lago','🏹',34,[
 ['Rio da Floresta','RioFloresta','Setembro de 2941. Os anões chegam ao lago dentro de barris, com Bilbo montado em cima.'],
 ['Salão do Mestre','SalaoMestre','Thorin se apresenta como Rei sob a Montanha, e a cidade o recebe com festa.'],
 ['Ponte da Cidade','PonteLago','Quando Smaug aparece no céu, a ponte é derrubada, e a cidade se prepara para o fogo.'],
 ['Esgaroth','Esgaroth','Smaug incendeia a cidade. Avisado por um tordo, Bard acerta a Flecha Negra no ponto fraco do dragão.'],
 ['Ossos de Smaug','OssosSmaug','Smaug cai sobre a cidade e afunda no lago.']]),'Smaug e a Cidade do Lago')
SUB=[['Fortaleza de Dol Guldur','FortalezaGuldur','A "Colina da Feitiçaria": a fortaleza do Necromante, que era Sauron escondido. Depois foi dos Nazgûl.','Sauron, Khamûl, Gandalf'],
 ['Masmorras','MasmorrasGuldur','Onde Gandalf encontrou Thráin, pai de Thorin, à beira da morte, e recebeu dele o mapa e a chave de Erebor.','Gandalf, Thráin'],
 ['Amon Lanc','AmonLanc','A "Colina Nua", que já foi a capital do reino élfico de Oropher, antes de a sombra tomar a floresta.','Oropher, Thranduil'],
 ['Caminho de Dol Guldur','CaminhoGuldur','A trilha escura pela Floresta das Trevas até a colina.','Gandalf'],
 ['Floresta das Trevas','FlorestaSul','A parte sul da grande floresta, a mais escura, cheia de aranhas e de coisas piores.','']]
integrate(pl('guldur'),SUB,'DolGuldur',18,'guldur',route_js('A sombra de Dol Guldur','🌑',34,[
 ['Caminho de Dol Guldur','CaminhoGuldur','Ano 2850. Gandalf entra em segredo em Dol Guldur para descobrir quem é o Necromante.'],
 ['Masmorras','MasmorrasGuldur','Nas masmorras, encontra Thráin, que lhe entrega o mapa e a chave de Erebor antes de morrer.'],
 ['Fortaleza de Dol Guldur','FortalezaGuldur','Ano 2941. O Conselho Branco ataca a fortaleza, e Sauron foge para Mordor. Dez anos depois, os Nazgûl a ocupam de novo.'],
 ['Amon Lanc','AmonLanc','Março de 3019. Depois da queda de Sauron, Celeborn toma Dol Guldur, e Galadriel derruba suas muralhas.']]),'A sombra de Dol Guldur')
