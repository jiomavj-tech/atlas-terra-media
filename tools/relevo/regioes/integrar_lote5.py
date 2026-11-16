import sys,json;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import integrate,route_js,embed
embed('/tmp/claude-0/b5','amroth','dol-amroth','Dol Amroth')
pl=lambda n:json.load(open(f'/tmp/claude-0/b5/{n}.json'))['places']
SUB=[['Colina de Barbárvore','ColinaBarbarvore','A prateleira de rocha com degraus, junto ao Entágua, onde Merry e Pippin encontraram Barbárvore. Ali também Aragorn, Legolas e Gimli reencontraram Gandalf, o Branco.','Barbárvore, Merry, Pippin, Gandalf'],
 ['Gruta da Nascente','GrutaNascente','Uma das casas de Barbárvore, perto das nascentes do Entágua, com uma cortina de água na entrada. Lá os hobbits beberam a água dos Ents e cresceram.','Barbárvore, Merry, Pippin'],
 ['Valarcano','Valarcano','O vale redondo, cercado por uma sebe de árvores escuras, onde os Ents se reúnem. O Entebate durou três dias.','Barbárvore, Tronquesperto'],
 ['Monte dos orcs','MonteOrcs','Na borda da floresta, os Cavaleiros de Éomer mataram e queimaram os orcs que levavam Merry e Pippin.','Éomer, Uglúk, Grishnákh'],
 ['Entágua','Entagua','O rio que nasce em Fangorn e corre para as planícies de Rohan.','']]
integrate(pl('fangorn'),SUB,'Fangorn',14,'fangorn',route_js('Os Ents de Fangorn','🌲',30,[
 ['Monte dos orcs','MonteOrcs','29 de fevereiro de 3019. Os Cavaleiros de Éomer atacam os orcs. Merry e Pippin escapam para dentro da floresta.'],
 ['Colina de Barbárvore','ColinaBarbarvore','Os hobbits sobem a colina de rocha e encontram Barbárvore, o mais velho dos Ents.'],
 ['Gruta da Nascente','GrutaNascente','Barbárvore os leva para casa e lhes dá a água dos Ents.'],
 ['Valarcano','Valarcano','No Entebate, depois de três dias, os Ents decidem marchar contra Isengard.'],
 ['Colina de Barbárvore','ColinaBarbarvore','1º de março. Aragorn, Legolas e Gimli reencontram Gandalf, agora o Branco.']]),'Os Ents de Fangorn')
SUB=[['Argonath','Argonath','Os Pilares dos Reis: as estátuas gigantes de Isildur e Anárion, com a mão esquerda erguida em aviso, na entrada do lago.','Aragorn, Isildur, Anárion'],
 ['Nen Hithoel','NenHithoel','O lago comprido acima das quedas de Rauros, entre as colinas de Emyn Muil.',''],
 ['Parth Galen','ParthGalen','O gramado verde na margem oeste, ao pé de Amon Hen, onde a Sociedade acampou pela última vez.','Frodo, Sam, Aragorn, Boromir'],
 ['Assento da Visão','AssentoVisao','No alto de Amon Hen, a Colina do Olho: um assento de pedra sobre quatro pilares. Com o Anel no dedo, Frodo viu dali toda a Terra-média — e o Olho de Sauron.','Frodo'],
 ['Tol Brandir','TolBrandir','A ilha-pináculo no meio do rio, logo acima das quedas. Ninguém jamais pôs os pés nela.',''],
 ['Amon Lhaw','AmonLhaw','A Colina do Ouvido, na margem leste, diante de Amon Hen. Frodo e Sam atravessaram para esse lado.','Frodo, Sam'],
 ['Quedas de Rauros','QuedasRauros','A grande cachoeira do Anduin. O barco fúnebre de Boromir desceu por ela.','Boromir'],
 ['Morte de Boromir','MorteBoromir','Na floresta ao pé de Amon Hen, Boromir caiu defendendo Merry e Pippin, crivado de flechas, depois de soar sua trompa.','Boromir, Aragorn, Merry, Pippin']]
