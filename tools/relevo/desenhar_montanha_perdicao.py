import numpy as np, cv2, json, math
from PIL import Image
rng=np.random.default_rng(23)
X0,Y0,X1,Y1=663.0,544.0,715.0,588.0
PX=32;TW,TH=int((X1-X0)*PX),int((Y1-Y0)*PX)
GR=5;GW,GH=int((X1-X0)*GR)+1,int((Y1-Y0)*GR)+1
HSW=46*1.35
ME='/tmp/claude-0/me/'
VC=(690.6,564.6)
def tp(x,y): return (int(round((x-X0)*PX)),int(round((y-Y0)*PX)))
def noise(base,octv,seed,w=TW,h=TH):
    r=np.random.default_rng(seed);out=np.zeros((h,w),np.float32);a=1;t=0
    for o in range(octv):
        n=r.standard_normal((int(base*2**o*h/w)+2,base*2**o+2)).astype(np.float32);out+=cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
    return out/t
def gauss(cx,cy,s,X,Y): return np.exp(-((X-cx)**2+(Y-cy)**2)/(2*s*s))
def sstep(a,b,x): t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
C=lambda r,g,b: np.array([r,g,b],np.float32)/255
ux=np.linspace(X0,X1,TW,dtype=np.float32);uy=np.linspace(Y0,Y1,TH,dtype=np.float32);UX,UY=np.meshgrid(ux,uy)
gx=np.linspace(X0,X1,GW);gy=np.linspace(Y0,Y1,GH);GX,GY=np.meshgrid(gx,gy)
# ---------- relevo ----------
hm=np.asarray(Image.open(ME+'height_hi.png').convert('RGB')).astype(np.float32)
h492=((hm[...,0]*256+hm[...,1])/65535*1.25-0.05)
fx=GX/984*491;fy=GY/877*437;i0=np.floor(fx).astype(int);j0=np.floor(fy).astype(int);u=fx-i0;v=fy-j0
hb=(h492[j0,i0]*(1-u)+h492[j0,i0+1]*u)*(1-v)+(h492[j0+1,i0]*(1-u)+h492[j0+1,i0+1]*u)*v
fade=np.clip(np.minimum.reduce([GX-X0,X1-GX,GY-Y0,Y1-GY])/4.0,0,1)
nzg=noise(8,5,3,GW,GH);nzf=noise(30,4,4,GW,GH)
# planalto de Gorgoroth: cinza ondulada, com valas e montes
plain=0.16+0.012*nzg+0.006*nzf
ang=np.arctan2(GY-VC[1],GX-VC[0]);R=np.hypot(GX-VC[0],GY-VC[1])
wob=1+0.10*np.sin(ang*3+0.7)+0.06*np.sin(ang*7+2.0)+0.05*nzg
Rm=R/wob
mound=0.16+0.12*np.clip(1-((Rm-6.0)/7.5),0,1)**1.5
mound=np.where(Rm<=6.0,0.28,mound)
# ravinas radiais na base
gul=(np.abs(np.sin(ang*11+nzg*2.0))**6)*sstep(6,8,Rm)*(1-sstep(11,13,Rm))
mound=mound-0.008*gul
cone=0.28+0.19*np.clip(1-(R*(1+0.05*np.sin(ang*5))-1.0)/5.2,0,1)**1.15
hd=np.maximum(plain,mound)
hd=np.where(R<6.3,np.maximum(hd,cone),hd)
# cratera no topo
hd=np.where(R<1.0,0.47-0.05*sstep(0.95,0.25,R),hd)
# colina de cinzas (onde Frodo e Sam esperaram o fim)
ASH=(683.2,572.6)
hd=np.maximum(hd,0.16+0.05*gauss(*ASH,0.9,GX,GY))
hd=hd*fade+hb*(1-fade)
enc=np.clip((hd+0.05)/1.25,0,1)*65535
Image.fromarray(np.dstack([(enc//256).astype(np.uint8),(enc%256).astype(np.uint8),np.zeros((GH,GW),np.uint8)]),'RGB').save('md_h.png',optimize=True)
def gz(x,y):
    fx=(x-X0)*GR;fy=(y-Y0)*GR;i=min(GW-2,int(fx));j=min(GH-2,int(fy));uu=fx-i;vv=fy-j
    return float(((hd[j,i]*(1-uu)+hd[j,i+1]*uu)*(1-vv)+(hd[j+1,i]*(1-uu)+hd[j+1,i+1]*uu)*vv)*HSW)
HT=cv2.resize(hd.astype(np.float32),(TW,TH),interpolation=cv2.INTER_CUBIC)
def mask_at(m,x,y): px,py=tp(x,y);return m[min(TH-1,max(0,py)),min(TW-1,max(0,px))]
RT=np.hypot(UX-VC[0],UY-VC[1])
# ---------- cores ----------
img=np.zeros((TH,TW,3),np.float32)
n1=noise(60,4,5)[...,None];n2=noise(200,3,6)[...,None]
ash=C(96,88,82)*(1-np.clip(n1*0.8+0.4,0,1))+C(70,62,58)*np.clip(n1*0.8+0.4,0,1)
_bt=cv2.resize(np.asarray(Image.open(ME+'me_tex.webp').convert('RGB')).astype(np.float32)[int(Y0*2):int(Y1*2),int(X0*2):int(X1*2)]/255,(TW,TH),interpolation=cv2.INTER_CUBIC)
_bt=cv2.GaussianBlur(_bt,(0,0),20)
farm=sstep(9,16,np.hypot(UX-VC[0],UY-VC[1]))[...,None]*0.55
img+=(ash*(1-farm)+_bt*1.15*farm)*(1+n2*0.10)
slope=np.hypot(*np.gradient(cv2.GaussianBlur(HT,(0,0),2)*HSW,1/PX,1/PX))
rk=sstep(0.6,1.6,slope)
basalt=C(46,40,40)*(1+noise(120,3,7)[...,None]*0.15)
img=img*(1-rk[...,None]*0.75)+basalt*rk[...,None]*0.75
coneM=1-sstep(5.8,6.6,RT)
img=img*(1-coneM[...,None]*0.6)+C(40,34,34)*coneM[...,None]*0.6
angT=np.arctan2(UY-VC[1],UX-VC[0])
streak=(0.5+0.5*np.sin(angT*41+noise(30,3,50)*5+RT*0.6))**3
cs=coneM*(0.35*streak+0.25*np.clip(noise(90,3,51)+0.3,0,1))
img=img*(1-cs[...,None])+C(92,78,70)*cs[...,None]
scorch=(1-sstep(0.9,2.2,RT))
img=img*(1-scorch[...,None]*0.5)+C(70,34,22)*scorch[...,None]*0.5
# estrada de Sauron: calçada vinda do leste e espiral até a porta
DOORA=0.05;DOOR=(VC[0]+2.6*math.cos(DOORA),VC[1]+2.6*math.sin(DOORA))
ROAD=[(X1+1,556.0),(710,558.2),(705,560.3),(700.5,562.0)]
for k in range(41):
    t=k/40;a=-0.55+t*(2*math.pi+DOORA+0.55);r=6.6-4.0*t
    ROAD.append((VC[0]+r*math.cos(a),VC[1]+r*math.sin(a)))
ROAD.append(DOOR)
def road(pts,w,col,ecol):
    global img
    m=np.zeros((TH,TW),np.float32);cv2.polylines(m,[np.array([tp(x,y) for x,y in pts],np.int32)],False,1.0,max(1,int(w*PX)),cv2.LINE_AA);m=cv2.GaussianBlur(m,(0,0),0.9)
    e=np.clip(cv2.dilate(m,np.ones((5,5),np.uint8))-m,0,1)
    img=img*(1-e[...,None]*0.5)+ecol*e[...,None]*0.5;img=img*(1-m[...,None])+col*m[...,None]
    return m
roadm=road(ROAD,0.26,C(120,108,96),C(30,26,26))
# trilha de orcs vinda do noroeste (por onde os hobbits cruzaram Gorgoroth)
ORC=[(X0-1,551.0),(668,553.0),(673,555.6),(678,558.4),(683,561.0),(686.3,562.4)]
road(ORC,0.12,C(110,100,90),C(40,34,32))
# rios de lava (escorrem da cratera e atravessam a planície)
FLOWS=[[(VC[0]-0.6,VC[1]+0.5),(689.0,566.6),(687.4,568.6),(685.6,570.4),(684.6,571.4),(682.0,571.8),(679.0,573.4),(676.0,576.6),(673.5,580.5)],
       [(VC[0]-0.2,VC[1]+0.8),(690.0,567.5),(689.6,570.2),(688.4,572.8),(686.6,574.0),(684.8,574.4),(682.5,575.2),(681.0,578.6)],
       [(VC[0]-0.75,VC[1]-0.2),(688.6,563.6),(686.6,562.9),(684.4,563.4),(682.0,564.9),(679.4,565.0),(676.5,566.2)]]
lava=np.zeros((TH,TW),np.float32)
for fl in FLOWS:
    L=len(fl)
    for i,((ax,ay),(bx,by)) in enumerate(zip(fl[:-1],fl[1:])):
        w=0.22+0.3*i/L
        cv2.line(lava,tp(ax,ay),tp(bx,by),1.0,max(2,int(w*PX)),cv2.LINE_AA)
lava=cv2.GaussianBlur(lava,(0,0),2.0)
lava=np.clip(lava*1.4,0,1)
lpool=np.clip((0.8-np.hypot((UX-674.0)/2.2,(UY-579.0)/1.4))*2,0,1)+np.clip((0.8-np.hypot((UX-680.6)/1.3,(UY-579.6)/0.9))*2,0,1)
lava=np.clip(lava+lpool,0,1)
# fendas incandescentes no planalto
cr=np.zeros((TH,TW),np.float32)
for q in range(40):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    if math.hypot(x-VC[0],y-VC[1])<6: continue
    pts=[(x,y)];a=rng.uniform(0,math.pi)
    for k in range(rng.integers(3,8)):
        a+=rng.uniform(-0.7,0.7);x+=math.cos(a)*rng.uniform(0.3,0.8);y+=math.sin(a)*rng.uniform(0.3,0.8);pts.append((x,y))
    cv2.polylines(cr,[np.array([tp(*p) for p in pts],np.int32)],False,1.0,2,cv2.LINE_AA)
crk=cv2.GaussianBlur(cr,(0,0),0.8)
img=img*(1-crk[...,None]*0.8)+C(24,18,18)*crk[...,None]*0.8
# ---------- luz assada ----------
hf=cv2.GaussianBlur(HT,(0,0),3)*HSW
gy_,gx_=np.gradient(hf,1/PX,1/PX)
Lv=np.array([-0.62,-0.55,0.56]);Lv/=np.linalg.norm(Lv)
nn=np.dstack([-gx_,-gy_,np.ones_like(hf)]);nn/=np.linalg.norm(nn,axis=2,keepdims=True)
lam=np.clip(nn@Lv,0,1);flatL=float(Lv[2])
Lt=(0.62+0.55*(lam-flatL)+0.42*flatL)
dim=np.array([0.95,0.86,0.80])                      # céu enfumaçado: luz baça e avermelhada
fin=img*dim*Lt[...,None]
# brilho da lava (depois da luz: não escurece)
glow=cv2.GaussianBlur(lava,(0,0),10)*0.55+cv2.GaussianBlur(crk,(0,0),3)*0.35
fin=fin+np.array([0.55,0.16,0.03])*glow[...,None]
lcol=C(255,120,20)*(1-np.clip(noise(150,3,9)*0.8+0.3,0,1)[...,None])+C(255,210,80)*np.clip(noise(150,3,9)*0.8+0.3,0,1)[...,None]
crust=np.clip(noise(260,2,10)*2-0.6,0,1)[...,None]*0.6
lcol=lcol*(1-crust)+C(40,20,16)*crust
fin=fin*(1-lava[...,None])+lcol*lava[...,None]
cg=cr*0.0+cv2.GaussianBlur(cr,(0,0),0.4)
fin=fin*(1-cg[...,None]*0.45)+C(230,80,20)*cg[...,None]*0.45
# lago de fogo na cratera
crat=1-sstep(0.45,0.75,RT)
fin=fin*(1-crat[...,None])+C(255,140,40)*crat[...,None]
tex=np.asarray(Image.open(ME+'me_tex.webp').convert('RGB')).astype(np.float32)/255
lm=np.asarray(Image.open(ME+'light_hi.png').convert('RGB')).astype(np.float32)/255
def crop_up(a_,sc): return cv2.resize(a_[int(Y0*sc):int(Y1*sc),int(X0*sc):int(X1*sc)],(TW,TH),interpolation=cv2.INTER_CUBIC)
cool=np.array([0.55,0.62,0.82]);warm=np.array([1.10,1.02,0.88])
bt=crop_up(tex,2);bl=crop_up(lm,1);Lb=bl[...,0]*1.3;mb=np.clip(Lb,0,1.2)[...,None]/1.2
base=bt*(cool*(1-mb)+warm*mb)*Lb[...,None]
bw=np.clip((np.minimum.reduce([UX-X0,X1-UX,UY-Y0,Y1-UY])-0.5)/6.0,0,1)[...,None]**1.5
out=np.clip(fin*bw+base*(1-bw),0,1)
cv2.imwrite('md_tex.webp',cv2.cvtColor((out*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,88])
Image.fromarray((out*255).astype(np.uint8)).resize((TW//2,TH//2)).save('prev.png')
# ================= MODELOS =================
MOD=[];TREES=[]
FIRE=[1.0,0.45,0.08,1.0];FIRE2=[1.0,0.62,0.18,1.0];DARK='#2a2424';BLACK='#141214'
# cratera: anel de rocha e lago de fogo
zr=gz(VC[0]+0.9,VC[1])
MOD.append(['capA',VC[0],VC[1],zr-1.2,0,0.62,20,FIRE2])
# Sammath Naur: a porta na face leste do cone
dz=gz(*DOOR);nx,ny=math.cos(DOORA),math.sin(DOORA)
MOD.append(['boxA',DOOR[0]+nx*0.1,DOOR[1]+ny*0.1,0.12,0.28,dz-0.3,dz+0.55,DOORA,DARK,DARK])
MOD.append(['discA',DOOR[0]+nx*0.23,DOOR[1]+ny*0.23,dz+0.18,nx,ny,0.16,FIRE])
# calçada elevada da Estrada de Sauron no planalto
CW=[p for p in ROAD[:5]]
MOD.append(['wall',[[round(x,2),round(y,2)] for x,y in CW],0.18,'#3a3230',0.32])
# torres de vigia e acampamentos de orcs
for (x,y) in [(706.5,557.4),(702.8,563.6),(698.4,558.2),(675.2,553.2),(671.5,560.8),(708.6,571.0)]:
    z=gz(x,y);MOD.append(['cylA',x,y,z-0.2,z+1.4,0.2,0.15,6,DARK]);MOD.append(['cylA',x,y,z+1.4,z+1.7,0.24,0.0,6,BLACK]);MOD.append(['discA',x+0.18,y,z+1.2,1,0,0.05,FIRE])
for (x,y) in [(704.0,566.5),(697.0,553.0),(676.5,557.0),(709.0,575.0),(668.5,582.0)]:
    for q in range(7):
        a=rng.uniform(0,2*math.pi);r=rng.uniform(0.2,0.9);xx,yy=x+math.cos(a)*r,y+math.sin(a)*r
        MOD.append(['blobA',xx,yy,gz(xx,yy)-0.02,[[0.16,0],[0.12,0.12],[0,0.2]],5,'#3c3230'])
    MOD.append(['discA',x,y,gz(x,y)+0.05,0,0,0.12,FIRE]) if False else MOD.append(['capA',x,y,gz(x,y)+0.04,0,0.1,8,FIRE])
# fumarolas: bocas de fogo e fumaça
for q in range(26):
    x,y=rng.uniform(X0+3,X1-3),rng.uniform(Y0+3,Y1-3)
    if math.hypot(x-VC[0],y-VC[1])<6 or mask_at(lava,x,y)>0.1 or mask_at(roadm,x,y)>0.1: continue
    z=gz(x,y);MOD.append(['capA',x,y,z+0.03,0,0.07,8,FIRE])
    MOD.append(['blobA',x,y,z+0.02,[[0.16,0],[0.12,0.08],[0.07,0.1]],8,'#3a3230'])
# rochas e pedregulhos
for q in range(160):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    if math.hypot(x-VC[0],y-VC[1])<5.4 or mask_at(lava,x,y)>0.05 or mask_at(roadm,x,y)>0.05: continue
    s=rng.uniform(0.08,0.28);MOD.append(['box',x,y,s,s*rng.uniform(0.5,1),-0.08,s*rng.uniform(0.6,1.4),rng.uniform(0,3),'#3a3434',None])
# árvores mortas e espinheiros esparsos (troncos secos)
for q in range(120):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    if math.hypot(x-VC[0],y-VC[1])<8 or mask_at(lava,x,y)>0.05: continue
    MOD.append(['cyl',x,y,-0.05,rng.uniform(0.25,0.55),0.03,0.008,4,'#2c2420'])
# ---------- lugares ----------
SAM=(686.6,562.2)
PL={'SammathNaur':DOOR,'CrateraOrodruin':VC,'EstradaSauron':ROAD[12],'Gorgoroth':(674.0,553.5),'SubidaSam':SAM,'ColinaCinzas':ASH,'RiosLava':(678.0,574.0)}
TOPS=[[round(DOOR[0],2),round(DOOR[1],2),0.8,0.3],[round(VC[0],2),round(VC[1],2),0.6,0.8]]
def _c(o):
    if isinstance(o,(list,tuple,np.ndarray)): return [_c(v) for v in o]
    if isinstance(o,(np.floating,float)): return round(float(o),3)
    if isinstance(o,np.integer): return int(o)
    return o
json.dump({'rect':[X0,Y0,X1,Y1],'models':_c(MOD),'trees':TREES,'tops':_c(TOPS),'places':{k:[round(float(x),2),round(float(y),2)] for k,(x,y) in PL.items()}},open('md.json','w'),separators=(',',':'))
import os;print('modelos',len(MOD),'pico',round(gz(VC[0]+0.95,VC[1]),1),{f:os.path.getsize(f) for f in ['md_tex.webp','md_h.png','md.json']})
