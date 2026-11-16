import sys,json;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import integrate,route_js,embed,INDEX
embed('/tmp/claude-0/b6','henneth','henneth-annun','Henneth Annûn')
pl=lambda n:json.load(open(f'/tmp/claude-0/b6/{n}.json'))['places']
# lugares novos no mapa geral (aparecem de longe)
BASE=[['Floresta Velha','FlorestaVelha',[279.0,284.0],'A floresta antiga a leste da Terra dos Buques, com o Velho Salgueiro-homem, a casa de Tom Bombadil e, mais adiante, as Colinas dos Túmulos.','Tom Bombadil, Fruta d\'Ouro, Frodo'],
 ['Salões de Thranduil','SaloesThranduil',[634.9,134.2],'O palácio subterrâneo do Rei Élfico, no norte da Floresta das Trevas, à beira do Rio da Floresta.','Thranduil, Legolas, Bilbo'],
 ['Fano-da-Colina','FanoColina',[479.6,548.0],'O refúgio antigo no alto do Vale Harg, acima de Edoras, de onde parte o caminho para as Sendas dos Mortos.','Théoden, Éowyn, Aragorn, Merry'],
 ['Henneth Annûn','HennethAnnun',[613.0,546.0],'A Janela do Poente: o refúgio secreto dos guardiões de Ithilien, numa caverna atrás de uma cachoeira.','Faramir, Frodo, Sam, Gollum']]
s=open(INDEX,encoding='utf-8').read()
i=s.index('const P={Condado:');j=s.index('};',i)
for n,k,xy,d,w in BASE: assert (','+k+':[') not in s[i:j]
s=s[:j]+','+','.join(f'{k}:[{xy[0]},{xy[1]}]' for n,k,xy,d,w in BASE)+s[j:]
i=s.index("const PINS=[");j=s.index("];",i);s=s[:j]+','+','.join(json.dumps([n,k,None,d,w],ensure_ascii=False) for n,k,xy,d,w in BASE)+s[j:]
open(INDEX,'w',encoding='utf-8').write(s)
SUB=[['Torre Negra','TorreNegra','Barad-dûr, a fortaleza de Sauron: muralha sobre muralha, torre sobre torre, de ferro e pedra negra. Desabou quando o Anel foi destruído.','Sauron, Boca de Sauron'],
 ['Olho de Sauron','OlhoSauron','No alto da torre, a Janela do Olho, voltada para a Montanha da Perdição.','Sauron'],
 ['Ponte de ferro','PonteFerro','A grande ponte sobre o abismo, por onde a Estrada de Sauron chega ao portão.',''],
 ['Fosso de fogo','FossoFogo','O abismo em volta da rocha da torre.',''],
 ['Estrada de Sauron','EstradaBarad','A estrada que liga Barad-dûr à porta do Sammath Naur, na Montanha da Perdição.','Sauron'],
 ['Esporão das Montanhas de Cinza','EsporaoCinza','A torre foi erguida sobre um longo esporão que desce das Ered Lithui.','']]
integrate(pl('barad'),SUB,'BaradDur',10,'barad',route_js('A Torre Negra','👁️',22,[
 ['Esporão das Montanhas de Cinza','EsporaoCinza','Por volta do ano 1000 da Segunda Era, Sauron escolhe Mordor e começa a erguer Barad-dûr.'],
 ['Torre Negra','TorreNegra','Com o poder do Um Anel, a torre é concluída em 1600. A Última Aliança a cerca por sete anos e a derruba em 3441.'],
 ['Olho de Sauron','OlhoSauron','Em 2951 da Terceira Era, Sauron se declara e reconstrói a torre. De lá, o Olho vigia a Terra-média.'],
 ['Ponte de ferro','PonteFerro','25 de março de 3019. O Anel cai no fogo: as torres desabam, as muralhas ruem, e a sombra de Sauron se desfaz no vento.']]),'A Torre Negra')
SUB=[['Velho Salgueiro-homem','VelhoSalgueiro','O salgueiro enorme e malvado à beira do Voltavime. Fez os hobbits dormirem e prendeu Merry e Pippin no tronco.','Merry, Pippin, Tom Bombadil'],
 ['Casa de Tom Bombadil','CasaBombadil','A casa do Mestre da floresta e de Fruta d\'Ouro, filha do Rio. Os hobbits passaram ali duas noites em paz.','Tom Bombadil, Fruta d\'Ouro, Frodo'],
 ['Voltavime','Voltavime','O rio de águas castanhas que corta a Floresta Velha, o centro de toda a estranheza da mata.','Fruta d\'Ouro'],
 ['Pedra erguida','PedraErguida','A pedra alta no meio das colinas, onde os hobbits pararam para descansar e adormeceram.','Frodo, Sam, Merry, Pippin'],
 ['Túmulo da Criatura','TumuloCriatura','Uma Criatura Tumular prendeu os hobbits dentro de um túmulo. Tom Bombadil os salvou e lhes deu as adagas dos Homens do Oeste.','Tom Bombadil, Frodo, Merry'],
 ['Colinas dos Túmulos','ColinasTumulos','Morros verdes cobertos de túmulos antiquíssimos e de névoa, assombrados por espíritos vindos de Angmar.',''],
 ['Floresta Velha','FlorestaVelhaSul','Resto das florestas imensas de antigamente. As árvores não gostam de estranhos, e as trilhas mudam de lugar.','Merry']]
