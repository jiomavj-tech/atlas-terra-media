import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('morgul',602,562,640,596,PX=40,GR=5,seed=111,out='/tmp/claude-0/b3')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
MM=(618.9,583.2)                   # Minas Morgul
PASS=(626.8,571.8)                 # passo de Cirith Ungol (Toca de Laracna)
TCU=(629.2,572.6)                  # Torre de Cirith Ungol (lado de Mordor)
XR=(607.6,584.6)                   # Encruzilhada
RIVER=[(626.5,585.6),(623.5,585.2),(620.5,584.8),(618.6,585.0),(615.5,585.0),(612.0,585.4),(608.5,586.0),(604.0,586.8),(601.0,587.4)]
RP,RS=dense(RIVER);RT=cKDTree(RP)
def rinfo(X,Y):
    d,i=RT.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape),RS[i].reshape(X.shape)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3)
nz=R.noise(8,5,3,True);rid=(1-np.abs(R.noise(16,4,9,True)))**2
hd=hbs+0.015*nz+0.03*rid*sstep(0.3,0.4,hbs)
# Ephel Dúath: crista ao norte do vale, por onde sobem as escadas
crest=0.42*np.exp(-((GY-(572.0+0.12*(GX-626)))/2.2)**2)*sstep(612,620,GX)*sstep(640,634,GX)
hd=np.maximum(hd,crest+0.02*nz)
# o vale de Imlad Morgul
dr,sr=rinfo(GX,GY)
fl=0.30-0.1*sstep(0,25,sr)
wf=0.6+1.2*sstep(4,14,sr);wall=wf+2.5+1.5*sstep(6,20,sr)
fl=cv2.GaussianBlur(fl.astype(np.float32),(0,0),3);wf=cv2.GaussianBlur(wf.astype(np.float32),(0,0),3);wall=np.maximum(cv2.GaussianBlur(wall.astype(np.float32),(0,0),3),wf+0.5)
pr=fl+(hd-fl)*sstep(wf,wall,dr)**0.8
hd=np.where(dr<wall,np.minimum(hd,pr),hd)
hd=R.soften(hd,0.75,6)
# a plataforma de rocha de Minas Morgul
dm=np.hypot(GX-MM[0],GY-MM[1]);zMM=float(fl[int((MM[1]-R.Y0)*5),int((MM[0]-R.X0)*5)])+0.05
hd=np.where(dm<1.0,zMM,np.where(dm<2.0,np.maximum(np.minimum(hd,zMM+0.05),zMM-0.05*sstep(1.0,2.0,dm)),hd))
# selada do passo
dp=np.hypot(GX-PASS[0],GY-PASS[1]);zp=0.38
hd=np.where(dp<0.6,np.minimum(hd,zp),hd)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
DR,SR=rinfo(UX,UY)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(80,92,64)*(1-np.clip(n1+0.5,0,1))+C(66,74,56)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
rk=np.clip(sstep(0.9,2.4,R.slope)+sstep(0.36,0.44,R.HT),0,1)
img=R.paint(img,rk,C(64,60,62)*(1+R.noise(80,4,8)[...,None]*0.15),0.88)
mordor=sstep(631,635,UX+0.5*(UY-575))
img=R.paint(img,mordor,C(70,60,56),0.7)
# campos de flores pálidas (cadavéricas) em volta da cidade
pale=np.exp(-((UX-MM[0]+1.0)**2/8+(UY-MM[1]-1.2)**2/2))*(DR>0.25)
img=R.paint(img,pale*np.clip(R.noise(150,2,15)+0.6,0,1),C(196,206,190),0.55)
water=np.clip((0.1-DR)/0.03+0.5,0,1)
img=R.paint(img,water,C(150,180,170))
# estrada de Morgul, escadas e o caminho até o passo
GATE=(MM[0]-0.75,MM[1]+0.55)
MROAD=[(R.X0-1,584.2),XR,(611.0,584.4),(614.5,584.4),(617.0,584.8),(617.7,585.0),(618.2,584.3),GATE]
img,roadm=R.road(img,MROAD,0.18,C(140,138,124),C(70,68,64))
XROAD=[(XR[0],R.Y0-1),XR,(XR[0]+0.3,R.Y1+1)]
img,rm2=R.road(img,XROAD,0.16,C(140,138,124),C(70,68,64))
STAIR=[(616.2,584.0),(616.0,582.0),(617.4,580.8),(616.6,579.4),(618.4,578.6),(617.8,577.2),(619.8,576.4),(619.6,575.0),(621.8,574.6),(621.6,573.4),(623.8,573.0),(625.2,572.3),PASS]
img,sm=R.road(img,STAIR,0.07,C(150,146,134),C(60,56,54))
img,_=R.road(img,[PASS,(628.0,572.0),TCU,(631.5,573.6),(636,575.0),(R.X1+1,576.5)],0.1,C(110,100,92),C(50,44,42))
fin=R.light(img,tint=[0.92,0.94,0.92])
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zc=zMM*HSW
PALE='#c4d0c0';PALE2='#aebcaa';GLOW=[0.55,1.0,0.65,1.0]
# Minas Morgul: muralhas pálidas, torre alta com o topo em camadas
for k in range(30):
    a=k/30*2*math.pi;da=2*math.pi/30;x,y=MM[0]+math.cos(a+da/2)*0.8,MM[1]+math.sin(a+da/2)*0.8
    M.append(['boxA',x,y,0.8*da/2+0.02,0.06,zc-0.5,zc+0.45,a+da/2+math.pi/2,PALE2,PALE])
