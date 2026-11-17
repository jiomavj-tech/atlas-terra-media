import json
P=json.load(open('/tmp/claude-0/realm/mine.json'))
D=[
('lindon','Lindon','#6fa8dc',['SA','TA','GA'],'Segunda Era, ano 1, até o fim da Terceira Era','Mithlond, os Portos Cinzentos',
 'O último pedaço de Beleriand a leste do Mar, dividido pelo Golfo de Lûn em Forlindon e Harlindon. Reino de Gil-galad e, depois dele, guardado por Círdan.',
 ['Gil-galad, último Grande Rei dos Noldor','Círdan, o Armador'],['Númenor','Arnor','Valfenda'],['Sauron','Angmar']),
('arnor','Arnor','#d2a85c',['SA','TA'],'Segunda Era 3320 – Terceira Era 1974 (restaurado na Quarta Era)','Annúminas, depois Fornost',
 'O Reino do Norte dos Dúnedain, fundado por Elendil depois da Queda de Númenor. Dividido em 861 em Arthedain, Cardolan e Rhudaur, foi desgastado por Angmar até a queda de Arthedain em 1974. Seus herdeiros seguiram como os Guardiões até Aragorn restaurá-lo.',
 ['Elendil, o Alto','Isildur','Valandil','Arvedui, último rei de Arthedain','os Chefes dos Dúnedain','Aragorn II Elessar'],['Gondor','Lindon','Valfenda'],['Angmar','Sauron']),
('angmar','Angmar','#9c8fb0',['TA'],'c. Terceira Era 1300 – 1975','Carn Dûm',
 'Um reino frio dos dois lados do norte das Montanhas Sombrias, governado de Carn Dûm pelo Rei-bruxo. Sua longa guerra destruiu o Reino do Norte, mas seu poder foi quebrado na Batalha de Fornost.',
 ['o Rei-bruxo de Angmar'],['Sauron','os Homens das Colinas de Rhudaur'],['Arnor','Lindon','Valfenda','Gondor']),
('eregion','Eregion (Azevim)','#5fb3a6',['SA'],'c. Segunda Era 750 – 1697','Ost-in-Edhil',
 'A terra dos ferreiros Noldor a oeste de Moria. Ensinados por Sauron disfarçado, forjaram os Anéis de Poder; Celebrimbor fez sozinho os Três. Quando o engano de Sauron foi descoberto, Eregion foi arrasada.',
 ['Celebrimbor, senhor dos Gwaith-i-Mírdain'],['Khazad-dûm','Lindon'],['Sauron']),
('shire','O Condado','#b5d34e',['TA','GA'],'Terceira Era 1601 – Quarta Era','Grã-Cava (sede do Prefeito)',
 'As quatro Quartas dos hobbits, depois somadas à Terra-dos-Buques e à Marca Ocidental. Governado de leve pelo Thain e pelo Prefeito.',
 ['o Thain','o Prefeito de Grã-Cava'],['Arnor (em nome)'],['os rufiões de Saruman (3019)']),
('khazad-dum','Khazad-dûm (Moria)','#c08440',['SA','TA'],'Dias Antigos – Terceira Era 1981','Khazad-dûm',
 'O reino do Povo de Durin sob as Montanhas Sombrias, o maior dos reinos dos anões até o Balrog expulsá-los.',
 ['Durin, o Imortal, e seus herdeiros','Durin VI'],['Eregion'],['os orcs','a Ruína de Durin']),
('lorien','Lórien','#e8c547',['SA','TA','GA'],'Segunda Era – início da Quarta Era','Caras Galadhon',
 'O reino élfico escondido da Floresta Dourada, governado na Terceira Era por Celeborn e Galadriel.',
 ['Amdír','Amroth','Celeborn e Galadriel'],['Valfenda','o Reino da Floresta'],['Dol Guldur']),
('woodland-realm','Reino da Floresta','#62a656',['SA','TA','GA'],'Segunda Era – Quarta Era','os Salões de Thranduil',
 'Reino dos elfos silvestres na Grande Floresta Verde, depois chamada Floresta das Trevas. Suas fronteiras recuaram para o nordeste conforme a sombra de Dol Guldur se espalhava.',
 ['Oropher','Thranduil'],['a Cidade do Lago','Lórien'],['Dol Guldur','as aranhas da Floresta das Trevas']),
('erebor-dale','Erebor e Valle','#e0913e',['TA','GA'],'Terceira Era 1999 – Quarta Era (interrompido de 2770 a 2941)','Erebor, a Montanha Solitária',
 'Os reinos irmãos do norte: o Reino sob a Montanha e os Homens de Valle e do Lago Comprido, unidos pelo comércio e pela guerra contra Smaug.',
 ['os Reis sob a Montanha','os Reis de Valle','o Mestre da Cidade do Lago'],['as Colinas de Ferro','o Reino da Floresta'],['Smaug','os Lestenses','os orcs do Norte']),
('rohan','Rohan','#86c860',['TA','GA'],'Terceira Era 2510 – Quarta Era','Edoras',
 'A Terra dos Cavaleiros, reino dos senhores de cavalos nas pradarias da antiga Calenardhon, dada por Gondor a Eorl, o Jovem, depois da Batalha do Campo de Celebrant.',
 ['Eorl, o Jovem','Helm Mão-de-Martelo','Théoden','Éomer'],['Gondor'],['os terra-pardenses','Saruman','Mordor']),
('gondor','Gondor','#eceff6',['SA','TA','GA'],'Segunda Era 3320 – Quarta Era','Minas Tirith (antes, Osgiliath)',
 'O Reino do Sul dos Dúnedain, fundado por Isildur e Anárion. O mais poderoso reino dos Homens na Terceira Era; governado por reis até 2050 e depois pelos Regentes, até a volta de Aragorn.',
 ['Isildur e Anárion','os Reis da linhagem de Anárion','os Regentes Governantes','o Rei Elessar'],['Arnor','Rohan','Dol Amroth'],['Mordor','Harad','Umbar','os Lestenses']),
('mordor','Mordor','#e0443a',['SA','TA','GA'],'c. Segunda Era 1000 – Terceira Era 3019','Barad-dûr',
 'A Terra Negra, cercada pelas Montanhas da Sombra e pelas Montanhas de Cinza. Reino de Sauron por duas Eras, com os campos de escravos de Núrnen alimentando seus exércitos.',
 ['Sauron','os Nazgûl'],['Harad','os Lestenses','Umbar'],['Gondor','os Povos Livres']),
]
out=[]
for i,n,c,e,per,sede,res,gov,ali,ini in D:
    out.append(dict(id=i,nome=n,cor=c,eras=e,periodo=per,sede=sede,resumo=res,gov=gov,ali=ali,ini=ini,poly=[[round(x,1),round(y,1)] for x,y in P[i]]))
open('/tmp/claude-0/realm/build/dados.js','w').write('window.ATLAS_REINOS='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';')
print(len(out))
