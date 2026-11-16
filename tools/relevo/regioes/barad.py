import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('barad',716,522,752,558,PX=40,GR=5,seed=211,out='/tmp/claude-0/b6')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
B=(733.1,539.4)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True);rid=(1-np.abs(R.noise(16,4,9,True)))**2
d=np.hypot(GX-B[0],GY-B[1])
hd=hbs+0.012*nz
# esporão das Montanhas de Cinza que desce do norte até a torre
spur=np.exp(-((GX-B[0]-0.25*(B[1]-GY))/2.2)**2)*sstep(B[1]+1.5,B[1]-10,GY)
hd=hd+spur*(0.10+0.03*rid)
z0=float(hd[int((B[1]-R.Y0)*5),int((B[0]-R.X0)*5)])
hd=np.where(d<1.6,z0,np.where(d<2.6,z0+(hd-z0)*sstep(1.6,2.6,d),hd))
# o abismo em volta da rocha (fosso de fogo), aberto para oeste onde passa a ponte
chasm=np.exp(-((d-2.1)/0.28)**2)
hd=hd-0.05*chasm
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
ash=C(84,76,72)*(1-np.clip(n1+0.5,0,1))+C(60,54,52)*np.clip(n1+0.5,0,1)
img+=(ash*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.1)
img=R.paint(img,np.clip(sstep(0.8,2.2,R.slope),0,1),C(40,36,36),0.8)
dT=np.hypot(UX-B[0],UY-B[1])
img=R.paint(img,1-sstep(1.5,1.7,dT),C(34,32,34),0.9)
lava=np.exp(-((dT-2.1)/0.14)**2)*np.clip(R.noise(40,3,22)*1.5+0.6,0,1)
ROAD=[(R.X0-1,549.0),(722,545.5),(727,542.6),(B[0]-2.6,B[1]+0.9),(B[0]-1.5,B[1]+0.4)]
img,roadm=R.road(img,ROAD,0.2,C(96,88,82),C(30,26,26))
fin=R.light(img,tint=[0.92,0.86,0.82])
glow=cv2.GaussianBlur(lava,(0,0),8)
fin=fin+np.array([0.5,0.15,0.03])*glow[...,None]*0.7
fin=fin*(1-lava[...,None]*(1-roadm[...,None]))+C(255,130,30)*lava[...,None]*(1-roadm[...,None])
R.save_tex(fin)
M=R.MOD;zc=gz(*B)
K='#18161a';K2='#0e0d10';K3='#242228';FIRE=[1.0,0.42,0.08,1.0]
# muralhas em anéis, cada uma mais alta que a outra
for (r,h,n) in [(1.45,0.9,30),(1.05,1.7,24),(0.7,2.6,18)]:
    for k in range(n):
        a=k/n*6.28;da=6.28/n;x,y=B[0]+math.cos(a+da/2)*r,B[1]+math.sin(a+da/2)*r
        M.append(['boxA',x,y,r*da/2+0.01,0.07,zc-0.6,zc+h*(0.85+0.15*((k*7)%3)/2),a+da/2+1.571,K,K2])
    for k in range(n//3):
        a=k/(n//3)*6.28+r;x,y=B[0]+math.cos(a)*r,B[1]+math.sin(a)*r
        M.append(['cylA',x,y,zc-0.5,zc+h+0.9,0.12,0.09,6,K3]);M.append(['cylA',x,y,zc+h+0.9,zc+h+1.5,0.11,0.0,6,K2])
# a Torre Negra: corpo em degraus, contrafortes e as pontas no alto com o Olho
TOP=9.5
for k,(r0,r1,z0_,z1_) in enumerate([(0.55,0.46,0,3.0),(0.44,0.36,3.0,5.6),(0.34,0.27,5.6,7.6),(0.25,0.2,7.6,TOP)]):
    M.append(['cylA',B[0],B[1],zc+z0_-0.3,zc+z1_,r0,r1,8,K if k%2==0 else K3])
    M.append(['cylA',B[0],B[1],zc+z1_-0.12,zc+z1_,r0*0.98+0.05,r1+0.06,8,K2])
for k in range(8):
    a=k/8*6.28;M.append(['cylA',B[0]+math.cos(a)*0.55,B[1]+math.sin(a)*0.55,zc-0.3,zc+3.6,0.09,0.03,5,K2])
for s_ in (-1,1):
    M.append(['cylA',B[0]+s_*0.16,B[1],zc+TOP,zc+TOP+1.3,0.07,0.0,5,K2])
M.append(['blobA',B[0],B[1],zc+TOP+0.35,[[0.0,0],[0.11,0.16],[0.11,0.34],[0,0.5]],10,[1.0,0.5,0.1,1.0]])
M.append(['blobA',B[0],B[1],zc+TOP+0.47,[[0.0,0],[0.035,0.08],[0.035,0.2],[0,0.26]],6,'#100808'])
for k in range(14):
    a=k*0.9;z=zc+1.0+k*0.55;r=0.5-k*0.022
    M.append(['discA',B[0]+math.cos(a)*r,B[1]+math.sin(a)*r,z,math.cos(a),math.sin(a),0.03,FIRE])
# a ponte de ferro sobre o abismo e o portão
bx,by=B[0]-2.1,B[1]+0.65
M.append(['boxA',bx,by,0.6,0.09,zc-0.12,zc,math.atan2(0.5,-1.1)+3.1416,K3,None])
gx_,gy_=B[0]-1.42,B[1]+0.35
M.append(['boxA',gx_,gy_,0.07,0.2,zc-0.2,zc+1.4,math.atan2(0.35,-1.42),K2,K2]);M.append(['discA',gx_-0.08,gy_+0.02,zc+0.45,-1,0.25,0.12,FIRE])
# forjas, fossos e acampamentos no planalto
for q in range(40):
    x,y=R.rng.uniform(R.X0+2,R.X1-2),R.rng.uniform(R.Y0+2,R.Y1-2)
    if math.hypot(x-B[0],y-B[1])<3.2 or R.at(roadm,x,y)>0.1: continue
    z=gz(x,y)
    if q%3==0: M.append(['capA',x,y,z+0.03,0,0.07,8,FIRE]);M.append(['blobA',x,y,z+0.02,[[0.16,0],[0.12,0.08],[0.07,0.1]],8,'#2e2828'])
    else: M.append(['box',x,y,R.rng.uniform(0.08,0.2),R.rng.uniform(0.06,0.14),-0.05,R.rng.uniform(0.1,0.3),R.rng.uniform(0,3),'#2a2626',None])
R.TOPS=[[B[0],B[1],round(TOP+1.6,1),0.8]]
R.PL={'TorreNegra':B,'OlhoSauron':(B[0]+0.01,B[1]-0.01),'PonteFerro':(bx,by),'FossoFogo':(B[0]+2.1,B[1]),'EstradaBarad':(724.0,544.3),'EsporaoCinza':(B[0]+1.4,B[1]-6.0)}
R.save_json()
