import csv,json,re,unicodedata,collections
AM='/home/claude/kwoxer/arda-maps/database/';GED='/home/claude/robsis/middle-earth-genealogy-project/arda.ged'
def norm(t): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFD',t).encode('ascii','ignore').decode().lower()).strip()
def rd(f): return list(csv.DictReader(open(AM+f,encoding='utf-8'),delimiter=';'))
C={r['uniquename']:r for r in rd('Creature.csv')}
P=collections.defaultdict(lambda:{'par':set(),'chi':set(),'spo':set(),'sib':set()})
for r in rd('BEGETS.csv'):
    a,b=r['momdad'],r['sondau']
    if a in C and b in C: P[b]['par'].add(a);P[a]['chi'].add(b)
for r in rd('LOVES.csv'):
    a,b=r['person1'],r['person2']
    if a in C and b in C: P[a]['spo'].add(b);P[b]['spo'].add(a)
for r in rd('HASSIBLING.csv'):
    a,b=r['person1'],r['person2']
    if a in C and b in C: P[a]['sib'].add(b);P[b]['sib'].add(a)
# GEDCOM
ind={};fam={};cur=None
for line in open(GED,encoding='utf-8'):
    p=line.rstrip('\n').split(' ',2)
    if p[0]=='0':
        cur=None
        if len(p)>2 and p[2]=='INDI': cur=ind.setdefault(p[1],{'names':[],'sex':'','famc':[],'fams':[],'nati':''});kind='I'
        elif len(p)>2 and p[2]=='FAM': cur=fam.setdefault(p[1],{'h':[],'w':[],'c':[]});kind='F'
        continue
    if cur is None or p[0]!='1': continue
    tag=p[1];val=p[2] if len(p)>2 else ''
    if kind=='I':
        if tag=='NAME': cur['names'].append(val.replace('/','').strip())
        elif tag=='SEX': cur['sex']=val
        elif tag=='FAMC': cur['famc'].append(val)
        elif tag=='FAMS': cur['fams'].append(val)
        elif tag=='NATI': cur['nati']=val
    else:
        if tag=='HUSB': cur['h'].append(val)
        elif tag=='WIFE': cur['w'].append(val)
        elif tag=='CHIL': cur['c'].append(val)
G=collections.defaultdict(lambda:{'par':set(),'chi':set(),'spo':set(),'sib':set()})
for fid,f in fam.items():
    pa=[x for x in f['h']+f['w'] if x in ind];ch=[x for x in f['c'] if x in ind]
    for a in pa:
        for b in pa:
            if a!=b: G[a]['spo'].add(b)
        for c in ch: G[c]['par'].add(a);G[a]['chi'].add(c)
    for c in ch:
        for d in ch:
            if c!=d: G[c]['sib'].add(d)
print('arda-maps pessoas',len(C),'com relação',len(P),'| gedcom',len(ind),'famílias',len(fam))
# junta: identidade por nome normalizado (nome principal ou alternativo)
AMn={}
for k,r in C.items():
    for n in [r['name']]+[x for x in re.split(r'[,;/]',r['altname']) if x.strip()]: AMn.setdefault(norm(n),k)
Gn={}
for k,r in ind.items():
    for n in r['names']: Gn.setdefault(norm(n),k)
json.dump({'C':C,'P':{k:{a:sorted(b) for a,b in v.items()} for k,v in P.items()},'ind':ind,'G':{k:{a:sorted(b) for a,b in v.items()} for k,v in G.items()},'AMn':AMn,'Gn':Gn},open('/tmp/claude-0/fam/src.json','w'),ensure_ascii=False)
print(list(C.items())[100][1])
print([ind[k]['names'] for k in list(ind)[:8]])
