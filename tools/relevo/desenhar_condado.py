import numpy as np, cv2, json, math
from PIL import Image
rng=np.random.default_rng(42)
X0,Y0,X1,Y1=184.0,244.0,268.0,290.0          # retângulo do Condado (unidades do mapa)
PX=24                                          # pixels por unidade na textura
TW,TH=int((X1-X0)*PX),int((Y1-Y0)*PX)          # 2016 x 1104
GR=4                                           # vértices por unidade na malha
GW,GH=int((X1-X0)*GR)+1,int((Y1-Y0)*GR)+1      # 337 x 185
ME='/tmp/claude-0/me/'
def tp(x,y): return (int(round((x-X0)*PX)),int(round((y-Y0)*PX)))
def noise(base,octv,seed,w=TW,h=TH):
    r=np.random.default_rng(seed);out=np.zeros((h,w),np.float32);a=1;t=0
    for o in range(octv):
        n=r.standard_normal((int(base*2**o*h/w)+2,base*2**o+2)).astype(np.float32);out+=cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
    return out/t
ux=np.linspace(X0,X1,TW,dtype=np.float32);uy=np.linspace(Y0,Y1,TH,dtype=np.float32);UX,UY=np.meshgrid(ux,uy)
def gauss(cx,cy,s,X=UX,Y=UY): return np.exp(-((X-cx)**2+(Y-cy)**2)/(2*s*s))
# ---------- água (mesma do mapa-base, ampliada) ----------
wbase=np.load(ME+'water.npy')
crop=wbase[int(Y0*2)-2:int(Y1*2)+2,int(X0*2)-2:int(X1*2)+2]
up=cv2.resize(crop,(TW+4*PX//2*2,TH+4*PX//2*2),interpolation=cv2.INTER_CUBIC)[PX:PX+TH,PX:PX+TW]
water=np.clip((up-0.45)/0.08,0,1)
for cx,cy,r in [(221.6,261.6,0.75)]: water=np.maximum(water,np.clip((r-np.hypot(UX-cx,UY-cy))*6,0,1))   # lagoa de Beirágua
water=cv2.GaussianBlur(water,(0,0),0.9)
# ---------- relevo ----------
hm=np.asarray(Image.open(ME+'height_hi.png').convert('RGB')).astype(np.float32)
h492=((hm[...,0]*256+hm[...,1])/65535*1.25-0.05)
gx=np.linspace(X0,X1,GW);gy=np.linspace(Y0,Y1,GH);GX,GY=np.meshgrid(gx,gy)
fx=GX/984*491;fy=GY/877*437;i0=np.floor(fx).astype(int);j0=np.floor(fy).astype(int);u=fx-i0;v=fy-j0
hb=(h492[j0,i0]*(1-u)+h492[j0,i0+1]*u)*(1-v)+(h492[j0+1,i0]*(1-u)+h492[j0+1,i0+1]*u)*v      # igual ao motor (bilinear)
def ridge(pts,s,h,X,Y):
    out=np.zeros_like(X)
    for (ax,ay),(bx,by) in zip(pts,pts[1:]):
        dx,dy=bx-ax,by-ay;L=dx*dx+dy*dy;t=np.clip(((X-ax)*dx+(Y-ay)*dy)/L,0,1);d=np.hypot(X-(ax+t*dx),Y-(ay+t*dy));out=np.maximum(out,np.exp(-d*d/(2*s*s))*h)
    return out
def local(X,Y,wat):
    a=gauss(213.5,255.3,1.5,X,Y)*0.030                      # A Colina
    a+=gauss(258.6,270.6,1.1,X,Y)*0.022                      # Colina dos Buques
    a+=ridge([(190,264),(194,268.5),(199,270)],2.0,0.020,X,Y)  # Colinas Brancas
    a+=ridge([(199,279.5),(206,280.5),(212,282.5),(218,284)],2.2,0.026,X,Y)  # Colinas Verdes
    a+=ridge([(212,250.5),(217,251.5)],1.4,0.012,X,Y)          # colinas ao norte
    return a
nz=noise(14,4,3,GW,GH)*0.0035+noise(40,3,4,GW,GH)*0.0012
watg=cv2.resize(water,(GW,GH),interpolation=cv2.INTER_AREA)
fade=np.clip(np.minimum.reduce([GX-X0,X1-GX,GY-Y0,Y1-GY])/3.0,0,1)
wg=cv2.resize(water,(GW,GH),interpolation=cv2.INTER_AREA);dw=cv2.distanceTransform((wg<0.2).astype(np.uint8),cv2.DIST_L2,5);land_w=(dw>10).astype(np.float32)
num=cv2.GaussianBlur((hb*land_w).astype(np.float32),(0,0),9);den=cv2.GaussianBlur(land_w,(0,0),9)+1e-4
hfill=hb*land_w+(num/den)*(1-land_w)
hbs=cv2.GaussianBlur(hfill.astype(np.float32),(0,0),8)
hbm=hbs*fade+hb*(1-fade)
hd=hbm+(local(GX,GY,watg)*0.75+nz*0.6-0.005*cv2.GaussianBlur(watg,(0,0),1.0))*fade
hd=np.maximum(hd,-0.04)
enc=np.clip((hd+0.05)/1.25,0,1)*65535
Image.fromarray(np.dstack([(enc//256).astype(np.uint8),(enc%256).astype(np.uint8),np.zeros((GH,GW),np.uint8)]),'RGB').save('shire_h.png',optimize=True)
HT=cv2.resize(hd.astype(np.float32),(TW,TH),interpolation=cv2.INTER_CUBIC)     # altura na resolução da textura
# ---------- lugares (unidades do mapa) ----------
PL={'Bolsao':(213.6,254.9),'VilaHobbits':(214.6,257.2),'ArvoreFesta':(211.2,257.3),'Moinho':(217.3,259.6),'Beiragua':(222.6,262.4),'DragaoVerde':(224.2,263.1),
    'PedraTresQuartas':(216.8,264.6),'GraCava':(196.2,267.6),'Tuqueburgo':(206.2,278.3),'GrandesSmials':(205.0,277.4),'PontaBosque':(233.5,271.5),'Pantano':(245.5,268.4),
    'Magote':(246.2,269.6),'Tronco':(248.3,271.0),'Balsa':(251.0,271.6),'Buqueburgo':(257.6,272.6),'SedeBrandevin':(258.6,270.4),'Criconcavo':(259.8,266.0),
    'PonteBrandevin':(253.8,266.2),'SebeAlta':(262.2,276.0),'PortaoSebe':(262.2,268.6),'TerraBuques':(258.0,279.0)}
# ---------- cores ----------
C=lambda r,g,b: np.array([r,g,b],np.float32)/255
img=np.zeros((TH,TW,3),np.float32)+C(112,146,72)
img*=1+noise(30,4,5)[...,None]*0.08
# florestas
def polym(pts,blur=6):
    m=np.zeros((TH,TW),np.float32);cv2.fillPoly(m,[np.array([tp(x,y) for x,y in pts],np.int32)],1.0);return cv2.GaussianBlur(m,(0,0),blur)
warpx=noise(10,4,8)*20;warpy=noise(10,4,9)*20
def warp(m): mx,my=np.meshgrid(np.arange(TW,dtype=np.float32),np.arange(TH,dtype=np.float32));return cv2.remap(m,mx+warpx,my+warpy,cv2.INTER_LINEAR)
woody=warp(polym([(226,268.6),(232,267.8),(240,268.4),(242,271),(239.5,274.6),(232,275.2),(226.5,273.8)]))
oldf=np.clip((UX-262.9)*2.5+noise(20,3,10)*0.8,0,1)
copse=np.zeros((TH,TW),np.float32)
for cx,cy,r in [(201,258,1.2),(228,256,1.0),(238,281,1.4),(190,276,1.3),(219,285.5,1.0),(244,251,1.2),(208,286,1.1),(196,250,1.0)]: copse=np.maximum(copse,np.clip((r-np.hypot(UX-cx,UY-cy)+noise(30,2,int(cx))*0.5)*3,0,1))
forest=np.clip(np.maximum.reduce([woody,oldf,copse]),0,1)
marsh=warp(polym([(242,266.6),(250.8,266.8),(251,270.2),(247,270.6),(242.5,269.6)],8))
villages=[('VilaHobbits',2.2),('Beiragua',1.6),('GraCava',2.0),('Tuqueburgo',1.7),('Buqueburgo',1.5),('Tronco',1.0),('Criconcavo',0.6),('Bolsao',0.8)]
vill=np.zeros((TH,TW),np.float32)
for k,r in villages:
    x,y=PL[k];vill=np.maximum(vill,np.clip((r-np.hypot(UX-x,UY-y))*1.5,0,1))
# campos: retângulos divididos em quadras irregulares (colcha de retalhos), bordas onduladas
labimg=np.zeros((TH,TW),np.int32);cnt=[0]
def split(x0,y0,x1,y1,depth):
    w,h=x1-x0,y1-y0
    if (w<2.6 and h<2.2) or depth>7 or (depth>2 and rng.random()<0.12):
        cnt[0]+=1;a,b=tp(x0,y0);c,d=tp(x1,y1);labimg[b:d,a:c]=cnt[0];return
    if w/h*rng.uniform(0.7,1.3)>1: t=rng.uniform(0.3,0.7);split(x0,y0,x0+w*t,y1,depth+1);split(x0+w*t,y0,x1,y1,depth+1)
    else: t=rng.uniform(0.3,0.7);split(x0,y0,x1,y0+h*t,depth+1);split(x0,y0+h*t,x1,y1,depth+1)
for by in np.arange(Y0-2,Y1+2,7.0):
    off=rng.uniform(0,6)
    for bx in np.arange(X0-6+off,X1+6,8.0): split(bx,by,bx+8.0,by+7.0,0)
mxx,myy=np.meshgrid(np.arange(TW,dtype=np.float32),np.arange(TH,dtype=np.float32))
lab=cv2.remap(labimg.astype(np.float32),mxx+noise(8,4,21)*30+noise(40,2,22)*5,myy+noise(8,4,23)*30+noise(40,2,24)*5,cv2.INTER_NEAREST).astype(np.int32)
nl=lab.max()+1
PAL=[C(112,150,66),C(100,142,60),C(124,160,74),C(134,166,82),C(118,156,92),C(108,148,70),C(206,182,98),C(218,196,116),C(190,170,92),C(150,124,84),C(132,168,84)]
W8=np.array([10,10,9,8,6,8,6,5,5,4,6],np.float64);W8/=W8.sum()
kind=rng.choice(len(PAL),nl,p=W8);ang=rng.uniform(0,np.pi,nl)
fc=np.array(PAL)[kind[lab]]*rng.uniform(0.93,1.07,nl)[lab][...,None]
a=ang[lab];stripe=np.sin((UX*np.cos(a)+UY*np.sin(a))*PX/1.8)
crop=np.isin(kind[lab],[6,7,8,9])
fc=fc*(1+np.where(crop,stripe*0.035,0)[...,None])*0.9
meadow=(kind[lab]==10)
flm=(rng.random((TH,TW))<0.03)&meadow
edge=((lab!=np.roll(lab,1,0))|(lab!=np.roll(lab,1,1))).astype(np.float32)
keep=rng.random(nl)<0.75
edge*=keep[lab]
edge=cv2.dilate(edge,np.ones((2,2),np.uint8))
fieldmask=np.clip(1-np.maximum.reduce([forest,water*1.5,vill*0.9,marsh]),0,1)
img=img*(1-fieldmask[...,None]*0.85)+fc*fieldmask[...,None]*0.85
hedgec=C(58,92,42)
img=img*(1-(edge*fieldmask)[...,None]*0.6)+hedgec*(edge*fieldmask)[...,None]*0.6
fl2=(flm*fieldmask>0.5)
img[fl2]=np.array([C(230,200,60),C(220,90,80),C(240,240,240)])[rng.integers(0,3,fl2.sum())]
# pântano
mtex=np.clip(noise(70,3,12)*1.4,0,1)
img=img*(1-marsh[...,None]*0.8)+(C(108,122,70)*(1-mtex[...,None])+C(84,112,84)*mtex[...,None])*marsh[...,None]*0.8
# florestas (copa)
can=np.clip(noise(120,3,13)*0.6+0.5,0,1)[...,None]
fcol=C(44,82,40)*(0.75+0.5*can)
fcol_old=C(30,58,30)*(0.7+0.5*can)
img=img*(1-forest[...,None])+np.where((oldf>0.5)[...,None],fcol_old,fcol)*forest[...,None]
# vilas: grama pisada e hortas
vt=np.clip(noise(90,2,14)*0.8+0.5,0,1)[...,None]
img=img*(1-vill[...,None]*0.55)+(C(132,150,82)*(1-vt*0.4)+C(150,120,80)*vt*0.4)*vill[...,None]*0.55
# estradas
def road(pts,w,col,edge_col):
    global img
    m=np.zeros((TH,TW),np.float32);cv2.polylines(m,[np.array([tp(x,y) for x,y in pts],np.int32)],False,1.0,int(w*PX)+2,cv2.LINE_AA);m=cv2.GaussianBlur(m,(0,0),1.0)
    e=cv2.dilate(m,np.ones((5,5),np.uint8))-m
    img=img*(1-e[...,None]*0.5)+edge_col*e[...,None]*0.5
    img=img*(1-m[...,None])+col*(1+noise(200,2,15)[...,None]*0.08)*m[...,None]
    return m
ROAD_E=[(184,266.6),(190,267.2),(196.2,267.8),(201,266.6),(205.4,265.6),(210,265.0),(214.5,264.7),(219,264.0),(222.6,263.5),(227,263.4),(232,263.6),(237,264.2),(241,264.9),(246,265.6),(250.3,266.1)]
ROAD_E2=[(257.2,266.4),(261,266.1),(264,265.8),(268,265.4)]
road(ROAD_E,0.42,C(186,160,112),C(120,104,72))
road(ROAD_E2,0.42,C(186,160,112),C(120,104,72))
LANES=[[(213.6,255.3),(214.0,256.6),(215.4,258.1),(217.1,259.4),(218.4,260.9),(220.6,262.3),(222.6,262.8),(222.8,263.5)],
 [(222.6,262.6),(221.4,259.0),(219.0,255.8),(216.0,252.8),(213.4,251.4)],
 [(205.4,265.6),(205.6,269.8),(206.0,274.5),(206.2,278.0)],
 [(196.2,267.8),(199.2,272.4),(202.4,276.0),(205.0,277.4)],
 [(241,264.9),(243.6,267.6),(246.2,269.6),(248.3,271.0),(250.9,271.6)],
 [(232,263.6),(232.6,267.0),(233.5,271.0)],
 [(257.2,266.5),(259.6,266.1)],
 [(257.4,266.6),(256.9,268.6),(257.6,270.6),(257.6,272.6),(257.8,276.0),(257.4,281.0),(256.6,288.0)],
 [(255.6,271.7),(257.6,272.4)],
 [(214.6,257.2),(211.4,257.3)],
 [(196.2,267.8),(193.0,262.0),(190.0,256.0)],
 [(222.8,263.5),(226,268.0),(228.6,272.6)]]
for L in LANES: road(L,0.2,C(172,150,104),C(122,108,76))
# hortas e jardins perto das casas (preenchidas depois de saber as casas)
# água por cima
ripple=noise(260,2,16)[...,None]*0.05
wcol=C(66,116,138)*(1+ripple)
bank=np.clip(cv2.dilate(water,np.ones((7,7),np.uint8))-water,0,1)
img=img*(1-bank[...,None]*0.35)+C(110,118,74)*bank[...,None]*0.35
img=img*(1-water[...,None])+wcol*water[...,None]
# ---------- casas, tocas e outros modelos ----------
MOD=[];SUB=[];TREES=[]
def onwater(x,y): px,py=tp(x,y);return 0<=px<TW and 0<=py<TH and water[min(TH-1,py),min(TW-1,px)]>0.2
def smial(x,y,r,face,door):MOD.append(['smial',round(x,2),round(y,2),max(r,0.4),round(face,2),door])
def house(x,y,w,d,rot,wall,roof,h=0.32):MOD.append(['house',round(x,2),round(y,2),w,d,round(rot,2),wall,roof,h])
DOORS=['#2f7a3a','#c9a227','#8a2f2f','#2f4f8a','#5a3a1e','#d0d0c0']
WALLS=['#e8dcc0','#dccfae','#efe6cf','#d8c49c'];ROOFS=['#9a7a3c','#8a6a34','#a88a4a','#6e5a3a']
gardens=np.zeros((TH,TW),np.float32)
def garden(x,y,r):
    global gardens
    px,py=tp(x,y);cv2.circle(gardens,(px,py),int(r*PX),1.0,-1)
def hillface(x,y,cx,cy): return math.atan2(y-cy,x-cx)
# Bolsão no alto da Colina, voltado para o sul
MOD.append(['smial',213.6,254.95,0.8,math.pi/2,'#2f7a3a']);garden(213.6,255.6,0.6)
# Vila dos Hobbits: tocas nas encostas da Colina + Fileira do Bolsinho (Bagshot Row)
cx,cy=213.5,255.3;placed=[(213.6,254.95)]
for k in range(60):
    if len(placed)>11:break
    a=rng.uniform(0.1*math.pi,1.1*math.pi);rr=rng.uniform(1.2,2.6);x=cx+math.cos(a)*rr*1.1;y=cy+math.sin(a)*rr*0.9
    if onwater(x,y) or any(math.hypot(x-px,y-py)<1.05 for px,py in placed) or math.hypot(x-211.2,y-257.3)<1.2:continue
    placed.append((x,y))
    smial(x,y,round(rng.uniform(0.4,0.5),2),a,DOORS[k%len(DOORS)]);garden(x+math.cos(a)*0.45,y+math.sin(a)*0.45,0.3)
for k in range(3): smial(212.6+k*1.0,256.7,0.42,math.pi/2,DOORS[(k+2)%6])
for k,(x,y) in enumerate([(215.8,258.0),(216.4,257.3),(212.4,258.4),(218.2,258.6),(216.0,259.0)]):
    house(x,y,0.30,0.22,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4]);garden(x,y+0.35,0.3)
# Moinho e ponte sobre O Água
MOD.append(['mill',217.3,259.55,0.0]);MOD.append(['bridge',218.2,260.3,218.75,261.45,0.28,1,'#9a9488'])
# Beirágua
for k in range(12):
    a=rng.uniform(0,2*math.pi);rr=rng.uniform(0.7,1.6);x,y=222.6+math.cos(a)*rr,262.6+math.sin(a)*rr*0.8
    if onwater(x,y) or abs(y-263.5)<0.3:continue
    if k%3==0: smial(x,y,0.3,a,DOORS[k%6])
    else: house(x,y,0.30,0.22,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4])
    garden(x,y+0.3,0.28)
MOD.append(['inn',224.2,263.05,0.08])               # Dragão Verde
MOD.append(['tree_big',211.2,257.3,1.0])             # Árvore da Festa
MOD.append(['stone',216.8,264.45])                   # Pedra das Três Quartas
# Grã Cava (Colinas Brancas) com a Casa dos Mathoms
for k in range(14):
    a=rng.uniform(0,2*math.pi);rr=rng.uniform(0.5,1.9);x,y=196.2+math.cos(a)*rr,267.6+math.sin(a)*rr*0.8
    if abs(y-267.8)<0.35:continue
    if k%2: smial(x,y,0.32,a,DOORS[k%6])
    else: house(x,y,0.30,0.22,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4])
MOD.append(['house',196.6,268.4,0.55,0.32,0.1,'#d8c8a0','#7a5a30',0.45])   # Casa dos Mathoms
# Tuqueburgo e Grandes Smials
MOD.append(['bigsmial',205.0,277.35,1.05,-math.pi/2+0.2,9])
for k in range(8):
    a=rng.uniform(0,2*math.pi);rr=rng.uniform(1.4,2.2);x,y=206.2+math.cos(a)*rr,278.3+math.sin(a)*rr*0.8
    smial(x,y,0.3,a,DOORS[k%6]) if k%2 else house(x,y,0.28,0.2,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4])
# Fazenda do Magote, Tronco
house(246.2,269.6,0.4,0.26,0.3,'#d8c49c','#8a6a34',0.38);house(246.8,269.2,0.3,0.2,1.8,'#cdb890','#7a5a30',0.3)
for k in range(5): MOD.append(['hay',245.4+k*0.35,270.2+(k%2)*0.25])
for k,(x,y) in enumerate([(248.3,271.0),(248.9,270.6),(247.8,271.4),(248.6,271.6)]): house(x,y,0.28,0.2,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4])
# Ponte do Brandevin (pedra, vários arcos)
MOD.append(['bridge',250.2,266.15,257.3,266.45,0.42,5,'#a8a090'])
# Balsa de Buqueburgo
MOD.append(['ferry',252.9,271.6,0.0])
MOD.append(['jetty',251.3,271.6,0.0]);MOD.append(['jetty',255.4,271.7,math.pi])
# Terra dos Buques: Sede do Brandevin, Buqueburgo, Cricôncavo, Sebe Alta
MOD.append(['bigsmial',258.6,270.45,1.1,math.pi,12])
for k in range(10):
    x,y=257.0+rng.uniform(-0.6,1.6),272.0+rng.uniform(0,1.8)
    smial(x,y,0.3,math.pi,DOORS[k%6]) if k%3==0 else house(x,y,0.28,0.2,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4])