integrate(pl('rauros'),SUB,['Rauros','AmonHen'],12,'rauros',route_js('A dissolução da Sociedade','🛶',26,[
 ['Argonath','Argonath','25 de fevereiro de 3019. Os barcos passam entre os Pilares dos Reis.'],
 ['Parth Galen','ParthGalen','A Sociedade acampa em Parth Galen e precisa decidir o caminho.'],
 ['Assento da Visão','AssentoVisao','26 de fevereiro. Boromir tenta tomar o Anel. Frodo foge, sobe ao Assento da Visão e decide seguir sozinho.'],
 ['Morte de Boromir','MorteBoromir','Os orcs atacam. Boromir morre defendendo Merry e Pippin, que são levados.'],
 ['Quedas de Rauros','QuedasRauros','Aragorn, Legolas e Gimli entregam o corpo de Boromir ao rio, num barco élfico.'],
 ['Amon Lhaw','AmonLhaw','Frodo e Sam atravessam para a margem leste, rumo a Mordor.']]),'A dissolução da Sociedade')
SUB=[['Cais de Mithlond','CaisMithlond','Os cais de pedra dos Portos Cinzentos, de onde os navios élficos partem para o Oeste.','Círdan'],
 ['Navio Branco','NavioBranco','O navio que levou os Portadores dos Anéis — Frodo, Bilbo, Gandalf, Elrond e Galadriel — para além do mar.','Frodo, Bilbo, Gandalf, Elrond, Galadriel'],
 ['Torres de Mithlond','TorresMithlond','As torres brancas dos elfos de Círdan.','Círdan'],
 ['Estaleiro de Círdan','EstaleiroCirdan','Círdan, o Armador, construía ali os navios dos elfos. Foi ele quem deu o anel Narya a Gandalf.','Círdan, Gandalf'],
 ['Margem norte','MithlondNorte','A parte de Mithlond do outro lado do golfo.',''],
 ['Golfo de Lhûn','GolfoLhun','O braço de mar que entra pela terra de Lindon até os Portos.',''],
 ['Estrada do Condado','EstradaPortos','O caminho que vem do Condado, passando pelas Colinas das Torres.','Frodo, Sam']]
integrate(pl('mithlond'),SUB,'Mithlond',18,'portos',route_js('A última viagem','⛵',34,[
 ['Estrada do Condado','EstradaPortos','29 de setembro de 3021. Frodo e Bilbo cavalgam com Elrond e Galadriel até os Portos; Sam os acompanha.'],
 ['Torres de Mithlond','TorresMithlond','Círdan, o Armador, recebe os viajantes nos portões.'],
 ['Cais de Mithlond','CaisMithlond','No cais, Gandalf espera, com o anel Narya no dedo. Merry e Pippin chegam a tempo da despedida.'],
 ['Navio Branco','NavioBranco','Frodo se despede de Sam, Merry e Pippin e embarca.'],
 ['Golfo de Lhûn','GolfoLhun','O navio desce o golfo e some no Oeste. Sam volta para casa: "Bem, estou de volta."']]),'A última viagem')
SUB=[['Ruínas de Fornost','RuinasFornost','Fornost Erain, a "Fortaleza do Norte dos Reis", última capital de Arthedain. No fim da Terceira Era era só um monte de ruínas cobertas de capim.','Arvedui, Aragorn'],
 ['Fosso dos Mortos','FossoMortos','O povo de Bri chamava as ruínas de Fosso dos Mortos e tinha medo de chegar perto.',''],
 ['Caminho Verde','CaminhoVerdeNorte','A antiga Estrada do Norte, tão pouco usada que o capim tomou conta.',''],
 ['Colinas do Norte','ColinasNorte','As colinas onde ficava Fornost.',''],
 ['Batalha de Fornost','BatalhaFornost','Em 1975, o exército de Gondor, os elfos de Círdan e Glorfindel derrotaram o Rei-Bruxo de Angmar. Glorfindel previu que ele não cairia pela mão de um homem.','Eärnur, Glorfindel, Círdan, Rei-Bruxo de Angmar']]
