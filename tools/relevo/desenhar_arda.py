import numpy as np, cv2, json
from PIL import Image
rng=np.random.default_rng(3)
RW,RH=1600,1200   # raster "mapa" (u,v)
def P(pts): return np.array([[x*RW,y*RH] for x,y in pts],np.int32)
def fill(pts,val=255):
    m=np.zeros((RH,RW),np.uint8);cv2.fillPoly(m,[P(pts)],val);return m
LAND={
'aman':[(0.335,0.0),(0.385,0.0),(0.36,0.06),(0.31,0.14),(0.26,0.24),(0.215,0.34),(0.195,0.44),(0.205,0.52),(0.225,0.60),(0.255,0.70),(0.285,0.80),(0.315,0.90),(0.33,1.0),(0.25,1.0),(0.17,0.90),(0.09,0.78),(0.04,0.62),(0.03,0.46),(0.06,0.30),(0.13,0.16),(0.22,0.06)],
'helcar':[(0.36,0.0),(0.44,0.0),(0.43,0.03),(0.39,0.05),(0.365,0.04)],
'meio':[(0.42,0.0),(0.72,0.0),(0.73,0.08),(0.70,0.13),(0.74,0.20),(0.73,0.30),(0.70,0.40),(0.66,0.50),(0.62,0.60),(0.57,0.66),(0.51,0.64),(0.48,0.56),(0.47,0.46),(0.45,0.38),(0.41,0.32),(0.40,0.26),(0.44,0.21),(0.49,0.22),(0.51,0.17),(0.47,0.13),(0.43,0.10),(0.41,0.05)],
'escura':[(0.44,1.0),(0.47,0.90),(0.52,0.82),(0.58,0.77),(0.65,0.74),(0.70,0.68),(0.73,0.58),(0.75,0.45),(0.76,0.33),(0.775,0.24),(0.80,0.22),(0.81,0.35),(0.81,0.55),(0.80,0.75),(0.78,0.90),(0.74,1.0)],
'leste':[(0.86,0.26),(0.885,0.24),(0.91,0.32),(0.92,0.45),(0.91,0.58),(0.89,0.66),(0.87,0.60),(0.865,0.45)],
}
land=np.zeros((RH,RW),np.uint8)
for k,v in LAND.items(): land=np.maximum(land,fill(v))
for x,y,r in [(0.300,0.47,0.014)]+[(0.285+0.02*np.sin(t*0.9),0.25+t*0.035,0.004) for t in range(11)]:
    cv2.circle(land,(int(x*RW),int(y*RH)),int(r*RW),255,-1)
lake=fill([(0.55,0.15),(0.62,0.14),(0.67,0.16),(0.66,0.19),(0.60,0.20),(0.55,0.18)])
inner=fill([(0.58,0.30),(0.66,0.26),(0.71,0.32),(0.68,0.44),(0.63,0.52),(0.59,0.46)])  # Mar Interior
land=np.where((lake>0)|(inner>0),0,land)
# litoral irregular: deforma com ruído
def noise(w,h,base,octv=5,seed=0):
    r=np.random.default_rng(seed);out=np.zeros((h,w),np.float32);a=1;t=0
    for o in range(octv):
        n=r.standard_normal((int(base*2**o*h/w)+2,base*2**o+2)).astype(np.float32);out+=cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
    return out/t
dx=noise(RW,RH,8,6,1)*34+noise(RW,RH,40,3,3)*8;dy=noise(RW,RH,8,6,2)*34+noise(RW,RH,40,3,4)*8
mx,my=np.meshgrid(np.arange(RW,dtype=np.float32),np.arange(RH,dtype=np.float32))
landf=cv2.remap(cv2.GaussianBlur(land.astype(np.float32)/255,(0,0),2),mx+dx,my+dy,cv2.INTER_LINEAR)
L=(landf>0.5).astype(np.float32)
# altura
def ridge(pts,w,hgt):
    m=np.zeros((RH,RW),np.float32);cv2.polylines(m,[P(pts)],False,1.0,int(w*1.8));m=cv2.remap(m,mx+dx*0.8,my+dy*0.8,cv2.INTER_LINEAR);m=cv2.GaussianBlur(m,(0,0),w*0.9);return m/max(1e-6,m.max())*hgt
