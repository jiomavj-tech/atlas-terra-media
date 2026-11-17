import json,re,unicodedata,collections
S=json.load(open('/tmp/claude-0/fam/src.json'));M=json.load(open('/tmp/claude-0/fam/match.json'))
C,P,ind,G,AMn=S['C'],S['P'],S['ind'],S['G'],S['AMn']
def norm(t): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFD',t).encode('ascii','ignore').decode().lower()).strip()
OV={'rosinha-villa':('roseCotton','@I8cca1f7ba6@'),'denethor-ii':('denethor2',None),'aldarion':('tar-aldarion','@I8fed95705d@'),'d-in-ii-p-de-ferro':('dain2','@I3f3f86102b@'),
'thorin-escudo-de-carvalho':('thorin2','@I39249679be@'),'bregalad':('quickbeam',None),'pallando':('pallando',None),'alatar':('alatar',None),'b-rd-o-arqueiro':('bard1',None),'gr-ma-l-ngua-de-cobra':('grima',None)}
for k,(a,g) in OV.items(): M[k]['am']=a;M[k]['gd']=g
gname=lambda g:[n for n in ind[g]['names'] if n!='?']
# 1) liga indivíduos do GEDCOM a pessoas do Arda-Maps: mesmo nome E pelo menos um parente com mesmo nome
def amrel(a): return {norm(C[x]['name']) for t in P.get(a,{}).values() for x in t}
def gdrel(g): return {norm(n) for t in G.get(g,{}).values() for x in t for n in gname(x)}
cand=collections.defaultdict(set)
for k,r in C.items(): cand[norm(r['name'])].add(k)
link={}
for v in M.values():
    if v['am'] and v['gd'] and (amrel(v['am'])&gdrel(v['gd']) or not P.get(v['am'])): link[v['gd']]=v['am']
for g in ind:
    if g in link: continue
    cs={a for n in gname(g) for a in cand.get(norm(n),())}
    ok=[a for a in cs if amrel(a)&gdrel(g)]
    if len(ok)==1: link[g]=ok[0]
    elif len(cs)==1 and not P.get(next(iter(cs))) : link[g]=next(iter(cs))      # pessoa sem parentes no Arda-Maps
# 1b) segundo passo: junta quem tem o mesmo primeiro nome e um parente já identificado em comum
first=lambda n:norm(n).split(' ')[0] if norm(n) else ''
for _ in range(3):
    for g in ind:
        if g in link: continue
        fn={first(n) for n in gname(g)}
        hits=set()
        for t,lst in G.get(g,{}).items():
            for o in lst:
                if o not in link: continue
                ao=link[o]
                for tt,al in P.get(ao,{}).items():
                    for a in al:
                        if first(C[a]['name']) in fn and a not in link.values(): hits.add(a)
        if len(hits)==1: link[g]=hits.pop()
NODE=lambda g:'a:'+link[g] if g in link else 'g:'+g
# 2) arestas: para cada pessoa e tipo, o GEDCOM tem prioridade quando traz dados; senão vale o Arda-Maps
TY=('par','spo','sib')
E={t:set() for t in TY}
gd_has=collections.defaultdict(set)
for g,v in G.items():
    for t in TY:
        if v.get(t): gd_has[NODE(g)].add(t)
for g,v in G.items():
    for t in TY:
        for o in v.get(t,[]):
            a,b=NODE(g),NODE(o)
            if t=='par': E['par'].add((a,b))
            else: E[t].add(tuple(sorted((a,b))))
for a,v in P.items():
    n='a:'+a
    for t in TY:
        if t in gd_has[n]: continue
        for o in v.get(t,[]):
            m='a:'+o
            if t=='par':
                if 'par' in gd_has[n]: continue
                E['par'].add((n,m))
            else:
                if t in gd_has[m]: continue
                E[t].add(tuple(sorted((n,m))))
    # filhos vindos do Arda-Maps, quando o filho não tem pais no GEDCOM
    for o in v.get('chi',[]):
        m='a:'+o
        if 'par' not in gd_has[m]: E['par'].add((m,n))
