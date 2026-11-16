import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('guldur',540,362,572,392,PX=40,GR=5,seed=141,out='/tmp/claude-0/b4')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
DG=(556.0,377.1)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
d=np.hypot(GX-DG[0],GY-DG[1])
hd=hbs+0.01*nz+0.07*np.exp(-(d/1.7)**2)*(1+0.2*nz)       # Amon Lanc, a colina nua
hd=np.where(d<0.75,np.maximum(hd,float(hbs.mean())+0.062),hd)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
fl=C(44,56,40)*(1-np.clip(n1+0.5,0,1))+C(34,44,34)*np.clip(n1+0.5,0,1)
img+=(fl*0.6+R.base_tex(10)*0.9*0.4)*(1+n2*0.08)
dT=np.hypot(UX-DG[0],UY-DG[1])
bare=1-sstep(1.6,2.8,dT+0.4*R.noise(10,3,12))
img=R.paint(img,bare,C(74,68,62)*(1+R.noise(90,3,8)[...,None]*0.15),0.9)
PATH=[(R.X0-1,384.5),(545,383.0),(549.5,381.0),(553.0,379.4),(554.6,378.2),(DG[0]-0.5,DG[1]+0.55)]
img,roadm=R.road(img,PATH,0.1,C(92,84,74),C(40,36,34))
fin=R.light(img,amb=0.55,tint=[0.9,0.92,0.95])
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zc=gz(*DG)
DARK='#2c2a2e';DARK2='#1c1a1e';GLOW=[0.9,0.35,0.12,1.0]
# a fortaleza do Necromante: muralha quebrada, torres e o torreão
for k in range(26):
    a=k/26*2*math.pi;da=2*math.pi/26
    if R.rng.random()<0.15: continue
    x,y=DG[0]+math.cos(a+da/2)*0.62,DG[1]+math.sin(a+da/2)*0.62
    M.append(['boxA',x,y,0.62*da/2+0.02,0.06,zc-0.6,zc+R.rng.uniform(0.2,0.55),a+da/2+math.pi/2,DARK,DARK2])
for k in range(6):
    a=k/6*2*math.pi+0.3;x,y=DG[0]+math.cos(a)*0.62,DG[1]+math.sin(a)*0.62;h=R.rng.uniform(0.7,1.3)
    M.append(['cylA',x,y,zc-0.5,zc+h,0.1,0.085,7,DARK]);M.append(['cylA',x,y,zc+h,zc+h+0.3,0.11,0.0,7,DARK2])
M.append(['boxA',DG[0],DG[1],0.22,0.2,zc-0.1,zc+1.3,0.3,DARK,DARK2])
M.append(['cylA',DG[0]+0.05,DG[1]-0.03,zc+1.3,zc+2.6,0.14,0.1,8,DARK])
for k in range(5):
    a=k/5*6.28;M.append(['cylA',DG[0]+0.05+math.cos(a)*0.11,DG[1]-0.03+math.sin(a)*0.11,zc+2.6,zc+3.0,0.03,0.0,4,DARK2])
M.append(['discA',DG[0]+0.05,DG[1]+0.11,zc+2.2,0,1,0.035,GLOW])
# a boca das masmorras
DUN=(DG[0]-0.35,DG[1]+0.3)
M.append(['discA',DUN[0],DUN[1]+0.02,zc+0.12,-0.6,0.8,0.09,'#050405'])
# floresta fechada e escura; árvores mortas junto à colina
for _ in range(30000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    dd=math.hypot(x-DG[0],y-DG[1])
    if R.at(roadm,x,y)>0.05 or dd<1.3: continue
    if dd<2.6:
        if R.rng.random()<0.05: M.append(['cyl',x,y,-0.03,R.rng.uniform(0.3,0.6),0.03,0.008,4,'#2a2622'])
    elif R.rng.random()<0.11: R.tree(x,y,R.rng.uniform(0.7,1.15),1 if R.rng.random()<0.55 else 0,C(26,44,30)*R.rng.uniform(0.8,1.2))
R.TOPS=[[DG[0],DG[1],3.3,0.5]]
R.PL={'FortalezaGuldur':DG,'MasmorrasGuldur':DUN,'AmonLanc':(DG[0]+1.3,DG[1]-0.9),'CaminhoGuldur':(549.5,381.0),'FlorestaSul':(563.0,370.0)}
R.save_json()
