exec(open('/tmp/claude-0/jor/warp.py').read())
MES={'jan':'janeiro','fev':'fevereiro','mar':'março','abr':'abril','mai':'maio','jun':'junho','jul':'julho','ago':'agosto','set':'setembro','out':'outubro','nov':'novembro','dez':'dezembro'}
def cal(year_months,extra):
    L=[]
    for y,m,d0,d1 in year_months:
        for d in range(d0,d1+1):L.append((f'{d} {m}',f'{d} de {MES[m]} de {y}'))
        if (y,m) in extra:L+=extra[(y,m)]
    return L
GUERRA=cal([(3018,'set',23,30),(3018,'out',1,30),(3018,'nov',1,30),(3018,'dez',1,30),(3019,'jan',1,30),(3019,'fev',1,30),(3019,'mar',1,25)],
  {(3018,'dez'):[('1 yule','1º Yule (fim de 3018)')],(3019,'jan'):[]})
# o 2º Yule abre o ano novo, antes de 1º de janeiro
k=[i for i,(a,b) in enumerate(GUERRA) if a=='1 jan'][0];GUERRA.insert(k,('2 yule','2º Yule (início de 3019)'))
HOBBIT=cal([(2941,'abr',26,30),(2941,'mai',1,30),(2941,'jun',1,30),(2941,'jul',1,30),(2941,'ago',1,30),(2941,'set',1,30),(2941,'out',1,30),(2941,'nov',1,30)],
  {(2941,'jun'):[('1 lithe','1º Lithe de 2941'),('meio','Meio-do-Ano de 2941 (solstício)'),('2 lithe','2º Lithe de 2941')]})
def loc(l):
    if isinstance(l,int):return W(WP[l])
    if isinstance(l,str) and l.startswith('A:'):return W(A[l[2:]])
    if isinstance(l,str):return list(P[l])
    return list(l)
def track(CAL,pts):
    idx={a:i for i,(a,b) in enumerate(CAL)};o=[]
    for p in pts:
        d,l=p[0],p[1];lab=p[2] if len(p)>2 else None
        x,y=loc(l);o.append([idx[d],round(x,1),round(y,1)]+([lab] if lab else []))
    for a,b in zip(o,o[1:]):assert a[0]<=b[0],(a,b)
    return o
