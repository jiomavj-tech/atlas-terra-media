import numpy as np, cv2, json, math
from PIL import Image
from scipy.spatial import cKDTree
rng=np.random.default_rng(11)
X0,Y0,X1,Y1=398.0,236.0,446.0,278.0
PX=32;TW,TH=int((X1-X0)*PX),int((Y1-Y0)*PX)
GR=5;GW,GH=int((X1-X0)*GR)+1,int((Y1-Y0)*GR)+1
HSW=46*1.35
ME='/tmp/claude-0/me/'
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

# ---------- o rio Bruinen ----------
RV=[(441.2,245.2),(438.5,246.0),(435.5,247.4),(432.5,248.6),(429.6,249.7),(427.0,251.0),(425.0,252.6),(423.6,254.6),(422.6,257.0),(421.6,259.6),(420.3,262.4),(419.0,265.2),(418.4,267.4),(417.6,270.0),(416.8,273.0),(416.2,276.0),(416.0,279.5)]
def dense(pts,step=0.04):
    o=[];s=[];acc=0
    for (ax,ay),(bx,by) in zip(pts[:-1],pts[1:]):
        L=math.hypot(bx-ax,by-ay);n=max(1,int(L/step))
        for k in range(n): o.append((ax+(bx-ax)*k/n,ay+(by-ay)*k/n));s.append(acc+L*k/n)
        acc+=L
    o.append(pts[-1]);s.append(acc);return np.array(o),np.array(s)
RP,RS=dense(RV)
_t=np.gradient(RP,axis=0);_t/=np.linalg.norm(_t,axis=1,keepdims=True);RN=np.stack([-_t[:,1],_t[:,0]],1)
RP=RP+RN*(0.22*np.sin(RS*1.3)+0.12*np.sin(RS*3.1+1.0))[:,None]*np.clip(RS/2,0,1)[:,None]
TREE=cKDTree(RP)
def rinfo(X,Y):
    d,i=TREE.query(np.stack([X.ravel(),Y.ravel()],1));return d.reshape(X.shape),RP[i,1].reshape(X.shape),RS[i].reshape(X.shape),i.reshape(X.shape)
FORD=(418.4,267.4)
HOUSE=(422.0,252.85)
# largura do rio (meia-largura) e piso do vale ao longo do rio
def half_w(yr): return 0.16+0.10*sstep(250,262,yr)+0.30*np.exp(-((yr-FORD[1])/1.1)**2)
def floor_h(s):  # s = distância ao longo do rio a partir da nascente
    return 0.30-0.105*sstep(0,17,s)-0.04*sstep(17,30,s)-0.015*sstep(30,40,s)
