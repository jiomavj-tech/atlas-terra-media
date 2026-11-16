import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('thranduil',606,112,646,146,PX=40,GR=5,seed=231,out='/tmp/claude-0/b6')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
water=R.base_water(0.5,0.1)
# o rio da Floresta, tirado do mapa-base; os salões ficam numa colina à beira dele
ys,xs=np.where(water>0.6);pts=np.stack([R.X0+xs/R.PX,R.Y0+ys/R.PX],1)
c=pts[np.argmin(np.hypot(pts[:,0]-629,pts[:,1]-130))]
GATE=(float(c[0]),float(c[1])-0.35);HALL=(GATE[0]+0.2,GATE[1]-1.2)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.012*nz+0.05*gauss(HALL[0],HALL[1],1.3,GX,GY)
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
fl=C(50,72,42)*(1-np.clip(n1+0.5,0,1))+C(38,56,36)*np.clip(n1+0.5,0,1)
img+=(fl*0.6+R.base_tex(10)*1.0*0.4)*(1+n2*0.08)
img=R.paint(img,np.clip(sstep(1.0,2.4,R.slope),0,1),C(104,100,92),0.7)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1),C(70,84,56),0.4)
img=R.paint(img,water,C(40,58,62))                           # rio escuro e rápido
PATH=[(R.X0-1,GATE[1]+3.5),(612,GATE[1]+2.8),(618,GATE[1]+2.0),(624,GATE[1]+1.3),(GATE[0]-0.4,GATE[1]+0.75),(GATE[0],GATE[1]+0.6)]
img,roadm=R.road(img,PATH,0.07,C(120,116,90),C(60,58,46))
fin=R.light(img,amb=0.56)
R.save_tex(fin)
M=R.MOD;zg=gz(*GATE)
ST='#8e8a7e'
# a ponte sobre o rio e os grandes portões de pedra na encosta
M.append(['bridge',GATE[0],GATE[1]+0.75,GATE[0],GATE[1]+0.05,0.14,1,'#9a968a'])
M.append(['boxA',GATE[0],GATE[1]-0.02,0.3,0.05,zg-0.2,zg+0.85,0,'#7a766c','#6a665c'])
M.append(['boxA',GATE[0],GATE[1]+0.035,0.12,0.012,zg,zg+0.55,0,'#2a3a2a',None])
M.append(['discA',GATE[0],GATE[1]+0.05,zg+0.55,0,1,0.12,'#2a3a2a'])
for s_ in (-1,1):
    M.append(['cylA',GATE[0]+s_*0.2,GATE[1]+0.06,zg-0.1,zg+0.75,0.035,0.03,8,ST]);M.append(['capA',GATE[0]+s_*0.2,GATE[1]+0.06,zg+0.78,0,0.03,6,[0.7,1.0,0.75,1.0]])
# lanternas na floresta e o salão do rei (clarabóias no alto da colina)
for k in range(6):
    a=k/6*6.28;x,y=HALL[0]+math.cos(a)*0.5,HALL[1]+math.sin(a)*0.5;M.append(['capA',x,y,gz(x,y)+0.03,0,0.05,8,[1.0,0.85,0.5,0.8]])
# o alçapão dos barris: a saída do riacho subterrâneo, rio abaixo
down=pts[np.argmin(np.hypot(pts[:,0]-(GATE[0]+2.2),pts[:,1]-(GATE[1]+0.9)))]
TRAP=(float(down[0]),float(down[1])-0.2);zt=gz(*TRAP)
M.append(['discA',TRAP[0],TRAP[1],zt+0.1,0,1,0.1,'#0c0c0c'])
for k in range(7):
    q=pts[np.argmin(np.hypot(pts[:,0]-(TRAP[0]+0.5+k*0.45),pts[:,1]-(TRAP[1]+0.3+k*0.25)))]
    M.append(['cylA',float(q[0]),float(q[1]),gz(q[0],q[1])-0.01,gz(q[0],q[1])+0.045,0.03,0.03,7,'#9a7448'])
# a clareira das festas dos elfos, com fogueira
FEAST=(GATE[0]-5.0,GATE[1]+4.2);zf=gz(*FEAST)
M.append(['capA',FEAST[0],FEAST[1],zf+0.02,0,0.06,8,[1.0,0.6,0.2,1.0]])
for k in range(10):
    a=k/10*6.28;M.append(['cylA',FEAST[0]+math.cos(a)*0.3,FEAST[1]+math.sin(a)*0.3,zf,zf+0.1,0.02,0.02,5,'#6a5a40'])
# teias das aranhas mais ao sul
WEB=(GATE[0]-8.5,GATE[1]+9.0);zw=gz(*WEB)
for k in range(8):
    a=k*0.8;M.append(['boxA',WEB[0]+math.cos(a)*0.4,WEB[1]+math.sin(a)*0.4,0.35,0.003,zw+0.2,zw+0.9,a+1.2,[0.85,0.85,0.8,0.1],None])
for _ in range(34000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.1: continue
    if math.hypot(x-GATE[0],y-GATE[1])<0.5 or math.hypot(x-FEAST[0],y-FEAST[1])<0.45: continue
    if R.rng.random()<0.12: R.tree(x,y,R.rng.uniform(0.75,1.2),1 if R.rng.random()<0.6 else 0,(C(34,56,34) if y>GATE[1]+5 else C(46,76,40))*R.rng.uniform(0.8,1.2))
R.TOPS=[[GATE[0],GATE[1],1.2,0.4]]
R.PL={'PortoesThranduil':GATE,'SalaoThranduil':HALL,'AlcapaoBarris':TRAP,'ClareiraElfos':FEAST,'TeiasAranhas':WEB,'RioFlorestaAlto':(float(down[0])+3.0,float(down[1])+1.6)}
R.save_json()
