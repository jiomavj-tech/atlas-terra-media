import numpy as np, json, sys
from PIL import Image, ImageDraw
from scipy import ndimage as nd
W,H=984,877
im=np.asarray(Image.open('/tmp/claude-0/m3d/map.webp').convert('RGB')).astype(np.float32)/255
r,g,b=im[...,0],im[...,1],im[...,2]
mx=im.max(-1);mn=im.min(-1);sat=(mx-mn)/(mx+1e-5);val=mx
water=(b>r+0.04)&(b>g-0.02)&(val>0.18)
lab,nl=nd.label(water)
objs=nd.find_objects(lab)
areas=nd.sum(water,lab,range(1,nl+1))
for i,(sl,a) in enumerate(zip(objs,areas)):
    hgt=sl[0].stop-sl[0].start;wid=sl[1].stop-sl[1].start;fill=a/max(1,hgt*wid)
    if a<2500 and (fill>0.35 or a<150): water[lab==i+1]=False   # ícones e manchas, não rios
gray=(sat<0.28)&~water
dark_red=(r>g*1.25)&(val<0.45)
cand=(gray|dark_red)
# áreas de interface desenhadas na imagem (botões, legenda, bússola): sem relevo
ui=[(0,20,62,215),(0,612,228,845),(832,18,984,68),(812,720,984,860)]
for x0,y0,x1,y1 in ui: cand[y0:y1,x0:x1]=False
cand=nd.binary_opening(cand,iterations=1)
dens=nd.gaussian_filter(cand.astype(np.float32),4)
def poly(pts,sig=10):
    m=Image.new('L',(W,H),0);ImageDraw.Draw(m).polygon(pts,fill=255);return nd.gaussian_filter(np.asarray(m,np.float32)/255,sig)
ranges=[
 [(380,0),(705,0),(705,60),(600,110),(565,170),(552,262),(522,352),(492,392),(445,382),(440,300),(455,200),(430,120),(380,60)],  # Montanhas Sombrias + Cinzentas
 [(280,18),(385,18),(425,100),(385,142),(300,122)],   # Angmar
 [(20,118),(142,108),(152,200),(62,232),(20,200)],    # Ered Luin norte
 [(108,288),(222,298),(232,372),(150,392),(98,350)],  # Ered Luin sul
 [(268,418),(382,428),(382,522),(288,522)],           # Methedras / Isengard
 [(180,560),(320,518),(420,538),(520,556),(605,572),(615,612),(520,622),(420,642),(300,700),(200,690)], # Ered Nimrais (Montanhas Brancas)
 [(820,0),(984,0),(984,62),(858,62)],                 # Colinas de Ferro / norte
 [(625,440),(984,425),(984,725),(820,745),(690,745),(625,700)], # Mordor (cordilheiras)
]
M=np.zeros((H,W),np.float32)
for p in ranges: M=np.maximum(M,poly(p))
M=np.clip(M*1.15,0,1)
snow=nd.gaussian_filter(((val>0.78)&(sat<0.22)).astype(np.float32),2)
Hm=M*(0.08+0.92*np.clip(dens*1.6,0,1)**1.3)+M*0.18*snow+(1-M)*0.06*np.clip(dens*1.5,0,1)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
# ícones e torres desenhados no mapa não são montanhas: achatar ao redor deles
icons=[(90,258),(217,262),(425,222),(476,333),(650,213),(605,385),(452,425),(532,497),(476,598),(326,490),(565,625),(690,630),(808,595),(835,568),(352,90),(160,203),(282,200),(465,525)]
flat=np.ones((H,W),np.float32)
for cx,cy in icons: flat=np.minimum(flat,1-np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*24*24))*0.92)
Hm=Hm*flat
def peak(cx,cy,s,a): return a*np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*s*s))
Hm=np.maximum(Hm,peak(800,140,15,0.95))      # Erebor
Hm=np.maximum(Hm,peak(884,492,13,1.05))      # Orodruin
Hm+=peak(660,470,22,0.18)                    # Emyn Muil
Hm=nd.gaussian_filter(Hm,2.6)
wm=nd.gaussian_filter(water.astype(np.float32),1.5)
for x0,y0,x1,y1 in ui: wm[y0:y1,x0:x1]=nd.gaussian_filter(water.astype(np.float32),8)[y0:y1,x0:x1]
Hm=Hm*(1-wm)+(-0.06)*wm
q=np.clip((Hm+0.08)/1.18,0,1)
small=Image.fromarray((q*255).astype(np.uint8)).resize((246,220),Image.LANCZOS)
small.save('height.png',optimize=True)
# visualização: sombreamento
hs=np.asarray(small,np.float32)/255
gy,gx=np.gradient(hs*60)
L=np.array([-1,-1,1.2]);L/=np.linalg.norm(L)
n=np.dstack([-gx,-gy,np.ones_like(gx)]);n/=np.linalg.norm(n,axis=2,keepdims=True)
shade=np.clip(n@L,0,1)
base=np.asarray(Image.open('/tmp/claude-0/m3d/map.webp').convert('RGB').resize((246,220)),np.float32)
out=np.clip(base*(0.55+0.65*shade[...,None]),0,255).astype(np.uint8)
Image.fromarray(out).resize((984,880)).save('preview.png')
Image.fromarray((q*255).astype(np.uint8)).save('height_full.png')
import os;print(os.path.getsize('height.png'))
