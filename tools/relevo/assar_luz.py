import numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd
q=np.asarray(Image.open('/tmp/claude-0/relevo/height.png').convert('L'),np.float32)/255
HS=46.0;GW,GH=246,220;dx=984/(GW-1);dy=877/(GH-1)
h=np.maximum(-0.03,q*1.18-0.08)*HS
gy,gx=np.gradient(h,dy,dx)
L=np.array([-1.0,-1.0,1.25]);L/=np.linalg.norm(L)
n=np.dstack([-gx*1.6,-gy*1.6,np.ones_like(h)]);n/=np.linalg.norm(n,axis=2,keepdims=True)
lam=np.clip(n@L,0,1)
# sombras projetadas: anda na direção do sol e vê se algum terreno fica acima do raio
elev=np.arctan2(L[2],np.hypot(L[0],L[1]))
sx,sy=L[0]/np.hypot(L[0],L[1]),L[1]/np.hypot(L[0],L[1])
sh=np.zeros_like(h);yy,xx=np.mgrid[0:GH,0:GW].astype(np.float32)
for t in range(1,90):
    px=xx+sx*t*0.8;py=yy+sy*t*0.8
    hh=nd.map_coordinates(h,[py,px],order=1,mode='nearest')
    dist=t*0.8*np.hypot(dx*sx,dy*sy)
    over=hh-(h+dist*np.tan(elev)*0.9)
    sh=np.maximum(sh,np.clip(over/3.0,0,1))
sh=nd.gaussian_filter(sh,1.0)
ao=np.clip(1-(nd.gaussian_filter(h,5)-h)*0.035,0.6,1.0)
light=(0.40+0.72*lam)*(1-0.42*sh)*ao
water=(q*1.18-0.08<-0.01).astype(np.float32)
water=nd.gaussian_filter(water,0.8)
rgb=np.dstack([q*255,np.clip(light/1.4,0,1)*255,water*255]).astype(np.uint8)
Image.fromarray(rgb,'RGB').save('/tmp/claude-0/relevo/height_rgb.png',optimize=True)
Image.fromarray((np.clip(light/1.4,0,1)*255).astype(np.uint8)).resize((492,440)).save('/tmp/claude-0/relevo/light_preview.png')
import os;print(os.path.getsize('/tmp/claude-0/relevo/height_rgb.png'),light.min(),light.max())