house(259.8,266.0,0.34,0.24,0.2,'#e2d6b6','#5e4a2e',0.3)                 # Cricôncavo
MOD.append(['fence',[[259.3,265.6],[260.4,265.6],[260.4,266.5],[259.3,266.5],[259.3,265.6]]])
MOD.append(['hedge',[[262.0,267.4],[262.1,270],[262.3,274],[262.1,278],[262.4,282],[262.2,286],[262.4,290]],0.3])
MOD.append(['gate',262.15,268.6])
# casas espalhadas pelo campo
for k in range(46):
    x,y=rng.uniform(X0+2,X1-8),rng.uniform(Y0+2,Y1-2)
    px,py=tp(x,y)
    if forest[py,px]>0.3 or water[py,px]>0.1 or marsh[py,px]>0.3 or vill[py,px]>0.2: continue
    if k%3==0: smial(x,y,0.3,rng.uniform(0,6.28),DOORS[k%6])
    else: house(x,y,0.28,0.2,rng.uniform(0,3.1),WALLS[k%4],ROOFS[k%4])
    garden(x,y+0.3,0.26)
    for j in range(rng.integers(0,3)): MOD.append(['hay',x+rng.uniform(-0.8,0.8),y+rng.uniform(-0.8,0.8)])
# ovelhas nos pastos
for k in range(70):
    x,y=rng.uniform(X0+2,X1-8),rng.uniform(Y0+2,Y1-2);px,py=tp(x,y)
    if fieldmask[py,px]>0.8 and kind[lab[py,px]] in (0,1,2,8): MOD.append(['sheep',round(x,2),round(y,2),round(rng.uniform(0,6.28),2)])
