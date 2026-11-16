import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('rauros',528,462,570,506,PX=40,GR=5,seed=161,out='/tmp/claude-0/b5')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
water=R.base_water(0.5,0.1);wg=R.base_water_grid()
# pontos tirados da água de base
def shore_x(y,side):
    row=water[R.tp(0,y)[1]];c=np.where(row>0.5)[0];return R.X0+(c.min() if side<0 else c.max())/R.PX
def lake_mid(y): return (shore_x(y,-1)+shore_x(y,1))/2
ys=[y for y in np.arange(470,500,0.25) if (water[R.tp(0,y)[1]]>0.5).any()]
wid=[shore_x(y,1)-shore_x(y,-1) for y in ys]
yf=next(y for y,w in zip(ys,wid) if y>484 and w<3.2)            # onde o lago estreita: as quedas
FALL=(lake_mid(yf),yf)
TOL=(lake_mid(yf-2.2),yf-2.2)
HEN=(shore_x(yf-2.0,-1)-1.6,yf-2.0);LHAW=(shore_x(yf-2.0,1)+1.8,yf-2.0)
PARTH=(shore_x(yf-4.6,-1)-0.5,yf-4.6)
yn=ys[0]+4.5;ARG=[(lake_mid(yn)-1.5,yn),(lake_mid(yn)+1.5,yn)]
BOR=(HEN[0]-0.6,HEN[1]+1.5)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.012*nz
hd=hd+0.07*gauss(*HEN,1.1,GX,GY)+0.06*gauss(*LHAW,1.2,GX,GY)
# água plana: o lago num nível, o rio abaixo das quedas em outro
L1,L2=0.075,0.0
lvl=L1+(L2-L1)*sstep(yf+0.1,yf+0.9,GY)
wm=cv2.GaussianBlur((wg>0.45).astype(np.float32),(0,0),0.8)
land=np.maximum(hd,lvl+0.012)
below=sstep(yf+0.2,yf+2.5,GY)
land=land-0.05*below*np.exp(-((GX-FALL[0])/5.0)**2)*(land>lvl+0.03)
dist=cv2.distanceTransform((wg<0.45).astype(np.uint8),cv2.DIST_L2,5)/R.GR
ramp=sstep(0.0,1.6,dist)**0.8
hd=np.where(wm>0.5,lvl,lvl+0.004+(np.maximum(land,lvl+0.012)-lvl)*ramp)
R.set_height(hd);gz=R.gz
ZL=gz(TOL[0],TOL[1]-1.5)
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(110,132,70)*(1-np.clip(n1+0.5,0,1))+C(92,112,60)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
rk=np.clip(sstep(1.1,2.6,R.slope)+sstep(566,570,UX)*0,0,1)
img=R.paint(img,rk,C(124,118,108),0.85)
img=R.paint(img,1-sstep(0.5,0.8,np.hypot(UX-PARTH[0],UY-PARTH[1])),C(118,160,70),0.8)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((7,7),np.uint8))-water,0,1),C(110,112,84),0.5)
img=R.paint(img,water,C(58,98,128)*(1+R.noise(120,3,13)[...,None]*0.05))
foam=np.exp(-((UY-yf-0.5)/0.7)**2)*water
img=R.paint(img,foam,C(232,240,244),0.9)
fin=R.light(img)
R.save_tex(fin)
M=R.MOD
STONE='#a8a294'
# Argonath: os Pilares dos Reis, Isildur e Anárion, com a mão esquerda erguida
for (x,y),s_ in zip(ARG,(-1,1)):
    z=gz(x,y);K=2.4
    M.append(['boxA',x,y,0.22*K,0.2*K,z-0.3,z+0.5*K,0,'#8e887a','#8e887a'])
    M.append(['cylA',x,y,z+0.5*K,z+2.3*K,0.17*K,0.13*K,8,STONE]);M.append(['blobA',x,y,z+2.3*K,[[0.1*K,0],[0.12*K,0.1*K],[0.08*K,0.24*K],[0,0.3*K]],8,STONE])
    M.append(['cylA',x,y,z+2.52*K,z+2.62*K,0.13*K,0.11*K,8,'#b8b2a2'])
    M.append(['boxA',x-s_*0.2*K,y+0.12*K,0.035*K,0.035*K,z+1.7*K,z+2.5*K,0,STONE,None])
