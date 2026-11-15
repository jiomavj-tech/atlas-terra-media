import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('edoras',458,505,492,535,PX=40,GR=5,seed=51,out='/tmp/claude-0/ro')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
E=(474.3,519.2);HR=1.5
RIVER=[(477.2,535.8),(476.8,531.0),(476.5,526.5),(476.7,523.0),(477.4,519.6),(478.6,516.4),(480.6,513.2),(483.4,510.2),(486.8,507.4),(490.2,505.4),(492.8,504.0)]
RP,RS=dense(RIVER);RT=cKDTree(RP)
def rinfo(X,Y):
    d,i=RT.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape),RS[i].reshape(X.shape)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),4);hbs=np.where(hbs>0.28,0.28+(hbs-0.28)*0.55,hbs)
nz=R.noise(8,5,3,True);nzf=R.noise(30,4,4,True)
hd=hbs+0.012*nz+0.004*nzf
# montanhas ao sul, com o vale do Snowbourn (Harrowdale) entrando nelas
hd=hd+0.16*sstep(527,535,GY)*(0.8+0.4*nz)
dr,sr=rinfo(GX,GY)
fl=0.21-0.06*sstep(0,16,sr)-0.03*sstep(16,40,sr)
wf=0.4+1.0*sstep(4,10,sr);wall=wf+1.8+3.0*sstep(8,18,sr)
fl=cv2.GaussianBlur(fl.astype(np.float32),(0,0),3);wf=cv2.GaussianBlur(wf.astype(np.float32),(0,0),3);wall=np.maximum(cv2.GaussianBlur(wall.astype(np.float32),(0,0),3),wf+0.5)
prof=fl+(hd-fl)*sstep(wf,wall,dr)
hd=np.where(dr<wall,np.minimum(hd,prof),hd)
hd=R.soften(hd,0.7,7)
# a colina de Edoras
rr=np.hypot(GX-E[0],GY-E[1])
z0=float(hd[int((E[1]-R.Y0)*5),int((E[0]-R.X0)*5)])
HT_=z0+0.036
hill=HT_-0.036*sstep(0.3,HR+0.8,rr)
hd=np.maximum(hd,np.where(rr<HR+0.7,hill,0))
# dique e vala ao pé da colina
hd=hd-0.006*np.exp(-((rr-(HR+0.05))/0.08)**2)
hd=hd-0.006*sstep(0.25,0.0,dr)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
DR,SR=rinfo(UX,UY);RRt=np.hypot(UX-E[0],UY-E[1])
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
grass=C(150,150,84)*(1-np.clip(n1+0.5,0,1))+C(118,132,70)*np.clip(n1+0.5,0,1)
img+=(grass*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.09)
rk=np.clip(sstep(1.5,2.8,R.slope)+sstep(0.36,0.44,R.HT),0,1)
img=R.paint(img,rk,C(130,126,118)*(1+R.noise(80,4,8)[...,None]*0.14),0.9)
snow=sstep(0.44,0.52,R.HT+0.03*R.noise(50,3,9));img=R.paint(img,snow,C(236,240,246))
# encosta da colina: grama verde viva e trilhas
img=R.paint(img,1-sstep(HR-0.1,HR+0.1,RRt),C(104,140,64),0.8)
GATE=(E[0]-0.05,E[1]-HR)
ROADN=[(474.0,R.Y0-1),(474.1,509.0),(474.2,513.0),(474.25,516.5),GATE]
img,roadm=R.road(img,ROADN,0.2,C(178,160,120),C(100,90,68))
ROADW=[(GATE[0]-0.4,GATE[1]+0.2),(472.0,518.2),(468.0,518.6),(463.0,519.2),(R.X0-1,519.6)]
img,rm2=R.road(img,ROADW,0.18,C(178,160,120),C(100,90,68))
ROADE=[(474.2,513.0),(477.0,513.4),(479.6,514.3),(R.X1+1,512.0)]
img,rm3=R.road(img,ROADE,0.15,C(178,160,120),C(100,90,68))
roadm=np.clip(roadm+rm2+rm3,0,1)
# rua que sobe a colina até Meduseld, com a escadaria e o canal da fonte
MED=(E[0]+0.05,E[1]+0.3)
STREET=[GATE,(E[0]+0.25,E[1]-0.85),(E[0]-0.2,E[1]-0.45),(E[0]+0.05,E[1]-0.12)]
img,sm=R.road(img,STREET,0.09,C(170,156,128),C(110,100,80))
img=R.paint(img,R.line_mask([(E[0]+0.1,E[1]-0.1),(E[0]+0.32,E[1]-0.86)],0.03,0.6),C(150,196,220))
# túmulos dos reis com simbelmynë (flores brancas)
MOUNDS=[]
for k in range(9): MOUNDS.append((474.1-0.75-0.2*(k%2),510.6+k*0.6))
for k in range(7): MOUNDS.append((474.2+0.75+0.2*(k%2),510.9+k*0.66))
mm=np.zeros((R.TH,R.TW),np.float32)
for x,y in MOUNDS: cv2.circle(mm,R.tp(x,y),int(0.26*R.PX),1.0,-1,cv2.LINE_AA)
mm=cv2.GaussianBlur(mm,(0,0),2)
img=R.paint(img,mm,C(96,138,60),0.8)
fl_=(R.rng.random((R.TH,R.TW))<0.12)*(mm>0.3)
img=R.paint(img,fl_.astype(np.float32),C(240,240,236),0.9)
# água
water=np.clip((0.1+0.12*sstep(4,14,SR)-DR)/0.035+0.5,0,1)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1),C(98,110,74),0.4)
img=R.paint(img,water,C(64,100,122))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zt=HT_*HSW
THATCH=['#9a8a50','#8a7a46','#a8935a','#7e8a4a'];WOOD=['#8a6a44','#7a5a3a','#9a7650','#6e5236']
# paliçada no alto do dique e o portão
pal=[]
for k in range(73):
    a=k/72*2*math.pi
    if abs(((a-(-math.pi/2)+math.pi)%(2*math.pi))-math.pi)<0.08: pal.append(None);continue
    pal.append([round(E[0]+math.cos(a)*(HR+0.12),3),round(E[1]+math.sin(a)*(HR+0.12),3)])
