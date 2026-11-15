import numpy as np, cv2, json
from PIL import Image
rng=np.random.default_rng(11)
W,H=1968,1754          # textura (2x do espaço 984x877 do motor)
def P(pts): return np.array([[x*W,y*H] for x,y in pts],np.int32)
def noise(base,octv=5,seed=0,w=W,h=H):
    r=np.random.default_rng(seed);out=np.zeros((h,w),np.float32);a=1;t=0
    for o in range(octv):
        n=r.standard_normal((int(base*2**o*h/w)+2,base*2**o+2)).astype(np.float32);out+=cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
    return out/t
mx,my=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
DX=noise(10,6,1)*26+noise(60,3,3)*6;DY=noise(10,6,2)*26+noise(60,3,4)*6
def warp(m,k=1.0): return cv2.remap(m,mx+DX*k,my+DY*k,cv2.INTER_LINEAR)
def poly(pts,blur=2):
    m=np.zeros((H,W),np.float32);cv2.fillPoly(m,[P(pts)],1.0);return cv2.GaussianBlur(m,(0,0),blur)
def line(pts,w,blur=None):
    m=np.zeros((H,W),np.float32);cv2.polylines(m,[P(pts)],False,1.0,max(1,int(w)),cv2.LINE_AA);return cv2.GaussianBlur(m,(0,0),blur or max(1,w*0.5))
# ---------------- terra ----------------
LAND=[(0.06,0.0),(0.15,0.0),(0.17,0.04),(0.21,0.08),(0.26,0.095),(0.30,0.075),(0.33,0.035),(0.345,0.0),(1.0,0.0),(1.0,1.0),(0.47,1.0),(0.475,0.965),(0.455,0.94),(0.47,0.925),(0.50,0.91),(0.505,0.885),(0.515,0.86),(0.525,0.83),(0.535,0.805),
 (0.52,0.795),(0.50,0.792),(0.48,0.775),(0.455,0.76),(0.435,0.748),(0.42,0.742),(0.405,0.755),(0.385,0.77),(0.36,0.785),(0.335,0.795),(0.32,0.785),(0.31,0.76),(0.30,0.725),(0.29,0.69),(0.275,0.655),(0.255,0.62),(0.235,0.59),(0.215,0.56),(0.19,0.53),(0.16,0.495),(0.13,0.465),(0.10,0.435),(0.075,0.40),(0.065,0.37),(0.075,0.345),(0.10,0.33),(0.13,0.322),(0.165,0.312),
 (0.13,0.30),(0.10,0.292),(0.075,0.282),(0.06,0.26),(0.055,0.22),(0.06,0.16),(0.055,0.10),(0.06,0.05)]
land=warp(poly(LAND,3))
for u,v,r in [(0.475,0.80,0.012),(0.035,0.30,0.012)]: cv2.circle(land,(int(u*W),int(v*H)),int(r*W),1.0,-1)   # Tolfalas, ilhota
LAKES=[[(0.735,0.36),(0.80,0.33),(0.86,0.35),(0.875,0.42),(0.84,0.48),(0.78,0.47),(0.74,0.42)],          # Mar de Rhûn
 [(0.72,0.69),(0.77,0.68),(0.80,0.71),(0.78,0.74),(0.73,0.735)],                                        # Nurnen
 [(0.679,0.155),(0.69,0.158),(0.692,0.20),(0.682,0.205)],                                                 # Lago Longo
 [(0.553,0.52),(0.565,0.52),(0.568,0.552),(0.556,0.552)],                                                 # Nen Hithoel
 [(0.23,0.175),(0.25,0.17),(0.255,0.195),(0.235,0.20)],                                                   # Lago Evendim
 [(0.18,0.06),(0.23,0.09),(0.27,0.095),(0.31,0.07),(0.33,0.03),(0.33,0.0),(0.15,0.0)]]                     # Baía de Forochel (gelo)
