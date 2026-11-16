import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('fornost',250,164,282,196,PX=40,GR=5,seed=181,out='/tmp/claude-0/b5')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
F=(265.7,179.8)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.012*nz
hd=R.soften(hd,0.7,6)
d=np.hypot(GX-F[0],GY-F[1])
z0=float(hd[int((F[1]-R.Y0)*5),int((F[0]-R.X0)*5)])
hd=np.where(d<1.3,z0,np.where(d<2.4,z0+(hd-z0)*sstep(1.3,2.4,d),hd))
hd=hd-0.008*np.exp(-((d-1.55)/0.1)**2)                   # o Fosso dos Mortos
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(122,134,80)*(1-np.clip(n1+0.5,0,1))+C(100,112,68)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
img=R.paint(img,np.clip(sstep(1.2,2.6,R.slope),0,1),C(124,120,108),0.6)
dT=np.hypot(UX-F[0],UY-F[1])
img=R.paint(img,(1-sstep(1.2,1.45,dT))*np.clip(R.noise(60,3,12)+0.6,0,1),C(140,136,120),0.6)
img=R.paint(img,np.exp(-((dT-1.55)/0.07)**2),C(60,62,48),0.7)
ROAD=[(262.0,R.Y1+1),(262.6,190.0),(263.8,185.0),(265.0,182.4),(F[0]-0.1,F[1]+1.3)]
img,roadm=R.road(img,ROAD,0.14,C(140,146,96),C(90,92,66))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD;zc=gz(*F)
ST=['#a8a498','#989488','#b4b0a2']
# muralha em ruínas: trechos de alturas diferentes, com falhas
for k in range(44):
    a=k/44*6.28;da=6.28/44
    if R.rng.random()<0.3: continue
    x,y=F[0]+math.cos(a+da/2)*1.25,F[1]+math.sin(a+da/2)*1.25
    M.append(['boxA',x,y,1.25*da/2+0.01,0.06,zc-0.3,zc+R.rng.uniform(0.08,0.5),a+da/2+1.571,ST[k%3],ST[(k+1)%3]])
# torres quebradas e a cidadela
for k in range(7):
    a=k/7*6.28+0.2;x,y=F[0]+math.cos(a)*1.25,F[1]+math.sin(a)*1.25;h=R.rng.uniform(0.4,1.1)
    M.append(['cylA',x,y,zc-0.3,zc+h,0.11,0.1,7,ST[k%3]])
M.append(['boxA',F[0],F[1]-0.2,0.3,0.24,zc-0.1,zc+0.45,0.2,ST[0],None])
M.append(['cylA',F[0]+0.1,F[1]-0.25,zc+0.3,zc+1.5,0.16,0.14,8,ST[1]])
M.append(['boxA',F[0]-0.25,F[1]-0.3,0.05,0.2,zc+0.45,zc+0.9,0.2,ST[2],None])
# restos de casas e colunas caídas
for q in range(70):
    a=R.rng.uniform(0,6.28);rr=R.rng.uniform(0.3,1.1);x,y=F[0]+math.cos(a)*rr,F[1]+math.sin(a)*rr
    if R.rng.random()<0.5: M.append(['boxA',x,y,R.rng.uniform(0.05,0.12),0.02,zc-0.05,zc+R.rng.uniform(0.05,0.25),R.rng.uniform(0,3.1),ST[q%3],None])
    else: M.append(['cylA',x,y,zc-0.05,zc+R.rng.uniform(0.08,0.35),0.025,0.022,6,ST[q%3]])
# campo de batalha a oeste: montes funerários
BAT=(259.0,181.0)
for k in range(6):
    x,y=BAT[0]+R.rng.uniform(-1.2,1.2),BAT[1]+R.rng.uniform(-1,1);M.append(['blobA',x,y,gz(x,y)-0.03,[[0.22,0],[0.18,0.07],[0.08,0.12],[0,0.14]],9,'#6a8a48'])
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if math.hypot(x-F[0],y-F[1])<1.8 or R.at(roadm,x,y)>0.05: continue
    if R.rng.random()<0.012: R.tree(x,y,R.rng.uniform(0.45,0.75),1 if R.rng.random()<0.5 else 0,C(60,90,48)*R.rng.uniform(0.85,1.1))
R.TOPS=[[F[0],F[1],1.8,0.5]]
R.PL={'RuinasFornost':F,'FossoMortos':(F[0]+1.55,F[1]),'CaminhoVerdeNorte':(263.2,187.5),'ColinasNorte':(270.0,172.0),'BatalhaFornost':BAT}
R.save_json()