integrate(pl('velha'),SUB,'FlorestaVelha',16,'velha',route_js('Tom Bombadil','🌼',36,[
 ['Floresta Velha','FlorestaVelhaSul','26 de setembro de 3018. Para fugir dos Cavaleiros, os hobbits entram na Floresta Velha.'],
 ['Velho Salgueiro-homem','VelhoSalgueiro','O Velho Salgueiro-homem faz os hobbits dormirem e prende Merry e Pippin.'],
 ['Casa de Tom Bombadil','CasaBombadil','Tom Bombadil os liberta e os leva para casa. O Anel não tem poder nenhum sobre ele.'],
 ['Pedra erguida','PedraErguida','28 de setembro. Nas Colinas, os hobbits adormecem junto à pedra, e a névoa os cerca.'],
 ['Túmulo da Criatura','TumuloCriatura','Uma Criatura Tumular os captura. Frodo chama Tom com a canção que ele ensinou, e Tom os salva.']]),'Tom Bombadil')
SUB=[['Portões do Rei Élfico','PortoesThranduil','Os grandes portões de pedra, que se fecham por magia, do outro lado da ponte sobre o rio.','Thranduil, Thorin'],
 ['Salão de Thranduil','SalaoThranduil','O palácio escavado na colina, com salões de colunas e lanternas. Os anões ficaram presos em suas celas.','Thranduil, Legolas, Thorin, Bilbo'],
 ['Alçapão dos barris','AlcapaoBarris','Por onde os barris vazios eram jogados no rio. Bilbo escondeu os treze anões dentro deles.','Bilbo, Thorin'],
 ['Clareira das festas','ClareiraElfos','Onde os elfos da floresta faziam banquetes à luz de fogueiras. Sempre que os anões se aproximavam, as luzes se apagavam.','Thorin, Bilbo'],
 ['Teias das aranhas','TeiasAranhas','As aranhas gigantes capturaram os anões. Bilbo os salvou com a espada Ferroada e o anel.','Bilbo'],
 ['Rio da Floresta','RioFlorestaAlto','O rio que leva os barris até a Cidade do Lago.','']]
integrate(pl('thranduil'),SUB,'SaloesThranduil',16,'thranduil',route_js('Barris soltos','🛢️',34,[
 ['Teias das aranhas','TeiasAranhas','Outono de 2941. Bilbo salva os anões das aranhas gigantes e dá nome à sua espada: Ferroada.'],
 ['Clareira das festas','ClareiraElfos','Famintos, os anões invadem as festas dos elfos e são capturados.'],
 ['Portões do Rei Élfico','PortoesThranduil','Levados pela ponte e pelos portões mágicos, são trancados nas celas do Rei Élfico.'],
 ['Salão de Thranduil','SalaoThranduil','Invisível, Bilbo vive semanas escondido no palácio até achar uma saída.'],
 ['Alçapão dos barris','AlcapaoBarris','Bilbo esconde os anões nos barris vazios e os joga no rio.'],
 ['Rio da Floresta','RioFlorestaAlto','Os barris descem o rio rumo à Cidade do Lago, com Bilbo agarrado a um deles.']]),'Barris soltos')
SUB=[['A Carrocha','RochedoCarrocha','O grande rochedo no meio do Anduin, com degraus talhados por Beorn. As águias deixaram ali a companhia de Thorin.','Gandalf, Bilbo, Thorin, Beorn'],
 ['Casa de Beorn','CasaBeorn','O salão de madeira do troca-peles, que podia virar um urso enorme. Seus animais serviam a mesa.','Beorn, Gandalf, Bilbo'],
 ['Colmeias de Beorn','ColmeiasBeorn','Beorn vivia de mel e creme, e criava abelhas maiores que um polegar em campos de trevo.','Beorn'],
 ['Ninho das Águias','NinhoAguias','O pico onde vive o Senhor das Águias, que salvou a companhia dos orcs e dos wargs.','Gwaihir, Gandalf'],
 ['Vau da Carrocha','VauCarrocha','A passagem rasa do rio junto ao rochedo.',''],
 ['Borda da Floresta das Trevas','BordaTrevas','A leste, a muralha escura da floresta. Beorn emprestou pôneis até ali.','Beorn, Gandalf']]