lakes=np.zeros((H,W),np.float32)
for L in LAKES[:5]: lakes=np.maximum(lakes,warp(poly(L,2),1.1))
# rios: (pontos, largura em px)
RIV={'Anduin':([(0.52,0.09),(0.522,0.16),(0.515,0.22),(0.51,0.30),(0.505,0.37),(0.51,0.44),(0.53,0.48),(0.55,0.51),(0.56,0.535),(0.565,0.56),(0.578,0.59),(0.586,0.625),(0.59,0.66),(0.582,0.69),(0.57,0.715),(0.565,0.735),(0.55,0.77),(0.535,0.805)],[4,9]),
 'Brandevin':([(0.245,0.20),(0.25,0.24),(0.258,0.30),(0.252,0.36),(0.235,0.44),(0.21,0.51),(0.195,0.54)],[3,6]),
 'Fontegris':([(0.37,0.18),(0.378,0.30),(0.372,0.40),(0.35,0.44),(0.33,0.475),(0.30,0.52),(0.27,0.555),(0.235,0.585)],[2,7]),
 'Ruidoságua':([(0.432,0.27),(0.42,0.32),(0.40,0.37),(0.374,0.40)],[2,3]),
 'Glanduin':([(0.44,0.47),(0.40,0.465),(0.36,0.47),(0.335,0.475)],[2,3]),
 'Isen':([(0.432,0.55),(0.43,0.585),(0.415,0.605),(0.38,0.62),(0.34,0.645),(0.31,0.665),(0.29,0.675)],[2,5]),
 'Entágua':([(0.455,0.515),(0.48,0.535),(0.51,0.555),(0.54,0.575),(0.565,0.595),(0.582,0.615)],[2,4]),
 'Veio-de-Prata':([(0.455,0.43),(0.48,0.445),(0.505,0.46),(0.525,0.475)],[1,3]),
 'Limclaro':([(0.462,0.475),(0.50,0.49),(0.545,0.505)],[1,3]),
 'Rio Corrente':([(0.69,0.205),(0.705,0.25),(0.725,0.30),(0.75,0.345)],[2,4]),
 'Rio da Floresta':([(0.62,0.12),(0.645,0.15),(0.67,0.165),(0.68,0.17)],[1,3]),
 'Carnen':([(0.785,0.15),(0.775,0.21),(0.76,0.27),(0.75,0.33)],[1,3]),
 'Morthond':([(0.48,0.635),(0.47,0.68),(0.455,0.72),(0.44,0.745)],[1,3]),
 'Gilrain':([(0.52,0.655),(0.51,0.70),(0.50,0.745),(0.495,0.79)],[1,3]),
 'Poros':([(0.645,0.75),(0.61,0.765),(0.58,0.77),(0.555,0.775)],[1,3]),
 'Harnen':([(0.70,0.80),(0.63,0.83),(0.57,0.855),(0.525,0.87)],[1,3]),
 'Lúnir':([(0.11,0.22),(0.14,0.27),(0.165,0.31)],[1,4]),
 'Hoarwell-sul':([(0.30,0.52),(0.27,0.555)],[1,1])}
rivers=np.zeros((H,W),np.float32)
for k,(pts,(w0,w1)) in RIV.items():
    n=len(pts)
    for i in range(n-1):
        w=w0+(w1-w0)*i/max(1,n-2)
        seg=np.zeros((H,W),np.float32);cv2.line(seg,tuple(P([pts[i]])[0]),tuple(P([pts[i+1]])[0]),1.0,max(1,int(w*1.3)),cv2.LINE_AA);rivers=np.maximum(rivers,seg)
