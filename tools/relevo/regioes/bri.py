import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('bri',282,250,312,276,PX=44,GR=5,seed=81,out='/tmp/claude-0/b2')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
BH=(297.6,259.4)                 # Colina de Bri
WGATE=(293.2,261.9);SGATE=(297.0,263.5)
PONY=(294.9,262.3)
CROSS=(288.4,262.4)
ROAD=[(R.X0-1,262.8),(286.0,262.6),CROSS,(291.0,262.2),WGATE,(294.2,262.1),PONY,(295.8,262.7),(296.6,263.2),SGATE,(299.0,264.2),(302.0,264.6),(306.0,264.9),(R.X1+1,265.2)]
GREEN=[(288.2,R.Y0-1),(288.3,256.0),CROSS,(288.6,268.0),(288.9,R.Y1+1)]
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),4)
nz=R.noise(8,5,3,True)
hd=hbs+0.01*nz
db=np.hypot((GX-BH[0])/1.0,(GY-BH[1])/0.85)
hd=hd+0.04*np.exp(-(db/2.4)**2)
# vale de Combe a leste da colina
hd=hd-0.02*np.exp(-(((GX-301.0)/0.7)**2+((GY-258.8)/1.3)**2))
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
grass=C(112,140,66)*(1-np.clip(n1+0.5,0,1))+C(94,126,58)*np.clip(n1+0.5,0,1)
img+=(grass*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.08)
# campos e hortas em volta da vila
lab=cv2.resize(R.rng.integers(0,6,(26,30)).astype(np.float32),(R.TW,R.TH),interpolation=cv2.INTER_NEAREST)
PAL=np.array([C(130,150,70),C(150,160,80),C(186,170,100),C(120,140,64),C(160,140,90),C(110,138,60)])
fields=PAL[lab.astype(int)]
fm=np.clip(1-np.hypot((UX-293.5)/6,(UY-264.5)/4),0,1)
img=R.paint(img,fm,fields,0.5)
# floresta Chet (nordeste)
chet=np.clip((UX-300.5)*0.4-(UY-257.0)*0.35+R.noise(8,3,14)*1.2,0,1)
img=R.paint(img,chet,C(40,70,40),0.6)
# dique e sebe em volta da vila
HEDGE=[(BH[0]-1.6,256.9),(292.4,258.6),(291.9,260.6),(292.3,262.6),(293.6,264.2),(295.6,264.8),(297.6,264.4),(299.2,263.2)]
dk=R.line_mask(HEDGE,0.14)
img=R.paint(img,dk,C(70,62,48),0.7)
img,roadm=R.road(img,ROAD,0.22,C(176,156,118),C(100,88,66))
img,gm=R.road(img,GREEN,0.14,C(150,150,104),C(100,96,70))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD
WALLS=['#d8ccb0','#cdbf9e','#e2d8c0'];ROOFS=['#6a4a34','#5a3e2c','#7a5a3a','#4e4e46']
M.append(['inn',PONY[0],PONY[1]-0.12,0.3])                                     # o Pônei Saltitante
M.append(['house',PONY[0]+0.32,PONY[1]-0.42,0.42,0.26,1.6,'#ddd0b0','#5a3e2c',0.42])   # alas da estalagem e estábulo
M.append(['house',PONY[0]-0.35,PONY[1]-0.4,0.36,0.22,1.6,'#a88a60','#4e4e46',0.3])
# casas dos homens (encosta oeste) e tocas de hobbit (no alto)
HP=[(PONY[0],PONY[1])]
for q in range(3000):
    a=R.rng.uniform(1.6,4.4);r=R.rng.uniform(1.2,2.4);x,y=BH[0]+math.cos(a)*r*1.0,BH[1]+math.sin(a)*r*0.85
    if any(math.hypot(x-px,y-py)<0.26 for px,py in HP) or R.at(roadm,x,y)>0.2: continue
    if len(HP)>110: break
    HP.append((x,y));rot=math.atan2(y-BH[1],x-BH[0])+math.pi/2
    if r>1.7 or R.rng.random()<0.7:
        M.append(['house',round(x,3),round(y,3),0.24,0.17,round(rot,3),WALLS[R.rng.integers(3)],ROOFS[R.rng.integers(4)],round(R.rng.uniform(0.2,0.3),3)])
    else:
        M.append(['smial',round(x,3),round(y,3),0.22,round(rot+math.pi/2,3),['#2f6a8a','#8a2f2f','#2f7a3a','#c09a2a'][R.rng.integers(4)]])
# Staddle (encosta sudeste) e Archet (borda da floresta Chet), Combe
for (cx,cy,n,hob) in [(299.8,261.6,9,True),(303.2,256.4,9,False),(301.0,259.2,7,False)]:
    for q in range(n):
        x,y=cx+R.rng.uniform(-0.8,0.8),cy+R.rng.uniform(-0.6,0.6)
        if hob and R.rng.random()<0.6: M.append(['smial',round(x,3),round(y,3),0.2,round(R.rng.uniform(0,6),2),'#2f7a3a'])
        else: M.append(['house',round(x,3),round(y,3),0.22,0.16,round(R.rng.uniform(0,3),2),WALLS[R.rng.integers(3)],ROOFS[R.rng.integers(4)],0.22])
# casa de Bill Samambaia, junto ao portão sul
FERNY=(SGATE[0]+0.6,SGATE[1]-0.55);M.append(['house',FERNY[0],FERNY[1],0.22,0.16,0.4,'#8a7a62','#3e3a34',0.22])
# sebe alta sobre o dique e os portões
M.append(['hedge',[[round(x,3),round(y,3)] for x,y in HEDGE[:4]],0.32])
M.append(['hedge',[[round(x,3),round(y,3)] for x,y in HEDGE[3:]],0.32])
for (gx_,gy_,r_) in [(WGATE[0],WGATE[1],0.0),(SGATE[0],SGATE[1],0.7)]:
    for s_ in (-1,1):
        x,y=gx_-math.sin(r_)*0.2*s_,gy_+math.cos(r_)*0.2*s_;M.append(['cyl',x,y,-0.05,0.42,0.04,0.04,6,'#6a5236'])
    M.append(['box',gx_,gy_,0.03,0.2,0.36,0.42,r_,'#6a5236',None])
    M.append(['house',gx_-0.25*math.cos(r_)+0.2,gy_-0.25*math.sin(r_)-0.25,0.16,0.12,r_,'#cdbf9e','#4e4e46',0.18])   # casa do porteiro
# árvores: floresta Chet, sebes dos campos
for _ in range(16000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(roadm,x,y)>0.05 or R.at(gm,x,y)>0.05 or any(math.hypot(x-px,y-py)<0.25 for px,py in HP): continue
    c=R.at(chet,x,y)
    if c>0.5 and R.rng.random()<0.12: R.tree(x,y,R.rng.uniform(0.6,0.95),1 if R.rng.random()<0.6 else 0,C(42,72,40)*R.rng.uniform(0.85,1.15))
    elif R.rng.random()<0.004: R.tree(x,y,R.rng.uniform(0.45,0.7),1,C(70,104,48))
R.TOPS=[[PONY[0],PONY[1],0.8,0.3]]
R.PL={'PoneiSaltitante':PONY,'PortaoOesteBri':WGATE,'PortaoSulBri':SGATE,'ColinaBri':BH,'CasaFerny':FERNY,'Encruzilhada':CROSS,'Staddle':(299.8,261.6),'Archet':(303.2,256.4),'Combe':(301.0,259.2),'FlorestaChet':(306.5,255.0)}
R.save_json()
