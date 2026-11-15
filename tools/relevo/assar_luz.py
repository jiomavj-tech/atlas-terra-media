import numpy as np, cv2, json
from PIL import Image
from scipy import ndimage as nd
rng=np.random.default_rng(7)
q=np.asarray(Image.open('height.png').convert('L'),np.float32)/255      # 246x220
H0=np.maximum(-0.03,q*1.18-0.08)                                          # unidades "relativas" (x46 = altura)
GW,GH=492,438
h=cv2.resize(H0,(GW,GH),interpolation=cv2.INTER_CUBIC)
def fbm(w,hh,oct=5,base=8):
    out=np.zeros((hh,w),np.float32);amp=1;tot=0
    for o in range(oct):
        n=rng.standard_normal((base*2**o+1,int(base*2**o*w/hh)+1)).astype(np.float32)
        out+=cv2.resize(n,(w,hh),interpolation=cv2.INTER_CUBIC)*amp;tot+=amp;amp*=0.5
    return out/tot
mt=np.clip((h-0.12)/0.35,0,1)
ridge=1-np.abs(fbm(GW,GH,5,10))                     # cristas
h=h+mt*(ridge-0.6)*0.12+fbm(GW,GH,4,16)*0.012
h=np.maximum(h,-0.03)
enc=np.clip((h+0.05)/1.25,0,1)*65535
hi=(enc//256).astype(np.uint8);lo=(enc%256).astype(np.uint8)
Image.fromarray(np.dstack([hi,lo,np.zeros_like(hi)]),'RGB').save('height_hi.png',optimize=True)
# ---- mapa de luz em resolução cheia ----
W,H=984,877;HS=46*1.35
hf=cv2.resize(h,(W,H),interpolation=cv2.INTER_CUBIC)*HS
gy,gx=np.gradient(hf)
L=np.array([-0.62,-0.55,0.56]);L/=np.linalg.norm(L)
n=np.dstack([-gx,-gy,np.ones_like(hf)]);n/=np.linalg.norm(n,axis=2,keepdims=True)
lam=np.clip(n@L,0,1)
# sombras projetadas (marcha na direção do sol, em resolução reduzida)
s=0.5;hs=cv2.resize(hf,(int(W*s),int(H*s)));yy,xx=np.mgrid[0:hs.shape[0],0:hs.shape[1]].astype(np.float32)
sx,sy=L[0]/np.hypot(L[0],L[1]),L[1]/np.hypot(L[0],L[1]);tanE=L[2]/np.hypot(L[0],L[1])
sh=np.zeros_like(hs)
for t in range(1,140):
    d=t*1.0;hh=nd.map_coordinates(hs,[yy+sy*d,xx+sx*d],order=1,mode='nearest')
    sh=np.maximum(sh,np.clip((hh-(hs+d/s*tanE))/2.5,0,1))
sh=cv2.resize(cv2.GaussianBlur(sh,(0,0),1.2),(W,H))
ao=np.clip(1-(cv2.GaussianBlur(hf,(0,0),9)-hf)*0.05,0.55,1)
light=(0.38+0.78*lam)*(1-0.5*sh)*ao
img=np.asarray(Image.open('mapa_limpo.png').convert('RGB')).astype(np.float32)/255
r,g,b=img[...,0],img[...,1],img[...,2]
water=((b>r+0.05)&(b>g-0.02)&(hf<2)).astype(np.float32);water=cv2.GaussianBlur(water,(0,0),1.0)
snow=np.clip((hf/HS-0.62)/0.25,0,1)*np.clip((img.mean(-1)-0.38)/0.2,0,1)*(1-np.clip((r-b-0.06)/0.1,0,1))
Image.fromarray((np.dstack([np.clip(light/1.3,0,1),snow,water])*255).astype(np.uint8),'RGB').save('light_hi.png',optimize=True)
# ---- árvores: verde-escuro com textura ----
hsv=cv2.cvtColor((img*255).astype(np.uint8),cv2.COLOR_RGB2HSV)
fm=((hsv[...,0]>28)&(hsv[...,0]<85)&(hsv[...,1]>70)&(hsv[...,2]<150)&(water<0.2)&(hf<HS*0.35)).astype(np.float32)
fm=cv2.GaussianBlur(fm,(0,0),3)
bm=(fm>0.42).astype(np.uint8);bm[:, :75]=0;bm[:24,:]=0;bm[-24:,:]=0;bm[:,-20:]=0
nl,lab,st,_=cv2.connectedComponentsWithStats(bm)
keep=np.zeros_like(bm)
for i in range(1,nl):
    if st[i,cv2.CC_STAT_AREA]>900: keep[lab==i]=1
fm=cv2.GaussianBlur(keep.astype(np.float32),(0,0),2)*fm
pts=[]
cand=rng.random((60000,2))*[W,H]
for x,y in cand:
    xi,yi=int(x),int(y)
    if rng.random()<fm[yi,xi]**1.2*0.7:
        c=img[yi,xi];pts.append([round(x,1),round(y,1),round(float(c[0]),2),round(float(c[1]),2),round(float(c[2]),2)])
print('árvores',len(pts))
json.dump(pts,open('trees.json','w'),separators=(',',':'))
Image.fromarray((np.clip(light/1.3,0,1)*255).astype(np.uint8)).resize((492,438)).save('lp2.png')
Image.fromarray((fm*255).astype(np.uint8)).resize((492,438)).save('fm.png')
import os;print({f:os.path.getsize(f) for f in ['height_hi.png','light_hi.png','trees.json']})
