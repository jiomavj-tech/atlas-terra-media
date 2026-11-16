import json,re,sys
INDEX='/home/claude/atlas-terra-media/index.html'
people=json.load(open('/tmp/claude-0/people.json'))
byname={p['name']:p['key'] for p in people};keys={p['key'] for p in people}
A={ # apelidos curtos -> nome exato da ficha
'Frodo':'Frodo Bolseiro','Sam':'Samwise Gamgee','Bilbo':'Bilbo Bolseiro','Aragorn':'Aragorn II','Arwen':'Arwen Undómiel','Gollum':'Gollum (Sméagol)',
'Merry':'Meriadoc Brandebuque','Pippin':'Peregrin Tûk','Rosinha':'Rosinha Villa','Hamfast':'Hamfast Gamgee','Lobélia':'Lobélia Sacola-Bolseiro','Lotho':'Lotho Sacola-Bolseiro',
'Fredegar':'Fredegar Bolger','Primula':'Primula Brandebuque','Drogo':'Drogo Bolseiro','Denethor':'Denethor II','Gríma':'Gríma Língua de Cobra','Bárd':'Bárd, o Arqueiro',
'Túrin':'Túrin Turambar','Morwen':'Morwen Eledhwen','Nienor':'Nienor Níniel','Elros':'Elros Tar-Minyatur','Finrod':'Finrod Felagund','Idril':'Idril Celebrindal',
'Lúthien':'Lúthien Tinúviel','Beleg':'Beleg Cúthalion','Dior':'Dior Eluchíl','Dáin':'Dáin II Pé de Ferro','Thorin':'Thorin Escudo de Carvalho','Thráin':'Thráin II',
'Durin I':'Durin, o Imortal','Melkor':'Melkor (Morgoth)','Gothmog':'Gothmog (Balrog)','Ancalagon':'Ancalagon, o Negro','Balrog de Moria':'Durin, o Flagelo','Rei Bruxo':'Rei Bruxo de Angmar',
'Celebrimbor (Shadow)':'Celebrimbor (versão Shadow)','Idril (Shadow)':'Idril (Shadow of War)','Morwen (Third Age)':'Morwen (The Third Age)','Marwen':'Marwen (Shadow of Mordor)',
'Dirhael':'Dirhael (Shadow of Mordor)','Ioreth':'Ioreth (Shadow of War)','Durin IV':'Durin IV (série)','Míriel (série)':'Míriel (série)'}
def K(n):
    n=A.get(n,n)
    if n in byname: return byname[n]
    raise SystemExit('nome sem ficha: '+n)
