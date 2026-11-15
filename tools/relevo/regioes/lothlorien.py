import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('lorien',470,378,512,414,PX=40,GR=5,seed=71,out='/tmp/claude-0/b2')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
CG=(493.6,396.2)        # Caras Galadhon
CA=(487.4,391.4)        # Cerin Amroth
NIM=[(476.5,379.0),(477.4,382.5),(478.0,385.8),(479.2,388.6),(480.4,391.6)]    # Nimrodel (até o Veio de Prata)
water=R.base_water()
wg=R.base_water_grid()
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3)
nz=R.noise(8,5,3,True)
hd=hbs+0.012*nz
hd=hd+0.035*gauss(*CG,1.4,GX,GY)+0.03*gauss(*CA,0.7,GX,GY)
hd=hd-0.012*cv2.GaussianBlur(np.clip((wg-0.4)/0.2,0,1).astype(np.float32),(0,0),1.5)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
grass=C(104,138,62)*(1-np.clip(n1+0.5,0,1))+C(88,124,56)*np.clip(n1+0.5,0,1)
img+=(grass*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.08)
# chão da floresta dourada (folhas caídas dos mallorns)
wood=np.clip(R.noise(10,3,12)*1.2+0.75,0,1)*(1-np.clip(water*3,0,1))
leaf=C(170,140,60)*(1+R.noise(150,3,13)[...,None]*0.12)
img=R.paint(img,wood,leaf,0.55)
# Cerin Amroth: colina de relva com elanor (dourada) e niphredil (branca)
dca=np.hypot(UX-CA[0],UY-CA[1])
img=R.paint(img,1-sstep(0.6,0.75,dca),C(110,160,70),0.9)
fl1=(R.rng.random((R.TH,R.TW))<0.08)*(dca<0.6);fl2=(R.rng.random((R.TH,R.TW))<0.05)*(dca<0.6)
img=R.paint(img,fl1.astype(np.float32),C(240,200,60));img=R.paint(img,fl2.astype(np.float32),C(240,240,236))
# Caras Galadhon: muralha verde e fosso, gramados dentro
dcg=np.hypot(UX-CG[0],UY-CG[1])
img=R.paint(img,1-sstep(1.15,1.25,dcg),C(98,140,64),0.8)
img=R.paint(img,np.exp(-((dcg-1.3)/0.05)**2),C(40,60,40),0.8)
# Nimrodel
nimm=np.clip(R.line_mask(NIM,0.1,0.8)*1.4,0,1)
water=np.maximum(water,nimm)
img=R.paint(img,np.clip(cv2.dilate(water,np.ones((5,5),np.uint8))-water,0,1),C(96,110,70),0.4)
img=R.paint(img,water,C(70,110,128))
# trilhas élficas
img,_=R.road(img,[(480.0,391.0),(483.5,391.2),CA,(489.8,393.0),(491.8,394.7),(CG[0]-0.2,CG[1]+1.3)],0.06,C(180,170,130),C(120,110,80))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD
TRUNK='#c8ccc8';GOLD='#d7b544';GOLD2='#c9a23a';GREEN='#7a9a40'
def mallorn(x,y,h,r,col=GOLD,lamps=0,flet=True):
    z=gz(x,y)
    M.append(['cylA',x,y,z-0.05,z+h,0.05*h/1.5,0.03*h/1.5,7,TRUNK])
    M.append(['blobA',x,y,z+h*0.45,[[r*0.5,0],[r,r*0.35],[r*0.95,r*0.75],[r*0.6,r*1.05],[0,r*1.2]],10,col])
    if flet: M.append(['capA',x,y,z+h*0.42,0.03,r*0.45,10,'#ece6d0'])
    for k in range(lamps):
        a=k/max(1,lamps)*2*math.pi+0.3;M.append(['capA',x+math.cos(a)*r*0.5,y+math.sin(a)*r*0.5,z+h*0.43,0,0.02,6,[0.7,0.95,0.8,1.0]])
# Caras Galadhon: mallorns gigantes, o maior no centro (Celeborn e Galadriel)
mallorn(CG[0],CG[1],2.6,0.55,GOLD,8)
M.append(['capA',CG[0],CG[1],gz(*CG)+2.6*0.62,0.03,0.38,12,'#f2eedc'])
for k in range(5):
    M.append(['capA',CG[0],CG[1],gz(*CG)+0.3+k*0.4,0.05,0.12,8,'#e8e2cc'])
for q in range(400):
    a=R.rng.uniform(0,2*math.pi);r=math.sqrt(R.rng.uniform(0.04,1))*1.05;x,y=CG[0]+math.cos(a)*r,CG[1]+math.sin(a)*r
    if r<0.5: continue
    if any(math.hypot(x-m[1],y-m[2])<0.32 for m in M if m[0]=='blobA'): continue
    mallorn(x,y,R.rng.uniform(1.3,1.8),R.rng.uniform(0.22,0.3),[GOLD,GOLD2][R.rng.integers(2)],R.rng.integers(1,4))
