import sys,json;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import integrate,route_js
pl=lambda n:json.load(open(f'/tmp/claude-0/b3/{n}.json'))['places']
SUB=[['Amon Sûl','AmonSul','No topo achatado, o anel de pedras em ruínas da grande torre de Amon Sûl, que guardava o palantír principal do Norte.','Elendil, Aragorn'],
 ['Pedra de Gandalf','PedraGandalf','Uma pedra plana com uma runa G e três riscos: Gandalf esteve ali em 3 de outubro e lutou contra os Nove.','Gandalf, Aragorn'],
 ['A clareira','ClareiraTopo','A cavidade na encosta oeste onde os hobbits acamparam. À noite, cinco Cavaleiros atacaram, e o Rei-Bruxo feriu Frodo com uma lâmina de Morgul.','Frodo, Aragorn, Rei-Bruxo'],
 ['Grande Estrada Leste','EstradaTopo','A estrada que passa ao sul do Topo do Vento, rumo ao Vau do Bruinen.',''],
 ['Colinas do Vento','ColinasVento','A crista de colinas que se estende para o norte a partir do Topo do Vento, por onde Aragorn guiou os hobbits.','Aragorn']]
integrate(pl('topo'),SUB,'TopoVento',18,'topo',route_js('O ataque no Topo do Vento','🗡️',36,[
 ['Colinas do Vento','ColinasVento','5 de outubro de 3018. Passolargo guia os hobbits pelas Colinas do Vento.'],
 ['Amon Sûl','AmonSul','6 de outubro. No topo, encontram as ruínas da torre e veem Cavaleiros Negros na estrada.'],
 ['Pedra de Gandalf','PedraGandalf','Aragorn acha a marca de Gandalf: uma runa G e três riscos — ele passou por ali em 3 de outubro.'],
 ['A clareira','ClareiraTopo','À noite, cinco Cavaleiros atacam. Frodo põe o Anel e é ferido pela lâmina de Morgul do Rei-Bruxo.'],
 ['Grande Estrada Leste','EstradaTopo','Aragorn leva os hobbits para longe da estrada, rumo a Valfenda, com Frodo ferido.']]),'O ataque no Topo do Vento')
SUB=[['Morannon','Morannon','O Portão Negro de Mordor: portas de ferro numa muralha que fecha a passagem de Cirith Gorgor.','Frodo, Sam, Gollum, Aragorn, Boca de Sauron'],
 ['Narchost','Narchost','Uma das Torres dos Dentes, construídas por Gondor para vigiar Mordor e depois tomadas por Sauron.',''],
 ['Carchost','Carchost','A outra Torre dos Dentes, do lado oposto da passagem.',''],
 ['Morros de escória','MorrosEscoria','Montes de escória e lama diante do Portão. Neles o exército do Oeste se posicionou para a última batalha.','Aragorn, Gandalf, Pippin'],
 ['Dagorlad','Dagorlad','A Planície da Batalha, onde a Última Aliança venceu Sauron no fim da Segunda Era. Os pântanos guardam os mortos.','Elendil, Gil-galad'],
 ['Udûn','Udun','O vale fechado atrás do Portão Negro, cheio de túneis e fortalezas de orcs.','']]
integrate(pl('morannon'),SUB,'PortaoNegro',16,'morannon',route_js('A batalha do Morannon','⚔️',30,[
 ['Morannon','Morannon','5 de março de 3019. Frodo, Sam e Gollum observam o Portão Negro e desistem de entrar por ali.'],
 ['Dagorlad','Dagorlad','23 de março. O exército do Oeste atravessa a planície rumo ao Portão, para distrair os olhos de Sauron.'],
 ['Morros de escória','MorrosEscoria','25 de março. Aragorn posiciona o exército sobre dois morros de escória.'],
 ['Morannon','Morannon','A Boca de Sauron mostra a cota de mithril de Frodo. Gandalf recusa os termos, e o Portão se abre.'],
 ['Udûn','Udun','Quando a batalha parece perdida, as águias chegam. O Anel é destruído, e Mordor desmorona.']]),'A batalha do Morannon')
SUB=[['Minas Morgul','CidadeMorgul','A antiga Minas Ithil, Torre da Lua, tomada pelos Nazgûl. Suas muralhas brilham com uma luz pálida e fria.','Rei-Bruxo de Angmar'],
 ['Ponte de Morgul','PonteMorgul','A ponte branca sobre o Morgulduin, cheia de estátuas, entre flores pálidas e malcheirosas.','Frodo, Sam, Gollum'],
 ['Escada Reta','EscadaReta','A primeira escadaria, longa e íngreme, cortada no paredão ao norte do vale.','Frodo, Sam, Gollum'],
 ['Escada Sinuosa','EscadaSinuosa','A segunda escadaria, que serpenteia até o alto, junto ao túnel de Laracna.','Frodo, Sam, Gollum'],
 ['Toca de Laracna','TocaLaracna','Torech Ungol: o túnel escuro da aranha gigante Laracna, no passo de Cirith Ungol. Gollum levou os hobbits para lá de propósito.','Laracna, Frodo, Sam, Gollum'],
 ['Torre de Cirith Ungol','TorreCirithUngol','A torre de orcs que guarda o passo pelo lado de Mordor. Sam resgatou Frodo ali.','Sam, Frodo, Shagrat, Gorbag'],
 ['Encruzilhada','EncruzilhadaRei','O cruzamento de estradas em Ithilien, com a estátua de um antigo rei de Gondor. Os orcs quebraram a cabeça, mas ela estava coroada de flores.','Frodo, Sam, Gollum'],
 ['Imlad Morgul','ImladMorgul','O vale de Minas Morgul, por onde corre o Morgulduin de águas pálidas.','']]
integrate(pl('morgul'),SUB,['MinasMorgul','CirithUngol'],16,'cirith',route_js('O caminho de Cirith Ungol','🕷️',30,[
 ['Encruzilhada','EncruzilhadaRei','10 de março de 3019. Na Encruzilhada, Frodo vê a cabeça do rei de pedra coroada de flores, sob o pôr do sol.'],
 ['Ponte de Morgul','PonteMorgul','O Rei-Bruxo sai de Minas Morgul com seu exército. Frodo, escondido, resiste à vontade de pôr o Anel.'],
 ['Escada Reta','EscadaReta','Gollum leva os hobbits pela Escada Reta, no paredão do vale.'],
 ['Escada Sinuosa','EscadaSinuosa','Depois sobem a Escada Sinuosa. Gollum hesita, quase arrependido, ao ver Frodo dormindo.'],
 ['Toca de Laracna','TocaLaracna','13 de março. Laracna pica Frodo. Sam a enfrenta com Ferroada e o frasco de Galadriel.'],
 ['Torre de Cirith Ungol','TorreCirithUngol','Os orcs levam Frodo para a torre. Sam, com o Anel, entra e o resgata.']]),'O caminho de Cirith Ungol')
