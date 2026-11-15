import sys;sys.path.insert(0,'/tmp/claude-0/lib')
from reg import *
from scipy.spatial import cKDTree
R=Region('moria',420,348,462,384,PX=40,GR=5,seed=61,out='/tmp/claude-0/b2')
GX,GY,UX,UY=R.GX,R.GY,R.UX,R.UY
WG=(430.6,366.0)          # Portão Oeste (Portas de Durin), voltado para o oeste
LAKE=(428.6,366.3)
EG=(447.6,370.6)          # Portão Leste (do Riacho Escuro), voltado para leste
MIRROR=(450.6,374.6)      # Kheled-zâram
CARAD=(443.0,352.5);ZIRAK=(434.5,378.2)
SIRANNON=[(420.0,367.2),(422.5,367.0),(425.0,366.8),(427.2,366.5),LAKE]
DIMRILL=[EG,(448.6,372.0),(449.6,373.4),MIRROR,(452.6,375.6),(455.0,376.8),(458.0,378.6),(462.5,380.6)]
# ---------- relevo ----------
hbs=cv2.GaussianBlur(R.hb,(0,0),3)
nz=R.noise(8,5,3,True);nzf=R.noise(30,3,33,True);rid=(1-np.abs(R.noise(14,4,9,True)))**2
hd=hbs+0.02*nz+0.03*rid*sstep(0.35,0.45,hbs)
hd=hd+0.05*gauss(*ZIRAK,1.8,GX,GY)
hd=R.soften(hd,0.6,7)
def carve(hd,path,f0,f1,w0,w1,wall):
    P,S=dense(path);T=cKDTree(P);d,i=T.query(np.stack([GX.ravel(),GY.ravel()],1));d=d.reshape(GX.shape);t=(S[i]/S[-1]).reshape(GX.shape)
    fl=f0+(f1-f0)*t;wf=(w0+(w1-w0)*t)*(1+0.35*nz+0.5*nzf);wall=wall*(1+0.4*np.abs(nz))
    pr=fl+(hd-fl)*sstep(wf,wf+wall,d)**0.8
    return np.where(d<wf+wall,np.minimum(hd,pr),hd),d