integrate(pl('beorn'),SUB,'Carrocha',14,'beorn',route_js('Da Carrocha à casa de Beorn','🐻',30,[
 ['Ninho das Águias','NinhoAguias','Verão de 2941. As águias salvam a companhia e a levam para o seu ninho.'],
 ['A Carrocha','RochedoCarrocha','Na manhã seguinte, as águias a deixam no alto da Carrocha.'],
 ['Vau da Carrocha','VauCarrocha','Eles descem os degraus e atravessam o vau.'],
 ['Casa de Beorn','CasaBeorn','Gandalf apresenta os anões de dois em dois, para não assustar Beorn.'],
 ['Borda da Floresta das Trevas','BordaTrevas','Com pôneis e mantimentos de Beorn, chegam à floresta — e Gandalf os deixa.']]),'Da Carrocha à casa de Beorn')
SUB=[['Campo do Fano','CampoFano','O Firienfeld: o campo alto e verde onde Théoden acampou e reuniu os Cavaleiros de Rohan.','Théoden, Éowyn, Merry'],
 ['Homens-Púkel','HomensPukel','Estátuas antigas e gastas, de homens atarracados sentados, em cada curva da estrada que sobe do vale.','Merry'],
 ['Pedras erguidas','PedrasErguidas','A fila dupla de pedras que atravessa o campo e leva ao Dimholt.',''],
 ['Dimholt','Dimholt','O bosque de árvores negras diante da Porta Escura.','Aragorn, Legolas, Gimli'],
 ['Porta Escura','PortaEscura','A entrada das Sendas dos Mortos, sob o Dwimorberg. "O caminho está fechado", dizia a tradição — até a chegada do herdeiro de Isildur.','Aragorn, Legolas, Gimli, Rei dos Mortos'],
 ['Dwimorberg','Dwimorberg','A Montanha Assombrada.',''],
 ['Vale Harg','ValeHarg','O vale do Snowbourn, que sobe de Edoras até o Fano-da-Colina.','']]
integrate(pl('dunharrow'),SUB,'FanoColina',16,'fano',route_js('As Sendas dos Mortos','💀',34,[
 ['Vale Harg','ValeHarg','7 de março de 3019. Aragorn e a Companhia Cinzenta chegam ao Fano-da-Colina.'],
 ['Homens-Púkel','HomensPukel','A estrada sobe em zigue-zague, vigiada pelas estátuas dos homens-Púkel.'],
 ['Campo do Fano','CampoFano','Éowyn pede para ir com Aragorn, e ele recusa.'],
 ['Dimholt','Dimholt','8 de março. Ao amanhecer, a Companhia atravessa o Dimholt.'],
 ['Porta Escura','PortaEscura','Aragorn, Legolas, Gimli e os Dúnedain entram nas Sendas dos Mortos.'],
 ['Campo do Fano','CampoFano','9 de março. Théoden chega e reúne Rohan. Éowyn parte disfarçada de Dernhelm, levando Merry.']]),'As Sendas dos Mortos')
SUB=[['Janela do Poente','JanelaPoente','A caverna atrás da cortina de água, voltada para o oeste. Ao pôr do sol, a luz atravessa a cachoeira como joias.','Faramir, Frodo, Sam'],
 ['Lago Proibido','LagoProibido','O lago ao pé da cachoeira. Quem o olhasse sem permissão pagava com a vida. Gollum foi pego pescando ali.','Gollum, Faramir, Frodo'],
 ['Emboscada aos Haradrim','EmboscadaHaradrim','Os guardiões de Faramir emboscaram os homens de Harad na estrada. Sam viu um olifante de verdade.','Faramir, Sam, Damrod, Mablung'],
 ['Fogueira de Sam','FogueiraSam','Onde Sam cozinhou o coelho ensopado com ervas. A fumaça denunciou os hobbits aos guardiões.','Sam, Frodo, Gollum'],
 ['Estrada de Ithilien','EstradaIthilien','A estrada norte-sul entre o Portão Negro e a Encruzilhada.',''],
 ['Jardim de Gondor','JardimGondor','Ithilien, ainda cheia de ervas, flores e árvores perfumadas, apesar da sombra de Mordor.','']]
integrate(pl('henneth'),SUB,'HennethAnnun',16,'henneth',route_js('A Janela do Poente','🐘',34,[
 ['Fogueira de Sam','FogueiraSam','7 de março de 3019. Sam cozinha um coelho ensopado; a fumaça atrai os guardiões de Gondor.'],
 ['Emboscada aos Haradrim','EmboscadaHaradrim','Faramir embosca os Haradrim. Sam vê um olifante.'],
 ['Janela do Poente','JanelaPoente','Vendados, os hobbits são levados ao refúgio. Faramir descobre o segredo do Anel e não o toma.'],
 ['Lago Proibido','LagoProibido','À noite, Gollum é pego pescando no Lago Proibido. Frodo salva sua vida.'],
 ['Estrada de Ithilien','EstradaIthilien','8 de março. Faramir os deixa partir rumo à Encruzilhada e a Cirith Ungol.']]),'A Janela do Poente')
