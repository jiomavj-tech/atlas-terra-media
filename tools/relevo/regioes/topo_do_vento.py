import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
R=Region('topo',322,240,354,270,PX=44,GR=5,seed=91,out='/tmp/claude-0/b3')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
WT=(337.6,254.0)
ROAD=[(R.X0-1,259.6),(328,259.4),(332,259.0),(335,258.6),(338.5,258.5),(342,258.9),(346,259.6),(350,260.0),(R.X1+1,260.3)]
DELL=(336.1,254.9)
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),4)
nz=R.noise(8,5,3,True)
hd=hbs*0.85+0.03+0.012*nz
# Colinas do Vento: crista para o norte
ridge=0.07*np.exp(-((GX-336.8+0.08*(GY-254))/1.6)**2)*sstep(257,250,GY)*(0.8+0.4*nz)
hd=hd+ridge
# o Topo do Vento: cone de topo achatado
d=np.hypot(GX-WT[0],GY-WT[1])
top=float(hd[int((WT[1]-R.Y0)*5),int((WT[0]-R.X0)*5)])+0.045
cone=top-0.09*sstep(0.55,4.2,d)
hd=np.maximum(hd,cone)
# clareira (depressão) a oeste
hd=hd-0.012*np.exp(-((GX-DELL[0])**2+(GY-DELL[1])**2)/(2*0.25**2))
hd=R.soften(hd,0.65,6)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
grass=C(128,132,82)*(1-np.clip(n1+0.5,0,1))+C(108,114,72)*np.clip(n1+0.5,0,1)
img+=(grass*0.6+R.base_tex(10)*1.1*0.4)*(1+n2*0.08)
dT=np.hypot(UX-WT[0],UY-WT[1])
img=R.paint(img,np.clip(sstep(0.9,2.2,R.slope),0,1),C(124,120,106),0.6)
img=R.paint(img,1-sstep(0.45,0.6,dT),C(132,128,104),0.8)
img,roadm=R.road(img,ROAD,0.22,C(170,154,118),C(100,90,68))
PATH=[(338.0,258.55),(338.6,257.2),(337.3,256.4),(338.4,255.4),(337.9,254.5)]
img,_=R.road(img,PATH,0.06,C(160,148,118),C(100,90,68))
img,_=R.road(img,[(336.0,258.6),(335.8,256.6),DELL],0.05,C(150,140,112),C(100,90,68))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD;zt=gz(*WT)
# Amon Sûl: anel de pedras em ruínas da antiga torre
n=26
for k in range(n):
    a=k/n*2*math.pi
    if R.rng.random()<0.22: continue
    x,y=WT[0]+math.cos(a)*0.42,WT[1]+math.sin(a)*0.42;h=R.rng.uniform(0.06,0.3)
    M.append(['boxA',x,y,0.05,0.035,zt-0.1,zt+h,a+math.pi/2,'#9a968c','#8a867c'])
for q in range(10):
    a=R.rng.uniform(0,6.28);r=R.rng.uniform(0.15,0.6);M.append(['stone',WT[0]+math.cos(a)*r,WT[1]+math.sin(a)*r])
# a pedra com a marca de Gandalf (runa G e três riscos)
GS=(WT[0]+0.1,WT[1]+0.12)
M.append(['boxA',GS[0],GS[1],0.06,0.04,zt-0.02,zt+0.05,0.3,'#b8b4a8','#b8b4a8'])
M.append(['discA',GS[0],GS[1],zt+0.052,0,0,0.018,[0.75,0.85,1.0,0.6]])
# a clareira: pedras e a fogueira dos hobbits
for q in range(6):
    a=q/6*6.28;M.append(['stone',DELL[0]+math.cos(a)*0.22,DELL[1]+math.sin(a)*0.18])
M.append(['capA',DELL[0],DELL[1],gz(*DELL)+0.02,0,0.035,8,[1.0,0.55,0.15,1.0]])
# árvores esparsas e arbustos
for _ in range(9000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(roadm,x,y)>0.05 or math.hypot(x-WT[0],y-WT[1])<1.6: continue
    if R.rng.random()<0.012: R.tree(x,y,R.rng.uniform(0.45,0.7),1 if R.rng.random()<0.6 else 0,C(62,88,48)*R.rng.uniform(0.85,1.1))
R.TOPS=[[WT[0],WT[1],0.6,0.5]]
R.PL={'AmonSul':WT,'PedraGandalf':GS,'ClareiraTopo':DELL,'EstradaTopo':(334.0,258.8),'ColinasVento':(336.5,246.5)}
R.save_json()