# vale do Sirannon até o paredão do Portão Oeste
hd,dW=carve(hd,SIRANNON+[(WG[0]-0.15,WG[1])],0.27,0.32,1.0,0.6,4.0)
# paredão: a rocha sobe a prumo atrás das portas
cliff=sstep(WG[0]-0.05,WG[0]+0.35,GX)*np.exp(-((GY-WG[1])/2.2)**2)
hd=np.maximum(hd,0.30+0.12*cliff)
# Vale do Riacho Escuro: do Portão Leste ao Lago Espelhado e o Veio de Prata
hd,dE=carve(hd,DIMRILL,0.34,0.17,0.4,1.4,4.0)
mir=np.hypot((GX-MIRROR[0])/1.2,(GY-MIRROR[1])/0.75)
zm=float(hd[int((MIRROR[1]-R.Y0)*5),int((MIRROR[0]-R.X0)*5)])
hd=np.where(mir<1.4,np.minimum(hd,zm+0.01*sstep(0.9,1.4,mir)),hd)
cliffE=sstep(EG[0]+0.05,EG[0]-0.35,GX)*np.exp(-((GY-EG[1])/1.6)**2)
hd=np.maximum(hd,float(hd[int((EG[1]-R.Y0)*5),int((EG[0]+0.3-R.X0)*5)])+0.10*cliffE)
R.set_height(hd);gz=R.gz
# ---------- textura ----------
img=np.zeros((R.TH,R.TW,3),np.float32)
n1=R.noise(40,4,5)[...,None];n2=R.noise(200,3,6)[...,None]
grass=C(112,124,76)*(1-np.clip(n1+0.5,0,1))+C(92,106,64)*np.clip(n1+0.5,0,1)
img+=(grass*0.5+R.base_tex(10)*1.1*0.5)*(1+n2*0.08)
rk=np.clip(sstep(0.9,3.5,R.slope)+sstep(0.5,0.6,R.HT),0,1)
strata=0.5+0.5*np.sin(R.HT*HSW*7+R.noise(30,3,44)*3)
img=R.paint(img,rk,C(118,112,108)*(1+R.noise(80,4,8)[...,None]*0.14),0.92)
snow=sstep(0.68,0.76,R.HT+0.03*R.noise(50,3,9));img=R.paint(img,snow,C(236,240,246))
# lagos: o do Vigia (escuro) e o Lago Espelhado
lake=np.clip((1.0-np.hypot((UX-LAKE[0])/1.5,(UY-LAKE[1])/1.0))*6,0,1)*(UX<WG[0]-0.15)
img=R.paint(img,lake,C(28,40,38))
mirr=np.clip((1.0-np.hypot((UX-MIRROR[0])/1.15,(UY-MIRROR[1])/0.7))*6,0,1)
img=R.paint(img,mirr,C(30,52,84))
silver=np.clip(R.line_mask(DIMRILL[3:],0.12,0.8)*1.5,0,1)
img=R.paint(img,silver,C(150,180,196))
dry=R.line_mask(SIRANNON[:-1],0.1,0.8)
img=R.paint(img,dry,C(120,112,96),0.7)          # leito seco do Sirannon
# trilhas: rumo ao Portão Oeste, a Escada do Riacho Escuro e o caminho do Passo do Chifre Vermelho
img,_=R.road(img,[(420.0,366.0),(423.5,365.8),(427.0,365.3),(429.0,365.0),(WG[0]-0.1,365.6)],0.08,C(150,138,112),C(96,88,72))
STAIR=[EG,(448.2,371.1),(447.9,371.6),(448.6,372.0),(448.3,372.6),(449.2,373.3),(449.6,373.8)]
img,_=R.road(img,STAIR,0.07,C(170,160,140),C(96,88,72))
PASS=[(423.0,362.0),(429.0,359.5),(435.0,356.5),(440.0,354.6),(445.0,354.0),(450.0,356.0)]
img,_=R.road(img,PASS,0.06,C(160,150,130),C(96,88,72))
fin=R.light(img)
R.save_tex(fin)
# ================= MODELOS =================
M=R.MOD
zw=gz(WG[0]-0.25,WG[1]);GLOW=[0.78,0.88,1.0,1.0]
# Portas de Durin: ithildin brilhando na rocha (arco, pilares, coroa e estrela)
fx=WG[0]+0.02
for s_ in (-1,1): M.append(['boxA',fx,WG[1]+s_*0.22,0.006,0.012,zw,zw+0.62,0,GLOW,None])
for k in range(13):
    a=k/12*math.pi;M.append(['boxA',fx,WG[1]+math.cos(a)*0.22,0.006,0.02,zw+0.62+math.sin(a)*0.18,zw+0.64+math.sin(a)*0.18,0,GLOW,None])
M.append(['discA',fx-0.004,WG[1],zw+0.5,-1,0,0.05,GLOW])
for k in range(7): M.append(['discA',fx-0.004,WG[1]-0.09+k*0.03,zw+0.74,-1,0,0.008,GLOW])
M.append(['boxA',fx+0.01,WG[1],0.01,0.2,zw,zw+0.6,0,'#4a4a4c',None])
# azevinhos dos dois lados das portas
for s_ in (-1,1):
    x,y=WG[0]-0.3,WG[1]+s_*0.55;z=gz(x,y)
    M.append(['cylA',x,y,z-0.05,z+0.15,0.03,0.025,5,'#4a3424']);M.append(['blobA',x,y,z+0.12,[[0.12,0],[0.18,0.12],[0.14,0.3],[0,0.38]],8,'#1f4a2a'])
