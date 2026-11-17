import json,re,unicodedata
S=json.load(open('/tmp/claude-0/fam/src.json'));people=json.load(open('/tmp/claude-0/people.json'))
C,AMn,Gn,ind=S['C'],S['AMn'],S['Gn'],S['ind']
def norm(t): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFD',t).encode('ascii','ignore').decode().lower()).strip()
EN={'Frodo Bolseiro':'Frodo Baggins','Samwise Gamgee':'Samwise Gamgee','Bilbo Bolseiro':'Bilbo Baggins','Aragorn II':'Aragorn II','Arwen Undómiel':'Arwen','Gollum (Sméagol)':'Gollum',
'Meriadoc Brandebuque':'Meriadoc Brandybuck','Peregrin Tûk':'Peregrin Took','Rosinha Villa':'Rosie Cotton','Hamfast Gamgee':'Hamfast Gamgee','Lobélia Sacola-Bolseiro':'Lobelia Sackville-Baggins',
'Lotho Sacola-Bolseiro':'Lotho Sackville-Baggins','Fredegar Bolger':'Fredegar Bolger','Bandobras Tûk':'Bandobras Took','Primula Brandebuque':'Primula Brandybuck','Drogo Bolseiro':'Drogo Baggins',
'Denethor II':'Denethor II','Théoden':'Théoden','Éomer':'Éomer','Éowyn':'Éowyn','Gríma Língua de Cobra':'Gríma','Bárd, o Arqueiro':'Bard','Túrin Turambar':'Túrin','Morwen Eledhwen':'Morwen',
'Nienor Níniel':'Nienor','Elros Tar-Minyatur':'Elros','Finrod Felagund':'Finrod','Idril Celebrindal':'Idril','Lúthien Tinúviel':'Lúthien','Beleg Cúthalion':'Beleg','Dior Eluchíl':'Dior',
'Dáin II Pé de Ferro':'Dáin II Ironfoot','Thorin Escudo de Carvalho':'Thorin II Oakenshield','Thráin II':'Thráin II','Thrór':'Thrór','Durin, o Imortal':'Durin I','Barbárvore':'Treebeard',
"Fruta d'Ouro":'Goldberry','Melkor (Morgoth)':'Melkor','Gothmog (Balrog)':'Gothmog','Ancalagon, o Negro':'Ancalagon','Durin, o Flagelo':"Durin's Bane",'Rei Bruxo de Angmar':'Witch-king of Angmar',
'Boca de Sauron':'Mouth of Sauron','Laracna':'Shelob','Ar-Pharazôn':'Ar-Pharazôn','Tar-Míriel':'Tar-Míriel','Gil-galad':'Gil-galad','Círdan':'Círdan','Fëanor':'Fëanor','Eöl':'Eöl','Manwë':'Manwë','Aulë':'Aulë','Oromë':'Oromë',
'Gollum (versão LEGO)':None,'Dís':'Dís','Óin':'Óin','Glóin':'Glóin','Fíli':'Fíli','Kíli':'Kíli','Celebrían':'Celebrían','Anárion':'Anárion','Eärendil':'Eärendil','Húrin':'Húrin'}
SKIP=lambda p: p['source'] and any(w in p['source'] for w in ['Rings of Power','Shadow','LEGO','Filmes','Third Age','Battle for','War in the North','Lord of the Rings Online','jogo'])
out={};miss=[]
for p in people:
    if SKIP(p) or p['key'].startswith('game-'): continue
    n=p['name'];cand=[EN.get(n,n),re.sub(r'\s*\(.*\)','',n),n.split(',')[0]]
    am=gd=None
    for c in cand:
        if c is None: break
        k=norm(c);am=am or AMn.get(k);gd=gd or Gn.get(k)
    if not am:
        first=norm(cand[0] or n).split(' ')[0];hits=[k for k,r in C.items() if norm(r['name']).split(' ')[0]==first]
        if len(hits)==1: am=hits[0]
    out[p['key']]={'name':n,'am':am,'gd':gd}
    if not am and not gd: miss.append(n)
json.dump(out,open('/tmp/claude-0/fam/match.json','w'),ensure_ascii=False)
print('fichas literárias',len(out),'casadas AM',sum(1 for v in out.values() if v['am']),'GED',sum(1 for v in out.values() if v['gd']))
print('sem par:',miss)
for k,v in list(out.items())[:200]:
    if v['am'] and norm(C[v['am']]['name']).split()[0]!=norm(v['name']).split()[0] and v['name'] not in EN: print('conferir',v['name'],'->',C[v['am']]['name'])