rivers=cv2.remap(cv2.GaussianBlur(rivers,(0,0),0.8),mx+noise(40,4,51)*7+DX*0.3,my+noise(40,4,52)*7+DY*0.3,cv2.INTER_LINEAR)
L=np.clip(land,0,1)*(1-np.clip(lakes,0,1))
water_all=np.maximum(1-L,np.clip(rivers*1.4,0,1)*L)
landB=(L>0.5).astype(np.float32)
# ---------------- altura ----------------
ridgeN=(1-np.abs(noise(30,5,5)))**2
def rng_(pts,w,h,blur=None): return warp(line(pts,w*W/984*2.2,blur),0.6)*h
MT=[([(0.10,0.06),(0.105,0.13),(0.115,0.20),(0.125,0.27)],12,0.70),([(0.11,0.335),(0.10,0.38),(0.09,0.42)],10,0.55),
 ([(0.47,0.035),(0.465,0.10),(0.458,0.18),(0.455,0.26),(0.452,0.34),(0.45,0.42),(0.442,0.49),(0.433,0.545)],16,1.0),
 ([(0.48,0.075),(0.53,0.065),(0.58,0.07),(0.63,0.075),(0.665,0.085)],11,0.65),
 ([(0.755,0.115),(0.785,0.11),(0.815,0.125)],9,0.55),
 ([(0.36,0.11),(0.40,0.095),(0.44,0.085)],10,0.55),
 ([(0.405,0.635),(0.44,0.625),(0.48,0.63),(0.52,0.64),(0.555,0.648),(0.575,0.652)],13,0.85),([(0.405,0.635),(0.37,0.68),(0.345,0.73),(0.335,0.775)],10,0.6),
 ([(0.64,0.585),(0.68,0.575),(0.72,0.57),(0.77,0.575),(0.83,0.585)],11,0.8),
 ([(0.636,0.59),(0.628,0.625),(0.627,0.66),(0.632,0.70),(0.64,0.74),(0.68,0.755),(0.74,0.76),(0.80,0.755),(0.84,0.745)],11,0.8),
 ([(0.565,0.24),(0.585,0.30),(0.60,0.36)],7,0.30),   # Montanhas de Trevamata
 ([(0.84,0.60),(0.87,0.70),(0.88,0.78)],8,0.4)]       # Khand/leste
mount=np.zeros((H,W),np.float32)
for pts,w,h in MT: mount=np.maximum(mount,rng_(pts,w,h))
HILLS=[(0.27,0.19,0.035,0.25),(0.34,0.29,0.012,0.25),(0.42,0.21,0.04,0.3),(0.275,0.335,0.02,0.18),(0.575,0.525,0.025,0.30),(0.20,0.24,0.03,0.15),(0.44,0.585,0.012,0.35),
 (0.50,0.60,0.02,0.18),(0.39,0.52,0.04,0.22),(0.62,0.85,0.06,0.15),(0.86,0.90,0.08,0.25),(0.30,0.40,0.03,0.12)]
yy,xx=mx,my
hills=np.zeros((H,W),np.float32)
for u,v,r,h in HILLS: hills=np.maximum(hills,np.exp(-(((mx-u*W)**2+(my-v*H)**2)/(2*(r*W)**2)))*h)
hills*=0.6+0.8*np.clip(noise(40,4,8)*0.5+0.5,0,1)
peaks=[(0.68,0.13,0.010,1.0),(0.70,0.645,0.011,1.05),(0.449,0.40,0.008,1.25),(0.47,0.04,0.009,1.1)]
pk=np.zeros((H,W),np.float32)
for u,v,r,h in peaks: pk=np.maximum(pk,np.exp(-np.sqrt((mx-u*W)**2+(my-v*H)**2)/(r*W*1.1))*h*(0.8+0.35*ridgeN))
MOR=warp(poly([(0.64,0.59),(0.73,0.585),(0.83,0.595),(0.835,0.67),(0.82,0.745),(0.70,0.75),(0.64,0.745),(0.632,0.66)],14),1.6)
base=0.05+0.04*noise(6,4,6)
hgt=landB*(base+hills+MOR*0.12+mount*(0.40+0.7*ridgeN))
hgt=np.maximum(hgt,pk*landB)
hgt=cv2.GaussianBlur(hgt,(0,0),1.0)
hgt=hgt*(1-np.clip(rivers*1.2,0,1)*0.85)
sea=1-L;dist=cv2.distanceTransform((sea>0.5).astype(np.uint8),cv2.DIST_L2,5);depth=np.clip(dist/110,0,1)
hgt=np.where(L>0.5,hgt,-(0.02+0.08*depth))
# ---------------- cores ----------------
def soft(pts,b=30): return warp(poly(pts,b),2.2)
C=lambda r,g,b: np.array([r,g,b],np.float32)/255
reg=[ # (máscara, cor, força)
 (np.ones((H,W),np.float32), C(104,132,72),1.0),  # Eriador verde
 (soft([(0,0),(1,0),(1,0.10),(0,0.12)],40), C(170,170,150),0.85),  # Ermos do Norte (tundra)
 (soft([(0.44,0.49),(0.60,0.50),(0.60,0.62),(0.44,0.62)],25), C(150,160,88),0.75),  # Rohan
 (soft([(0.54,0.47),(0.62,0.46),(0.63,0.53),(0.55,0.53)],20), C(140,112,70),0.8),  # Terras Pardas
 (soft([(0.60,0.53),(0.66,0.53),(0.66,0.58),(0.60,0.58)],12), C(105,104,80),0.8),   # Dagorlad / Pântanos
 (soft([(0.64,0.59),(0.83,0.59),(0.83,0.745),(0.64,0.745)],10), C(78,66,58),0.95),  # Mordor
 (soft([(0.70,0.68),(0.83,0.66),(0.83,0.745),(0.70,0.745)],20), C(102,96,64),0.6),  # Nurn
 (soft([(0.40,0.66),(0.62,0.62),(0.62,0.79),(0.40,0.79)],25), C(96,140,70),0.6),   # Gondor
 (soft([(0.45,0.80),(1,0.78),(1,1),(0.45,1)],45), C(200,170,110),0.95),             # Harad
 (soft([(0.66,0.78),(1,0.76),(1,0.86),(0.66,0.87)],35), C(180,150,98),0.6),         # Harad Próximo / Khand
 (soft([(0.70,0.18),(1,0.15),(1,0.58),(0.86,0.60),(0.72,0.55)],40), C(150,148,92),0.75), # Rhûn estepe
 (soft([(0.33,0.42),(0.43,0.44),(0.42,0.56),(0.30,0.60)],25), C(118,128,78),0.5),   # Terra Parda / Enedwaith
 (soft([(0.05,0.18),(0.13,0.18),(0.13,0.45),(0.05,0.45)],20), C(84,138,74),0.55),    # Lindon
]
col=np.zeros((H,W,3),np.float32)
for m,c,s in reg:
    m=np.clip(m,0,1)[...,None]*s;col=col*(1-m)+c[None,None]*m
