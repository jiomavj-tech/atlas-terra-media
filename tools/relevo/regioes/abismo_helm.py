import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('helm',426,504,458,532,PX=44,GR=5,seed=41,out='/tmp/claude-0/ro')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
MOUTH=(441.0,517.0)
ux_,uy_=0.737,-0.676                      # eixo do vale (do Abismo para fora)
nx_,ny_=uy_,-ux_                          # lado norte (esquerda de quem sai)
nx_,ny_=-0.676,-0.737
HB=(MOUTH[0]+nx_*1.05,MOUTH[1]+ny_*1.05)  # Forte da Trombeta
STREAM=[(435.0,522.8),(436.8,521.4),(438.8,519.4),(440.2,517.8),MOUTH,(443.0,515.3),(445.5,513.6),(448.0,511.9),(451.0,510.3),(454.5,508.9),(458.8,507.6)]
SP,SS=dense(STREAM);ST=cKDTree(SP)
def sinfo(X,Y):
    d,i=ST.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape),SS[i].reshape(X.shape)
S_MOUTH=float(SS[np.argmin(np.hypot(SP[:,0]-MOUTH[0],SP[:,1]-MOUTH[1]))])
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3);hbs=np.where(hbs>0.30,0.30+(hbs-0.30)*0.5,hbs)
nz=R.noise(8,5,3,True)
hd=hbs+0.015*nz
# Thrihyrne: três picos atrás do Abismo
for (px,py) in [(432.2,525.6),(434.6,527.4),(437.4,527.2)]:
    hd=hd+0.13*gauss(px,py,1.3,GX,GY)
# crista que fecha o Abismo dos dois lados
along=(GX-MOUTH[0])*ux_+(GY-MOUTH[1])*uy_;across=(GX-MOUTH[0])*nx_+(GY-MOUTH[1])*ny_
ridge=0.36*sstep(2.5,-1.0,along)*np.exp(-(across/4.5)**2)
hd=np.maximum(hd,ridge+0.02*nz)
flank=0.30*np.exp(-((np.abs(across)-4.2)/1.8)**2)*sstep(14,5,along)*sstep(-3,0,along)
hd=np.maximum(hd,flank+0.03*nz)
hd=R.soften(hd,0.6,7)
dr,sr=sinfo(GX,GY)
inner=sr<S_MOUTH
fl=np.where(inner,0.27-0.05*sstep(0,S_MOUTH,sr),0.22-0.08*sstep(S_MOUTH,S_MOUTH+18,sr))
wf=np.where(inner,0.28,0.45+2.0*sstep(S_MOUTH,S_MOUTH+10,sr)+0.3*nz)
wall=np.where(inner,0.75,wf+2.2+2.0*sstep(S_MOUTH,S_MOUTH+12,sr))
fl=cv2.GaussianBlur(fl.astype(np.float32),(0,0),2.5);wf=cv2.GaussianBlur(wf.astype(np.float32),(0,0),2.5);wall=np.maximum(cv2.GaussianBlur(wall.astype(np.float32),(0,0),2.5),wf+0.3)
prof=fl+(hd-fl)*sstep(wf,wall,dr)
hd=np.where(dr<wall,np.minimum(hd,prof),hd)
# esporão de rocha do Forte da Trombeta
zH=0.30
hb_=np.hypot(GX-HB[0],GY-HB[1])
hd=np.where(hb_<1.0,np.maximum(hd,zH),np.maximum(hd,zH-(hb_-1.0)*0.11))*(hb_<2.0)+hd*(hb_>=2.0)
hd=hd-0.006*sstep(0.25,0.0,dr)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
DR,SR=sinfo(UX,UY)
n1=R.noise(40,4,5)[...,None];n2=R.noise(160,3,6)[...,None]
grass=C(134,140,80)*(1-np.clip(n1+0.5,0,1))+C(112,124,68)*np.clip(n1+0.5,0,1)
img+=(grass*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
rk=np.clip(sstep(1.4,2.6,R.slope)+sstep(0.38,0.46,R.HT),0,1)
img=R.paint(img,rk,C(132,128,120)*(1+R.noise(80,4,8)[...,None]*0.14),0.9)
snow=sstep(0.45,0.52,R.HT+0.03*R.noise(50,3,9));img=R.paint(img,snow,C(236,240,246))
# estrada: do portão pela calçada, descendo o vale
ROAD=[(HB[0]+0.55,HB[1]+0.25),(442.6,515.2),(444.6,514.2),(447.2,512.8),(450.4,511.4),(454.0,510.2),(458.5,509.4)]
img,roadm=R.road(img,ROAD,0.16,C(176,160,124),C(100,90,70))
# Dique de Helm: vala e aterro atravessando o vale
DA=S_MOUTH+5.3;di=int(np.argmin(np.abs(SS-DA)));dp=SP[di];dt=SP[min(len(SP)-1,di+5)]-SP[max(0,di-5)];dt/=np.linalg.norm(dt);dn=np.array([-dt[1],dt[0]])
DIKE=[tuple(dp+dn*q) for q in np.linspace(-3.2,3.2,9)]
dikem=R.line_mask(DIKE,0.22)
img=R.paint(img,dikem,C(92,78,58),0.8)
# água
water=np.clip((0.07+0.05*(SR>S_MOUTH)-DR)/0.03+0.5,0,1)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1),C(96,104,74),0.4)
img=R.paint(img,water,C(64,98,118))
# campo de batalha: chão pisado diante da muralha
bat=np.exp(-((UX-442.6)**2+(UY-515.6)**2)/(2*1.2**2))
img=R.paint(img,bat,C(116,104,80),0.5)
# floresta dos Huorns na saída do vale
HUORN=dp+dt*3.4
hu=np.exp(-(((UX-HUORN[0])*dt[0]+(UY-HUORN[1])*dt[1])/2.2)**2-(((UX-HUORN[0])*dn[0]+(UY-HUORN[1])*dn[1])/3.6)**2)*(1+0.3*R.noise(10,3,77))
hu=np.clip(hu*1.6-0.3,0,1)
img=R.paint(img,hu,C(40,58,36),0.7)
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD
STONE='#b9b2a0';STONE2='#a8a190';ROOF='#5c4a3a'
zb=zH*HSW
# Forte da Trombeta: muralha externa, torre alta e salão (escala K)
K=1.7;NW=18
for k in range(NW):
    a=k/NW*2*math.pi;da=2*math.pi/NW;r=0.52*K
    if abs(((a-0.35+math.pi)%(2*math.pi))-math.pi)<0.16: continue      # portão (lado da calçada)
    x,y=HB[0]+math.cos(a+da/2)*r,HB[1]+math.sin(a+da/2)*r
    M.append(['boxA',x,y,r*da/2+0.02,0.06,zb-0.9,zb+0.36*K,a+da/2+math.pi/2,STONE,STONE2])
