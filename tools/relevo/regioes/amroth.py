import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('amroth',396,630,434,668,PX=40,GR=5,seed=201,out='/tmp/claude-0/b5')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
wg=R.base_water_grid()
def coast_y(x):
    col=wg[:,int((x-R.X0)*R.GR)];c=np.where(col>0.45)[0];return R.Y0+c.min()/R.GR
CX=414.6;CY=coast_y(CX)
TIP=(CX-0.4,CY+3.6);TOWN=(CX+0.3,CY-1.6)
# promontório rochoso avançando no mar
ax=np.clip((GY-(CY-0.5))/(TIP[1]-CY+0.5),0,1)
cx=CX+(TIP[0]-CX)*ax
cape=np.exp(-((GX-cx)/(1.5-0.8*ax))**2)*(GY>CY-1.5)*(GY<TIP[1]+0.9)*sstep(TIP[1]+0.9,TIP[1]+0.2,GY)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
sea=(wg>0.45)&(cape<0.35)
lvl=-0.01
dist=cv2.distanceTransform((~sea).astype(np.uint8),cv2.DIST_L2,5)/R.GR
land=np.maximum(hbs+0.008*nz,lvl+0.012)
land=np.where(cape>0.35,np.maximum(land,lvl+0.03+0.075*sstep(0.35,0.9,cape)*(0.6+0.4*ax)),land)
hd=np.where(sea,lvl,lvl+0.004+(land-lvl)*sstep(0.0,1.2,dist))
R.set_height(hd);gz=R.gz;ZW=lvl*HSW
seaT=cv2.GaussianBlur(cv2.resize(sea.astype(np.float32),(R.TW,R.TH),interpolation=cv2.INTER_LINEAR),(0,0),2);seaT=np.clip((seaT-0.4)/0.2,0,1)
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(126,148,76)*(1-np.clip(n1+0.5,0,1))+C(106,130,66)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
rk=np.clip(sstep(1.0,2.4,R.slope),0,1)
img=R.paint(img,rk,C(168,160,144),0.85)
img=R.paint(img,np.clip(cv2.dilate(seaT,np.ones((9,9),np.uint8))-seaT,0,1),C(214,204,170),0.6)
img=R.paint(img,seaT,C(60,112,146)*(1+R.noise(100,3,13)[...,None]*0.06))
ROAD=[(R.X1+1,640.0),(426,642.5),(420,646.0),(416.5,649.5),(TOWN[0]+0.3,TOWN[1]-0.8),TOWN,(CX-0.1,CY+1.2),(TIP[0]+0.05,TIP[1]-1.0)]
img,roadm=R.road(img,ROAD,0.13,C(196,184,150),C(110,100,78))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD
WHITE='#f0ece0';BLUE='#3a5a8a';BLUE2='#4a6a9a'
# o castelo do Príncipe na ponta do promontório
K=(TIP[0],TIP[1]-0.5);zk=gz(*K)
for k in range(18):
    a=k/18*6.28;da=6.28/18;x,y=K[0]+math.cos(a+da/2)*0.5,K[1]+math.sin(a+da/2)*0.5
    M.append(['boxA',x,y,0.5*da/2+0.01,0.05,zk-0.8,zk+0.35,a+da/2+1.571,WHITE,'#e2dccc'])
for k in range(6):
    a=k/6*6.28;x,y=K[0]+math.cos(a)*0.5,K[1]+math.sin(a)*0.5
    M.append(['cylA',x,y,zk-0.8,zk+0.6,0.08,0.07,8,WHITE]);M.append(['cylA',x,y,zk+0.6,zk+0.85,0.09,0.0,8,BLUE])
M.append(['boxA',K[0],K[1],0.24,0.18,zk,zk+0.55,0.2,WHITE,BLUE2])
M.append(['cylA',K[0]+0.1,K[1]-0.05,zk+0.4,zk+1.5,0.1,0.085,8,WHITE]);M.append(['cylA',K[0]+0.1,K[1]-0.05,zk+1.5,zk+1.9,0.11,0.0,8,BLUE])
# Tirith Aear, a Torre do Mar, na extremidade
T=(TIP[0]-0.05,TIP[1]+0.25);zt=gz(*T)
M.append(['cylA',T[0],T[1],zt-0.5,zt+1.8,0.09,0.07,8,WHITE]);M.append(['cylA',T[0],T[1],zt+1.8,zt+2.1,0.1,0.0,8,BLUE]);M.append(['discA',T[0],T[1]+0.08,zt+1.6,0,1,0.025,[1.0,0.9,0.6,1.0]])
# a cidade e o porto abrigado, com os navios-cisne
HP=[]
for q in range(4000):
    x,y=TOWN[0]+R.rng.uniform(-1.6,1.6),TOWN[1]+R.rng.uniform(-0.9,0.7)
    if R.at(seaT,x,y)>0.1 or R.at(roadm,x,y)>0.3 or any(math.hypot(x-px,y-py)<0.19 for px,py in HP): continue
    HP.append((x,y))
    if len(HP)>90: break
    M.append(['house',round(x,3),round(y,3),0.17,0.12,round(R.rng.uniform(0,3.1),2),WHITE,[BLUE,BLUE2,'#a85a3a'][R.rng.integers(3)],round(R.rng.uniform(0.18,0.3),3)])
PORT=(CX+2.2,coast_y(CX+2.2)+0.1)
for k in range(3): M.append(['boxA',PORT[0]-0.6+k*0.6,PORT[1]+0.3,0.05,0.35,ZW-0.1,ZW+0.08,0,'#c8c0ac',None])
for k in range(4):
    x,y=PORT[0]-0.9+k*0.6,PORT[1]+0.9
    M.append(['blobA',x,y,ZW-0.02,[[0.08,0],[0.17,0.05],[0.15,0.11],[0,0.12]],9,WHITE]);M.append(['cylA',x,y,ZW+0.1,ZW+0.6,0.012,0.008,5,'#d8d4c8']);M.append(['boxA',x,y,0.01,0.15,ZW+0.25,ZW+0.55,0.2,[0.3,0.45,0.75,0.2],None])
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(seaT,x,y)>0.03 or R.at(roadm,x,y)>0.05 or R.at(rk,x,y)>0.4 or any(math.hypot(x-px,y-py)<0.3 for px,py in HP): continue
    if R.rng.random()<0.014: R.tree(x,y,R.rng.uniform(0.5,0.75),1,C(70,110,52)*R.rng.uniform(0.85,1.1))
R.TOPS=[[K[0],K[1],2.1,0.6],[T[0],T[1],2.3,0.3]]
R.PL={'CasteloAmroth':K,'TorreMar':T,'CidadeAmroth':TOWN,'PortoAmroth':PORT,'BaiaBelfalas':(404.0,662.0)}
R.save_json()