R=noise(RW,RH,26,5,5);rid=(1-np.abs(R))**2
hgt=L*(0.06+0.05*noise(RW,RH,5,4,6))
mount=np.zeros_like(hgt)
mount=np.maximum(mount,ridge([(0.355,0.03),(0.30,0.13),(0.25,0.24),(0.215,0.36),(0.21,0.48),(0.23,0.60),(0.265,0.72),(0.30,0.85),(0.32,0.97)],18,1.0))  # Pelóri
mount=np.maximum(mount,ridge([(0.47,0.02),(0.475,0.10),(0.465,0.18)],12,0.55))   # Ered Luin
mount=np.maximum(mount,ridge([(0.505,0.24),(0.50,0.33),(0.495,0.42)],12,0.5))    # Montanhas Cinzentas/Sombrias
mount=np.maximum(mount,ridge([(0.53,0.03),(0.60,0.05),(0.68,0.06)],10,0.55))     # Ered Engrin (Montanhas de Ferro)
mount=np.maximum(mount,ridge([(0.70,0.10),(0.715,0.20),(0.705,0.30)],12,0.65))   # Orocarni
mount=np.maximum(mount,ridge([(0.79,0.28),(0.795,0.50),(0.79,0.72)],12,0.6))     # Montanhas do Sol? (leste)
mount=np.maximum(mount,ridge([(0.90,0.30),(0.905,0.45),(0.895,0.60)],10,0.55))   # Muralhas do Sol (Terras do Leste)
yy,xx=np.mgrid[0:RH,0:RW];tq=np.exp(-(((xx-0.205*RW)**2+(yy-0.46*RH)**2)/(2*(0.012*RW)**2)))*1.5  # Taniquetil
hgt=hgt+L*(mount*(0.45+0.65*rid)+tq)
hgt=cv2.GaussianBlur(hgt,(0,0),1.2)
sea=1-L
dist=cv2.distanceTransform((sea>0.5).astype(np.uint8),cv2.DIST_L2,5)
depth=np.clip(dist/90,0,1)
hgt=hgt*L-(0.02+0.10*depth)*sea
# cores
ice=np.clip(1-(yy/RH)/0.09,0,1)*L
green=np.array([0.36,0.50,0.24]);dry=np.array([0.62,0.55,0.32]);dark=np.array([0.36,0.24,0.17]);forest=np.array([0.18,0.33,0.16]);rock=np.array([0.48,0.44,0.40]);snow=np.array([0.93,0.94,0.96])
nz=noise(RW,RH,8,5,9)*0.5+0.5;fz=noise(RW,RH,34,4,11)
col=green[None,None]*(1-nz[...,None])+dry[None,None]*nz[...,None]
col=np.where((fz>0.25)[...,None],forest[None,None]*0.9+col*0.1,col)
darkm=fill(LAND['escura']).astype(np.float32)/255;darkm=cv2.GaussianBlur(darkm,(0,0),20)
col=col*(1-darkm[...,None]*0.65)+dark[None,None]*darkm[...,None]*0.65
amanm=cv2.GaussianBlur(fill(LAND['aman']).astype(np.float32)/255,(0,0),10)
col=col*(1-amanm[...,None]*0.35)+np.array([0.42,0.62,0.30])[None,None]*amanm[...,None]*0.35   # Aman mais verde e luminosa
m=np.clip((hgt-0.25)/0.4,0,1)[...,None];col=col*(1-m)+rock[None,None]*m
s=np.clip((hgt-0.75)/0.3,0,1)[...,None];col=col*(1-s)+snow[None,None]*s
col=col*(1-ice[...,None])+snow[None,None]*ice[...,None]
shallow=np.array([0.20,0.48,0.56]);deep=np.array([0.06,0.16,0.33])
seacol=shallow[None,None]*(1-depth[...,None])+deep[None,None]*depth[...,None]
ice_s=np.clip(1-(yy/RH)/0.06,0,1)*sea;seacol=seacol*(1-ice_s[...,None]*0.7)+snow[None,None]*ice_s[...,None]*0.7
# relevo sombreado
gy,gx=np.gradient(hgt*90);n=np.dstack([-gx,-gy,np.ones_like(gx)]);n/=np.linalg.norm(n,axis=2,keepdims=True)
lv=np.array([-0.6,-0.5,0.62]);lv/=np.linalg.norm(lv);sh=np.clip(n@lv,0,1)
col=col*(0.55+0.62*sh[...,None])
# costa: linha escura + espuma
edge=cv2.morphologyEx((L>0.5).astype(np.uint8),cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8)).astype(np.float32)
img=np.where(L[...,None]>0.5,col,seacol)
img=img*(1-edge[...,None]*0.35)
paper=noise(RW,RH,60,3,13)[...,None]*0.035
img=np.clip(img+paper,0,1)
Image.fromarray((img*255).astype(np.uint8)).save('mapa_arda.png')
# ---- equiretangular para o globo ----
EW,EH=2048,1024
lon=(np.arange(EW)+0.5)/EW*360-180;lat=90-(np.arange(EH)+0.5)/EH*180
LO,LA=np.meshgrid(lon,lat)
U=(LO+100)/200;V=(68-LA)/136
inside=(U>=0)&(U<=1)&(V>=0)&(V<=1)
ux=np.clip(U*RW,0,RW-1).astype(np.float32);vy=np.clip(V*RH,0,RH-1).astype(np.float32)
eq=cv2.remap((img*255).astype(np.uint8),ux,vy,cv2.INTER_LINEAR)
eh=cv2.remap(hgt.astype(np.float32),ux,vy,cv2.INTER_LINEAR)
# fora do mapa: Ekkaia (oceano exterior) e gelo nos polos
ek=np.dstack([0.05+0.03*np.cos(np.radians(LA)),0.13+0.04*np.cos(np.radians(LA)),np.full_like(LA,0.30)])*255
fade=np.clip(np.minimum.reduce([U+0.04,1.04-U,V+0.04,1.04-V])/0.04,0,1)
eq=(eq*fade[...,None]+ek*(1-fade[...,None]))
pole=np.clip((np.abs(LA)-74)/8,0,1)[...,None];eq=eq*(1-pole)+np.array([235,240,245])*pole
eh=eh*fade-0.12*(1-fade)
Image.fromarray(eq.astype(np.uint8)).save('arda_eq.jpg',quality=86)
cv2.imwrite('arda_eq.webp',cv2.cvtColor(eq.astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,84])
hh=cv2.resize(eh,(512,256),interpolation=cv2.INTER_AREA);enc=np.clip((hh+0.15)/2.0,0,1)*255
Image.fromarray(enc.astype(np.uint8)).save('arda_h.png',optimize=True)
import os;print({f:os.path.getsize(f) for f in ['arda_eq.webp','arda_h.png']})
Image.fromarray((img*255).astype(np.uint8)).resize((800,600)).save('preview.png')