# hortas
gardens=cv2.GaussianBlur(gardens,(0,0),1.5)*(1-water)
gt=(np.sin(UX*PX/1.6)>0).astype(np.float32)[...,None]
gcol=C(112,104,64)*(1-gt)+C(100,146,62)*gt
flw=(rng.random((TH,TW))<0.02).astype(np.float32)*gardens
img=img*(1-gardens[...,None]*0.45)+gcol*gardens[...,None]*0.45
fl_col=np.array([C(220,60,60),C(240,210,60),C(160,90,200),C(250,250,250)])[rng.integers(0,4,(TH,TW))]
img=img*(1-flw[...,None])+fl_col*flw[...,None]
# ---------- árvores ----------
def tree(x,y,s,t,c): TREES.append([round(x,2),round(y,2),round(s,2),t,round(c[0],2),round(c[1],2),round(c[2],2)])
def mask_at(m,x,y): px,py=tp(x,y);return m[min(TH-1,max(0,py)),min(TW-1,max(0,px))]
for _ in range(9000):                                    # florestas
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    f=mask_at(forest,x,y)
    if f>0.5 and rng.random()<0.55 and mask_at(water,x,y)<0.02:
        old=mask_at(oldf,x,y)>0.5;g=rng.uniform(0.75,1.1)
        tree(x,y,rng.uniform(0.7,1.05)*(1.15 if old else 1.0),0 if (old and rng.random()<0.5) else 1,C(40,80,36)*g if not old else C(30,62,32)*g)
