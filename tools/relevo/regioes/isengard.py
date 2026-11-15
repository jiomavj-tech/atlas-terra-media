import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('isengard',410,466,446,502,PX=40,GR=5,seed=31,out='/tmp/claude-0/ro')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
RC=(427.6,481.2);RR=1.75
RIVER=[(428.6,466.0),(428.2,468.5),(427.0,471.5),(425.7,475.0),(424.8,478.3),(424.5,481.5),(424.4,484.8),(424.9,488.0),(424.2,491.8),(423.5,495.5),(423.6,498.6),(423.5,500.5),(423.8,503.5)]
FORD=(423.6,498.6)
RP,RS=dense(RIVER);RT=cKDTree(RP)
def rinfo(X,Y):
    d,i=RT.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape),RS[i].reshape(X.shape)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3);hbs=np.where(hbs>0.30,0.30+(hbs-0.30)*0.45,hbs)
nz=R.noise(8,5,3,True)
hd=hbs+0.02*nz
# braços de montanha em volta do anel (N, O, L) e o Methedras ao norte
ang=np.arctan2(GY-RC[1],GX-RC[0]);rr=np.hypot(GX-RC[0],GY-RC[1])
arm=0.16*np.exp(-((rr-6.0)/2.6)**2)*sstep(0.6,-0.4,np.sin(ang))   # aberto para o sul
hd=hd+arm*(0.8+0.3*nz)
hd=hd+0.12*gauss(429.0,467.0,3.6,GX,GY)*(0.85+0.3*nz)
# vale do Isen (Nan Curunír)
dr,sr=rinfo(GX,GY)
fl=0.30-0.10*sstep(0,14,sr)-0.03*sstep(14,34,sr)
wf=0.6+2.2*sstep(8,20,sr)+0.5*nz+3.2*np.exp(-((GX-RC[0])**2+(GY-RC[1])**2)/(2*2.6**2))
wall=wf+3.5+2.5*sstep(14,30,sr)
fl=cv2.GaussianBlur(fl.astype(np.float32),(0,0),4);wf=cv2.GaussianBlur(wf.astype(np.float32),(0,0),4);wall=np.maximum(cv2.GaussianBlur(wall.astype(np.float32),(0,0),4),wf+0.8)
prof=fl+(hd-fl)*sstep(wf,wall,dr)
hd=np.where(dr<wall,np.minimum(hd,prof),hd)
hd=R.soften(hd,0.5,7)
# planície do anel
HC=float(hd[int((RC[1]-466)*5),int((RC[0]-410)*5)])+0.005;print('HC',HC)
pl=1-sstep(RR+0.15,RR+1.4,rr)
hd=hd*(1-pl)+HC*pl
hd=np.where(rr<RR+0.15,HC+0.002*nz,hd)
# rocha de Orthanc
hd=np.where(rr<0.6,np.maximum(hd,HC+0.012*gauss(*RC,0.25,GX,GY)),hd)
hd=hd-0.01*sstep(0.35,0.0,dr)
R.set_height(hd)
gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(160,3,6)[...,None]
grass=C(118,128,78)*(1-np.clip(n1+0.5,0,1))+C(96,108,66)*np.clip(n1+0.5,0,1)
bt=R.base_tex(10)*1.12
img+=(grass*0.5+bt*0.5)*(1+n2*0.08)
DR,SR=rinfo(UX,UY);RRt=np.hypot(UX-RC[0],UY-RC[1]);ANG=np.arctan2(UY-RC[1],UX-RC[0])
# terra devastada em volta do anel (árvores cortadas)
waste=1-sstep(RR+1.0,RR+4.5,RRt)
img=R.paint(img,waste,C(110,98,78),0.75)
rock=C(118,114,108)*(1+R.noise(80,4,8)[...,None]*0.14)
rk=np.clip(sstep(1.6,3.0,R.slope)+sstep(0.42,0.5,R.HT),0,1)
img=R.paint(img,rk,rock,0.85)
snow=sstep(0.52,0.6,R.HT+0.03*R.noise(50,3,9))
img=R.paint(img,snow,C(236,240,246))
# chão do anel: pedra escura, estradas de pedra radiais
fl_in=1-sstep(RR-0.05,RR+0.05,RRt)
pave=C(88,86,84)*(1+R.noise(200,3,11)[...,None]*0.1)
img=R.paint(img,fl_in,pave)
spokes=[i*math.pi/4+math.pi/2 for i in range(8)]
for a in spokes:
    img,_=R.road(img,[(RC[0]+0.3*math.cos(a),RC[1]+0.3*math.sin(a)),(RC[0]+(RR-0.1)*math.cos(a),RC[1]+(RR-0.1)*math.sin(a))],0.07,C(140,136,128),C(60,58,56))