vn=noise(50,5,9)[...,None];col*=1+vn*0.10
# florestas
FOR={'Trevamata':[(0.535,0.14),(0.62,0.12),(0.665,0.15),(0.67,0.24),(0.655,0.33),(0.635,0.40),(0.60,0.455),(0.56,0.46),(0.54,0.40),(0.535,0.30),(0.53,0.20)],
 'Lórien':[(0.495,0.44),(0.52,0.44),(0.53,0.47),(0.505,0.48)],'Fangorn':[(0.442,0.50),(0.48,0.505),(0.488,0.545),(0.45,0.55)],
 'Floresta Velha':[(0.255,0.295),(0.285,0.30),(0.29,0.33),(0.26,0.335)],'Bosque Chet':[(0.305,0.28),(0.325,0.28),(0.325,0.30),(0.305,0.30)],
 'Trollshaws':[(0.38,0.27),(0.41,0.265),(0.415,0.30),(0.385,0.305)],'Drúadan':[(0.555,0.63),(0.575,0.63),(0.575,0.65),(0.555,0.65)],
 'Ithilien':[(0.597,0.60),(0.618,0.60),(0.622,0.73),(0.596,0.74),(0.592,0.69)],'Eryn Vorn':[(0.18,0.46),(0.21,0.46),(0.21,0.50),(0.18,0.50)],
 'Firien':[(0.525,0.615),(0.54,0.615),(0.54,0.63),(0.525,0.63)],'Minhiriath':[(0.24,0.50),(0.27,0.49),(0.28,0.53),(0.25,0.54)],
 'Lindon':[(0.07,0.22),(0.10,0.21),(0.10,0.26),(0.075,0.27)],'Harad-oásis':[(0.62,0.92),(0.65,0.92),(0.65,0.95),(0.62,0.95)]}
