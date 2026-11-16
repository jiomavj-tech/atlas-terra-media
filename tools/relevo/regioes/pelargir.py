import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('pelargir',536,622,574,656,PX=40,GR=5,seed=191,out='/tmp/claude-0/b5')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
water=R.base_water(0.5,0.1);wg=R.base_water_grid()
def shore_x(y,side):
    row=water[R.tp(0,y)[1]];c=np.where(row>0.5)[0];return R.X0+(c.min() if side<0 else c.max())/R.PX
YC=638.5;XW=shore_x(YC,-1);C0=(XW-1.3,YC)
SIR=[(R.X0-1,628.0),(541,629.6),(545,632.0),(548.0,635.2),(XW-0.3,636.4),(XW+0.3,636.8)]      # rio Sirith
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.008*nz
sm=cv2.resize(R.line_mask(SIR,0.3,2),(R.GW,R.GH))
wall=np.maximum((wg>0.45).astype(np.float32),(sm>0.4).astype(np.float32))
lvl=0.02
dist=cv2.distanceTransform((wall<0.5).astype(np.uint8),cv2.DIST_L2,5)/R.GR
hd=np.where(wall>0.5,lvl,lvl+0.005+(np.maximum(hd,lvl+0.01)-lvl)*sstep(0.2,3.0,dist))
R.set_height(hd);gz=R.gz;ZW=lvl*HSW
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(124,146,74)*(1-np.clip(n1+0.5,0,1))+C(104,128,64)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
lab=cv2.resize(R.rng.integers(0,5,(30,34)).astype(np.float32),(R.TW,R.TH),interpolation=cv2.INTER_NEAREST)
PAL=np.array([C(140,156,76),C(170,164,90),C(120,146,66),C(190,176,104),C(110,140,62)])
img=R.paint(img,np.clip(1-np.hypot((UX-C0[0])/8,(UY-C0[1])/7),0,1),PAL[lab.astype(int)],0.45)
water=np.maximum(water,np.clip(R.line_mask(SIR,0.22,0.8)*1.5,0,1))
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((7,7),np.uint8))-water,0,1),C(120,116,84),0.5)
img=R.paint(img,water,C(64,100,124)*(1+R.noise(120,3,13)[...,None]*0.05))
dT=np.hypot((UX-C0[0])/1.25,(UY-C0[1])/1.6)
img=R.paint(img,(1-sstep(0.85,1.0,dT))*(1-np.clip(water*3,0,1)),C(196,186,164),0.7)
ROAD=[(R.X0-1,640.5),(544,640.0),(C0[0]-1.1,C0[1]+0.3)]
img,roadm=R.road(img,ROAD,0.14,C(184,170,134),C(104,94,72))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD
WALLS=['#e6dcc4','#dccfb0','#efe6d2'];ROOFS=['#a8522e','#b86a36','#8a4630','#c08040']
HP=[]
for q in range(5000):
    a=R.rng.uniform(0,6.28);rr=math.sqrt(R.rng.uniform(0,1));x,y=C0[0]+math.cos(a)*rr*1.1,C0[1]+math.sin(a)*rr*1.45
    if R.at(water,x,y)>0.1 or any(math.hypot(x-px,y-py)<0.17 for px,py in HP): continue
    HP.append((x,y))
    if len(HP)>130: break
    M.append(['house',round(x,3),round(y,3),0.17,0.12,round(R.rng.uniform(0,3.1),2),WALLS[R.rng.integers(3)],ROOFS[R.rng.integers(4)],round(R.rng.uniform(0.18,0.34),3)])
wp=[[round(C0[0]+math.cos(a)*1.3,3),round(C0[1]+math.sin(a)*1.68,3)] for a in np.linspace(0.9,2*math.pi-0.9,50)]
M.append(['wall',wp,0.3,'#cfc4a8',0.07])
for a in np.linspace(0.9,2*math.pi-0.9,7):
    x,y=C0[0]+math.cos(a)*1.3,C0[1]+math.sin(a)*1.68;M.append(['cyl',x,y,-0.1,0.6,0.09,0.08,8,'#cfc4a8']);M.append(['cyl',x,y,0.6,0.8,0.1,0.0,8,'#a8522e'])
M.append(['cyl',C0[0]-0.2,C0[1],-0.05,1.3,0.1,0.08,8,'#efe6d2']);M.append(['cyl',C0[0]-0.2,C0[1],1.3,1.6,0.11,0.0,8,'#a8522e'])
# o porto: cais de pedra e a frota negra dos Corsários de Umbar
for k in range(5):
    y=YC-1.2+k*0.6;M.append(['boxA',XW+0.35,y,0.4,0.05,ZW-0.1,ZW+0.09,0,'#b8b0a0',None])
M.append(['boxA',XW+0.0,YC,0.06,1.4,ZW-0.1,ZW+0.1,0,'#b8b0a0',None])
FLEET=(XW+1.6,YC)
for k in range(11):
    M.append(['boat',FLEET[0]+(k%3)*0.55+R.rng.uniform(-0.1,0.1),YC-1.6+k*0.32,1.57+R.rng.uniform(-0.2,0.2),'#1c1a1c'])
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.03 or R.at(roadm,x,y)>0.05 or math.hypot((x-C0[0])/1.4,(y-C0[1])/1.8)<1: continue
    if R.rng.random()<0.012: R.tree(x,y,R.rng.uniform(0.5,0.75),1,C(70,108,50)*R.rng.uniform(0.85,1.1))
R.TOPS=[[C0[0],C0[1],1.6,1.2]]
R.PL={'CidadePelargir':C0,'CaisPelargir':(XW+0.3,YC),'FrotaNegra':FLEET,'RioSirith':(545.0,632.0),'AnduinPelargir':((XW+shore_x(YC+8,1))/2+1,YC+8)}
R.save_json()
