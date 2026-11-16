import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('fangorn',440,444,474,476,PX=40,GR=5,seed=151,out='/tmp/claude-0/b5')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
WELL=(453.0,455.6);HILL=(464.6,466.4);DERN=(460.4,469.6);EDGE=(470.6,471.8)
water=R.base_water(0.5,0.1)
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.012*nz
hd=R.soften(hd,0.5,6)
hd=hd+0.03*gauss(*HILL,0.6,GX,GY)                                   # a colina de Barbárvore
hd=hd-0.02*gauss(*DERN,1.3,GX,GY)+0.01*np.exp(-((np.hypot(GX-DERN[0],GY-DERN[1])-1.85)/0.3)**2)   # Valarcano: uma tigela cercada de sebe
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
fl=C(52,74,44)*(1-np.clip(n1+0.5,0,1))+C(40,58,38)*np.clip(n1+0.5,0,1)
img+=(fl*0.6+R.base_tex(10)*1.0*0.4)*(1+n2*0.08)
rk=np.clip(sstep(1.4,3.0,R.slope)+sstep(0.6,0.7,R.HT),0,1)
img=R.paint(img,rk,C(110,106,100),0.85)
plain=sstep(466.0,470.5,UX+0.5*(UY-468)+1.2*R.noise(8,3,14))
img=R.paint(img,plain,C(140,146,84),0.75)
img=R.paint(img,1-sstep(1.4,1.75,np.hypot(UX-DERN[0],UY-DERN[1])),C(120,160,74),0.9)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1),C(70,84,56),0.4)
img=R.paint(img,water,C(64,104,116))
fin=R.light(img,amb=0.58)
R.save_tex(fin)
M=R.MOD
# colina de Barbárvore: prateleira de rocha com degraus
zh=gz(*HILL)
M.append(['blobA',HILL[0],HILL[1],zh-0.3,[[0.45,0],[0.4,0.35],[0.3,0.6],[0.22,0.72]],9,'#8a867c'])
M.append(['capA',HILL[0],HILL[1],zh+0.42,0,0.22,9,'#9a968a'])
for k in range(6): M.append(['boxA',HILL[0]+0.3+k*0.045,HILL[1]+0.25,0.03,0.07,zh-0.2,zh-0.12+k*0.09,0.6,'#9a968a',None])
# Barbárvore (um Ent) junto à colina
def ent(x,y,h,col='#5a4a34',top='#4a6a36'):
    h*=2.6
    z=gz(x,y);M.append(['cylA',x,y,z-0.05,z+h,0.05*h,0.035*h,6,col]);M.append(['blobA',x,y,z+h*0.8,[[0.07*h,0],[0.16*h,0.1*h],[0.12*h,0.28*h],[0,0.36*h]],7,top])
    for s_ in (-1,1): M.append(['cylA',x+s_*0.07*h,y,z+h*0.45,z+h*0.75,0.015*h,0.012*h,4,col])
ent(HILL[0]-0.55,HILL[1]+0.45,0.95)
# Gruta da Nascente: a casa de Barbárvore, com a cortina de água e as árvores do portão
zw=gz(*WELL)
M.append(['boxA',WELL[0]-0.25,WELL[1],0.05,0.3,zw-0.1,zw+0.7,0,'#7a766e','#6a665e'])
M.append(['boxA',WELL[0]-0.18,WELL[1],0.01,0.14,zw,zw+0.6,0,[0.8,0.92,0.98,0.4],None])
M.append(['capA',WELL[0]+0.05,WELL[1],zw+0.02,0,0.12,10,[0.55,0.8,0.7,0.5]])
for s_ in (-1,1):
    x,y=WELL[0]+0.45,WELL[1]+s_*0.3;z=gz(x,y);M.append(['cylA',x,y,z-0.05,z+0.9,0.05,0.04,6,'#4a3a28']);M.append(['blobA',x,y,z+0.6,[[0.15,0],[0.28,0.2],[0.2,0.5],[0,0.62]],8,'#2c5a30'])
# Valarcano: o Entebate, com os Ents reunidos em roda
for k in range(14):
    a=k/14*6.28;ent(DERN[0]+math.cos(a)*0.95,DERN[1]+math.sin(a)*0.95,R.rng.uniform(0.6,0.85),['#8a7650','#9a8660','#7a6a48'][k%3],['#7a9a46','#6a8a3c','#96a44a'][k%3])
for a in np.linspace(0.25,6.28,56): R.tree(DERN[0]+math.cos(a)*1.85,DERN[1]+math.sin(a)*1.85,0.9,0,C(26,58,34))
# borda leste: o monte dos orcs queimados pelos Rohirrim, com lanças
ze=gz(*EDGE)
M.append(['blobA',EDGE[0],EDGE[1],ze-0.03,[[0.3,0],[0.24,0.08],[0.1,0.15],[0,0.17]],10,'#3a3430'])
for k in range(9):
    a=k/9*6.28;M.append(['cylA',EDGE[0]+math.cos(a)*0.32,EDGE[1]+math.sin(a)*0.32,ze-0.05,ze+0.3,0.008,0.004,4,'#c8c8c0'])
# floresta antiga e densa
for _ in range(34000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(rk,x,y)>0.5 or R.at(plain,x,y)>0.5: continue
    if math.hypot(x-DERN[0],y-DERN[1])<2.0 or math.hypot(x-HILL[0],y-HILL[1])<0.7 or math.hypot(x-WELL[0],y-WELL[1])<0.6: continue
    if R.rng.random()<0.12: R.tree(x,y,R.rng.uniform(0.8,1.3),1 if R.rng.random()<0.7 else 0,C(40,66,36)*R.rng.uniform(0.75,1.2))
R.TOPS=[[HILL[0],HILL[1],1.0,0.4]]
R.PL={'ColinaBarbarvore':HILL,'GrutaNascente':WELL,'Valarcano':DERN,'MonteOrcs':EDGE,'Entagua':(467.5,468.6)}
R.save_json()
