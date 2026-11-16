import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('beorn',490,158,528,192,PX=40,GR=5,seed=241,out='/tmp/claude-0/b6')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
water=R.base_water(0.5,0.1);wg=R.base_water_grid()
row=water[R.tp(0,175.4)[1]];cols=np.where(row>0.5)[0]
xr=(R.X0+cols.mean()/R.PX) if len(cols) else 506.8
CAR=(xr,175.4);HOUSE=(xr+9.5,180.5);EYRIE=(xr-9.0,166.0)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.01*nz
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(122,146,72)*(1-np.clip(n1+0.5,0,1))+C(102,128,62)*np.clip(n1+0.5,0,1)
img+=(gr*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.08)
img=R.paint(img,np.clip(sstep(1.2,2.6,R.slope),0,1),C(120,116,106),0.7)
dH=np.hypot(UX-HOUSE[0],UY-HOUSE[1])
clover=np.clip(1-dH/3.2,0,1)*np.clip(R.noise(60,3,15)+0.6,0,1)
img=R.paint(img,clover,C(150,170,90),0.5)
fl_=(R.rng.random((R.TH,R.TW))<0.03)*(dH<3.0)
img=R.paint(img,fl_.astype(np.float32),C(236,226,240),0.9)       # campos de trevo e flores (as abelhas de Beorn)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((7,7),np.uint8))-water,0,1),C(120,116,84),0.5)
img=R.paint(img,water,C(64,100,122))
PATH=[(CAR[0]+0.6,CAR[1]+0.3),(CAR[0]+3,177.0),(CAR[0]+6,179.0),(HOUSE[0]-0.9,HOUSE[1]),(HOUSE[0]+3,181.5),(R.X1+1,183.0)]
img,roadm=R.road(img,PATH,0.07,C(170,158,120),C(100,92,70))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD;zc=gz(*CAR)
# a Carrocha: o rochedo no meio do rio, com os degraus e a pedra chata no alto
M.append(['blobA',CAR[0],CAR[1],zc-0.3,[[0.38,0],[0.34,0.5],[0.26,1.0],[0.2,1.3]],8,'#8a867c'])
M.append(['capA',CAR[0],CAR[1],zc+1.0,0,0.2,8,'#9a968c'])
for k in range(6): M.append(['boxA',CAR[0]+0.25+k*0.035,CAR[1]+0.2,0.025,0.05,zc-0.2,zc+k*0.17,0.6,'#9a968c',None])
for k in range(7): M.append(['stone',CAR[0]+0.5+k*0.22,CAR[1]+0.28+0.05*math.sin(k)])
# a casa de Beorn: salão comprido de madeira, alas, colmeias, cerca de espinhos e carvalhos
zh=gz(*HOUSE)
M.append(['house',HOUSE[0],HOUSE[1],0.75,0.3,0.1,'#7a5a38','#8a7a46',0.3])
M.append(['house',HOUSE[0]-0.3,HOUSE[1]-0.38,0.4,0.2,1.67,'#7a5a38','#8a7a46',0.22])
M.append(['house',HOUSE[0]+0.35,HOUSE[1]-0.38,0.4,0.2,1.67,'#6e5232','#8a7a46',0.22])
M.append(['cyl',HOUSE[0],HOUSE[1],0.3,0.5,0.03,0.03,6,'#5a4a3a'])
for k in range(9): M.append(['blobA',HOUSE[0]-0.9+k*0.1,HOUSE[1]+0.5,gz(HOUSE[0]-0.9+k*0.1,HOUSE[1]+0.5)-0.01,[[0.035,0],[0.04,0.03],[0.025,0.07],[0,0.085]],7,'#d8b860'])
M.append(['hedge',[[round(HOUSE[0]+math.cos(a)*1.3,3),round(HOUSE[1]+math.sin(a)*1.0,3)] for a in np.linspace(0.25,6.28,36)],0.22])
for (dx,dy) in [(-0.9,-0.6),(0.95,-0.5),(1.0,0.55),(-1.0,0.35)]:
    x,y=HOUSE[0]+dx,HOUSE[1]+dy;z=gz(x,y);M.append(['cylA',x,y,z-0.05,z+0.5,0.05,0.04,6,'#4a3a28']);M.append(['blobA',x,y,z+0.35,[[0.16,0],[0.3,0.15],[0.24,0.4],[0,0.5]],8,'#3c6a34'])
for k in range(6):
    x,y=HOUSE[0]+R.rng.uniform(-1.0,1.0),HOUSE[1]+R.rng.uniform(0.2,0.8);M.append(['box',x,y,0.04,0.014,0.03,0.07,R.rng.uniform(0,6),['#5a3a22','#d8d0c0','#3a2618'][k%3],None])
# o Ninho das Águias, num pico a oeste (rochedo alto)
ze=gz(*EYRIE)
M.append(['blobA',EYRIE[0],EYRIE[1],ze-0.3,[[0.5,0],[0.4,0.8],[0.25,1.7],[0.12,2.3],[0.1,2.5]],7,'#7e7a72']);M.append(['capA',EYRIE[0],EYRIE[1],ze+2.2,0,0.11,7,'#9a968c'])
for _ in range(12000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.03 or R.at(roadm,x,y)>0.05 or math.hypot(x-HOUSE[0],y-HOUSE[1])<1.6: continue
    east=x>CAR[0]+14
    if R.rng.random()<(0.1 if east else 0.012): R.tree(x,y,R.rng.uniform(0.55,0.95),1 if R.rng.random()<0.7 else 0,(C(36,60,36) if east else C(64,100,50))*R.rng.uniform(0.85,1.1))
R.TOPS=[[CAR[0],CAR[1],1.5,0.4],[HOUSE[0],HOUSE[1],0.7,0.6],[EYRIE[0],EYRIE[1],2.8,0.4]]
R.PL={'RochedoCarrocha':CAR,'CasaBeorn':HOUSE,'ColmeiasBeorn':(HOUSE[0]-0.5,HOUSE[1]+0.5),'NinhoAguias':EYRIE,'VauCarrocha':(CAR[0]+1.2,CAR[1]+0.3),'BordaTrevas':(CAR[0]+17.0,181.0)}
R.save_json()
