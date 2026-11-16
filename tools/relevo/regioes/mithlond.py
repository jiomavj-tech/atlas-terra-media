import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('mithlond',142,256,180,290,PX=40,GR=5,seed=171,out='/tmp/claude-0/b5')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
water=R.base_water(0.5,0.1);wg=R.base_water_grid()
def shore_y(x,side):
    col=water[:,R.tp(x,0)[0]];c=np.where(col>0.5)[0];return R.Y0+(c.min() if side<0 else c.max())/R.PX
HX=160.4;S=(HX,shore_y(HX,1));N=(HX+2.0,shore_y(HX+2.0,-1))
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.01*nz
lvl=0.0
dist=cv2.distanceTransform((wg<0.45).astype(np.uint8),cv2.DIST_L2,5)/R.GR
hd=np.where(wg>0.45,lvl,lvl+0.006+(np.maximum(hd,lvl+0.01)-lvl)*sstep(0.3,5.0,dist)*0.8)
R.set_height(hd);gz=R.gz;ZW=lvl*HSW
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(108,140,72)*(1-np.clip(n1+0.5,0,1))+C(92,124,62)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((9,9),np.uint8))-water,0,1),C(196,186,150),0.6)
img=R.paint(img,water,C(70,116,140)*(1+R.noise(120,3,13)[...,None]*0.05))
TOWN=(S[0],S[1]+0.75)
img=R.paint(img,1-sstep(0.9,1.2,np.hypot((UX-TOWN[0])/1.4,UY-TOWN[1])),C(206,200,184),0.7)
ROAD=[(R.X1+1,281.0),(174,280.4),(168,278.6),(164,276.4),(TOWN[0]+0.4,TOWN[1]+0.6)]
img,roadm=R.road(img,ROAD,0.16,C(190,178,146),C(110,100,78))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD
WHITE='#f0eee6';GREY='#b8c0c4';ROOF='#7c98a8'
def town(c,n,seed):
    r=np.random.default_rng(seed);HP=[]
    for q in range(3000):
        x,y=c[0]+r.uniform(-1.3,1.3),c[1]+r.uniform(-0.75,0.75)
        if R.at(water,x,y)>0.1 or any(math.hypot(x-px,y-py)<0.2 for px,py in HP): continue
        HP.append((x,y))
        if len(HP)>n: break
        M.append(['house',round(x,3),round(y,3),0.18,0.13,round(r.uniform(0,3.1),2),WHITE,[ROOF,'#8aa6b4','#6a8898'][r.integers(3)],round(r.uniform(0.2,0.32),3)])
    return HP
HP=town(TOWN,45,1)
NT=(N[0],N[1]-0.75);HP+=town(NT,25,2)
# torres brancas dos Portos
for (x,y,h) in [(TOWN[0]-0.9,TOWN[1]-0.3,1.6),(TOWN[0]+0.9,TOWN[1]-0.35,1.3),(NT[0],NT[1]+0.3,1.4)]:
    M.append(['cyl',x,y,-0.05,h,0.09,0.07,8,WHITE]);M.append(['cyl',x,y,h,h+0.35,0.1,0.0,8,ROOF])
# cais de pedra e os navios élficos; o Navio Branco à espera
QUAY=(S[0],S[1]-0.05)
M.append(['boxA',QUAY[0],QUAY[1],1.3,0.07,ZW-0.1,ZW+0.1,0,GREY,None])
for k in range(3): M.append(['boxA',QUAY[0]-0.9+k*0.9,QUAY[1]-0.4,0.05,0.4,ZW-0.1,ZW+0.08,0,GREY,None])
SHIP=(QUAY[0]+0.45,QUAY[1]-0.95)
M.append(['blobA',SHIP[0],SHIP[1],ZW-0.02,[[0.1,0],[0.2,0.05],[0.18,0.12],[0,0.13]],10,WHITE])
M.append(['cylA',SHIP[0],SHIP[1],ZW+0.1,ZW+0.75,0.015,0.01,5,'#d8d4c8']);M.append(['boxA',SHIP[0],SHIP[1],0.012,0.2,ZW+0.3,ZW+0.7,0.2,[0.96,0.96,0.92,0.15],None])
M.append(['cylA',SHIP[0]-0.2,SHIP[1],ZW+0.08,ZW+0.32,0.02,0.01,5,WHITE])
for k,(dx,dy) in enumerate([(-0.9,-1.0),(-0.45,-0.9),(1.3,-0.8)]): M.append(['boat',QUAY[0]+dx,QUAY[1]+dy,1.4,'#f4f2ea','#e8e4d8'])
# estaleiro de Círdan
YARD=(TOWN[0]+1.6,S[1]+0.25)
M.append(['house',YARD[0],YARD[1],0.5,0.22,0.1,'#c8b890','#7c98a8',0.3])
M.append(['boat',YARD[0]+0.1,YARD[1]-0.4,0.1,'#f4f2ea','#c8b890'])
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.03 or R.at(roadm,x,y)>0.05 or any(math.hypot(x-px,y-py)<0.3 for px,py in HP): continue
    if R.rng.random()<0.02: R.tree(x,y,R.rng.uniform(0.5,0.8),1 if R.rng.random()<0.7 else 0,C(60,100,52)*R.rng.uniform(0.85,1.1))
R.TOPS=[[TOWN[0],TOWN[1],1.2,1.2]]
R.PL={'CaisMithlond':QUAY,'NavioBranco':SHIP,'TorresMithlond':(TOWN[0]-0.9,TOWN[1]-0.3),'EstaleiroCirdan':YARD,'MithlondNorte':NT,'GolfoLhun':(150.0,266.0),'EstradaPortos':(170.0,279.3)}
R.save_json()
