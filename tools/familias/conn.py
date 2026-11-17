import json,re
INDEX='/home/claude/atlas-terra-media/index.html'
D=json.load(open('/tmp/claude-0/fam/family.json'));people={p['key']:p for p in json.load(open('/tmp/claude-0/people.json'))}
N=D['n'];rel={}
def link(a,b):
    ka,kb=N[a][3],N[b][3]
    if ka and kb and ka!=kb: rel.setdefault(ka,[]).append(kb);rel.setdefault(kb,[]).append(ka)
for c,p in D['p']: link(c,p)
for a,b in D['s']: link(a,b)
for a,b in D['b']: link(a,b)
s=open(INDEX,encoding='utf-8').read();n=0;added=0
for key,lst in rel.items():
    a='{"key":'+json.dumps(key,ensure_ascii=False)+',"name"'
    if s.count(a)!=1: continue
    i=s.index(a);nxt=s.find('{"key":"',i+10)
    m=re.compile(r'"connections":"((?:[^"\\]|\\.)*)"').search(s,i);r=re.compile(r'"resolved_connection_keys":(\[[^\]]*\])').search(s,i)
    if not m or not r or (nxt>0 and r.start()>nxt): continue
    have=json.loads(r.group(1));new=[k for k in dict.fromkeys(lst) if k not in have]
    if not new: continue
    names=[people[k]['name'] for k in new]
    txt=json.loads('"'+m.group(1)+'"');txt=(txt+', ' if txt and txt!='A catalogar' else '')+', '.join(names)
    s=s[:r.start()]+'"resolved_connection_keys":'+json.dumps(have+new,ensure_ascii=False)+s[r.end():]
    m=re.compile(r'"connections":"((?:[^"\\]|\\.)*)"').search(s,i)
    s=s[:m.start()]+'"connections":'+json.dumps(txt,ensure_ascii=False)+s[m.end():];n+=1;added+=len(new)
open(INDEX,'w',encoding='utf-8').write(s);print('fichas com parentes acrescentados',n,'ligações novas',added)