for k in range(6):
    a=k/6*2*math.pi;x,y=MM[0]+math.cos(a)*0.8,MM[1]+math.sin(a)*0.8
    M.append(['cylA',x,y,zc-0.4,zc+0.65,0.09,0.08,8,PALE]);M.append(['cylA',x,y,zc+0.65,zc+0.85,0.09,0.0,8,PALE2])
for q in range(40):
    a=R.rng.uniform(0,6.28);r=R.rng.uniform(0.3,0.7);x,y=MM[0]+math.cos(a)*r,MM[1]+math.sin(a)*r
    M.append(['houseA',x,y,0.12,0.08,a,PALE,'#8a9888',R.rng.uniform(0.15,0.3),zc])
TX,TY=MM[0]+0.05,MM[1]-0.1
M.append(['cylA',TX,TY,zc,zc+2.6,0.2,0.16,10,PALE])
for k in range(3):
    z0=zc+2.6+k*0.28;M.append(['cylA',TX,TY,z0,z0+0.28,0.2-k*0.05,0.15-k*0.05,10,PALE if k%2==0 else PALE2])
M.append(['cylA',TX,TY,zc+3.44,zc+3.9,0.08,0.0,10,PALE])
M.append(['cylA',TX,TY,zc+2.2,zc+2.3,0.17,0.17,10,GLOW])
for k in range(10): M.append(['discA',TX+math.cos(k*0.63)*0.17,TY+math.sin(k*0.63)*0.17,zc+1.2+k*0.12,math.cos(k*0.63),math.sin(k*0.63),0.025,GLOW])
M.append(['discA',GATE[0]-0.05,GATE[1]+0.03,gz(*GATE)+0.25,-0.8,0.6,0.16,'#0c140e'])
M.append(['discA',GATE[0]-0.06,GATE[1]+0.04,gz(*GATE)+0.25,-0.8,0.6,0.1,GLOW])
# a ponte sobre o Morgulduin, com estátuas
M.append(['bridge',617.55,585.35,617.85,584.45,0.16,2,'#b8c2b4'])
for q in range(4):
    x,y=617.55+q*0.1,585.35-q*0.3;M.append(['cyl',x-0.12,y,0.1,0.28,0.02,0.015,5,PALE]);M.append(['cyl',x+0.12,y,0.1,0.28,0.02,0.015,5,PALE])