REL={ # chave da ficha -> ligações (só o que está nas obras citadas)
'Bilbo':'Gandalf, Thorin, Frodo',
'game-4':'Idril (Shadow), Talion','game-6':'Idril (Shadow), Talion','game-21':'Berethor, Morwen (Third Age)','game-23':'Berethor, Morwen (Third Age)',
'meriadoc-brandebuque':'Pippin, Frodo, Sam, Éowyn, Théoden, Barbárvore','peregrin-t-k':'Merry, Frodo, Gandalf, Denethor, Beregond, Faramir, Barbárvore',
'rosinha-villa':'Sam','hamfast-gamgee':'Sam, Bilbo, Frodo','lob-lia-sacola-bolseiro':'Lotho, Bilbo, Frodo','lotho-sacola-bolseiro':'Lobélia, Saruman, Frodo',
'fredegar-bolger':'Frodo, Merry, Pippin, Sam','d-agol':'Gollum','bandobras-t-k':'Bilbo, Pippin','primula-brandebuque':'Drogo, Frodo','drogo-bolseiro':'Primula, Frodo, Bilbo',
'boromir':'Faramir, Denethor, Aragorn, Frodo, Merry, Pippin','faramir':'Boromir, Denethor, Éowyn, Frodo, Sam, Gandalf','denethor-ii':'Boromir, Faramir, Gandalf, Pippin',
'th-oden':'Éomer, Éowyn, Gríma, Gandalf, Merry','-omer':'Éowyn, Théoden, Aragorn','-owyn':'Éomer, Théoden, Faramir, Merry, Rei Bruxo, Aragorn',
'gr-ma-l-ngua-de-cobra':'Saruman, Théoden, Éowyn','beregond':'Pippin, Faramir, Denethor','imrahil':'Denethor, Boromir, Faramir, Aragorn, Éomer','halbarad':'Aragorn, Elladan, Elrohir',
'b-rd-o-arqueiro':'Smaug, Thorin, Bilbo, Thranduil, Gandalf','beorn':'Gandalf, Bilbo, Thorin, Bolg',
'beren':'Lúthien, Thingol, Finrod, Dior, Melkor','t-rin-turambar':'Húrin, Morwen, Nienor, Beleg, Gwindor, Glaurung, Thingol','tuor':'Huor, Idril, Eärendil, Turgon, Ulmo, Maeglin',
'h-rin':'Morwen, Túrin, Nienor, Huor, Melkor, Turgon','huor':'Húrin, Tuor, Turgon','morwen-eledhwen':'Húrin, Túrin, Nienor','nienor-n-niel':'Túrin, Húrin, Morwen, Glaurung',
'e-rendil':'Tuor, Idril, Elrond, Elros, Ancalagon','elros-tar-minyatur':'Elrond, Eärendil, Maglor','isildur':'Elendil, Anárion, Sauron, Elrond, Círdan, Gil-galad',
'elendil':'Isildur, Anárion, Gil-galad, Sauron','an-rion':'Elendil, Isildur','ar-pharaz-n':'Tar-Míriel, Sauron','tar-m-riel':'Ar-Pharazôn','aldarion':'Erendis','erendis':'Aldarion',
'celebr-an':'Elrond, Galadriel, Celeborn, Arwen, Elladan, Elrohir','elrond':'Celebrían, Arwen, Elladan, Elrohir, Elros, Eärendil, Gil-galad, Aragorn, Gandalf',
'celeborn':'Galadriel, Celebrían, Haldir','thranduil':'Legolas, Bilbo, Thorin, Bárd','glorfindel':'Frodo, Elrond, Aragorn, Rei Bruxo','c-rdan':'Gandalf, Elrond, Gil-galad, Isildur',
'haldir':'Galadriel, Celeborn, Frodo, Legolas','elladan':'Elrohir, Elrond, Celebrían, Arwen, Aragorn, Halbarad','elrohir':'Elladan, Elrond, Celebrían, Arwen, Aragorn, Halbarad',
'f-anor':'Maedhros, Maglor, Celegorm, Curufin, Caranthir, Amrod, Amras, Fingolfin, Finarfin, Melkor, Gothmog','fingolfin':'Fëanor, Finarfin, Turgon, Aredhel, Melkor',
'finarfin':'Fëanor, Fingolfin, Finrod, Orodreth, Galadriel','finrod-felagund':'Finarfin, Galadriel, Orodreth, Beren, Sauron',
'maedhros':'Fëanor, Maglor, Celegorm, Curufin, Caranthir, Amrod, Amras, Melkor','maglor':'Fëanor, Maedhros, Elrond, Elros','celegorm':'Fëanor, Curufin, Lúthien, Orodreth, Dior',
'curufin':'Fëanor, Celegorm, Lúthien, Orodreth','caranthir':'Fëanor, Maedhros','amrod':'Amras, Fëanor','amras':'Amrod, Fëanor',
'turgon':'Fingolfin, Aredhel, Idril, Tuor, Maeglin, Húrin, Huor','idril-celebrindal':'Turgon, Tuor, Eärendil, Maeglin','l-thien-tin-viel':'Beren, Thingol, Melian, Dior, Sauron, Melkor',
'thingol':'Melian, Lúthien, Beren, Túrin, Beleg','melian':'Thingol, Lúthien','beleg-c-thalion':'Túrin, Thingol, Gwindor','gwindor':'Túrin, Beleg, Orodreth',
'orodreth':'Finarfin, Finrod, Gwindor, Túrin','gil-galad':'Elrond, Elendil, Círdan, Sauron, Isildur','e-l':'Aredhel, Maeglin, Turgon','maeglin':'Eöl, Aredhel, Turgon, Idril, Tuor',
'aredhel':'Eöl, Maeglin, Turgon, Fingolfin','dior-eluch-l':'Beren, Lúthien, Nimloth, Celegorm','nimloth':'Dior',
'd-in-ii-p-de-ferro':'Thorin, Azog, Bolg, Gandalf, Bárd','thorin-escudo-de-carvalho':'Bilbo, Gandalf, Thráin, Thrór, Dís, Fíli, Kíli, Balin, Dwalin, Dáin, Smaug',
'balin':'Dwalin, Thorin, Bilbo, Óin, Ori','dwalin':'Balin, Thorin','f-li':'Kíli, Thorin, Dís','k-li':'Fíli, Thorin, Dís','-in':'Glóin, Balin, Thorin','gl-in':'Óin, Gimli, Thorin',
'bifur':'Bofur, Bombur, Thorin','bofur':'Bombur, Bifur, Thorin','bombur':'Bofur, Bifur, Thorin','nori':'Dori, Ori, Thorin','dori':'Nori, Ori, Thorin','ori':'Dori, Nori, Balin',
'durin-o-imortal':'Thrór, Thorin, Dáin','thr-r':'Thráin, Thorin, Azog, Smaug','thr-in-ii':'Thrór, Thorin, Dís, Gandalf, Sauron','d-s':'Thorin, Fíli, Kíli, Thráin',
'smaug':'Bilbo, Bárd, Thorin, Thrór','laracna':'Frodo, Sam, Gollum, Ungoliant','barb-rvore':'Merry, Pippin, Gandalf, Saruman, Bregalad','bregalad':'Barbárvore, Merry, Pippin',
'tom-bombadil':"Fruta d'Ouro, Frodo, Sam, Merry, Pippin",'fruta-d-ouro':'Tom Bombadil, Frodo','radagast':'Gandalf, Saruman, Beorn','alatar':'Pallando, Oromë','pallando':'Alatar, Oromë',
'manw-':'Varda, Melkor, Ulmo','varda':'Manwë, Melkor','ulmo':'Manwë, Tuor, Turgon','aul-':'Yavanna, Sauron, Saruman','yavanna':'Aulë, Radagast','mandos':'Nienna, Lúthien, Fëanor',
'nienna':'Mandos, Gandalf','orom-':'Alatar, Pallando','tulkas':'Melkor, Manwë','melkor-morgoth-':'Manwë, Sauron, Ungoliant, Gothmog, Glaurung, Ancalagon, Fëanor, Fingolfin, Húrin, Beren, Lúthien',
'ungoliant':'Melkor, Laracna','gothmog-balrog-':'Melkor, Fëanor','glaurung':'Melkor, Túrin, Nienor','ancalagon-o-negro':'Melkor, Eärendil','durin-o-flagelo':'Gandalf, Melkor',
'rei-bruxo-de-angmar':'Sauron, Éowyn, Merry, Frodo, Gandalf, Glorfindel, Khamûl','kham-l':'Sauron, Rei Bruxo','boca-de-sauron':'Sauron, Gandalf, Aragorn',
'gorbag':'Shagrat, Frodo, Sam, Laracna','shagrat':'Gorbag, Frodo, Sam','ugl-k':'Grishnákh, Saruman, Merry, Pippin, Éomer','grishn-kh':'Uglúk, Merry, Pippin, Sauron',
'azog':'Thrór, Thráin, Bolg, Dáin','bolg':'Azog, Beorn',
'lurtz':'Saruman, Boromir, Aragorn','tauriel':'Legolas, Thranduil, Kíli','alfrid-lickspittle':'Bárd',
'adar':'Galadriel, Arondir, Sauron','arondir':'Bronwyn, Theo, Adar','bronwyn':'Arondir, Theo','theo':'Bronwyn, Arondir','nori-brandifoot':'Poppy Proudfellow','poppy-proudfellow':'Nori Brandifoot',
'disa':'Durin IV, Elrond','durin-iv-s-rie-':'Disa, Elrond','e-rien':'Elendil, Isildur, Kemen','kemen':'Ar-Pharazôn, Eärien','estrid':'Isildur','m-riel-s-rie-':'Elendil, Ar-Pharazôn',
'elanor-brandyfoot':'Nori Brandifoot, Poppy Proudfellow',
'hirgon':'Talion','lithariel':'Marwen, Talion','marwen-shadow-of-mordor-':'Lithariel, Saruman, Talion','torvin':'Talion','dirhael-shadow-of-mordor-':'Talion, Ioreth','ioreth-shadow-of-war-':'Talion, Dirhael',
'golum-lego-':'Frodo, Sam','the-bright-lord-game-':'Talion, Celebrimbor (Shadow)','seregost-shadow-of-war-':'Talion','orc-nemesis-shadow-of-war-':'Talion'}
PLACES={'game-24':'Gondor','game-25':'Elrond, Valfenda','game-26':'Lothlórien'}
s=open(INDEX,encoding='utf-8').read();n=0
def setrec(key,conn_text,res):
    global s,n
    a='{"key":'+json.dumps(key,ensure_ascii=False)+',"name"';assert s.count(a)==1,(key,s.count(a))
    i=s.index(a)
    m=re.compile(r'"connections":"(?:[^"\\]|\\.)*"').search(s,i);assert m and m.start()-i<1500,(key,'conn')
    s=s[:m.start()]+'"connections":'+json.dumps(conn_text,ensure_ascii=False)+s[m.end():]
    m=re.compile(r'"resolved_connection_keys":\[[^\]]*\],"unresolved_connection_labels":\[[^\]]*\],"connection_review_status":"[^"]*"').search(s,i)
    nxt=s.find('{"key":"',i+10);assert m and (nxt<0 or m.start()<nxt),(key,'res')
    s=s[:m.start()]+'"resolved_connection_keys":'+json.dumps(res,ensure_ascii=False)+',"unresolved_connection_labels":[],"connection_review_status":"Referências resolvidas"'+s[m.end():];n+=1
for key,txt in REL.items():
    assert key in keys,key
    names=[A.get(x.strip(),x.strip()) for x in txt.split(', ')]
    res=[K(x) for x in names]
    assert key not in res,key
    setrec(key,', '.join(names),res)
for key,txt in PLACES.items():
    names=[x.strip() for x in txt.split(', ')];res=[byname[x] for x in names if x in byname]
    setrec(key,txt,res)
open(INDEX,'w',encoding='utf-8').write(s);print('fichas atualizadas',n)