img=R.paint(img,1-sstep(0.3,0.42,RRt),C(70,68,68))
# metade norte inundada pelos Ents
flood=fl_in*sstep(0.25,-0.35,(UY-RC[1])/RR+0.15*R.noise(6,3,12))
wcol=C(58,92,112)*(1+R.noise(220,2,13)[...,None]*0.05)
img=R.paint(img,flood,wcol,0.92)
# poços de Saruman (metade sul): bocas escuras com brilho
PITS=[]
for q in range(260):
    a=R.rng.uniform(0,2*math.pi);r=R.rng.uniform(0.5,RR-0.2);x,y=RC[0]+math.cos(a)*r,RC[1]+math.sin(a)*r
    if y<RC[1]+0.15+0.2*math.sin(a*3) or any(math.hypot(x-px,y-py)<0.2 for px,py in PITS): continue
    if any(abs(((a-sa+math.pi)%(2*math.pi))-math.pi)<0.08 for sa in spokes): continue
    PITS.append((x,y))
    if len(PITS)>=26: break
pm=np.zeros((R.TH,R.TW),np.float32)
for x,y in PITS: cv2.circle(pm,R.tp(x,y),int(0.07*R.PX),1.0,-1,cv2.LINE_AA)
img=R.paint(img,cv2.GaussianBlur(pm,(0,0),1),C(22,20,20))
# rio Isen, canal dos Ents e a represa
water=np.clip((0.16+0.10*sstep(470,490,UY)-DR)/0.04+0.5,0,1)
water=np.maximum(water,np.clip(R.line_mask([(424.85,478.5),(425.6,479.0),(426.2,479.5)],0.18,1.0)*1.5,0,1))
bank=np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1)
img=R.paint(img,bank,C(100,104,78),0.4)
img=R.paint(img,water,wcol)
# estrada do sul: do portão aos Vaus
GATE=(RC[0],RC[1]+RR)
ROAD=[GATE,(427.2,484.6),(426.4,488.0),(425.6,492.0),(424.6,496.0),FORD,(422.0,500.4),(420.4,503.0)]
img,roadm=R.road(img,ROAD,0.22,C(170,156,124),C(100,92,70))
# Fangorn (leste)
fang=sstep(436.5,440.5,UX+1.5*R.noise(6,3,14)+0.15*(UY-484))*(1-sstep(0.55,0.6,R.HT))
fang=np.clip(fang,0,1)
img=R.paint(img,fang*np.clip(R.noise(60,3,15)*1.2+0.7,0,1),C(40,66,40),0.85)
fin=R.light(img)
# brilho dos poços
glow=cv2.GaussianBlur(pm,(0,0),5)
fin=fin+np.array([0.5,0.18,0.04])*glow[...,None]*0.6
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zc=HC*HSW
DARK='#121214';BLACK=[0.06,0.06,0.07];FIRE=[1.0,0.45,0.08,1.0]
# muralha do anel: segmentos de rocha, com o portão ao sul e uma brecha (os Ents)
N=96
for k in range(N):
    a=k/N*2*math.pi;da=2*math.pi/N
    d_gate=abs(((a-math.pi/2+math.pi)%(2*math.pi))-math.pi)
    if d_gate<0.09: continue
    brk=abs(((a-(-2.55)+math.pi)%(2*math.pi))-math.pi)<0.12
    h=0.25 if brk else 0.95
    x,y=RC[0]+math.cos(a+da/2)*RR,RC[1]+math.sin(a+da/2)*RR
    M.append(['boxA',x,y,RR*da/2+0.02,0.13,zc-0.5,zc+h,a+da/2+math.pi/2,'#4c4a48','#5a5856'])
# portão: arco na rocha, ladeado por torres
for s_ in (-1,1):
    a=math.pi/2+s_*0.12;x,y=RC[0]+math.cos(a)*RR,RC[1]+math.sin(a)*RR
    M.append(['cylA',x,y,zc-0.3,zc+1.25,0.16,0.14,8,'#3c3a3a']);M.append(['cylA',x,y,zc+1.25,zc+1.45,0.17,0.0,8,'#2a2828'])
M.append(['boxA',GATE[0],GATE[1],0.2,0.14,zc+0.55,zc+0.95,0,'#3c3a3a','#3c3a3a'])
# portões arrebentados no chão
for s_ in (-1,1): M.append(['boxA',GATE[0]+s_*0.25,GATE[1]+0.35,0.1,0.02,zc-0.02,zc+0.03,0.4*s_,'#2a2a2c',None])
# Orthanc: quatro pilares de muitas faces unidos, abrindo-se em chifres no alto
OH=4.2
for k in range(4):
    a=k*math.pi/2+math.pi/4;x,y=RC[0]+math.cos(a)*0.12,RC[1]+math.sin(a)*0.12
    M.append(['cylA',x,y,zc-0.2,zc+OH,0.17,0.14,7,DARK])
    hx,hy=RC[0]+math.cos(a)*0.2,RC[1]+math.sin(a)*0.2
    M.append(['cylA',hx,hy,zc+OH,zc+OH+0.75,0.08,0.015,6,DARK])
