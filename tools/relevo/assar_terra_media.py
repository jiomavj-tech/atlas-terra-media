import numpy as np, cv2, json
from PIL import Image
from scipy import ndimage as nd
rng=np.random.default_rng(5)
hgt=np.load('hgt.npy');water=np.load('water.npy');fm=np.load('forest.npy');snow=np.load('snow.npy');col=np.load('col.npy')
GW,GH=492,438
h=cv2.resize(hgt,(GW,GH),interpolation=cv2.INTER_AREA);h=np.maximum(h,-0.04)
enc=np.clip((h+0.05)/1.25,0,1)*65535;hi=(enc//256).astype(np.uint8);lo=(enc%256).astype(np.uint8)
Image.fromarray(np.dstack([hi,lo,np.zeros_like(hi)]),'RGB').save('height_hi.png',optimize=True)
W,H=984,877;HS=46*1.05
hf=cv2.resize(hgt,(W,H),interpolation=cv2.INTER_AREA)*HS
gy,gx=np.gradient(hf);L=np.array([-0.62,-0.55,0.56]);L/=np.linalg.norm(L)
n=np.dstack([-gx,-gy,np.ones_like(hf)]);n/=np.linalg.norm(n,axis=2,keepdims=True);lam=np.clip(n@L,0,1)
s=0.5;hs=cv2.resize(hf,(int(W*s),int(H*s)));yy,xx=np.mgrid[0:hs.shape[0],0:hs.shape[1]].astype(np.float32)
sx,sy=L[0]/np.hypot(L[0],L[1]),L[1]/np.hypot(L[0],L[1]);tanE=L[2]/np.hypot(L[0],L[1]);sh=np.zeros_like(hs)
for t in range(1,160):
    d=float(t);hh=nd.map_coordinates(hs,[yy+sy*d,xx+sx*d],order=1,mode='nearest');sh=np.maximum(sh,np.clip((hh-(hs+d/s*tanE))/2.5,0,1))
sh=cv2.resize(cv2.GaussianBlur(sh,(0,0),1.2),(W,H))
ao=np.clip(1-(cv2.GaussianBlur(hf,(0,0),9)-hf)*0.05,0.55,1)
flatL=float(L[2])
light=(0.55+0.62*(lam-flatL)+0.45*flatL)*(1-0.5*sh)*ao
wat=cv2.resize(water,(W,H),interpolation=cv2.INTER_AREA);sn=cv2.resize(snow,(W,H),interpolation=cv2.INTER_AREA)
Image.fromarray((np.dstack([np.clip(light/1.3,0,1),np.clip(sn,0,1),np.clip(wat,0,1)])*255).astype(np.uint8),'RGB').save('light_hi.png',optimize=True)
f=cv2.resize(fm,(W,H),interpolation=cv2.INTER_AREA)
pts=[]
for x,y in rng.random((140000,2))*[W,H]:
    xi,yi=int(x),int(y)
    if f[yi,xi]>0.35 and rng.random()<f[yi,xi]**1.3*0.5 and wat[yi,xi]<0.2:
        c=col[yi,xi]*[0.6,0.7,0.6];pts.append([round(float(x),1),round(float(y),1),round(float(c[0]),2),round(float(c[1]),2),round(float(c[2]),2)])
print('árvores',len(pts));json.dump(pts,open('trees.json','w'),separators=(',',':'))
import os;print({k:os.path.getsize(k) for k in ['height_hi.png','light_hi.png','trees.json','me_tex.webp']})
