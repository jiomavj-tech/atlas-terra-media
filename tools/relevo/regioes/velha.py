import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('velha',268,276,304,302,PX=44,GR=5,seed=221,out='/tmp/claude-0/b6')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
WILLOW=(273.6,285.6);TOM=(281.6,283.4);BARROW=(291.6,285.2);STONE=(288.6,282.0)
WITHY=[(R.X0-1,288.6),(270.5,287.4),(272.8,286.0),(275.0,285.4),(277.4,284.6),(279.6,283.9),(281.2,282.6),(282.4,280.6),(283.6,278.4)]
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs*0.8+0.02+0.01*nz
# as Colinas dos Túmulos: morros redondos e verdes
MOUNDS=[(288.0+R.rng.uniform(0,10),279.0+R.rng.uniform(0,12)) for _ in range(16)]+[BARROW]
mb=np.zeros_like(hd)
for mx,my in MOUNDS: mb=np.maximum(mb,gauss(mx,my,0.8,GX,GY))
hd=hd+0.02*mb
wm=cv2.resize(R.line_mask(WITHY,0.9,6),(R.GW,R.GH));hd=hd-0.02*np.clip(wm*2,0,1)
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(112,140,68)*(1-np.clip(n1+0.5,0,1))+C(96,126,60)*np.clip(n1+0.5,0,1)
img+=(gr*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.08)
forest=sstep(284.0,281.0,UX+1.2*R.noise(8,3,14)+0.15*(UY-286))
img=R.paint(img,forest,C(40,62,36),0.75)
img=R.paint(img,1-sstep(0.5,0.8,np.hypot(UX-TOM[0],UY-TOM[1])),C(110,160,70),0.9)
fog=np.clip(R.noise(6,3,33)*1.5+0.2,0,1)*sstep(286,289,UX)
img=R.paint(img,fog,C(190,200,196),0.28)                     # a névoa das Colinas
water=np.clip(R.line_mask(WITHY,0.14,0.8)*1.5,0,1)
img=R.paint(img,water,C(120,116,70))                         # o Voltavime, de água castanha
PATH=[(R.X0-1,280.5),(271.0,281.6),(273.0,284.4),WILLOW,(276.5,284.2),(279.5,283.2),TOM,(284.0,282.6),(286.5,282.4),STONE,(290.2,283.6),BARROW,(293.0,281.0),(294.0,277.5),(294.6,R.Y0-1)]
img,roadm=R.road(img,PATH,0.06,C(160,150,116),C(90,84,64))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD
# o Velho Salgueiro-homem: enorme, torto, com raízes e uma fenda no tronco
zw=gz(*WILLOW)
M.append(['cylA',WILLOW[0],WILLOW[1],zw-0.1,zw+0.5,0.16,0.11,7,'#5a4e3a']);M.append(['cylA',WILLOW[0]+0.04,WILLOW[1],zw+0.5,zw+0.95,0.11,0.06,7,'#5a4e3a'])
M.append(['boxA',WILLOW[0],WILLOW[1]+0.15,0.012,0.02,zw+0.05,zw+0.4,0,'#1a140e',None])
M.append(['blobA',WILLOW[0]+0.05,WILLOW[1],zw+0.55,[[0.35,0],[0.6,0.12],[0.55,0.45],[0.3,0.7],[0,0.8]],10,'#7a8a48'])
for k in range(10):
    a=k/10*6.28;M.append(['cylA',WILLOW[0]+0.05+math.cos(a)*0.5,WILLOW[1]+math.sin(a)*0.5,zw+0.1,zw+0.72,0.012,0.02,4,'#8a9a50'])
# a casa de Tom Bombadil: baixa, de pedra, com telhado de palha e luz amarela nas janelas
zt=gz(*TOM)
M.append(['house',TOM[0],TOM[1],0.5,0.26,0.2,'#d8cdb0','#a89050',0.2])
M.append(['house',TOM[0]+0.3,TOM[1]-0.18,0.24,0.18,1.77,'#d8cdb0','#a89050',0.16])
for k in range(4): M.append(['discA',TOM[0]-0.18+k*0.12,TOM[1]+0.135,zt+0.1,0,1,0.022,[1.0,0.85,0.4,1.0]])
M.append(['cyl',TOM[0]-0.15,TOM[1]-0.05,0.2,0.42,0.03,0.03,6,'#8a7a66'])
for k in range(14):
    a=k/14*6.28;x,y=TOM[0]+math.cos(a)*0.62,TOM[1]+math.sin(a)*0.5
    M.append(['capA',x,y,gz(x,y)+0.03,0,0.03,6,['#f2e04a','#f0f0f0','#e86a7a','#7a9af0'][k%4]])
# o lago dos lírios de Fruta d'Ouro
M.append(['capA',TOM[0]-0.5,TOM[1]+0.45,gz(TOM[0]-0.5,TOM[1]+0.45)+0.02,0,0.14,10,[0.4,0.6,0.7,0.2]])
for k in range(5): M.append(['capA',TOM[0]-0.5+math.cos(k*1.3)*0.08,TOM[1]+0.45+math.sin(k*1.3)*0.08,gz(TOM[0]-0.5,TOM[1]+0.45)+0.03,0,0.018,5,'#f8f8f0'])
# as Colinas dos Túmulos: túmulos com anel de pedras; a pedra erguida no meio
for mx,my in MOUNDS[::2]:
    z=gz(mx,my)
    for k in range(8):
        a=k/8*6.28;x,y=mx+math.cos(a)*0.32,my+math.sin(a)*0.32;M.append(['cylA',x,y,gz(x,y)-0.03,gz(x,y)+0.12,0.02,0.015,5,'#b0aca0'])
zb=gz(*BARROW)
M.append(['boxA',BARROW[0]-0.3,BARROW[1],0.03,0.08,zb-0.2,zb-0.02,0,'#1a1816',None])
for s_ in (-1,1): M.append(['cylA',BARROW[0]-0.32,BARROW[1]+s_*0.09,zb-0.25,zb+0.0,0.02,0.02,5,'#9a968a'])
M.append(['cylA',STONE[0],STONE[1],gz(*STONE)-0.05,gz(*STONE)+0.55,0.05,0.035,5,'#9a968a'])
# floresta antiga e fechada a oeste
for _ in range(22000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.1: continue
    if math.hypot(x-TOM[0],y-TOM[1])<0.8 or math.hypot(x-WILLOW[0],y-WILLOW[1])<0.6: continue
    f=R.at(forest,x,y)
    if f>0.5 and R.rng.random()<0.14:
        wil=float(R.at(wm.repeat(1,0),0,0)) if False else 0
        R.tree(x,y,R.rng.uniform(0.7,1.15),2 if R.rng.random()<0.15 else (1 if R.rng.random()<0.75 else 0),C(40,64,36)*R.rng.uniform(0.8,1.2))
R.TOPS=[[WILLOW[0],WILLOW[1],1.5,0.5],[TOM[0],TOM[1],0.6,0.5]]
R.PL={'VelhoSalgueiro':WILLOW,'CasaBombadil':TOM,'Voltavime':(277.4,284.6),'PedraErguida':STONE,'TumuloCriatura':BARROW,'ColinasTumulos':(294.0,288.0),'FlorestaVelhaSul':(271.5,280.0)}
R.save_json()
