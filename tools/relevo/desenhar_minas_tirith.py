import numpy as np, cv2, json, math
from PIL import Image
rng=np.random.default_rng(7)
X0,Y0,X1,Y1=548.0,554.0,600.0,598.0
PX=28;TW,TH=int((X1-X0)*PX),int((Y1-Y0)*PX)
GR=4;GW,GH=int((X1-X0)*GR)+1,int((Y1-Y0)*GR)+1
HSW=46*1.35
ME='/tmp/claude-0/me/'
CX,CY=568.8,574.4
def tp(x,y): return (int(round((x-X0)*PX)),int(round((y-Y0)*PX)))
def noise(base,octv,seed,w=TW,h=TH):
    r=np.random.default_rng(seed);out=np.zeros((h,w),np.float32);a=1;t=0
    for o in range(octv):
        n=r.standard_normal((int(base*2**o*h/w)+2,base*2**o+2)).astype(np.float32);out+=cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
    return out/t
ux=np.linspace(X0,X1,TW,dtype=np.float32);uy=np.linspace(Y0,Y1,TH,dtype=np.float32);UX,UY=np.meshgrid(ux,uy)
def gauss(cx,cy,s,X,Y): return np.exp(-((X-cx)**2+(Y-cy)**2)/(2*s*s))
def sstep(a,b,x): t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
# ---------- água (do mapa-base) ----------
wbase=np.load(ME+'water.npy')
x0p,y0p=int(X0*2)-2,int(Y0*2)-2;crop=wbase[y0p:int(Y1*2)+2,x0p:int(X1*2)+2]
up=cv2.resize(crop,((crop.shape[1])*PX//2,(crop.shape[0])*PX//2),interpolation=cv2.INTER_CUBIC)[PX:PX+TH,PX:PX+TW]
water=cv2.GaussianBlur(np.clip((up-0.45)/0.08,0,1),(0,0),0.9)
# ---------- relevo ----------
hm=np.asarray(Image.open(ME+'height_hi.png').convert('RGB')).astype(np.float32)
h492=((hm[...,0]*256+hm[...,1])/65535*1.25-0.05)
gx=np.linspace(X0,X1,GW);gy=np.linspace(Y0,Y1,GH);GX,GY=np.meshgrid(gx,gy)
fx=GX/984*491;fy=GY/877*437;i0=np.floor(fx).astype(int);j0=np.floor(fy).astype(int);u=fx-i0;v=fy-j0
hb=(h492[j0,i0]*(1-u)+h492[j0,i0+1]*u)*(1-v)+(h492[j0+1,i0]*(1-u)+h492[j0+1,i0+1]*u)*v
fade=np.clip(np.minimum.reduce([GX-X0,X1-GX,GY-Y0,Y1-GY])/4.0,0,1)
wg=cv2.resize(water,(GW,GH),interpolation=cv2.INTER_AREA)
hbs=cv2.GaussianBlur(hb.astype(np.float32),(0,0),4);hbs=np.where(hbs>0.28,0.28+(hbs-0.28)*0.55,hbs)
nz=noise(10,4,3,GW,GH)
plain=sstep(560.5,564.5,GX+1.6*np.sin(GY*0.35))*sstep(555,559,GY)
plain_h=0.105+0.008*nz-0.004*(GX-570)/10
eastrise=sstep(586,598,GX)*0.05
hd=hbs*(1-plain)+(plain_h+eastrise)*plain
mind=gauss(556.5,571.5,5.2,GX,GY)*0.27+gauss(552,567,6.8,GX,GY)*0.14
ridgeN=(1-np.abs(noise(18,4,9,GW,GH)))**2
hd=np.maximum(hd,(0.1+mind*(0.9+0.2*ridgeN))*sstep(0.04,0.14,mind))
# esporão que liga a cidade à montanha
d_c=np.hypot(GX-CX,GY-CY)
t=np.clip((CX-GX)/(CX-557.0),0,1);spur=(0.13+0.24*t**1.3)*np.exp(-((GY-CY+ (CY-571.5)*t)**2)/(2*2.0**2))*(GX<CX)
hd=np.maximum(hd,spur*(d_c>2.2))
HC=0.13
hd=hd*(1-sstep(2.7,3.4,d_c)*0+0)  # (sem efeito; mantido para leitura)
plat=1-sstep(2.9,3.6,d_c)
hd=hd*(1-plat)+HC*plat
hd=hd-0.006*cv2.GaussianBlur(wg,(0,0),1.0)
hd=hd*fade+hb*(1-fade)
hd=np.maximum(hd,-0.04)
enc=np.clip((hd+0.05)/1.25,0,1)*65535
Image.fromarray(np.dstack([(enc//256).astype(np.uint8),(enc%256).astype(np.uint8),np.zeros((GH,GW),np.uint8)]),'RGB').save('mt_h.png',optimize=True)
def gz(x,y):
    fx=(x-X0)*GR;fy=(y-Y0)*GR;i=min(GW-2,int(fx));j=min(GH-2,int(fy));uu=fx-i;vv=fy-j
    return float(((hd[j,i]*(1-uu)+hd[j,i+1]*uu)*(1-vv)+(hd[j+1,i]*(1-uu)+hd[j+1,i+1]*uu)*vv)*HSW)
HT=cv2.resize(hd.astype(np.float32),(TW,TH),interpolation=cv2.INTER_CUBIC)
def mask_at(m,x,y): px,py=tp(x,y);return m[min(TH-1,max(0,py)),min(TW-1,max(0,px))]
# ---------- cores ----------
C=lambda r,g,b: np.array([r,g,b],np.float32)/255
dcen=np.hypot(UX-CX,UY-CY);ang=np.arctan2(UY-CY,UX-CX)
RAM=9.6
inside=(dcen<RAM)&(UX>562)
mountain=np.clip((HT-0.2)/0.15,0,1)
img=np.zeros((TH,TW,3),np.float32)+C(120,142,74)
img*=1+noise(30,4,5)[...,None]*0.08
# campos do Pelennor (colcha), só dentro do Rammas
labimg=np.zeros((TH,TW),np.int32);cnt=[0]
def split(a0,b0,a1,b1,depth):
    w,h=a1-a0,b1-b0
    if (w<2.2 and h<1.9) or depth>7 or (depth>2 and rng.random()<0.12):
        cnt[0]+=1;a,b=tp(a0,b0);c,d=tp(a1,b1);labimg[max(0,b):max(0,d),max(0,a):max(0,c)]=cnt[0];return
    if w/h*rng.uniform(0.7,1.3)>1: q=rng.uniform(0.3,0.7);split(a0,b0,a0+w*q,b1,depth+1);split(a0+w*q,b0,a1,b1,depth+1)
    else: q=rng.uniform(0.3,0.7);split(a0,b0,a1,b0+h*q,depth+1);split(a0,b0+h*q,a1,b1,depth+1)
for by in np.arange(Y0-2,Y1+2,6.0):
    for bx in np.arange(X0-4+rng.uniform(0,4),X1+4,7.0): split(bx,by,bx+7.0,by+6.0,0)
mxx,myy=np.meshgrid(np.arange(TW,dtype=np.float32),np.arange(TH,dtype=np.float32))
lab=cv2.remap(labimg.astype(np.float32),mxx+noise(8,4,21)*30,myy+noise(8,4,23)*30,cv2.INTER_NEAREST).astype(np.int32)
nl=lab.max()+1
PAL=[C(118,150,70),C(104,140,62),C(130,160,78),C(140,164,84),C(204,182,100),C(214,194,118),C(186,166,92),C(150,126,86),C(128,158,92)]
W8=np.array([10,9,8,7,6,5,5,4,6],np.float64);W8/=W8.sum()
kind=rng.choice(len(PAL),nl,p=W8);an=rng.uniform(0,np.pi,nl)
fc=np.array(PAL)[kind[lab]]*rng.uniform(0.93,1.07,nl)[lab][...,None]
a=an[lab];stripe=np.sin((UX*np.cos(a)+UY*np.sin(a))*PX/1.8)
fc=fc*(1+np.where(np.isin(kind[lab],[4,5,6,7]),stripe*0.035,0)[...,None])*0.92
edge=((lab!=np.roll(lab,1,0))|(lab!=np.roll(lab,1,1))).astype(np.float32);edge*=(rng.random(nl)<0.7)[lab]
edge=cv2.dilate(edge,np.ones((2,2),np.uint8))
fieldm=(inside&(dcen>3.3)).astype(np.float32)*(1-np.clip(water*2,0,1))*(1-mountain)
fieldm=cv2.GaussianBlur(fieldm,(0,0),3)
img=img*(1-fieldm[...,None]*0.85)+fc*fieldm[...,None]*0.85
img=img*(1-(edge*fieldm)[...,None]*0.5)+C(70,98,48)*(edge*fieldm)[...,None]*0.5
# fora do Rammas: capim e arbustos; Ithilien a leste; montanha
scrub=np.clip(noise(60,3,31)*1.2,0,1)
outm=(1-fieldm)*(1-mountain)
img=img*(1-outm[...,None]*0.5)+(C(128,140,78)*(1-scrub[...,None])+C(96,118,62)*scrub[...,None])*outm[...,None]*0.5
ith=sstep(585,589,UX)*(1-np.clip(water*2,0,1))
rock=C(126,120,112)*(1+noise(90,3,32)[...,None]*0.12)
img=img*(1-mountain[...,None])+rock*mountain[...,None]
snow=np.clip((HT-0.62)/0.12,0,1)
img=img*(1-snow[...,None])+C(236,240,246)*snow[...,None]
# chão da cidade (pedra) e caminhos
cityg=1-sstep(2.75,3.05,dcen)
img=img*(1-cityg[...,None])+C(196,190,176)*cityg[...,None]
def road(pts,w,col,ecol):
    global img
    m=np.zeros((TH,TW),np.float32);cv2.polylines(m,[np.array([tp(x,y) for x,y in pts],np.int32)],False,1.0,int(w*PX)+2,cv2.LINE_AA);m=cv2.GaussianBlur(m,(0,0),1.0)
    e=cv2.dilate(m,np.ones((5,5),np.uint8))-m
    img=img*(1-e[...,None]*0.45)+ecol*e[...,None]*0.45;img=img*(1-m[...,None])+col*m[...,None]
GG=(CX+2.85,CY)
FORT=(CX+RAM*math.cos(0.12),CY+RAM*math.sin(0.12))
OSG=(580.6,578.8)
road([GG,(CX+5.5,CY+0.5),FORT,(OSG[0]-1.2,OSG[1]-0.1)],0.38,C(198,186,160),C(130,120,100))          # calçada até Osgiliath
NGATE=(CX+RAM*math.cos(-1.95),CY+RAM*math.sin(-1.95))
road([GG,(CX+3.6,CY-2.6),(CX+2.5,CY-6.0),NGATE,(NGATE[0]-1.5,Y0-2)],0.3,C(190,176,146),C(130,120,100))  # estrada do norte
HARL=(575.8,588.6)
road([GG,(CX+4.2,CY+3.0),(573.2,584.0),HARL],0.28,C(190,176,146),C(130,120,100))                         # estrada do Harlond
road([(573.2,584.0),(568.0,588.0),(562.0,593.0),(558.0,Y1+1)],0.26,C(186,170,140),C(130,120,100))       # para Lossarnach
# água
bank=np.clip(cv2.dilate(water,np.ones((7,7),np.uint8))-water,0,1)
img=img*(1-bank[...,None]*0.35)+C(118,120,80)*bank[...,None]*0.35
img=img*(1-water[...,None])+C(64,104,126)*(1+noise(260,2,16)[...,None]*0.05)*water[...,None]
# Ithilien (copa)
ithf=ith*np.clip(noise(40,3,33)*1.3+0.6,0,1)
can=np.clip(noise(120,3,13)*0.6+0.5,0,1)[...,None]
img=img*(1-ithf[...,None]*0.85)+C(46,82,42)*(0.75+0.5*can)*ithf[...,None]*0.85
# ---------- luz assada ----------
hf=cv2.GaussianBlur(HT,(0,0),6)*HSW
gy_,gx_=np.gradient(hf,1/PX,1/PX)
Lv=np.array([-0.62,-0.55,0.56]);Lv/=np.linalg.norm(Lv)
nn=np.dstack([-gx_,-gy_,np.ones_like(hf)]);nn/=np.linalg.norm(nn,axis=2,keepdims=True)
lam=np.clip(nn@Lv,0,1);flatL=float(Lv[2])
Lt=(0.55+0.62*(lam-flatL)+0.45*flatL)*np.clip(1-(cv2.GaussianBlur(hf,(0,0),30)-hf)*0.05,0.6,1)
cool=np.array([0.55,0.62,0.82]);warm=np.array([1.10,1.02,0.88]);mixw=np.clip(Lt,0,1.2)[...,None]/1.2
fin=img*(cool*(1-mixw)+warm*mixw)*Lt[...,None]
# emenda com a base
tex=np.asarray(Image.open(ME+'me_tex.webp').convert('RGB')).astype(np.float32)/255
lm=np.asarray(Image.open(ME+'light_hi.png').convert('RGB')).astype(np.float32)/255
def crop_up(a_,sc):
    return cv2.resize(a_[int(Y0*sc):int(Y1*sc),int(X0*sc):int(X1*sc)],(TW,TH),interpolation=cv2.INTER_CUBIC)
bt=crop_up(tex,2);bl=crop_up(lm,1);Lb=bl[...,0]*1.3;mb=np.clip(Lb,0,1.2)[...,None]/1.2
base=bt*(cool*(1-mb)+warm*mb)*Lb[...,None];wcb=bl[...,2][...,None]*0.8;sky=np.array([0.62,0.70,0.76]);base=base*(1-wcb)+(bt*0.3+sky*0.38)*wcb
bw=np.clip((np.minimum.reduce([UX-X0,X1-UX,UY-Y0,Y1-UY])-0.5)/6.0,0,1)[...,None]**1.5
out=np.clip(fin*bw+base*(1-bw),0,1)
cv2.imwrite('mt_tex.webp',cv2.cvtColor((out*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,88])
Image.fromarray((out*255).astype(np.uint8)).resize((TW//2,TH//2)).save('prev.png')
np.save('state.npy',{'hd':hd},allow_pickle=True)
# ================= MODELOS =================
MOD=[];TREES=[];TOPS=[]
def tree(x,y,s,t,c): TREES.append([round(x,2),round(y,2),round(s,2),t,round(float(c[0]),2),round(float(c[1]),2),round(float(c[2]),2)])
zc=gz(CX,CY)
TH_=0.58
R=[2.8-k*0.36 for k in range(7)]
F=[zc+k*TH_ for k in range(7)]
STONE='#ece7da';STONE2='#ddd7c8';PAVE='#cbc4b2'
for k in range(7):
    z0=(F[k-1] if k>0 else zc-0.6)
    MOD.append(['cylA',CX,CY,z0,F[k]+0.17,R[k],R[k],48,STONE if k%2==0 else STONE2])
    MOD.append(['capA',CX,CY,F[k]+0.17,R[k]-0.06,R[k],48,'#f4f0e6'])           # topo da muralha
    ri=R[k+1] if k<6 else 0
    MOD.append(['capA',CX,CY,F[k],ri,R[k]-0.05,48,PAVE])
# esporão de rocha (proa) para o leste
MOD.append(['polyA',[[CX-0.1,CY-0.34],[CX+2.62,CY],[CX-0.1,CY+0.34]],zc-0.2,F[6]+0.17,'#e2ddd0'])
# portões: o Grande Portão no leste e os demais alternando
gates=[0.0]+[(-1)**k*0.62 for k in range(1,7)]
for k,a in enumerate(gates):
    nx,ny=math.cos(a),math.sin(a);r=R[k]+0.012;zb=(zc if k==0 else F[k-1])
    big=k==0;rr=0.36 if big else 0.16
    MOD.append(['discA',CX+nx*r,CY+ny*r,zb+(0.30 if big else 0.18),nx,ny,rr*1.25,'#bdb6a6'])
    MOD.append(['discA',CX+nx*(r+0.01),CY+ny*(r+0.01),zb+(0.30 if big else 0.18),nx,ny,rr,'#2c2622' if big else '#3a342e'])
    if big:
        for s_ in (-1,1):
            px,py=CX+nx*(r+0.05)-ny*0.62*s_,CY+ny*(r+0.05)+nx*0.62*s_
            MOD.append(['cylA',px,py,zc-0.3,zc+1.15,0.22,0.2,10,STONE]);MOD.append(['capA',px,py,zc+1.15,0,0.2,10,'#f4f0e6'])
# casas em cada nível
ROOFS=['#5c6672','#6b7480','#4c5560','#7a6a5a','#808a96'];WALLS=['#f2eee4','#e6e0d2','#ddd6c6','#f6f3ec']
nh=0
for k in range(6):
    ri,ro=R[k+1],R[k];rm=(ri+ro)/2;wd=ro-ri
    for row in ([rm] if wd<0.3 else [ri+wd*0.3,ri+wd*0.72]):
        n=int(2*math.pi*row/0.2)
        for q in range(n):
            a=q/n*2*math.pi+rng.uniform(-0.02,0.02);x,y=CX+math.cos(a)*row,CY+math.sin(a)*row
            if math.cos(a)>0 and abs(math.sin(a))*row<0.45: continue                # esporão
            if any(abs(((a-g_+math.pi)%(2*math.pi))-math.pi)<0.16 for g_ in (gates[k],gates[k+1] if k+1<7 else 9)): continue
            if k==5 and abs(((a-1.6+math.pi)%(2*math.pi))-math.pi)<0.45: continue   # Casas de Cura
            w_=rng.uniform(0.11,0.16);d_=min(wd*0.6,rng.uniform(0.08,0.12));h_=rng.uniform(0.16,0.34)*(1.25 if row<1.2 else 1)
            MOD.append(['houseA',round(x,3),round(y,3),round(w_,3),round(d_,3),round(a+math.pi/2,3),WALLS[rng.integers(4)],ROOFS[rng.integers(5)],round(h_,3),round(F[k],3)]);nh+=1
# Cidadela: Torre de Ecthelion, Salão dos Reis, Pátio da Fonte e a Árvore Branca
tx,ty=CX-0.12,CY
MOD.append(['cylA',tx,ty,F[6],F[6]+2.1,0.19,0.16,16,'#f7f5ef']);MOD.append(['cylA',tx,ty,F[6]+1.7,F[6]+1.78,0.22,0.22,16,'#e8e2d4']);MOD.append(['capA',tx,ty,F[6]+1.78,0.16,0.22,16,'#e8e2d4'])
MOD.append(['cylA',tx,ty,F[6]+2.1,F[6]+2.55,0.17,0.0,16,[0.95,0.97,1.0,0.25]])
MOD.append(['boxA',CX+0.12,CY,0.17,0.12,F[6],F[6]+0.42,0,'#f2eee4','#c8ccd4'])
MOD.append(['capA',CX+0.36,CY+0.16,F[6]+0.03,0,0.07,12,'#5a8aa8'])
MOD.append(['treeW',CX+0.36,CY+0.16,F[6]+0.03,1.0])
# Casas de Cura (sexto círculo, ao sul)
hx,hy=CX+math.cos(1.6)*(R[6]+R[5])/2,CY+math.sin(1.6)*(R[6]+R[5])/2
MOD.append(['boxA',hx,hy,0.22,0.08,F[5],F[5]+0.3,1.6+math.pi/2,'#f4f0e8','#7c8a6c'])
# Rath Dínen: Rua Silenciosa e túmulos na encosta atrás da cidade
for q in range(7):
    x,y=CX-3.3-q*0.42,CY+(-0.35 if q%2 else 0.35)+q*0.05;z=gz(x,y)
    MOD.append(['blobA',x,y,z-0.05,[[0.18,0],[0.18,0.12],[0.13,0.24],[0.0,0.3]],10,'#e6e2d8'])
MOD.append(['boxA',CX-3.2,CY,0.22,0.14,gz(CX-3.2,CY)-0.05,gz(CX-3.2,CY)+0.3,0,'#d8d2c4','#9aa0a8'])
MOD.append(['wall',[[CX-2.9,CY-0.1],[CX-6.2,CY+0.2]],0.06,'#b8b2a4',0.14])
# Rammas Echor
pts=[[CX+RAM*math.cos(a),CY+RAM*math.sin(a)] for a in np.linspace(-1.95,1.45,90)]
pts+= [[CX+RAM*math.cos(1.45)+q*0.9,CY+RAM*math.sin(1.45)+q*0.35] for q in range(1,9)]
pts=[[round(x,2),round(y,2)] for x,y in pts if not mask_at(water,x,y)>0.3]
MOD.append(['wall',pts,0.32,'#b9b2a2',0.2])
for (fx_,fy_) in [FORT,NGATE]:
    a=math.atan2(fy_-CY,fx_-CX)
    for s_ in (-1,1):
        px,py=fx_-math.sin(a)*0.45*s_,fy_+math.cos(a)*0.45*s_
        MOD.append(['cyl',px,py,-0.2,0.85,0.22,0.2,10,'#c8c0ae']);MOD.append(['cyl',px,py,0.85,1.05,0.24,0.0,10,'#6a6f78'])
# Osgiliath: ruínas nas duas margens e a ponte quebrada
row=water[tp(*OSG)[1]];xs=np.where(row>0.5)[0];wx0,wx1=X0+xs.min()/PX,X0+xs.max()/PX
print('rio em Osgiliath',round(wx0,2),round(wx1,2))
MOD.append(['bridge',wx0-0.3,OSG[1],wx0+(wx1-wx0)*0.42,OSG[1],0.5,4,'#b4ad9e'])
MOD.append(['bridge',wx0+(wx1-wx0)*0.62,OSG[1],wx1+0.3,OSG[1],0.5,3,'#b4ad9e'])
for side,(xa,xb) in [(-1,(wx0-2.6,wx0-0.4)),(1,(wx1+0.4,wx1+2.6))]:
    for q in range(22):
        x,y=rng.uniform(xa,xb),OSG[1]+rng.uniform(-1.8,1.8)
        if mask_at(water,x,y)>0.1: continue
        if q%5==0: MOD.append(['cyl',x,y,-0.1,rng.uniform(0.5,1.2),0.12,0.1,8,'#c2bcae'])
        else: MOD.append(['box',x,y,rng.uniform(0.08,0.25),rng.uniform(0.05,0.12),-0.05,rng.uniform(0.12,0.45),rng.uniform(0,3.1),'#bdb7a8',None])
dx_=wx1+1.2;MOD.append(['blobA',dx_,OSG[1]+0.6,gz(dx_,OSG[1]+0.6)-0.1,[[0.5,0],[0.46,0.22],[0.3,0.42],[0.0,0.48]],12,'#cfc9ba'])   # Cúpula das Estrelas em ruínas
# Harlond: cais e os navios negros de Umbar
rowy=tp(*HARL)[1];xs=np.where(water[rowy]>0.5)[0];bx_=X0+xs.min()/PX
print('margem no Harlond',round(bx_,2))
for q in range(4): MOD.append(['jetty',round(bx_+0.15,2),round(HARL[1]-1.2+q*0.8,2),0.0])
for q in range(5): MOD.append(['boat',round(bx_+0.75+(q%2)*0.5,2),round(HARL[1]-1.4+q*0.7,2),round(1.3+rng.uniform(-0.2,0.2),2),'#1c1a1c'])
for q in range(3): MOD.append(['box',bx_-0.6-q*0.45,HARL[1]+q*0.5-0.5,0.2,0.12,-0.05,0.25,0.3,'#d8d0bc','#6a6f78'])
# fazendas do Pelennor
nf=0
for q in range(400):
    if nf>=34:break
    x,y=rng.uniform(CX+3.6,CX+RAM-0.6),rng.uniform(CY-RAM,CY+RAM)
    if math.hypot(x-CX,y-CY)>RAM-0.6 or mask_at(water,x,y)>0.05 or mask_at(mountain,x,y)>0.2:continue
    nf+=1;rot=rng.uniform(0,3.1)
    MOD.append(['house',round(x,2),round(y,2),0.26,0.18,round(rot,2),'#e6dcc4','#8a5a3a',0.22])
    MOD.append(['house',round(x+0.35*math.cos(rot),2),round(y+0.35*math.sin(rot),2),0.22,0.16,round(rot,2),'#b8996e','#6e4e30',0.2])
    for j in range(rng.integers(0,3)): MOD.append(['hay',round(x+rng.uniform(-0.6,0.6),2),round(y+rng.uniform(-0.6,0.6),2)])
    for j in range(6): tree(x+0.6+(j%3)*0.3,y-0.4+(j//3)*0.3,0.45,1,C(84,128,52))
# árvores: Ithilien e árvores esparsas
for _ in range(9000):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    if mask_at(ithf,x,y)>0.55 and rng.random()<0.3 and mask_at(water,x,y)<0.02: tree(x,y,rng.uniform(0.75,1.1),1 if rng.random()<0.7 else 0,C(44,84,40)*rng.uniform(0.8,1.15))
for _ in range(700):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    if mask_at(fieldm,x,y)>0.6 and mask_at(edge,x,y)>0 and math.hypot(x-CX,y-CY)>3.4: tree(x,y,rng.uniform(0.5,0.75),1,C(64,104,46))
for _ in range(800):
    x,y=rng.uniform(X0,X1),rng.uniform(Y0,Y1)
    m_=mask_at(mountain,x,y)
    if 0.2<m_<0.7 and rng.random()<0.25: tree(x,y,rng.uniform(0.7,1.0),0,C(40,70,44))
# alturas dos alfinetes (acima do chão)
TOPS=[[round(CX-0.12,2),round(CY,2),round(F[6]+2.7-zc,2),0.4],[round(CX+0.36,2),round(CY+0.16,2),round(F[6]+0.6-zc,2),0.15],[round(hx,2),round(hy,2),round(F[5]+0.4-zc,2),0.25],[round(GG[0],2),round(GG[1],2),1.3,0.5]]
PL={'GrandePortao':GG,'Cidadela':(CX-0.12,CY),'ArvoreBranca':(CX+0.36,CY+0.16),'CasasCura':(hx,hy),'RathDinen':(CX-4.4,CY),'Mindolluin':(557.0,571.5),
    'Pelennor':(CX+6.0,CY+3.0),'PelennorNorte':(CX+5.5,CY-4.8),'RammasEchor':(CX+RAM*math.cos(-0.9),CY+RAM*math.sin(-0.9)),'FortesCalcada':FORT,'Harlond':(bx_+0.6,HARL[1]),'PonteOsgiliath':((wx0+wx1)/2,OSG[1])}
def _c(o):
    if isinstance(o,(list,tuple)): return [_c(v) for v in o]
    if isinstance(o,(np.floating,float)): return round(float(o),3)
    if isinstance(o,np.integer): return int(o)
    return o
json.dump({'rect':[X0,Y0,X1,Y1],'models':_c(MOD),'trees':_c(TREES),'tops':_c(TOPS),'places':{k:[round(float(x),2),round(float(y),2)] for k,(x,y) in PL.items()}},open('mt.json','w'),separators=(',',':'))
import os;print('casas',nh,'modelos',len(MOD),'árvores',len(TREES),'zc',round(zc,2),{f:os.path.getsize(f) for f in ['mt_tex.webp','mt_h.png','mt.json']})