# muralha verde e o portão com a ponte branca ao sul
M.append(['wall',[[round(CG[0]+math.cos(a)*1.22,3),round(CG[1]+math.sin(a)*1.22,3)] for a in np.linspace(math.pi/2+0.18,math.pi/2+2*math.pi-0.18,70)],0.3,'#5e8a46',0.08])
gx_,gy_=CG[0],CG[1]+1.3
M.append(['boxA',gx_,gy_,0.05,0.18,gz(gx_,gy_)+0.04,gz(gx_,gy_)+0.07,0,'#f4f2ea',None])
for s_ in (-1,1): M.append(['cylA',gx_+s_*0.13,gy_-0.08,gz(gx_,gy_)-0.05,gz(gx_,gy_)+0.32,0.025,0.02,6,'#f4f2ea'])
# o Espelho de Galadriel: bacia de prata num vale ao sul, dentro da muralha
MIR=(CG[0]+0.45,CG[1]+0.75);zz=gz(*MIR)
M.append(['cylA',MIR[0],MIR[1],zz-0.05,zz+0.08,0.08,0.09,12,'#d8dde0']);M.append(['capA',MIR[0],MIR[1],zz+0.07,0,0.075,12,[0.55,0.7,0.85,0.4]])
# Cerin Amroth: dois anéis de árvores e o grande mallorn com o talan branco no topo
mallorn(CA[0],CA[1],1.9,0.4,GOLD,3)
for ring_r,n,col in [(0.62,12,'#e8e4d8'),(0.82,16,GOLD)]:
    for k in range(n):
        a=k/n*2*math.pi;x,y=CA[0]+math.cos(a)*ring_r,CA[1]+math.sin(a)*ring_r
        if col==GOLD: mallorn(x,y,1.2,0.18,GOLD2,0,False)
        else:
            z=gz(x,y);M.append(['cylA',x,y,z-0.03,z+0.5,0.025,0.015,6,'#f0ece0']);M.append(['blobA',x,y,z+0.3,[[0.08,0],[0.12,0.1],[0.08,0.25],[0,0.3]],7,'#e8ecd8'])
# o talan de Haldir perto do Nimrodel
HAL=(480.9,390.2);mallorn(HAL[0],HAL[1],1.6,0.3,GOLD,2)
# a Margem (Hithe) no Veio de Prata, com os barcos élficos e o barco-cisne
rows=np.where(R.base_water()[:,R.tp(495.0,0)[0]]>0.5)[0]
HITHE=(495.0,R.Y0+rows.min()/R.PX-0.15 if len(rows) else 399.5)
for q in range(3): M.append(['jetty',HITHE[0]-0.3+q*0.3,HITHE[1],1.57])
for q in range(3): M.append(['boat',HITHE[0]-0.35+q*0.35,HITHE[1]+0.45,0.0,'#f4f2ea'])
M.append(['blobA',HITHE[0]+0.9,HITHE[1]+0.4,gz(HITHE[0]+0.9,HITHE[1]+0.4)+0.02,[[0.12,0],[0.14,0.05],[0.06,0.1],[0,0.12]],8,'#f8f8f4'])
M.append(['cylA',HITHE[0]+1.02,HITHE[1]+0.4,gz(HITHE[0]+0.9,HITHE[1]+0.4)+0.08,gz(HITHE[0]+0.9,HITHE[1]+0.4)+0.35,0.02,0.012,5,'#f8f8f4'])
# floresta: mallorns (dourados) e árvores menores
for _ in range(30000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05: continue
    if math.hypot(x-CG[0],y-CG[1])<1.45 or math.hypot(x-CA[0],y-CA[1])<1.0: continue
    w=R.at(wood,x,y)
    if R.rng.random()<0.06*w:
        if R.rng.random()<0.75: R.tree(x,y,R.rng.uniform(0.9,1.35),1,C(214,178,64)*R.rng.uniform(0.85,1.1))
        else: R.tree(x,y,R.rng.uniform(0.6,0.9),1,C(110,140,60)*R.rng.uniform(0.85,1.1))
R.TOPS=[[CG[0],CG[1],2.0,0.3],[CA[0],CA[1],1.5,0.3]]
R.PL={'CarasGaladhon':CG,'EspelhoGaladriel':MIR,'CerinAmroth':CA,'Nimrodel':NIM[2],'TalanHaldir':HAL,'Margem':HITHE,'MuralhaVerde':(CG[0]-1.25,CG[1]),'Naith':(500.0,400.6)}
R.save_json()
