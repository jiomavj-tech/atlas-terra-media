import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('erebor',650,98,690,138,PX=40,GR=5,seed=121,out='/tmp/claude-0/b4')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
PK=(669.4,115.6)                 # o pico
GATE=(669.6,125.4)               # Portão da Frente (sul)
DALE=(671.2,129.6)               # Valle
RAVEN=(666.0,129.6)              # Colina do Corvo
DOOR=(663.2,118.6)               # porta secreta (flanco oeste)
RIVER=[GATE,(669.8,126.6),(670.6,127.6),(672.0,128.2),(672.9,129.4),(672.6,130.8),(671.2,131.6),(669.8,132.2),(669.0,133.2),(668.6,134.4),(668.4,136.5)]
RP,RS=dense(RIVER);RT=cKDTree(RP)
def rinfo(X,Y):
    d,i=RT.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape),RS[i].reshape(X.shape)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3)
nz=R.noise(8,5,3,True);rid=(1-np.abs(R.noise(16,4,9,True)))**2
ang=np.arctan2(GY-PK[1],GX-PK[0]);r=np.hypot(GX-PK[0],GY-PK[1])
# seis braços em estrela; o vale do portão fica entre os dois braços do sul
SP=[math.radians(a) for a in (62,118,180,245,300,0)]
spur=np.zeros_like(r)
for a in SP:
    da=np.abs(((ang-a+math.pi)%(2*math.pi))-math.pi)
    spur=np.maximum(spur,np.exp(-(da*np.maximum(r,1.0)/1.3)**2)*np.clip(1-r/11.5,0,1))
mm=sstep(0.14,0.3,hbs)
hd=hbs*0.92+0.06*spur*mm*sstep(3,7,r)-0.03*(1-spur)*mm*sstep(4,8,r)+0.015*nz*mm+0.02*rid*mm
dr,sr=rinfo(GX,GY)
fl=0.24-0.14*sstep(0,11,sr)
wf=0.35+0.9*sstep(1,5,sr);wall=wf+1.6
fl=cv2.GaussianBlur(fl.astype(np.float32),(0,0),3);wf=cv2.GaussianBlur(wf.astype(np.float32),(0,0),3)
pr=fl+(hd-fl)*sstep(wf,wf+1.6,dr)
hd=np.where(dr<wf+1.6,np.minimum(hd,pr),hd)
# paredão do portão

hd=hd-0.005*sstep(0.2,0.0,dr)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
DR,SR=rinfo(UX,UY)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
# a Desolação de Smaug: terra queimada, clareando para longe da Montanha
des=C(120,108,86)*(1-np.clip(n1+0.5,0,1))+C(98,90,74)*np.clip(n1+0.5,0,1)
img+=(des*0.65+R.base_tex(10)*1.1*0.35)*(1+n2*0.08)
rk=np.clip(sstep(0.9,2.4,R.slope)+sstep(0.36,0.46,R.HT),0,1)
img=R.paint(img,rk,C(104,100,98)*(1+R.noise(80,4,8)[...,None]*0.14),0.9)
snow=sstep(0.56,0.64,R.HT+0.03*R.noise(50,3,9));img=R.paint(img,snow,C(236,240,246))
# vale de Valle: verde e cultivado de novo
dd=np.hypot(UX-DALE[0],UY-DALE[1])
img=R.paint(img,(1-sstep(1.2,2.6,dd))*(1-rk),C(112,140,66),0.7)
water=np.clip((0.09+0.03*sstep(2,8,SR)-DR)/0.03+0.5,0,1)
lake=R.base_water()
water=np.maximum(water,lake)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1),C(90,96,72),0.4)
img=R.paint(img,water,C(62,98,124))
ROAD=[(GATE[0],GATE[1]+0.15),(669.9,126.9),(670.4,128.2),(DALE[0]-0.3,DALE[1]-0.5),(670.4,131.2),(669.4,132.6),(667.6,133.4),(662.0,134.0),(656.0,136.0)]
img,roadm=R.road(img,ROAD,0.12,C(170,158,130),C(96,88,70))
PATHR=[(669.3,126.8),(668.0,127.8),(667.0,128.8),RAVEN]
img,_=R.road(img,PATHR,0.06,C(150,140,118),C(96,88,70))
PATHD=[(665.0,129.4),(663.4,126.0),(662.4,122.6),(662.4,120.2),DOOR]
img,_=R.road(img,PATHD,0.05,C(150,140,118),C(96,88,70))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zg=gz(GATE[0],GATE[1]+0.2)
STONE='#8e8a86';GOLD=[1.0,0.78,0.3,0.7]
# o Portão da Frente: arco alto na rocha, com estátuas de anões e ameias
M.append(['boxA',GATE[0],GATE[1]-0.03,0.34,0.05,zg-0.1,zg+1.1,0,'#7a7672','#6a6662'])
M.append(['boxA',GATE[0],GATE[1]+0.03,0.13,0.02,zg,zg+0.62,0,'#0c0b0c',None])
M.append(['discA',GATE[0],GATE[1]+0.055,zg+0.62,0,1,0.13,'#0c0b0c'])
M.append(['discA',GATE[0],GATE[1]+0.06,zg+0.3,0,1,0.05,GOLD])
for s_ in (-1,1):
    M.append(['boxA',GATE[0]+s_*0.24,GATE[1]+0.08,0.05,0.05,zg-0.05,zg+0.8,0,STONE,STONE])
    M.append(['cylA',GATE[0]+s_*0.24,GATE[1]+0.08,zg+0.8,zg+0.95,0.04,0.02,6,STONE])