# Tol Brandir: a ilha-pináculo
M.append(['blobA',TOL[0],TOL[1],ZL-0.3,[[0.5,0],[0.42,0.6],[0.3,1.4],[0.18,2.2],[0.06,2.9],[0,3.1]],9,'#807a70'])
# Amon Hen: o Assento da Visão sobre quatro pilares, com a escada
zh=gz(*HEN)
M.append(['capA',HEN[0],HEN[1],zh+0.02,0,0.32,14,'#b8b2a2'])
for k in range(4):
    a=k*1.57+0.78;M.append(['cylA',HEN[0]+math.cos(a)*0.1,HEN[1]+math.sin(a)*0.1,zh,zh+0.3,0.025,0.022,6,'#c2bcac'])
M.append(['boxA',HEN[0],HEN[1],0.1,0.1,zh+0.3,zh+0.36,0,'#c2bcac',None]);M.append(['boxA',HEN[0],HEN[1]-0.07,0.08,0.02,zh+0.36,zh+0.52,0,'#c2bcac',None])
for k in range(8): M.append(['cylA',HEN[0]+math.cos(k*0.785)*0.3,HEN[1]+math.sin(k*0.785)*0.3,zh,zh+0.12,0.02,0.02,5,'#a8a294'])
zl=gz(*LHAW);M.append(['capA',LHAW[0],LHAW[1],zl+0.02,0,0.25,12,'#a8a294']);M.append(['boxA',LHAW[0],LHAW[1],0.08,0.08,zl,zl+0.25,0,'#a8a294',None])
# Parth Galen: os três barcos élficos na margem
for k in range(3): M.append(['boat',PARTH[0]+0.45,PARTH[1]-0.25+k*0.25,0.2,'#f0eee4','#d8d8d0'])
M.append(['capA',PARTH[0]-0.1,PARTH[1],gz(PARTH[0]-0.1,PARTH[1])+0.02,0,0.03,6,[1.0,0.55,0.15,1.0]])
# onde Boromir caiu: a trompa partida e as armas dos inimigos
zb=gz(*BOR);M.append(['stone',BOR[0],BOR[1]])
for k in range(7): M.append(['cylA',BOR[0]+math.cos(k*0.9)*0.2,BOR[1]+math.sin(k*0.9)*0.2,zb-0.03,zb+0.14,0.006,0.003,4,'#2a2a2a'])
# Rauros: a cortina de água e o barco fúnebre de Boromir
z0=gz(FALL[0],FALL[1]-0.3);z1=gz(FALL[0],FALL[1]+1.3)
hwf=(shore_x(yf+0.4,1)-shore_x(yf+0.4,-1))/2*0.85
M.append(['fall',lake_mid(yf+0.4),FALL[1]+0.42,0,1,hwf*2,z0+0.03,z1-0.05])
M.append(['boat',FALL[0]-0.2,FALL[1]-0.6,1.57,'#f0eee4','#d8d8d0'])
for _ in range(22000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.03 or R.at(rk,x,y)>0.5: continue
    if math.hypot(x-HEN[0],y-HEN[1])<0.45 or math.hypot(x-PARTH[0],y-PARTH[1])<0.7 or math.hypot(x-LHAW[0],y-LHAW[1])<0.4: continue
    near=min(math.hypot(x-HEN[0],y-HEN[1]),math.hypot(x-LHAW[0],y-LHAW[1]))
    if R.rng.random()<(0.14 if near<3.5 else 0.02): R.tree(x,y,R.rng.uniform(0.55,0.9),1 if R.rng.random()<0.6 else 0,C(52,86,44)*R.rng.uniform(0.85,1.15))
R.TOPS=[[ARG[0][0],ARG[0][1],6.9,0.8],[ARG[1][0],ARG[1][1],6.9,0.8],[TOL[0],TOL[1],3.2,0.5]]
R.PL={'Argonath':((ARG[0][0]+ARG[1][0])/2,ARG[0][1]),'NenHithoel':(lake_mid(yf-9),yf-9),'ParthGalen':PARTH,'AssentoVisao':HEN,'TolBrandir':TOL,'AmonLhaw':LHAW,'QuedasRauros':(FALL[0],FALL[1]+0.5),'MorteBoromir':BOR}
R.save_json()