# ---------- relevo ----------
hm=np.asarray(Image.open(ME+'height_hi.png').convert('RGB')).astype(np.float32)
h492=((hm[...,0]*256+hm[...,1])/65535*1.25-0.05)
fx=GX/984*491;fy=GY/877*437;i0=np.floor(fx).astype(int);j0=np.floor(fy).astype(int);u=fx-i0;v=fy-j0
hb=(h492[j0,i0]*(1-u)+h492[j0,i0+1]*u)*(1-v)+(h492[j0+1,i0]*(1-u)+h492[j0+1,i0+1]*u)*v
fade=np.clip(np.minimum.reduce([GX-X0,X1-GX,GY-Y0,Y1-GY])/4.0,0,1)
hbs=cv2.GaussianBlur(hb.astype(np.float32),(0,0),3)
hbs=np.where(hbs>0.30,0.30+(hbs-0.30)*0.6,hbs)
nzg=noise(8,5,3,GW,GH)
# planalto de charneca a oeste do vale, montanhas a leste
moor=0.235+0.02*nzg-0.03*sstep(262,278,GY)-0.02*sstep(408,398,GX)
east=sstep(429,440,GX+0.6*(GY-250))
hd=np.maximum(moor,hbs)*(1-east*0)+0
hd=np.maximum(hd,moor)
mtn=(0.30+0.24*sstep(430,446,GX)+0.06*nzg)*sstep(428,437,GX+0.5*(250-GY))
hd=np.maximum(hd,mtn)
ridge=(1-np.abs(noise(16,4,9,GW,GH)))**2
hd=hd+ridge*0.03*sstep(0.3,0.45,hd)
# vale escavado
dr,yr,sr,ir=rinfo(GX,GY)
fl=floor_h(sr)
gorge=1-sstep(262,268,yr)                       # desfiladeiro só a montante do vau
dhg=np.hypot(GX-HOUSE[0],GY-HOUSE[1]);wv=noise(6,3,41,GW,GH)
wf=0.9+0.5*sstep(252,259,yr)*gorge+3.0*(1-gorge)+1.1*np.exp(-dhg**2/(2*2.0**2))+0.35*wv   # fundo do vale (meia-largura)
wall=wf+2.3+4.5*(1-gorge)+0.6*np.abs(wv)+0.35*nzg
bl_=lambda a_:cv2.GaussianBlur(a_.astype(np.float32),(0,0),5)
wf=bl_(wf);wall=np.maximum(bl_(wall),wf+0.6);fl=bl_(fl)
W_=wall-wf
prof=fl+(hd-fl)*(0.55*sstep(wf,wf+0.42*W_,dr)+0.45*sstep(wf+0.58*W_,wall,dr))
hd=np.where(dr<wall,np.minimum(hd,prof),hd)
hd=np.where(dr<wf,fl+0.004*nzg,hd)
# terraço da casa de Elrond (meia encosta, na margem oeste)
dh=np.hypot(GX-HOUSE[0],GY-HOUSE[1])
_,_,sh,_=rinfo(np.array([[HOUSE[0]]]),np.array([[HOUSE[1]]]));HZ=float(floor_h(sh)[0,0])+0.03
tf=1-sstep(1.15,1.9,dh)
hd=hd*(1-tf)+HZ*tf
# leito do rio
hd=hd-0.012*sstep(0.6,0.0,dr/half_w(yr))
hd=hd*fade+hb*(1-fade)
hd=np.maximum(hd,-0.04)
enc=np.clip((hd+0.05)/1.25,0,1)*65535
Image.fromarray(np.dstack([(enc//256).astype(np.uint8),(enc%256).astype(np.uint8),np.zeros((GH,GW),np.uint8)]),'RGB').save('vf_h.png',optimize=True)
def gz(x,y):
    fx=(x-X0)*GR;fy=(y-Y0)*GR;i=min(GW-2,int(fx));j=min(GH-2,int(fy));uu=fx-i;vv=fy-j
    return float(((hd[j,i]*(1-uu)+hd[j,i+1]*uu)*(1-vv)+(hd[j+1,i]*(1-uu)+hd[j+1,i+1]*uu)*vv)*HSW)
HT=cv2.resize(hd.astype(np.float32),(TW,TH),interpolation=cv2.INTER_CUBIC)
def mask_at(m,x,y): px,py=tp(x,y);return m[min(TH-1,max(0,py)),min(TW-1,max(0,px))]
# ---------- água ----------
DR,YR,SR,_=rinfo(UX,UY)
water=np.clip((half_w(YR)-DR)/0.05+0.5,0,1)
water*=(SR>0.05)
src=gauss(*RV[0],0.35,UX,UY)
water=np.maximum(water,np.clip(src*1.6-0.3,0,1))
# riachos e cachoeiras laterais
def wall_at(x,y):
    i=min(GW-1,max(0,int(round((x-X0)*GR))));j=min(GH-1,max(0,int(round((y-Y0)*GR))));return float(wall[j,i])
STREAMS=[]
for (sv,side) in [(9.0,1),(12.5,1),(15.6,-1),(7.0,-1),(18.5,-1)]:
    k=int(np.searchsorted(RS,sv));p=RP[k];n=RN[k]*side;w=wall_at(*p)+0.5
    STREAMS.append([tuple(p+n*w),tuple(p+n*(w*0.62)+_t[k]*0.15),tuple(p+n*(w*0.3)),tuple(p)])
smask=np.zeros((TH,TW),np.float32)
for st in STREAMS: cv2.polylines(smask,[np.array([tp(x,y) for x,y in st],np.int32)],False,1.0,3,cv2.LINE_AA)
smask=cv2.GaussianBlur(smask,(0,0),0.8)
# ---------- cores ----------
slope=np.hypot(*np.gradient(cv2.GaussianBlur(HT,(0,0),2)*HSW,1/PX,1/PX))
cliff=sstep(1.8,3.2,slope)
img=np.zeros((TH,TW,3),np.float32)
heath=np.clip(noise(40,4,5)*1.4+0.5,0,1)[...,None]
heath=np.clip(noise(110,4,5)*1.2+0.45,0,1)[...,None]*0.7
moorc=C(104,124,66)*(1-heath)+C(118,108,76)*heath           # charneca: capim seco e urze
img+=moorc*(1+noise(120,3,6)[...,None]*0.08)
valley=np.clip((1-sstep(0.6,2.2,DR-np.where(YR<262,1.6,3.5)))+sstep(0.6,1.6,slope)*0.7,0,1)
valc=C(98,134,62)*(1+noise(90,3,7)[...,None]*0.10)
img=img*(1-valley[...,None])+valc*valley[...,None]
strata=0.5+0.5*np.sin(HT*HSW*9+noise(40,3,44)*3)
rockm=np.clip(sstep(2.2,3.6,slope)*0.8+sstep(0.36,0.46,HT),0,1)
rock_=None
rock=C(128,122,114)*(1+noise(80,4,8)[...,None]*0.14)*(0.9+0.15*strata[...,None])
img=img*(1-rockm[...,None])+rock*rockm[...,None]
snow=sstep(0.50,0.58,HT+0.03*noise(50,3,9))
img=img*(1-snow[...,None])+C(236,240,246)*snow[...,None]
# jardins de Elrond: canteiros, gramados e flores
DH=np.hypot(UX-HOUSE[0],UY-HOUSE[1])
gard=(1-sstep(1.2,1.6,DH))
lawn=C(92,142,60)
img=img*(1-gard[...,None])+lawn*gard[...,None]
fl_=(rng.random((TH,TW))<0.06)*gard*(DH>0.7)
fcol=np.array([C(220,180,60),C(200,90,80),C(230,230,220),C(170,120,190)])[rng.integers(0,4,(TH,TW))]
fl_=cv2.dilate(fl_.astype(np.float32),np.ones((2,2),np.uint8))
img=img*(1-fl_[...,None])+fcol*fl_[...,None]
# pátio de pedra sob a casa
pave=1-sstep(0.55,0.75,DH)
img=img*(1-pave[...,None])+C(200,190,168)*pave[...,None]
def road(pts,w,col,ecol,a=1.0):
    global img
    m=np.zeros((TH,TW),np.float32);cv2.polylines(m,[np.array([tp(x,y) for x,y in pts],np.int32)],False,1.0,max(1,int(w*PX)),cv2.LINE_AA);m=cv2.GaussianBlur(m,(0,0),0.9)*a
    e=np.clip(cv2.dilate(m,np.ones((5,5),np.uint8))-m,0,1)
    img=img*(1-e[...,None]*0.4)+ecol*e[...,None]*0.4;img=img*(1-m[...,None])+col*m[...,None]
# Grande Estrada Leste: do oeste até o vau e depois rumo ao Passo Alto
EROAD=[(X0-1,268.6),(404,268.2),(410,268.4),(414.5,267.9),(417.2,267.5),FORD,(419.8,267.3),(423,266.8),(427,265.4),(431,263.6),(435,262.2),(440,260.5),(X1+1,259.2)]
road(EROAD,0.32,C(176,156,118),C(110,96,70))
# trilha: sai da estrada, cruza a charneca e desce em zigue-zague até a ponte
_,_,_,ib=rinfo(np.array([[HOUSE[0]]]),np.array([[HOUSE[1]]]))
BRP=RP[int(ib[0,0])]                                   # ponto do rio sob a ponte
kb=int(ib[0,0]);nb=RN[kb]*np.sign(np.dot(RN[kb],np.array(BRP)-np.array(HOUSE)))*1;tb=_t[kb]
wb=wall_at(*BRP)
TRAIL=[(423.3,266.9),tuple(BRP+nb*(wb+1.2)+tb*3.2),tuple(BRP+nb*(wb+0.6)+tb*1.6)]
for q in range(6):
    f=1-(q+1)/7;TRAIL.append(tuple(BRP+nb*(0.7+f*wb)+tb*(0.9 if q%2==0 else 0.1)))
TRAIL.append(tuple(BRP+nb*0.62))
road(TRAIL,0.12,C(184,168,132),C(110,96,70))
HOUSE_PATH=[tuple(BRP-nb*0.62),(HOUSE[0]+(BRP[0]-HOUSE[0])*0.45,HOUSE[1]+(BRP[1]-HOUSE[1])*0.45)]
road(HOUSE_PATH,0.1,C(206,196,170),C(110,96,70))
# água
bank=np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1)
img=img*(1-bank[...,None]*0.35)+C(110,112,84)*bank[...,None]*0.35
foam=np.clip(noise(300,2,16)*1.5,0,1)*sstep(0.25,0.0,DR/np.maximum(half_w(YR),0.01)-0.6)
wcol=C(70,116,138)*(1+noise(260,2,17)[...,None]*0.06)
wcol=wcol*(1-foam[...,None]*0.0)
img=img*(1-water[...,None])+wcol*water[...,None]
# espuma: no desfiladeiro e no vau
fz=water*np.clip(noise(220,2,18)*1.6+0.2,0,1)*(sstep(256,250,YR)*0.7+np.exp(-((YR-FORD[1])/0.8)**2)*0.8)
img=img*(1-fz[...,None])+C(226,236,240)*fz[...,None]
img=img*(1-smask[...,None])+C(214,230,238)*smask[...,None]
# ---------- luz assada ----------
hf=cv2.GaussianBlur(HT,(0,0),3)*HSW
gy_,gx_=np.gradient(hf,1/PX,1/PX)
Lv=np.array([-0.62,-0.55,0.56]);Lv/=np.linalg.norm(Lv)
nn=np.dstack([-gx_,-gy_,np.ones_like(hf)]);nn/=np.linalg.norm(nn,axis=2,keepdims=True)
lam=np.clip(nn@Lv,0,1);flatL=float(Lv[2])
Lt=(0.66+0.5*(lam-flatL)+0.42*flatL)*np.clip(1-(cv2.GaussianBlur(hf,(0,0),30)-hf)*0.04,0.62,1)
cool=np.array([0.55,0.62,0.82]);warm=np.array([1.10,1.02,0.88]);mixw=np.clip(Lt,0,1.2)[...,None]/1.2
fin=img*(cool*(1-mixw)+warm*mixw)*Lt[...,None]
tex=np.asarray(Image.open(ME+'me_tex.webp').convert('RGB')).astype(np.float32)/255
lm=np.asarray(Image.open(ME+'light_hi.png').convert('RGB')).astype(np.float32)/255
def crop_up(a_,sc): return cv2.resize(a_[int(Y0*sc):int(Y1*sc),int(X0*sc):int(X1*sc)],(TW,TH),interpolation=cv2.INTER_CUBIC)
bt=crop_up(tex,2);bl=crop_up(lm,1);Lb=bl[...,0]*1.3;mb=np.clip(Lb,0,1.2)[...,None]/1.2
base=bt*(cool*(1-mb)+warm*mb)*Lb[...,None];wcb=bl[...,2][...,None]*0.8;sky=np.array([0.62,0.70,0.76]);base=base*(1-wcb)+(bt*0.3+sky*0.38)*wcb
bw=np.clip((np.minimum.reduce([UX-X0,X1-UX,UY-Y0,Y1-UY])-0.5)/6.0,0,1)[...,None]**1.5
out=np.clip(fin*bw+base*(1-bw),0,1)
cv2.imwrite('vf_tex.webp',cv2.cvtColor((out*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,88])
Image.fromarray((out*255).astype(np.uint8)).resize((TW//2,TH//2)).save('prev.png')
# ================= MODELOS =================
MOD=[];TREES=[]
def tree(x,y,s,t,c): TREES.append([round(x,2),round(y,2),round(s,2),t,round(float(c[0]),2),round(float(c[1]),2),round(float(c[2]),2)])
zh=HZ*HSW
# direção do rio junto à casa: a casa fica de frente para o rio
rdx,rdy=BRP[0]-HOUSE[0],BRP[1]-HOUSE[1];face=math.atan2(rdy,rdx)       # da casa para o rio
along=face+math.pi/2
S=1.45
def P(dx,dy):  # dx: na direção do rio, dy: ao longo do vale
    dx*=S;dy*=S
    return (HOUSE[0]+math.cos(face)*dx+math.cos(along)*dy, HOUSE[1]+math.sin(face)*dx+math.sin(along)*dy)
WALL='#efe3c8';WALL2='#e6d6b6';ROOF='#9a5236';ROOF2='#7e4430';ROOF3='#5f6e4a';GLOW=[1.0,0.78,0.42,0.6]
def hall(dx,dy,w,d,h,z0,rot,wall=WALL,roof=ROOF,win=True):
    w*=S;d*=S;h*=S;x,y=P(dx,dy);MOD.append(['boxA',x,y,w,d,z0,z0+h,rot,wall,roof])
    if win:
        nx,ny=math.cos(rot-math.pi/2),math.sin(rot-math.pi/2)
        for sgn in (1,-1):
            for k in range(max(1,int(w/0.09))):
                t=(k+0.5)/max(1,int(w/0.09))*2-1
                px,py=x+math.cos(rot)*t*w*0.85+nx*d*sgn*1.01,y+math.sin(rot)*t*w*0.85+ny*d*sgn*1.01
                MOD.append(['discA',px,py,z0+h*0.5,nx*sgn,ny*sgn,min(0.03,h*0.18),GLOW])
def tower(dx,dy,r,z0,h,roof=ROOF2):
    r*=S;h*=S
    x,y=P(dx,dy);MOD.append(['cylA',x,y,z0-0.2,z0+h,r,r*0.92,12,WALL]);MOD.append(['cylA',x,y,z0+h,z0+h+r*3.2,r*1.25,0,12,roof])
    MOD.append(['discA',x+math.cos(face)*r*0.95,y+math.sin(face)*r*0.95,z0+h*0.8,math.cos(face),math.sin(face),0.022,GLOW])
def pavilion(dx,dy,r,z0,h,n=6,dome='#b4c0b0'):
    r*=S;h*=S
    x,y=P(dx,dy)
    for k in range(n):
        a=k/n*2*math.pi;MOD.append(['cylA',x+math.cos(a)*r,y+math.sin(a)*r,z0,z0+h,0.018,0.016,6,'#f4ecd8'])
    MOD.append(['capA',x,y,z0+0.01,0,r+0.04,14,'#d8ccb0'])
    MOD.append(['cylA',x,y,z0+h,z0+h+0.03,r+0.04,r+0.04,14,'#f0e6d0'])
    MOD.append(['blobA',x,y,z0+h+0.03,[[r+0.03,0],[r*0.85,r*0.45],[r*0.45,r*0.8],[0,r*0.95]],12,dome])
# plataforma de pedra (terraços) e muros de arrimo
for (dx,dy,w,d,z) in [(-0.2,0.0,0.75,0.55,0.0),(0.45,0.15,0.45,0.6,-0.12),(0.9,-0.1,0.28,0.5,-0.24)]:
    x,y=P(dx,dy);MOD.append(['boxA',x,y,w*S,d*S,zh-0.6,zh+z*S,along,'#d6c8a8','#cfc3a6'])
# corpo principal (salão), alas e torres
hall(-0.25,0.0,0.48,0.17,0.42,zh,along)                      # salão principal
hall(-0.55,0.42,0.2,0.14,0.36,zh,face,WALL2,ROOF)             # ala norte
hall(-0.5,-0.45,0.22,0.14,0.32,zh,face,WALL2,ROOF2)           # ala sul
hall(0.12,-0.36,0.2,0.12,0.26,zh,along,WALL,ROOF)             # Salão do Fogo
hall(0.42,0.36,0.14,0.1,0.22,zh-0.12*S,along,WALL2,ROOF2)        # biblioteca
tower(-0.42,0.2,0.07,zh,0.85)
tower(-0.1,-0.5,0.06,zh,0.6)
tower(-0.75,-0.1,0.08,zh,1.05,ROOF3)
# varanda do Conselho: colunata aberta voltada para o rio
cx_,cy_=P(0.45,0.0)
for k in range(5):
    for s_ in (-1,1):
        x,y=P(0.3+s_*0.14+0.0,-0.24+k*0.12);MOD.append(['cylA',x,y,zh-0.12*S,zh+0.14*S,0.02,0.018,6,'#f6eedc'])
x,y=P(0.3,0.0);MOD.append(['boxA',x,y,0.17*S,0.3*S,zh+0.14*S,zh+0.18*S,face,'#efe6d2','#a35a3a'])
# pavilhões nos jardins
pavilion(0.95,-0.35,0.09,zh-0.24*S,0.16)
pavilion(-0.25,0.95,0.08,gz(*P(-0.25,0.95))+0.0,0.14,6,'#c8b080')
pavilion(0.7,0.75,0.07,gz(*P(0.7,0.75)),0.13)
# escadarias até a ponte
x,y=P(1.15,0.15);MOD.append(['boxA',x,y,0.18,0.06,gz(x,y)-0.2,gz(x,y)+0.03,face,'#d8ccb0',None])
# ponte estreita de pedra, sem parapeito
bx0,by0=BRP[0]-0.62*math.cos(face),BRP[1]-0.62*math.sin(face);bx1,by1=BRP[0]+0.62*math.cos(face),BRP[1]+0.62*math.sin(face)
bz=max(gz(bx0,by0),gz(bx1,by1))+0.06
MOD.append(['boxA',BRP[0],BRP[1],0.66,0.045,bz-0.05,bz,face,'#cfc6b2',None])
MOD.append(['blobA',BRP[0],BRP[1],gz(*BRP)-0.3,[[0.09,0],[0.08,0.2],[0.06,(bz-0.05-gz(*BRP)+0.3)]],6,'#bdb4a0'])
# Vau do Bruinen: pedras no leito
for q in range(16):
    t=q/15;x=FORD[0]-0.85+1.7*t+rng.uniform(-0.12,0.12);y=FORD[1]+rng.uniform(-0.5,0.5)
    MOD.append(['stone',round(x,2),round(y,2)])
# cachoeiras: véus de água nas escarpas (caixas finas claras)
FALLS=[]
for st in STREAMS:
    fall=False
    for (ax,ay),(bx,by) in zip(st[:-1],st[1:]):
        n=max(2,int(math.hypot(bx-ax,by-ay)/0.12));rot=math.atan2(by-ay,bx-ax)
        for k in range(n):
            x0_,y0_=ax+(bx-ax)*k/n,ay+(by-ay)*k/n;x1_,y1_=ax+(bx-ax)*(k+1)/n,ay+(by-ay)*(k+1)/n
            za,zb=gz(x0_,y0_),gz(x1_,y1_)
            if abs(za-zb)>0.12: fall=True
            if abs(za-zb)>0.06: MOD.append(['boxA',(x0_+x1_)/2,(y0_+y1_)/2,math.hypot(x1_-x0_,y1_-y0_)/2+0.01,0.035,min(za,zb)-0.03,max(za,zb)+0.025,rot,[0.88,0.94,0.98,0.4],None])
    if fall: FALLS.append(st[1])
# a nascente: cascata que sai das montanhas
sx,sy=RV[0];zs=gz(sx,sy);zt=gz(sx+0.9,sy-0.25)
MOD.append(['boxA',sx+0.1,sy-0.03,0.05,0.12,zs,max(zt,zs+1.2),math.atan2(-0.25,0.9),[0.88,0.94,0.98,0.4],None])
print('quedas',len(FALLS))
# ---------- árvores ----------
AUT=[C(196,140,48),C(178,96,40),C(150,60,36),C(206,170,64),C(90,128,52),C(76,116,46)]
for _ in range(26000):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    if mask_at(water,x,y)>0.02 or mask_at(smask,x,y)>0.05: continue
    if math.hypot(x-HOUSE[0],y-HOUSE[1])<0.75: continue
    d_,yy=float(TREE.query([x,y])[0]),y
    h_=mask_at(HT,x,y);rk=mask_at(rockm,x,y);sn=mask_at(snow,x,y)
    if sn>0.1: continue
    inval=d_<(2.8 if yy<262 else 4.5)
    if any(math.hypot(x-px,y-py)<0.18 for px,py in TRAIL+HOUSE_PATH): continue
    if any(math.hypot(x-px,y-py)<0.35 for px,py in EROAD): continue
    if inval:
        if rk>0.6 and rng.random()<0.7: continue
        if rng.random()<0.16:
            if rng.random()<0.55: tree(x,y,rng.uniform(0.38,0.6),1,AUT[rng.integers(6)]*rng.uniform(0.9,1.1))
            else: tree(x,y,rng.uniform(0.45,0.75),0,C(42,74,46)*rng.uniform(0.85,1.15))
    else:
        if rk>0.5:
            if rng.random()<0.012: tree(x,y,rng.uniform(0.4,0.6),0,C(46,74,48))
            continue
        fo=0.03+0.25*sstep(408,400,x)+0.12*sstep(0.30,0.36,h_)*(1-sstep(0.44,0.5,h_))
        if rng.random()<fo: tree(x,y,rng.uniform(0.45,0.8),0 if rng.random()<0.6 else 1,(C(40,72,44) if rng.random()<0.6 else C(88,108,52))*rng.uniform(0.85,1.15))
# bétulas/faias douradas nos jardins
for q in range(40):
    a=rng.uniform(0,2*math.pi);r=rng.uniform(0.85,1.5);x,y=HOUSE[0]+math.cos(a)*r,HOUSE[1]+math.sin(a)*r
    if mask_at(water,x,y)>0.02: continue
    tree(x,y,rng.uniform(0.32,0.48),1,AUT[rng.integers(4)])
# ---------- lugares ----------
SF=P(0.12,-0.36);VC=P(0.3,0.0)
PL={'UltimaCasa':P(-0.3,0.05),'SalaoFogo':SF,'VarandaConselho':VC,'PonteValfenda':tuple(BRP),'TrilhaValfenda':TRAIL[4],
    'CachoeirasValfenda':FALLS[0] if FALLS else (421,251.6),'RioBruinen':(433.5,248.1),'VauBruinen':FORD,'EstradaLeste':(408.0,268.3)}
TOPS=[[round(PL['UltimaCasa'][0],2),round(PL['UltimaCasa'][1],2),round(zh+1.2-gz(*PL['UltimaCasa']),2),0.3],
      [round(SF[0],2),round(SF[1],2),round(zh+0.45-gz(*SF),2),0.15],[round(VC[0],2),round(VC[1],2),round(zh+0.35-gz(*VC),2),0.15],
      [round(BRP[0],2),round(BRP[1],2),0.3,0.2]]
def _c(o):
    if isinstance(o,(list,tuple,np.ndarray)): return [_c(v) for v in o]
    if isinstance(o,(np.floating,float)): return round(float(o),3)
    if isinstance(o,np.integer): return int(o)
    return o
json.dump({'rect':[X0,Y0,X1,Y1],'models':_c(MOD),'trees':_c(TREES),'tops':_c(TOPS),'places':{k:[round(float(x),2),round(float(y),2)] for k,(x,y) in PL.items()}},open('vf.json','w'),separators=(',',':'))
import os;print('modelos',len(MOD),'árvores',len(TREES),'zh',round(zh,2),'ponte',BRP.round(2),{f:os.path.getsize(f) for f in ['vf_tex.webp','vf_h.png','vf.json']})