for k in range(6):
    a=k/6*2*math.pi+0.2;x,y=HB[0]+math.cos(a)*0.52*K,HB[1]+math.sin(a)*0.52*K
    M.append(['cylA',x,y,zb-0.7,zb+0.55*K,0.08*K,0.072*K,8,STONE]);M.append(['cylA',x,y,zb+0.55*K,zb+0.75*K,0.085*K,0,8,ROOF])
TWX,TWY=HB[0]-0.1*K,HB[1]-0.08*K
M.append(['cylA',TWX,TWY,zb-0.2,zb+1.7*K,0.17*K,0.14*K,12,STONE])           # a torre
M.append(['cylA',TWX,TWY,zb+1.4*K,zb+1.47*K,0.19*K,0.19*K,12,STONE2])
M.append(['cylA',TWX,TWY,zb+1.7*K,zb+2.1*K,0.17*K,0.0,12,ROOF])
M.append(['discA',TWX+0.15*K,TWY+0.02,zb+1.25*K,1,0,0.03*K,[1.0,0.8,0.4,0.6]])
M.append(['boxA',HB[0]+0.17*K,HB[1]+0.12*K,0.2*K,0.1*K,zb,zb+0.42*K,0.4,'#c2baa6',ROOF])          # salão
M.append(['boxA',HB[0]-0.05*K,HB[1]+0.3*K,0.12*K,0.08*K,zb,zb+0.3*K,1.2,'#c2baa6',ROOF])
# calçada (rampa) até o portão
M.append(['boxA',HB[0]+0.72*K,HB[1]+0.32*K,0.34*K,0.08,gz(HB[0]+1.05*K,HB[1]+0.46*K)-0.2,zb-0.02,0.4,STONE2,STONE2])
# Muralha do Abismo: do Forte até a escarpa sul, atravessando a boca do Abismo
WS=(MOUTH[0]-nx_*1.15,MOUTH[1]-ny_*1.15)
WALLP=[(HB[0]-nx_*0.48*1.7,HB[1]-ny_*0.48*1.7),MOUTH,WS]
M.append(['wall',[[round(x,3),round(y,3)] for x,y in WALLP],0.7,STONE,0.16])
for (x,y) in [WALLP[0],WS]: M.append(['cyl',x,y,-0.2,0.6,0.09,0.085,8,STONE])
# bueiro do riacho sob a muralha (arrombado)
M.append(['discA',MOUTH[0]+ux_*0.08,MOUTH[1]+uy_*0.08,gz(*MOUTH)+0.08,ux_,uy_,0.1,'#1a1816'])
for q in range(6): M.append(['box',MOUTH[0]+ux_*0.3+R.rng.uniform(-0.2,0.2),MOUTH[1]+uy_*0.3+R.rng.uniform(-0.2,0.2),0.05,0.04,-0.03,0.06,R.rng.uniform(0,3),STONE2,None])
# Cavernas Cintilantes: entrada no fundo do Abismo
CAVE=(435.4,523.2);cz=gz(*CAVE)
cdx,cdy=ux_,uy_
M.append(['discA',CAVE[0]+cdx*0.12,CAVE[1]+cdy*0.12,cz+0.35,cdx,cdy,0.22,'#141210'])
for q in range(8):
    M.append(['discA',CAVE[0]+cdx*0.13+R.rng.uniform(-0.12,0.12)*nx_,CAVE[1]+cdy*0.13+R.rng.uniform(-0.12,0.12)*ny_,cz+0.25+R.rng.uniform(0,0.25),cdx,cdy,0.012,[0.85,0.95,1.0,1.0]])