seg=[];segs=[]
for p in pal:
    if p is None:
        if seg: segs.append(seg);seg=[]
    else: seg.append(p)
if seg: segs.append(seg)
if len(segs)>1 and segs[-1][-1]==segs[0][0]: segs[0]=segs[-1]+segs[0];segs.pop()
for sg in segs: M.append(['wall',sg,0.22,'#6e5236',0.05])
for s_ in (-1,1):
    x,y=GATE[0]+s_*0.14,GATE[1]-0.08
    M.append(['cyl',x,y,-0.1,0.45,0.05,0.05,6,'#6e5236']);M.append(['cyl',x,y,0.45,0.58,0.065,0.0,6,'#4e6a3a'])
M.append(['box',GATE[0],GATE[1]-0.08,0.15,0.02,0.32,0.4,0,'#6e5236',None])
# casas de madeira com telhados de palha nas encostas
nh=0
HP=[]
for q in range(4000):
    a=R.rng.uniform(0,2*math.pi);r=math.sqrt(R.rng.uniform(0.2,1.0))*(HR-0.12);x,y=E[0]+math.cos(a)*r,E[1]+math.sin(a)*r
    if r<0.38 or math.hypot(x-MED[0],y-MED[1])<0.5: continue
    if any(math.hypot(x-px,y-py)<0.12 for px,py in STREET): continue
    if any(math.hypot(x-px,y-py)<0.17 for px,py in HP): continue
    HP.append((x,y));rot=a+math.pi/2+R.rng.uniform(-0.3,0.3)
    w_=R.rng.uniform(0.07,0.1);d_=R.rng.uniform(0.05,0.07)
    M.append(['house',round(x,3),round(y,3),round(w_*2,3),round(d_*2,3),round(rot,3),WOOD[R.rng.integers(4)],THATCH[R.rng.integers(4)],round(R.rng.uniform(0.1,0.15),3)]);nh+=1
