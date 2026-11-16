import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('morannon',618,496,652,526,PX=40,GR=5,seed=101,out='/tmp/claude-0/b3')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
G=(634.7,511.3)
ux_,uy_=0.78,0.62                   # eixo da passagem (de Dagorlad para dentro de Mordor)
nx_,ny_=-uy_,ux_
along=(GX-G[0])*ux_+(GY-G[1])*uy_;across=(GX-G[0])*nx_+(GY-G[1])*ny_
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),4)
nz=R.noise(8,5,3,True);rid=(1-np.abs(R.noise(16,4,9,True)))**2
hd=hbs*0.5+0.1+0.008*nz
# Ered Lithui (norte) e Ephel Dúath (sul), fechando a passagem de Cirith Gorgor
mm=sstep(1.3,3.4,np.abs(across)-1.5*sstep(0,8,along))*sstep(-7,-2.5,along)
mt=mm*(0.17+0.04*nz+0.025*rid)
hd=hd+mt
# colinas das Torres dos Dentes
TW=[(G[0]+nx_*1.7,G[1]+ny_*1.7),(G[0]-nx_*1.7,G[1]-ny_*1.7)]
for tx,ty in TW: hd=np.maximum(hd,float(hbs[int((G[1]-R.Y0)*5),int((G[0]-R.X0)*5)])*0.6+0.08+0.08*np.exp(-((GX-tx)**2+(GY-ty)**2)/(2*0.7**2)))
# Dagorlad: morros de escória diante do portão
SL=[(G[0]-ux_*4.0+nx_*1.2,G[1]-uy_*4.0+ny_*1.2),(G[0]-ux_*5.2-nx_*1.4,G[1]-uy_*5.2-ny_*1.4)]
for sx,sy in SL: hd=hd+0.04*np.exp(-((GX-sx)**2+(GY-sy)**2)/(2*0.8**2))
hd=R.soften(hd,0.8,4)

R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
dust=C(110,100,88)*(1-np.clip(n1+0.5,0,1))+C(84,76,70)*np.clip(n1+0.5,0,1)
img+=(dust*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.1)
rk=np.clip(sstep(1.0,2.6,R.slope),0,1)
img=R.paint(img,rk,C(56,50,50)*(1+R.noise(80,4,8)[...,None]*0.15),0.85)
# poças e lodaçais fétidos diante do portão
AL=(UX-G[0])*ux_+(UY-G[1])*uy_;AC=(UX-G[0])*nx_+(UY-G[1])*ny_
pools=np.clip(R.noise(30,3,12)*2-0.6,0,1)*sstep(-1,-2.5,AL)*sstep(-9,-6,AL)*(np.abs(AC)<2.5)
img=R.paint(img,pools,C(46,54,44),0.8)
ROAD=[(G[0]-ux_*14,G[1]-uy_*14),(G[0]-ux_*6,G[1]-uy_*6),G,(G[0]+ux_*6,G[1]+uy_*6),(G[0]+ux_*14,G[1]+uy_*14)]
img,roadm=R.road(img,ROAD,0.22,C(100,92,84),C(50,44,42))
fin=R.light(img,tint=[0.95,0.9,0.86])
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zg=gz(*G)
BLACK='#141214';DARK='#221f20'
# a muralha do Morannon atravessando a passagem
for s_ in (-1,1):
    for k in range(6):
        t0=0.35+k*0.25;t1=t0+0.25
        x,y=G[0]+nx_*(t0+t1)/2*s_,G[1]+ny_*(t0+t1)/2*s_
        z0=min(gz(x,y),zg)-0.5
        M.append(['boxA',x,y,0.14,0.12,z0,zg+1.0,math.atan2(ny_,nx_),DARK,BLACK])
# o Portão Negro: duas folhas de ferro
for s_ in (-1,1):
    x,y=G[0]+nx_*0.17*s_,G[1]+ny_*0.17*s_
    M.append(['boxA',x,y,0.17,0.05,zg-0.1,zg+0.85,math.atan2(ny_,nx_),'#0c0c0e','#0c0c0e'])
M.append(['boxA',G[0],G[1],0.38,0.13,zg+0.85,zg+1.05,math.atan2(ny_,nx_),DARK,BLACK])
# as Torres dos Dentes: Narchost e Carchost
for tx,ty in TW:
    z=gz(tx,ty)
    M.append(['cylA',tx,ty,z-0.3,z+2.2,0.32,0.24,8,DARK]);M.append(['cylA',tx,ty,z+2.2,z+2.9,0.26,0.0,8,BLACK])
    M.append(['discA',tx-ux_*0.25,ty-uy_*0.25,z+1.9,-ux_,-uy_,0.04,[1.0,0.35,0.1,1.0]])
# morros de escória
for sx,sy in SL:
    M.append(['blobA',sx,sy,gz(sx,sy)-0.05,[[0.6,0],[0.5,0.18],[0.3,0.3],[0,0.36]],12,'#4a4440'])
for q in range(120):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if abs((x-G[0])*nx_+(y-G[1])*ny_)>4 or (x-G[0])*ux_+(y-G[1])*uy_>-1.5 or R.at(roadm,x,y)>0.05: continue
    M.append(['blobA',x,y,gz(x,y)-0.03,[[0.12,0],[0.1,0.05],[0,0.08]],6,'#3e3a36'])
R.TOPS=[[G[0],G[1],1.4,0.4],[TW[0][0],TW[0][1],3.2,0.4],[TW[1][0],TW[1][1],3.2,0.4]]
R.PL={'Morannon':G,'Narchost':TW[1],'Carchost':TW[0],'MorrosEscoria':SL[0],'Dagorlad':(G[0]-ux_*10,G[1]-uy_*10),'Udun':(G[0]+ux_*7,G[1]+uy_*7)}
R.save_json()
