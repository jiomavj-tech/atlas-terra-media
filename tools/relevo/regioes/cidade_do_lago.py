import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('lago',654,140,692,172,PX=40,GR=5,seed=131,out='/tmp/claude-0/b4')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
water=R.base_water();wg=R.base_water_grid()
# a cidade fica sobre estacas, dentro do lago, perto da margem leste
row=water[R.tp(0,157.9)[1]];cols=np.where(row>0.5)[0];xe=R.X0+cols.max()/R.PX
LT=(xe-2.4,157.9)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.008*nz
R.set_height(hd);gz=R.gz
ZW=gz(*LT)                         # nível da água
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(116,134,72)*(1-np.clip(n1+0.5,0,1))+C(98,118,62)*np.clip(n1+0.5,0,1)
img+=(gr*0.55+R.base_tex(10)*1.1*0.45)*(1+n2*0.08)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((9,9),np.uint8))-water,0,1),C(120,116,84),0.5)
wcol=C(56,94,128)*(1+R.noise(120,3,13)[...,None]*0.06)
img=R.paint(img,water,wcol)
# sombra da cidade e das ruínas na água
dl=np.hypot(UX-LT[0],UY-LT[1])
img=R.paint(img,(1-sstep(1.4,1.8,dl))*water,C(40,60,78),0.6)
OLD=(LT[0]-0.8,LT[1]+4.2)
img=R.paint(img,(1-sstep(0.4,0.8,np.hypot(UX-OLD[0],UY-OLD[1])))*water,C(44,66,84),0.5)
img,roadm=R.road(img,[(xe+0.1,LT[1]),(xe+2,157.4),(xe+6,156.6),(R.X1+1,155.8)],0.1,C(170,156,124),C(96,88,70))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD
WOOD=['#8a6a44','#7a5a3a','#9a7650','#a88458'];ROOFS=['#5a3e2c','#6a4a34','#7a4a34','#4e5a4a','#8a5a36']
zp=ZW+0.1
# plataforma de madeira sobre estacas
poly=[[round(LT[0]+math.cos(a)*1.6*(1+0.08*math.sin(a*5)),3),round(LT[1]+math.sin(a)*1.3*(1+0.08*math.cos(a*4)),3)] for a in np.linspace(0,2*math.pi,24,endpoint=False)]
M.append(['polyA',poly,zp-0.04,zp,'#7a6244'])
for q in range(70):
    a=R.rng.uniform(0,6.28);rr=R.rng.uniform(0.3,0.8)*1.9;M.append(['cylA',LT[0]+math.cos(a)*rr*0.95,LT[1]+math.sin(a)*rr*0.78,ZW-0.15,zp-0.04,0.015,0.015,4,'#4a3a28'])
# casas de madeira apertadas, o salão do Mestre no centro e a praça do mercado (canal)
HP=[]
for q in range(4000):
    a=R.rng.uniform(0,6.28);rr=math.sqrt(R.rng.uniform(0.06,1))*1.42;x,y=LT[0]+math.cos(a)*rr,LT[1]+math.sin(a)*rr*0.82
    if any(math.hypot(x-px,y-py)<0.2 for px,py in HP) or math.hypot(x-LT[0],y-LT[1])<0.4: continue
    HP.append((x,y))
    if len(HP)>130: break
    M.append(['houseA',x,y,0.17,0.12,R.rng.uniform(0,3.1),WOOD[R.rng.integers(4)],ROOFS[R.rng.integers(5)],R.rng.uniform(0.2,0.36),zp])
M.append(['houseA',LT[0],LT[1],0.44,0.28,0.3,'#a88458','#7a2e22',0.55,zp])
M.append(['cylA',LT[0]+0.2,LT[1]-0.02,zp,zp+0.95,0.05,0.045,6,'#8a6a44']);M.append(['cylA',LT[0]+0.2,LT[1]-0.02,zp+0.95,zp+1.2,0.065,0.0,6,'#7a2e22'])
# a grande ponte de madeira até a margem
bx0=LT[0]+1.55;L=xe+0.05-bx0
M.append(['boxA',bx0+L/2,LT[1],L/2,0.07,zp-0.03,zp,0,'#8a7050',None])
for k in range(int(L/0.15)+1):
    for s_ in (-1,1): M.append(['cylA',bx0+k*0.15,LT[1]+s_*0.07,ZW-0.15,zp+0.05,0.01,0.01,4,'#4a3a28'])
M.append(['houseA',xe+0.15,LT[1]-0.12,0.09,0.07,0,'#8a6a44','#5a3e2c',0.14,gz(xe+0.15,LT[1]-0.12)])
# barcos no lago
for q in range(7):
    a=R.rng.uniform(0,6.28);rr=R.rng.uniform(2.0,3.6);x,y=LT[0]+math.cos(a)*rr,LT[1]+math.sin(a)*rr
    if R.at(water,x,y)>0.9: M.append(['boat',x,y,R.rng.uniform(0,6.28),'#6a4a30'])
# ruínas da cidade velha e os ossos de Smaug no fundo raso
for q in range(26):
    a=R.rng.uniform(0,6.28);rr=R.rng.uniform(0,0.6);M.append(['cylA',OLD[0]+math.cos(a)*rr,OLD[1]+math.sin(a)*rr*0.8,ZW-0.15,ZW+R.rng.uniform(0.03,0.2),0.014,0.012,4,'#2e2620'])
BON=(OLD[0]+0.1,OLD[1]+0.05)
for k in range(9):
    x=BON[0]-0.4+k*0.1
    for s_ in (-1,1): M.append(['cylA',x,BON[1]+s_*0.07,ZW-0.1,ZW+0.12-abs(k-4)*0.015,0.012,0.004,4,'#e6e0cc'])
M.append(['blobA',BON[0]+0.55,BON[1],ZW-0.03,[[0.07,0],[0.06,0.04],[0,0.07]],6,'#e6e0cc'])
# os barris dos anões chegando pelo Rio da Floresta
rw=np.where(water[:,R.tp(R.X0+3.0,0)[0]]>0.5)[0]
FR=(R.X0+4.0,R.Y0+(rw.mean()/R.PX if len(rw) else 1.5))
for q in range(8): M.append(['cylA',FR[0]+q*0.09,FR[1]+R.rng.uniform(-0.05,0.05),ZW-0.02,ZW+0.035,0.022,0.022,7,'#9a7448'])
M.append(['boat',FR[0]-0.3,FR[1],0.0,'#7a6a4a'])
# árvores nas margens
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.03 or R.at(roadm,x,y)>0.05: continue
    if R.rng.random()<(0.05 if x<660 else 0.012): R.tree(x,y,R.rng.uniform(0.5,0.8),1 if R.rng.random()<0.6 else 0,C(52,84,44)*R.rng.uniform(0.85,1.1))
R.TOPS=[[LT[0],LT[1],1.5,1.0]]
R.PL={'Esgaroth':LT,'SalaoMestre':(LT[0]-0.05,LT[1]+0.1),'PonteLago':(bx0+L/2,LT[1]),'OssosSmaug':BON,'CidadeVelha':OLD,'RioFloresta':FR,'LagoComprido':(667.5,150.0)}
R.save_json()