# Dique de Helm: aterro com abertura para a estrada e o riacho
for seg in (DIKE[:4],DIKE[5:]):
    M.append(['wall',[[round(float(x),3),round(float(y),3)] for x,y in seg],0.12,'#7a6a4e',0.18])
# Colina da Morte (pedras sobre os mortos) e o monte por onde Gandalf chegou
DEATH=tuple(HUORN+dn*3.6)
M.append(['blobA',DEATH[0],DEATH[1],gz(*DEATH)-0.05,[[0.45,0],[0.38,0.15],[0.2,0.28],[0,0.32]],12,'#7a7468'])
for q in range(14):
    a=R.rng.uniform(0,2*math.pi);r=R.rng.uniform(0,0.35);M.append(['stone',DEATH[0]+math.cos(a)*r,DEATH[1]+math.sin(a)*r])
GAND=tuple(dp-dn*3.0-dt*0.6)
# árvores: floresta dos Huorns (escuras e grandes), poucas no vale
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.02 or R.at(roadm,x,y)>0.1 or R.at(snow,x,y)>0.1: continue
    h=R.at(hu,x,y)
    if h>0.35 and R.rng.random()<0.55: R.tree(x,y,R.rng.uniform(0.8,1.2),1 if R.rng.random()<0.7 else 0,C(30,48,30)*R.rng.uniform(0.8,1.2))
    elif R.at(rk,x,y)<0.3 and R.rng.random()<0.006: R.tree(x,y,R.rng.uniform(0.5,0.75),1,C(70,98,50)*R.rng.uniform(0.85,1.1))
R.TOPS=[[HB[0],HB[1],3.9,0.6],[MOUTH[0],MOUTH[1],0.9,0.3]]
R.PL={'ForteTrombeta':HB,'MuralhaAbismo':((MOUTH[0]+WS[0])/2,(MOUTH[1]+WS[1])/2),'Bueiro':MOUTH,'CavernasCintilantes':CAVE,'DiqueHelm':tuple(dp+dn*1.5),
      'FlorestaHuorns':tuple(HUORN),'ColinaMorte':DEATH,'ColinaGandalf':GAND,'ValeAbismo':tuple(SP[int(np.argmin(np.abs(SS-(S_MOUTH+2.6))))]+dn*0.9)}
R.save_json()