px_=0;VILL=[PL[k] for k,_ in villages]
ys,xs=np.where((edge*fieldmask)>0.6)
pick=rng.choice(len(xs),size=min(2200,len(xs)),replace=False)
for i in pick:                                          # árvores das sebes
    if rng.random()<0.2:
        x,y=X0+xs[i]/PX,Y0+ys[i]/PX
        if min(abs(x-px_),0)==0 and all(math.hypot(x-vx,y-vy)>1.2 for vx,vy in VILL): tree(x,y,rng.uniform(0.45,0.7),1,C(60,104,44)*rng.uniform(0.8,1.15))
ys,xs=np.where(bank>0.4)                                 # salgueiros na margem
pick=rng.choice(len(xs),size=min(700,len(xs)),replace=False)
for i in pick:
    x,y=X0+xs[i]/PX,Y0+ys[i]/PX
    if rng.random()<0.4 and mask_at(water,x,y)<0.02: tree(x,y,rng.uniform(0.6,0.9),2,C(118,150,76))
for ox,oy in [(216.6,256.2),(220.0,263.4),(197.6,266.2),(207.5,276.6),(256.2,273.6),(225.0,262.0)]:   # pomares
    for i in range(4):
        for j in range(3): tree(ox+i*0.38,oy+j*0.38,0.5,1,C(84,128,52))