# Meduseld: o Paço Dourado no topo, sobre um terraço de pedra
ang=-0.15
M.append(['boxA',MED[0],MED[1],0.42,0.2,zt-0.3,zt+0.05,ang,'#b9b09a','#b9b09a'])
M.append(['boxA',MED[0],MED[1],0.32,0.12,zt+0.05,zt+0.3,ang,'#7a5a36','#d9a832'])
for s_ in (-1,1):
    x,y=MED[0]+math.cos(ang)*0.33*s_,MED[1]+math.sin(ang)*0.33*s_
    M.append(['cylA',x,y,zt+0.05,zt+0.38,0.012,0.006,4,'#d9a832'])
M.append(['discA',MED[0]-math.sin(ang)*0.125,MED[1]+math.cos(ang)*-0.125,zt+0.15,-math.sin(-ang+math.pi),-math.cos(ang),0.04,[1.0,0.82,0.45,0.6]])
# escadaria até o terraço
for k in range(4):
    x,y=E[0]+0.05,E[1]-0.12+k*0.06
    M.append(['boxA',x,y,0.12,0.03,zt-0.35,zt-0.25+k*0.07,0,'#c2b8a0',None])
# túmulos dos reis
for x,y in MOUNDS: M.append(['blobA',x,y,gz(x,y)-0.05,[[0.24,0],[0.2,0.08],[0.1,0.14],[0,0.16]],10,'#5f8c40'])
# ponte sobre o Snowbourn na estrada do leste
bi=int(np.argmin(np.hypot(RP[:,0]-479.7,RP[:,1]-514.4)));bp=RP[bi]
M.append(['bridge',float(bp[0]-0.45),float(bp[1]-0.12),float(bp[0]+0.45),float(bp[1]+0.12),0.22,2,'#a89e88'])
# cavalos pastando nos campos
for q in range(60):
    x,y=R.rng.uniform(462,490),R.rng.uniform(506,526)
    if math.hypot(x-E[0],y-E[1])<HR+1.2 or R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.05: continue
    r=R.rng.uniform(0,6.28);c=['#5a3a22','#3a2618','#8a6a48','#d8d0c0'][R.rng.integers(4)]
    M.append(['box',x,y,0.04,0.014,0.03,0.07,r,c,None])
# árvores: salgueiros no rio, algumas nos campos, pinheiros nas montanhas
for _ in range(14000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.02 or R.at(roadm,x,y)>0.05 or R.at(snow,x,y)>0.1 or math.hypot(x-E[0],y-E[1])<HR+0.3: continue
    d_=float(RT.query([x,y])[0])
    if d_<0.6 and R.rng.random()<0.12: R.tree(x,y,R.rng.uniform(0.5,0.75),2,C(96,130,64)*R.rng.uniform(0.85,1.1))
    elif R.at(R.HT,x,y)>0.27 and R.at(rk,x,y)<0.5 and R.rng.random()<0.03: R.tree(x,y,R.rng.uniform(0.6,0.9),0,C(40,70,44)*R.rng.uniform(0.85,1.1))
    elif R.rng.random()<0.002: R.tree(x,y,R.rng.uniform(0.5,0.7),1,C(80,110,52))
R.TOPS=[[MED[0],MED[1],round(zt+0.55-gz(*MED),2),0.3],[GATE[0],GATE[1],0.7,0.2]]
R.PL={'Meduseld':MED,'PortaoEdoras':GATE,'TumulosReis':(474.15,513.0),'EscadariaMeduseld':(E[0]+0.05,E[1]-0.2),'RioSnowbourn':tuple(RP[int(len(RP)*0.45)]),
      'PalicadaEdoras':(E[0]+HR+0.12,E[1]),'EstradaOeste':(465.0,518.9)}
print('casas',nh)
R.save_json()