# 3) rótulos em português para os nomes de família dos hobbits e expressões comuns
SUR=[('Sackville-Baggins','Sacola-Bolseiro'),('Baggins','Bolseiro'),('Brandybuck','Brandebuque'),('Took','Tûk'),('Cotton','Villa'),('Gamgee','Gamgee')]
def pt(n):
    for a,b in SUR: n=re.sub(r'\b'+re.escape(a)+r'\b',b,n)
    n=re.sub(r'\(son of ','(filho de ',n);n=re.sub(r'\(daughter of ','(filha de ',n);n=re.sub(r'\(wife of ','(esposa de ',n);n=re.sub(r'\(husband of ','(marido de ',n)
    n=n.replace('(Steward of Gondor)','(Regente de Gondor)').replace('(King of Gondor)','(rei de Gondor)').replace('(King of Arnor)','(rei de Arnor)').replace('(King of Rohan)','(rei de Rohan)')
    return n
lab={};meta={}
for k,r in C.items(): lab['a:'+k]=r['name'];meta['a:'+k]=(r['race'],r['gender'][:1].upper(),r['born'],r['died'])
for g,v in ind.items():
    n=NODE(g)
    if n not in lab:
        nm=gname(g);lab[n]=nm[0] if nm else '?';meta[n]=(v['nati'].capitalize(),v['sex'],'','')
atl={}
for key,v in M.items():
    n='a:'+v['am'] if v['am'] else (NODE(v['gd']) if v['gd'] else None)
    if n and n not in atl and key not in ('beleg-c-thalion','haldir'): atl[n]=key   # homônimos: o nó encontrado é outra pessoa
people=json.load(open('/tmp/claude-0/people.json'));pname={p['key']:p['name'] for p in people}
# remove nós de "desconhecido"
bad={n for n,l in lab.items() if l.startswith('Unknown') or l in ('?','nome desconhecido')}
for t in TY: E[t]={e for e in E[t] if e[0] not in bad and e[1] not in bad and e[0]!=e[1]}
# correções de erros conhecidos nas fontes
def L(n): return lab.get(n,'')
DROP_PAR={('Eöl','Fingolfin'),('Fluithuin','Melkor'),('Telimektar','Tulkas')}
E['par']={e for e in E['par'] if (L(e[0]),L(e[1])) not in DROP_PAR}
for n in list(lab):
    if lab[n].startswith('?'): lab[n]=re.sub(r'^\?\s*\((.*)\)$',r'\1',lab[n]) if '(' in lab[n] else 'nome desconhecido'
lab={n:(l.replace('father of','pai de').replace(' and ',' e ') if l.startswith('father of') else l) for n,l in lab.items()}
inE={x for t in TY for e in E[t] for x in e}
ids={n:i for i,n in enumerate(sorted(inE))}
OUT={'n':[[pt(pname.get(atl.get(n),lab[n])) if atl.get(n) else pt(lab[n]),meta[n][0],meta[n][1],atl.get(n,'')] for n in sorted(inE)],
     'p':sorted([ids[a],ids[b]] for a,b in E['par']),'s':sorted([ids[a],ids[b]] for a,b in E['spo']),'b':sorted([ids[a],ids[b]] for a,b in E['sib'])}
json.dump(OUT,open('/tmp/claude-0/fam/family.json','w'),ensure_ascii=False,separators=(',',':'))
print('pessoas',len(OUT['n']),'filiações',len(OUT['p']),'casais',len(OUT['s']),'irmãos',len(OUT['b']),'fichas',sum(1 for x in OUT['n'] if x[3]),'GED ligados',len(link),'bytes',len(json.dumps(OUT,ensure_ascii=False,separators=(',',':'))))
# conferência
rev={x[3]:i for i,x in enumerate(OUT['n']) if x[3]}
def rel(k):
    i=rev[k];N=OUT['n']
    par=[N[b][0] for a,b in OUT['p'] if a==i];chi=[N[a][0] for a,b in OUT['p'] if b==i];sp=[N[b if a==i else a][0] for a,b in OUT['s'] if i in (a,b)]
    return f"pais {par} | cônj {sp} | filhos {chi[:6]}"
for k in ['th-oden','morwen-eledhwen','elrond','beren','orodreth','gil-galad','Gimli','gl-in','d-in-ii-p-de-ferro','Frodo','Sam','hamfast-gamgee','isildur','Aragorn','celebr-an','thingol','l-thien-tin-viel','dior-eluch-l','f-anor','finarfin']:
    print(pname[k],'→',rel(k))