fm=np.zeros((H,W),np.float32)
for k,pp in FOR.items(): fm=np.maximum(fm,warp(poly(pp,4),0.9))
fm=np.clip(fm*(0.75+0.5*np.clip(noise(70,3,12)*0.5+0.5,0,1)),0,1)*landB*(1-np.clip(mount,0,1))
fcol=C(40,78,40)*(1+noise(150,2,13)[...,None]*0.25)
col=col*(1-fm[...,None]*0.85)+fcol*fm[...,None]*0.85
# rocha, neve, gelo
m=np.clip((hgt-0.30)/0.35,0,1)[...,None];col=col*(1-m)+C(118,110,100)[None,None]*m
mordorRock=np.clip(MOR,0,1)[...,None]*np.clip((hgt-0.18)/0.3,0,1)[...,None];col=col*(1-mordorRock*0.8)+C(60,44,40)[None,None]*mordorRock*0.8
snow=np.clip((hgt-0.80)/0.25,0,1)*(1-np.clip(MOR,0,1))*np.clip((0.66-my/H)/0.05,0,1)*np.clip(1-np.exp(-np.sqrt((mx-0.68*W)**2+(my-0.13*H)**2)/(0.02*W))*2,0,1);col=col*(1-snow[...,None])+C(238,240,245)[None,None]*snow[...,None]
ice=np.clip((0.07-my/H)/0.05,0,1)*landB;col=col*(1-ice[...,None]*0.8)+C(232,238,244)[None,None]*ice[...,None]*0.8
# Gorgoroth: cinza e lava ao redor do Orodruin
lava=np.exp(-(((mx-0.70*W)**2+(my-0.648*H)**2)/(2*(0.03*W)**2)))*np.clip(noise(90,3,21),0,1)*1.6
col=col*(1-np.clip(lava,0,1)[...,None]*0.6)+C(210,70,20)[None,None]*np.clip(lava,0,1)[...,None]*0.6
# dunas em Harad
du=(np.sin(mx/14+noise(20,3,22)*8)*0.5+0.5)*soft([(0.45,0.84),(1,0.82),(1,1),(0.45,1)],40);col*=(1-du[...,None]*0.06)
# sombreamento do relevo
gy,gx=np.gradient(hgt*140);n=np.dstack([-gx,-gy,np.ones_like(gx)]);n/=np.linalg.norm(n,axis=2,keepdims=True)
lv=np.array([-0.62,-0.55,0.56]);lv/=np.linalg.norm(lv);shd=np.clip(n@lv,0,1)
flat=np.dstack([np.zeros_like(gx),np.zeros_like(gx),np.ones_like(gx)]);base_l=float(np.array([0,0,1])@lv)
col_l=col*(0.78+0.45*(shd-base_l))[...,None]
# água
shallow=C(70,130,140);deep=C(18,52,92)
seac=shallow[None,None]*(1-depth[...,None])+deep[None,None]*depth[...,None]
waves=noise(120,2,30)[...,None]*0.03;seac=seac+waves
icesea=np.clip((0.10-my/H)/0.08,0,1)[...,None]*(1-landB[...,None]);seac=seac*(1-icesea*0.75)+C(225,235,242)[None,None]*icesea*0.75
rivc=C(60,115,140)
img=np.where(L[...,None]>0.5,col_l,seac)
lk=np.clip(lakes,0,1)[...,None];img=img*(1-lk)+C(45,95,125)[None,None]*lk
rv=np.clip(rivers*1.6,0,1)[...,None]*landB[...,None];img=img*(1-rv)+rivc[None,None]*rv
coast=cv2.morphologyEx((L>0.5).astype(np.uint8),cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8)).astype(np.float32)
beach=np.clip(1-cv2.distanceTransform((L>0.5).astype(np.uint8),cv2.DIST_L2,5)/6,0,1)*landB*(1-np.clip(mount,0,1))
img=img*(1-beach[...,None]*0.35)+C(200,186,140)[None,None]*beach[...,None]*0.35
img=img*(1-coast[...,None]*0.4)
img=np.clip(img+noise(300,2,40)[...,None]*0.02,0,1)
out=(img*255).astype(np.uint8)
cv2.imwrite('me_tex.webp',cv2.cvtColor(out,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,86])
Image.fromarray(out).resize((984,877)).save('me_prev.png')
np.save('hgt.npy',hgt.astype(np.float32));np.save('water.npy',np.clip(water_all,0,1).astype(np.float32));np.save('forest.npy',fm.astype(np.float32));np.save('snow.npy',np.maximum(snow,ice).astype(np.float32))
np.save('col.npy',cv2.resize(col,(984,877)).astype(np.float32))
import os;print(os.path.getsize('me_tex.webp'))
