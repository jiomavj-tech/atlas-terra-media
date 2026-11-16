import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('dunharrow',460,535,492,563,PX=44,GR=5,seed=251,out='/tmp/claude-0/b6')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
RIVER=[(477.2,534.0),(477.0,538.0),(476.4,542.0),(476.0,546.0),(475.6,550.0),(475.0,554.0),(474.0,558.0),(473.0,564.0)]   # Snowbourn (para o norte)
FIRI=(479.6,548.0)                 # Firienfeld, o campo alto do Fano-da-Colina
DOOR=(484.6,550.4)                 # a Porta Escura, no Dwimorberg
RP,RS=dense(RIVER);RT=cKDTree(RP)
def rinfo(X,Y):
    d,i=RT.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True);rid=(1-np.abs(R.noise(16,4,9,True)))**2
hd=hbs+0.015*nz+0.025*rid*sstep(0.36,0.46,hbs)
hd=hd+0.10*gauss(487.5,551.0,2.4,GX,GY)                          # Dwimorberg, a Montanha Assombrada
hd=R.soften(hd,0.75,6)
dr=rinfo(GX,GY)
fl=0.27+0.03*sstep(535,563,GY)
pr=fl+(hd-fl)*sstep(0.7,3.6,dr)**0.8
hd=np.where(dr<3.6,np.minimum(hd,pr),hd)
# o campo alto, numa prateleira bem acima do vale
d=np.hypot((GX-FIRI[0])/1.0,(GY-FIRI[1])/1.5);zF=float(fl.mean())+0.085
hd=np.where(d<1.0,zF,np.where(d<1.7,zF+(hd-zF)*sstep(1.0,1.7,d),hd))
# o desfiladeiro escuro até a Porta
ax=np.clip((GX-FIRI[0]-0.8)/(DOOR[0]-FIRI[0]-0.8),0,1);cy=FIRI[1]+(DOOR[1]-FIRI[1])*ax
glen=np.exp(-((GY-cy)/0.45)**2)*(GX>FIRI[0]+0.6)*(GX<DOOR[0]+0.1)
hd=np.where(glen>0.3,np.minimum(hd,zF+0.01+0.02*ax),hd)
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
DR=rinfo(UX,UY)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(120,138,74)*(1-np.clip(n1+0.5,0,1))+C(100,118,64)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
rk=np.clip(sstep(1.0,2.6,R.slope)+sstep(0.42,0.5,R.HT),0,1)
img=R.paint(img,rk,C(118,114,108)*(1+R.noise(80,4,8)[...,None]*0.14),0.9)
snow=sstep(0.52,0.6,R.HT+0.03*R.noise(50,3,9));img=R.paint(img,snow,C(236,240,246))
water=np.clip((0.1-DR)/0.03+0.5,0,1)
img=R.paint(img,water,C(70,108,128))
# a estrada em zigue-zague, subindo do vale até o campo
ZZ=[(476.6,546.4)]
for k in range(8): ZZ.append((477.0+0.3*k+(0.55 if k%2==0 else -0.15),546.4+(0.9 if k%2==0 else -0.6)+0.05*k))
ZZ.append((FIRI[0]-0.75,FIRI[1]))
img,zm=R.road(img,ZZ,0.06,C(176,164,134),C(96,88,70))
AVE=[(FIRI[0]-0.75,FIRI[1]),FIRI,(FIRI[0]+0.9,FIRI[1]+0.3),DOOR]
img,am=R.road(img,AVE,0.07,C(160,150,126),C(80,74,62))
VROAD=[(477.4,R.Y0-1),(477.2,540.0),(476.8,544.0),(476.6,546.4)]
img,vm=R.road(img,VROAD,0.1,C(176,164,134),C(96,88,70))
roadm=np.clip(zm+am+vm,0,1)
fin=R.light(img)
R.save_tex(fin)
M=R.MOD;zf=gz(*FIRI)
# os homens-Púkel: estátuas atarracadas em cada curva da estrada
for (x,y) in ZZ[1:-1]:
    z=gz(x,y);M.append(['blobA',x+0.08,y,z-0.02,[[0.05,0],[0.06,0.06],[0.04,0.11],[0.045,0.14],[0,0.18]],6,'#8a867a'])
# a fila dupla de pedras erguidas atravessando o campo até o Dimholt
for k in range(12):
    t=k/11;x,y=FIRI[0]-0.7+1.5*t,FIRI[1]+0.25*t
    for s_ in (-1,1): M.append(['cylA',x,y+s_*0.09,gz(x,y)-0.03,gz(x,y)+0.2,0.022,0.015,5,'#8e8a80'])
# o acampamento de Rohan: tendas e o pavilhão do rei
for q in range(34):
    x,y=FIRI[0]+R.rng.uniform(-0.8,0.8),FIRI[1]+R.rng.uniform(-1.2,1.2)
    if abs(y-FIRI[1]-0.1)<0.22: continue
    M.append(['blobA',x,y,zf-0.01,[[0.07,0],[0.05,0.06],[0,0.11]],5,['#e8e0c8','#d8ceb0','#c8bea0'][q%3]])
M.append(['blobA',FIRI[0]-0.2,FIRI[1]-0.45,zf-0.01,[[0.14,0],[0.11,0.1],[0,0.2]],8,'#f0ead8']);M.append(['cylA',FIRI[0]-0.2,FIRI[1]-0.45,zf+0.2,zf+0.4,0.006,0.006,4,'#3a6a3a'])
# o Dimholt (bosque escuro), a pedra de aviso e a Porta Escura
for q in range(46):
    t=R.rng.uniform(0.15,0.9);x=FIRI[0]+0.8+(DOOR[0]-FIRI[0]-0.8)*t;y=FIRI[1]+(DOOR[1]-FIRI[1])*t+R.rng.choice([-1,1])*R.rng.uniform(0.2,0.42)
    R.tree(x,y,R.rng.uniform(0.55,0.85),0,C(22,40,30))
WS=(DOOR[0]-1.0,DOOR[1]-0.25);M.append(['cylA',WS[0],WS[1],gz(*WS)-0.03,gz(*WS)+0.4,0.04,0.025,5,'#6e6a62'])
zd=gz(DOOR[0]-0.15,DOOR[1])
M.append(['boxA',DOOR[0],DOOR[1],0.03,0.22,zd-0.1,zd+0.75,0,'#5a5650','#4a4640'])
M.append(['boxA',DOOR[0]-0.035,DOOR[1],0.008,0.1,zd,zd+0.5,0,'#050505',None]);M.append(['discA',DOOR[0]-0.045,DOOR[1],zd+0.5,-1,0,0.1,'#050505'])
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.05 or R.at(rk,x,y)>0.45 or math.hypot((x-FIRI[0])/1.2,(y-FIRI[1])/1.7)<1: continue
    if R.rng.random()<0.03: R.tree(x,y,R.rng.uniform(0.5,0.8),0,C(40,70,46)*R.rng.uniform(0.85,1.1))
R.TOPS=[[DOOR[0],DOOR[1],1.0,0.4]]
R.PL={'CampoFano':FIRI,'HomensPukel':ZZ[4],'PedrasErguidas':(FIRI[0]+0.5,FIRI[1]+0.2),'Dimholt':((FIRI[0]+DOOR[0])/2+0.5,(FIRI[1]+DOOR[1])/2),'PortaEscura':DOOR,'Dwimorberg':(487.5,551.0),'ValeHarg':(476.6,541.0)}
R.save_json()
