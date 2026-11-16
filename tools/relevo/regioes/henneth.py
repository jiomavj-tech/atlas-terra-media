import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('henneth',600,532,630,560,PX=44,GR=5,seed=261,out='/tmp/claude-0/b6')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
HA=(613.0,546.0)                    # a cachoeira (janela voltada para o oeste)
STREAM=[(622.0,543.6),(619.0,544.6),(616.4,545.4),(614.2,545.9),HA,(612.4,546.1),(611.2,546.6),(609.0,547.8),(606.0,549.0),(602.0,550.2),(599.0,551.0)]
AMB=(606.5,555.0)                   # a emboscada aos Haradrim, na estrada
hbs=cv2.GaussianBlur(R.hb,(0,0),3);nz=R.noise(8,5,3,True)
hd=hbs+0.012*nz
hd=R.soften(hd,0.7,6)
# o degrau de rocha da cachoeira: terras altas a leste, o lago e o vale a oeste
step=sstep(HA[0]-0.35,HA[0]+0.25,GX+0.25*np.sin((GY-546)*0.8))*np.exp(-((GY-HA[1])/5.5)**2)
zl=float(hd[int((HA[1]-R.Y0)*5),int((HA[0]-1.2-R.X0)*5)])
hd=np.where(np.abs(GY-HA[1])<7,np.maximum(hd,zl+0.075*step),hd) if False else hd+0.06*step
POOL=(HA[0]-0.75,HA[1]+0.15);dp=np.hypot((GX-POOL[0])/0.6,(GY-POOL[1])/0.45)
zp=float(hd[int((POOL[1]-R.Y0)*5),int((POOL[0]-R.X0)*5)])-0.004
hd=np.where(dp<1.2,np.minimum(hd,zp+0.01*sstep(0.8,1.2,dp)),hd)
R.set_height(hd);gz=R.gz
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
gr=C(110,144,70)*(1-np.clip(n1+0.5,0,1))+C(92,126,60)*np.clip(n1+0.5,0,1)
img+=(gr*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.08)
rk=np.clip(sstep(1.2,2.6,R.slope),0,1)
img=R.paint(img,rk,C(128,122,110),0.85)
fl_=(R.rng.random((R.TH,R.TW))<0.012).astype(np.float32)
fcol=np.array([C(230,200,90),C(220,220,230),C(190,120,180)])[R.rng.integers(0,3,(R.TH,R.TW))]
img=img*(1-fl_[...,None]*(1-rk[...,None]))+fcol*fl_[...,None]*(1-rk[...,None])       # Ithilien, o jardim de Gondor
water=np.clip(R.line_mask(STREAM,0.09,0.8)*1.5,0,1)
water=np.maximum(water,np.clip((1-np.hypot((UX-POOL[0])/0.55,(UY-POOL[1])/0.4))*5,0,1))
img=R.paint(img,water,C(66,112,128))
ROAD=[(604.0,R.Y0-1),(604.6,540.0),(605.6,548.0),AMB,(607.4,R.Y1+1)]
img,roadm=R.road(img,ROAD,0.16,C(170,160,130),C(96,90,72))
fin=R.light(img)
R.save_tex(fin)
M=R.MOD
z1=gz(HA[0]+0.35,HA[1]);z0=gz(*POOL)
# a cortina de água e a caverna por trás (a Janela do Poente)
M.append(['boxA',HA[0]-0.05,HA[1],0.02,0.16,z0,z1+0.02,0,[0.72,0.82,0.88,0.08],None])
M.append(['boxA',HA[0]+0.02,HA[1],0.02,0.2,z0,z0+0.45,0,'#141210',None])
M.append(['discA',HA[0]-0.0,HA[1]+0.28,z0+0.25,-0.7,0.7,0.05,[1.0,0.7,0.3,0.9]])       # tocha na entrada lateral
# o Lago Proibido, com Gollum pescando numa pedra
M.append(['stone',POOL[0]+0.1,POOL[1]+0.25]);M.append(['blobA',POOL[0]+0.1,POOL[1]+0.25,z0+0.04,[[0.02,0],[0.025,0.02],[0,0.045]],5,'#6a6a58'])
# os guardiões de Ithilien nas pedras acima do lago
for (dx,dy) in [(0.5,-0.5),(0.55,0.55),(0.2,-0.75)]:
    x,y=HA[0]+dx,HA[1]+dy;M.append(['cylA',x,y,gz(x,y),gz(x,y)+0.09,0.014,0.01,5,'#3a5a34'])
# a emboscada: o mûmak (olifante) dos Haradrim e as flechas
zm=gz(*AMB)
M.append(['blobA',AMB[0],AMB[1],zm+0.16,[[0.0,0],[0.2,0.06],[0.24,0.2],[0.16,0.34],[0,0.4]],9,'#6e6660'])
for (dx,dy) in [(-0.11,-0.09),(0.11,-0.09),(-0.11,0.09),(0.11,0.09)]: M.append(['cylA',AMB[0]+dx,AMB[1]+dy,zm-0.02,zm+0.22,0.045,0.04,6,'#665e58'])
M.append(['blobA',AMB[0],AMB[1]+0.27,zm+0.22,[[0,0],[0.1,0.04],[0.11,0.12],[0,0.2]],8,'#6e6660'])
M.append(['cylA',AMB[0],AMB[1]+0.38,zm+0.02,zm+0.26,0.012,0.03,5,'#665e58'])
for s_ in (-1,1): M.append(['cylA',AMB[0]+s_*0.05,AMB[1]+0.36,zm+0.14,zm+0.2,0.006,0.012,4,'#f0ead8'])
M.append(['boxA',AMB[0],AMB[1]-0.02,0.09,0.11,zm+0.54,zm+0.7,0,'#8a2a2a','#c8a040'])
for k in range(12):
    a=R.rng.uniform(0,6.28);r=R.rng.uniform(0.4,1.0);M.append(['cylA',AMB[0]+math.cos(a)*r,AMB[1]+math.sin(a)*r,gz(AMB[0]+math.cos(a)*r,AMB[1]+math.sin(a)*r),gz(AMB[0]+math.cos(a)*r,AMB[1]+math.sin(a)*r)+0.1,0.004,0.004,3,'#d8d0b0'])
# a fogueira do coelho ensopado de Sam
FIRE=(607.6,551.6);M.append(['capA',FIRE[0],FIRE[1],gz(*FIRE)+0.02,0,0.03,6,[1.0,0.55,0.15,1.0]]);M.append(['stone',FIRE[0]+0.08,FIRE[1]])
for _ in range(26000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(water,x,y)>0.05 or R.at(roadm,x,y)>0.05 or R.at(rk,x,y)>0.5: continue
    if math.hypot(x-AMB[0],y-AMB[1])<0.5 or math.hypot(x-POOL[0],y-POOL[1])<0.7: continue
    if R.rng.random()<0.07: R.tree(x,y,R.rng.uniform(0.55,0.9),[1,1,0,2][R.rng.integers(4)],[C(60,104,50),C(84,120,56),C(44,84,48),C(110,130,60)][R.rng.integers(4)]*R.rng.uniform(0.85,1.1))
R.TOPS=[[AMB[0],AMB[1],0.9,0.4]]
R.PL={'JanelaPoente':HA,'LagoProibido':POOL,'EmboscadaHaradrim':AMB,'FogueiraSam':FIRE,'EstradaIthilien':(604.8,541.0),'JardimGondor':(617.0,553.0)}
R.save_json()