integrate(pl('fornost'),SUB,'Fornost',18,'fornost',route_js('A queda do Reino do Norte','🏚️',34,[
 ['Ruínas de Fornost','RuinasFornost','Ano 1974. O Rei-Bruxo de Angmar toma Fornost. O rei Arvedui foge para o norte e morre no gelo.'],
 ['Batalha de Fornost','BatalhaFornost','Ano 1975. A frota de Gondor, com Eärnur, junta-se a Círdan e derrota Angmar na planície.'],
 ['Colinas do Norte','ColinasNorte','O Rei-Bruxo foge. Glorfindel impede a perseguição e faz a profecia: ele não cairá pela mão de um homem.'],
 ['Caminho Verde','CaminhoVerdeNorte','Os Dúnedain viram os Guardiões. Mil anos depois, o rei Elessar reconstrói o Reino do Norte.']]),'A queda do Reino do Norte')
SUB=[['Pelargir','CidadePelargir','O grande porto de Gondor no Anduin, fundado pelos Númenóreanos na Segunda Era.',''],
 ['Cais de Pelargir','CaisPelargir','Os cais de pedra onde atracavam as frotas de Gondor.','Aragorn'],
 ['Frota negra','FrotaNegra','Os navios dos Corsários de Umbar, que subiam o rio para atacar Gondor. Aragorn os tomou com o Exército dos Mortos.','Aragorn, Legolas, Gimli, Rei dos Mortos'],
 ['Rio Sirith','RioSirith','O rio que desce das Montanhas Brancas e encontra o Anduin em Pelargir.',''],
 ['Anduin','AnduinPelargir','O Grande Rio, já perto da foz.','']]
integrate(pl('pelargir'),SUB,'Pelargir',16,'pelargir',route_js('Os navios negros','💀',32,[
 ['Pelargir','CidadePelargir','13 de março de 3019. Aragorn chega a Pelargir com a Companhia Cinzenta, seguido pelo Exército dos Mortos.'],
 ['Frota negra','FrotaNegra','Os Mortos varrem os navios dos Corsários; os inimigos fogem de pavor ou se atiram na água.'],
 ['Cais de Pelargir','CaisPelargir','Aragorn declara cumprido o juramento e liberta os Mortos.'],
 ['Anduin','AnduinPelargir','Com os homens do sul nos navios tomados, Aragorn sobe o Anduin rumo a Minas Tirith.']]),'Os navios negros')
SUB=[['Castelo de Dol Amroth','CasteloAmroth','O castelo dos Príncipes de Dol Amroth, no alto do promontório sobre a Baía de Belfalas.','Imrahil'],
 ['Torre do Mar','TorreMar','Tirith Aear, a torre na ponta do promontório, de onde se vigiava o mar.',''],
 ['Cidade de Dol Amroth','CidadeAmroth','A cidade ao pé do castelo. Diziam que a casa dos Príncipes tinha sangue élfico.','Imrahil, Lothíriel'],
 ['Porto dos Cisnes','PortoAmroth','O porto abrigado, com os navios de proa em forma de cisne. O emblema de Dol Amroth é um navio e um cisne de prata.','Imrahil'],
 ['Baía de Belfalas','BaiaBelfalas','A grande baía do sul de Gondor.','']]
integrate(pl('amroth'),SUB,'DolAmroth',16,'amroth',route_js('Os cavaleiros do cisne','🦢',32,[
 ['Castelo de Dol Amroth','CasteloAmroth','Março de 3019. O príncipe Imrahil reúne seus cavaleiros para socorrer Minas Tirith.'],
 ['Cidade de Dol Amroth','CidadeAmroth','Setecentos homens de armas e uma companhia de cavaleiros partem sob a bandeira do navio e do cisne.'],
 ['Porto dos Cisnes','PortoAmroth','Depois da guerra, Lothíriel, filha de Imrahil, casa-se com Éomer, rei de Rohan.']]),'Os cavaleiros do cisne')