# ---------- sombreamento igual ao do motor ----------
HS=46*1.35;hf=cv2.GaussianBlur(HT,(0,0),7)*HS
gy_,gx_=np.gradient(hf,1/PX,1/PX)
Lv=np.array([-0.62,-0.55,0.56]);Lv/=np.linalg.norm(Lv)
n=np.dstack([-gx_,-gy_,np.ones_like(hf)]);n/=np.linalg.norm(n,axis=2,keepdims=True)
lam=np.clip(n@Lv,0,1);flatL=float(Lv[2])
light=(0.55+0.62*(lam-flatL)+0.45*flatL)
ao=np.clip(1-(cv2.GaussianBlur(hf,(0,0),24)-hf)*0.12,0.75,1)
Lt=light*ao
canopy_shadow=cv2.GaussianBlur(forest,(0,0),10)
Lt*=1-0.15*canopy_shadow
cool=np.array([0.55,0.62,0.82]);warm=np.array([1.10,1.02,0.88])
mixw=np.clip(Lt,0,1.2)[...,None]/1.2
fin=img*(cool*(1-mixw)+warm*mixw)*Lt[...,None]
# ---------- emenda com o mapa-base na borda ----------
tex=np.asarray(Image.open(ME+'me_tex.webp').convert('RGB')).astype(np.float32)/255
lm=np.asarray(Image.open(ME+'light_hi.png').convert('RGB')).astype(np.float32)/255
def crop_up(a,scale):
    x0,y0,x1,y1=int(X0*scale),int(Y0*scale),int(X1*scale),int(Y1*scale)
    return cv2.resize(a[y0:y1,x0:x1],(TW,TH),interpolation=cv2.INTER_CUBIC)