for k in range(7): M.append(['boxA',GATE[0]-0.3+k*0.1,GATE[1]-0.03,0.03,0.05,zg+1.1,zg+1.18,0,'#7a7672',None])
# Valle: a cidade reconstruída, com muralha, torres e telhados coloridos
zd=gz(*DALE)
ROOFS=['#a8482e','#b86a2e','#8a3a2a','#c08a3a','#4a6a8a'];WALLS=['#e2d6ba','#d6c8a6','#eadfc8']
HP=[]
for q in range(3000):
    a=R.rng.uniform(0,6.28);rr=math.sqrt(R.rng.uniform(0,1))*0.7;x,y=DALE[0]+math.cos(a)*rr,DALE[1]+math.sin(a)*rr*0.85
    if any(math.hypot(x-px,y-py)<0.14 for px,py in HP) or R.at(water,x,y)>0.1: continue
    HP.append((x,y))
    if len(HP)>75: break
    M.append(['house',round(x,3),round(y,3),0.15,0.11,round(R.rng.uniform(0,3.1),2),WALLS[R.rng.integers(3)],ROOFS[R.rng.integers(5)],round(R.rng.uniform(0.16,0.28),3)])
M.append(['cyl',DALE[0],DALE[1],-0.05,0.75,0.06,0.05,8,'#e2d6ba']);M.append(['cyl',DALE[0],DALE[1],0.75,0.98,0.075,0.0,8,'#a8482e'])   # torre dos sinos
wallp=[[round(DALE[0]+math.cos(a)*0.85,3),round(DALE[1]+math.sin(a)*0.74,3)] for a in np.linspace(0.5,2*math.pi-0.5+0.5,48) if R.at(water,DALE[0]+math.cos(a)*0.85,DALE[1]+math.sin(a)*0.74)<0.1]
if len(wallp)>3: M.append(['wall',wallp,0.2,'#b8ae98',0.06])
# Colina do Corvo: o antigo posto de guarda
zr=gz(*RAVEN)
M.append(['boxA',RAVEN[0],RAVEN[1],0.12,0.1,zr-0.2,zr+0.3,0.3,STONE,'#7a7672']);M.append(['cylA',RAVEN[0]+0.12,RAVEN[1]-0.05,zr-0.1,zr+0.55,0.05,0.04,6,STONE])
# a porta secreta: o degrau na rocha e o brilho da fechadura no Dia de Durin
zs=gz(*DOOR)
M.append(['boxA',DOOR[0]+0.06,DOOR[1],0.01,0.07,zs,zs+0.28,0,'#6a6662',None])
M.append(['discA',DOOR[0]+0.045,DOOR[1],zs+0.14,-1,0,0.012,[1.0,0.9,0.5,1.0]])
M.append(['stone',DOOR[0]-0.12,DOOR[1]+0.1])
# árvores queimadas na Desolação; verdes no vale de Valle
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.05 or R.at(rk,x,y)>0.4 or any(math.hypot(x-px,y-py)<0.2 for px,py in HP): continue
    d_=math.hypot(x-DALE[0],y-DALE[1])
    if d_<2.4 and R.rng.random()<0.05: R.tree(x,y,R.rng.uniform(0.4,0.6),1,C(76,116,50)*R.rng.uniform(0.85,1.1))
    elif R.rng.random()<0.008: M.append(['cyl',x,y,-0.03,R.rng.uniform(0.2,0.4),0.022,0.006,4,'#3a302a'])
R.TOPS=[[GATE[0],GATE[1],1.5,0.4],[DALE[0],DALE[1],1.1,0.3]]
R.PL={'PortaoErebor':GATE,'ValleCidade':DALE,'ColinaCorvo':RAVEN,'PortaSecreta':DOOR,'RioCorrente':(669.3,132.8),'DesolacaoSmaug':(658.5,131.0),'CampoCincoExercitos':(670.5,127.4),'PicoErebor':PK}
R.save_json()