# a Encruzilhada: o rei de pedra com a cabeça coroada de flores, num anel de árvores
zx=gz(*XR)
M.append(['cylA',XR[0]+0.35,XR[1]-0.35,zx-0.05,zx+0.45,0.07,0.06,8,'#9a9488']);M.append(['blobA',XR[0]+0.5,XR[1]-0.3,zx-0.02,[[0.06,0],[0.07,0.05],[0,0.12]],8,'#9a9488'])
for k in range(8): M.append(['capA',XR[0]+0.5+math.cos(k*0.8)*0.06,XR[1]-0.3+math.sin(k*0.8)*0.06,zx+0.07,0,0.015,5,[0.95,0.85,0.3,0.6]])
for k in range(14):
    a=k/14*6.28;R.tree(XR[0]+math.cos(a)*1.0,XR[1]+math.sin(a)*1.0,0.75,1,C(56,80,46))
# a Torre de Cirith Ungol: três andares em degraus sobre o esporão, com muralha
zt=gz(*TCU)
for k,(w,h) in enumerate([(0.42,0.6),(0.3,0.55),(0.18,0.55)]):
    z0=zt-0.2+sum(hh for _,hh in [(0.42,0.6),(0.3,0.55),(0.18,0.55)][:k])
    M.append(['boxA',TCU[0]+k*0.06,TCU[1],w,w*0.8,z0,z0+h,0.4,'#2a2628','#1a1718'])
M.append(['cylA',TCU[0]+0.12,TCU[1],zt+1.5,zt+2.0,0.08,0.0,6,'#1a1718'])
M.append(['discA',TCU[0]+0.3,TCU[1]-0.05,zt+1.2,1,0,0.03,[1.0,0.4,0.1,1.0]])
M.append(['wall',[[TCU[0]-0.6,TCU[1]-0.6],[TCU[0]+0.6,TCU[1]-0.7],[TCU[0]+0.8,TCU[1]+0.5],[TCU[0]-0.5,TCU[1]+0.7],[TCU[0]-0.6,TCU[1]-0.6]],0.25,'#2a2628',0.08])
# a Toca de Laracna: boca escura na rocha, com teias
zp2=gz(*PASS)
M.append(['discA',PASS[0]-0.25,PASS[1]+0.15,zp2+0.25,-0.8,0.6,0.22,'#060506'])
for q in range(6):
    a=q*0.5;M.append(['boxA',PASS[0]-0.3+math.cos(a)*0.12,PASS[1]+0.18+math.sin(a)*0.12,0.12,0.002,zp2+0.1,zp2+0.45,a,[0.85,0.85,0.8,0.15],None])
# árvores: Ithilien a oeste, mortas no vale
for _ in range(12000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.05 or R.at(rm2,x,y)>0.05 or R.at(sm,x,y)>0.1 or R.at(rk,x,y)>0.5: continue
    if math.hypot(x-MM[0],y-MM[1])<1.6: continue
    if x<612 and R.rng.random()<0.06: R.tree(x,y,R.rng.uniform(0.6,0.9),1 if R.rng.random()<0.6 else 0,C(52,84,46)*R.rng.uniform(0.85,1.1))
    elif x<630 and R.rng.random()<0.006: M.append(['cyl',x,y,-0.03,R.rng.uniform(0.25,0.45),0.025,0.008,4,'#3a3430'])
R.TOPS=[[TX,TY,round(zc+4.2-gz(TX,TY),2),0.4],[TCU[0],TCU[1],2.3,0.4]]
R.PL={'CidadeMorgul':MM,'PonteMorgul':(617.7,584.8),'EscadaReta':STAIR[3],'EscadaSinuosa':STAIR[8],'TocaLaracna':PASS,'TorreCirithUngol':TCU,'EncruzilhadaRei':XR,'ImladMorgul':(623.5,585.0)}
R.save_json()