M.append(['cylA',RC[0],RC[1],zc-0.2,zc+OH-0.05,0.2,0.2,8,DARK])
M.append(['capA',RC[0],RC[1],zc+OH-0.05,0,0.23,8,'#1c1c20'])
M.append(['discA',RC[0],RC[1]+0.215,zc+OH*0.82,0,1,0.03,[1.0,0.7,0.3,0.8]])        # janela iluminada
M.append(['boxA',RC[0],RC[1]+0.3,0.12,0.1,zc-0.05,zc+0.3,0,DARK,DARK])             # escadaria
# pilares com correntes ao longo das estradas
for a in spokes:
    for q in range(1,6):
        r=0.35+q*(RR-0.45)/6
        for s_ in (-1,1):
            x,y=RC[0]+math.cos(a)*r-math.sin(a)*0.07*s_,RC[1]+math.sin(a)*r+math.cos(a)*0.07*s_
            M.append(['cylA',x,y,zc-0.02,zc+0.16,0.012,0.012,5,'#8a7f6c'])
# poços: bocas incandescentes e vapor (onde a água entrou)
for x,y in PITS:
    M.append(['capA',x,y,zc+0.01,0,0.05,8,FIRE])
    M.append(['cylA',x,y,zc-0.02,zc+0.05,0.075,0.07,8,'#2c2a2a'])
for q,(x,y) in enumerate(PITS[:10]):
    M.append(['blobA',x,y,zc+0.12,[[0.06,0],[0.12,0.12],[0.08,0.24],[0,0.3]],7,'#bfc2c4'])
# represa dos Ents no Isen
for q in range(9):
    x,y=424.85+0.06*q-0.25,478.0+0.07*q-0.3
    M.append(['box',x,y,0.12,0.09,-0.1,0.14,0.5,'#6e6a60',None])
# tocos de árvores cortadas no vale devastado
for q in range(500):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    r=math.hypot(x-RC[0],y-RC[1])
    if r<RR+0.5 or r>RR+4.0 or R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.05 or R.at(rk,x,y)>0.4: continue
    if R.rng.random()<0.6: M.append(['cyl',x,y,-0.03,0.05,0.035,0.03,5,'#7a5a3a'])
# Vaus do Isen: ilhota com o túmulo dos Cavaleiros cercado de lanças
M.append(['blobA',FORD[0]+0.05,FORD[1]-0.05,gz(*FORD)-0.05,[[0.32,0],[0.26,0.12],[0.12,0.22],[0,0.26]],12,'#5f7a48'])
zf=gz(*FORD)+0.18
for q in range(12):
    a=q/12*2*math.pi;M.append(['cylA',FORD[0]+0.05+math.cos(a)*0.28,FORD[1]-0.05+math.sin(a)*0.28,zf-0.25,zf+0.2,0.008,0.004,4,'#d0d0d0'])
for q in range(10):
    t=q/9;M.append(['stone',FORD[0]-0.6+1.2*t,FORD[1]+0.25+R.rng.uniform(-0.1,0.1)])
# árvores: Fangorn e algumas no vale
for _ in range(16000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.02 or R.at(roadm,x,y)>0.05 or R.at(snow,x,y)>0.1: continue
    f=R.at(fang,x,y);r=math.hypot(x-RC[0],y-RC[1])
    if f>0.5 and R.rng.random()<0.3:
        R.tree(x,y,R.rng.uniform(0.7,1.1),1 if R.rng.random()<0.65 else 0,C(38,66,38)*R.rng.uniform(0.8,1.15))
    elif r>RR+4.5 and R.at(rk,x,y)<0.4 and R.rng.random()<0.012:
        R.tree(x,y,R.rng.uniform(0.5,0.8),0 if R.rng.random()<0.5 else 1,C(52,84,46)*R.rng.uniform(0.85,1.1))
R.TOPS=[[RC[0],RC[1],round(OH+0.9,2),0.3],[GATE[0],GATE[1],1.6,0.3]]
R.PL={'Orthanc':RC,'AnelIsengard':(RC[0]-RR,RC[1]),'PortaoIsengard':GATE,'PocosSaruman':(RC[0]+0.7,RC[1]+0.8),'RepresaEnts':(424.75,478.0),
      'ValeMago':(426.3,489.0),'VausIsen':FORD,'TumuloCavaleiros':(FORD[0]+0.05,FORD[1]-0.05),'BordaFangorn':(441.5,479.0)}
R.save_json()