bt=crop_up(tex,2);bl=crop_up(lm,1)
Lb=bl[...,0]*1.3;mb=np.clip(Lb,0,1.2)[...,None]/1.2
base=bt*(cool*(1-mb)+warm*mb)*Lb[...,None]
wcb=bl[...,2][...,None]*0.8;sky=np.array([0.62,0.70,0.76])
base=base*(1-wcb)+(bt*0.55*0.55+sky*0.85*0.45)*wcb
bw=np.clip((np.minimum.reduce([UX-X0,X1-UX,UY-Y0,Y1-UY])-0.5)/7.0,0,1)[...,None]**1.5
out=np.clip(fin*bw+base*(1-bw),0,1)
cv2.imwrite('shire_tex.webp',cv2.cvtColor((out*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,88])
Image.fromarray((out*255).astype(np.uint8)).resize((TW//2,TH//2)).save('prev.png')
def _c(o):
    if isinstance(o,(list,tuple)): return [_c(v) for v in o]
    if isinstance(o,(np.floating,)): return round(float(o),3)
    if isinstance(o,(np.integer,)): return int(o)
    if isinstance(o,float): return round(o,3)
    return o
MOD=_c(MOD);TREES=_c(TREES)
json.dump({'rect':[X0,Y0,X1,Y1],'models':MOD,'trees':TREES,'places':{k:[round(x,2),round(y,2)] for k,(x,y) in PL.items()}},open('shire.json','w'),separators=(',',':'))
import os;print('modelos',len(MOD),'árvores',len(TREES),{f:os.path.getsize(f) for f in ['shire_tex.webp','shire_h.png','shire.json']})