# o Vigia da Água: tentáculos saindo do lago
zl=gz(*LAKE)
for k,(dx,dy,h) in enumerate([(0.3,-0.4,0.55),(0.6,0.1,0.75),(0.1,0.45,0.45),(-0.3,-0.1,0.35),(0.85,-0.3,0.6)]):
    x,y=LAKE[0]+dx,LAKE[1]+dy
    for q in range(4):
        M.append(['cylA',x+q*0.03,y-q*0.02,zl-0.05+q*h/4,zl-0.05+(q+1)*h/4,0.035*(1-q/5),0.035*(1-(q+1)/5),5,'#2c4434'])
# Portão Leste: abertura escura no paredão com pilares
ze=gz(EG[0]+0.25,EG[1])
M.append(['boxA',EG[0]-0.02,EG[1],0.02,0.28,ze,ze+0.55,0,'#0e0d0e',None])
for s_ in (-1,1): M.append(['cylA',EG[0]+0.05,EG[1]+s_*0.32,ze-0.05,ze+0.62,0.04,0.035,8,'#7a7672'])
# Pedra de Durin junto ao Lago Espelhado e a coroa de estrelas refletida
ds=(MIRROR[0]-1.35,MIRROR[1]-0.5);M.append(['cyl',ds[0],ds[1],-0.05,0.4,0.05,0.035,6,'#8e8a84'])
zm2=gz(*MIRROR)+0.015
for k in range(7):
    a=k/7*2*math.pi;M.append(['capA',MIRROR[0]+math.cos(a)*0.25,MIRROR[1]+math.sin(a)*0.14,zm2,0,0.02,6,[1,1,1,1]])
# Zirakzigil: a Torre de Durin no pico
zz=gz(*ZIRAK)
M.append(['cylA',ZIRAK[0],ZIRAK[1],zz-0.2,zz+0.5,0.09,0.07,8,'#9a948c']);M.append(['capA',ZIRAK[0],ZIRAK[1],zz+0.5,0,0.08,8,'#b8b2a8'])
# ruínas de Eregion (Azevim) no vale do Sirannon
for q in range(12):
    x,y=R.rng.uniform(420.8,426),366.8+R.rng.uniform(-1.4,1.4)
    M.append(['cyl',x,y,-0.05,R.rng.uniform(0.15,0.45),0.05,0.04,6,'#b8b0a0'])
# árvores: azevinhos em Eregion, pinheiros no Vale do Riacho Escuro
for _ in range(15000):
    x,y=R.rng.uniform(R.X0,R.X1),R.rng.uniform(R.Y0,R.Y1)
    if R.at(lake,x,y)>0.05 or R.at(mirr,x,y)>0.05 or R.at(snow,x,y)>0.1 or R.at(rk,x,y)>0.5: continue
    h=R.at(R.HT,x,y)
    if x<428 and R.rng.random()<0.03: R.tree(x,y,R.rng.uniform(0.5,0.75),1,C(32,72,40)*R.rng.uniform(0.85,1.1))
    elif x>449 and R.rng.random()<0.04: R.tree(x,y,R.rng.uniform(0.55,0.85),0,C(36,64,44)*R.rng.uniform(0.85,1.1))
    elif h<0.5 and R.rng.random()<0.01: R.tree(x,y,R.rng.uniform(0.5,0.75),0,C(40,70,46))
R.TOPS=[[WG[0],WG[1],1.0,0.3],[EG[0],EG[1],0.9,0.3]]
R.PL={'PortasDurin':(WG[0]-0.05,WG[1]),'LagoVigia':LAKE,'PortaoLeste':EG,'EscadaRiachoEscuro':STAIR[4],'LagoEspelhado':MIRROR,'PedraDurin':ds,
      'PonteKhazadDum':(445.6,369.6),'Caradhras':CARAD,'Zirakzigil':ZIRAK,'Azevim':(423.0,367.6),'VeioPrata':(457.0,377.9)}
R.save_json()
