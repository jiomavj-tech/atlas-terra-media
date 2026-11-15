import numpy as np, cv2
img=cv2.imread('/tmp/claude-0/m3d/map.webp');H,W=img.shape[:2];out=img.copy()
LABELS=[(108,12,224,66),(490,28,585,70),(365,68,420,88),(814,112,918,150),(855,146,984,168),(218,155,312,180),(58,280,120,300),(180,285,258,305),
 (388,248,460,270),(500,240,572,282),(595,240,705,285),(500,318,555,342),(755,302,885,330),(912,350,982,400),(630,383,722,405),(420,448,485,467),
 (4,454,136,526),(552,500,618,527),(292,520,362,540),(432,625,518,652),(530,660,625,682),(660,672,775,694),(866,556,984,584),(826,602,914,632),
 (830,646,924,686),(315,822,440,842),(652,820,712,846),(815,802,872,822)]
ICONS=[(90,258,27),(220,262,27),(425,222,27),(476,333,27),(650,213,26),(605,385,27),(452,425,26),(532,497,26),(476,598,28),(835,568,26),(160,203,17),(282,200,17)]
KEEP=[(800,140,36),(885,480,52)]
TOWERS=[(340,92,34),(326,490,34),(572,628,40),(690,628,38),(808,598,40)]  # torres/picos desenhados: não servem de fonte
UI=[(0,10,74,214),(818,10,984,76),(876,708,984,818),(812,820,984,866)]
LEG=(0,596,246,860)
F=np.zeros((H,W),np.uint8)
bb_,gg_,rr_=[img[...,i].astype(int) for i in range(3)]
WAT=((bb_>rr_+12)&(bb_>gg_-5)).astype(np.uint8)
WI=cv2.integral(WAT)
def wfrac(x0,y0,x1,y1): return (WI[y1,x1]-WI[y0,x1]-WI[y1,x0]+WI[y0,x0])/max(1,(x1-x0)*(y1-y0))
def fbox(b,m=8): cv2.rectangle(F,(b[0]-m,b[1]-m),(b[2]+m,b[3]+m),1,-1)
for b in LABELS+UI+[LEG]: fbox(b)
for x,y,r in ICONS+KEEP+TOWERS: cv2.circle(F,(x,y),r+10,1,-1)
def integ(): return cv2.integral(F)
def forb(Fi,x0,y0,x1,y1):
    if x0<0 or y0<0 or x1>W or y1>H: return 10**9
    return Fi[y1,x1]-Fi[y0,x1]-Fi[y1,x0]+Fi[y0,x0]
def best_offset(region_mask,bbox,maxd=220,step=12):
    x0,y0,x1,y1=bbox;Fi=integ()
    ring=cv2.dilate(region_mask,np.ones((15,15),np.uint8))-region_mask
    ys,xs=np.nonzero(ring);tgt=out[ys,xs].astype(np.int16);rw=WAT[ys,xs].mean()
    best=None
    for dy in range(-maxd,maxd+1,step):
        for dx in range(-maxd,maxd+1,step):
            if abs(dx)<(x1-x0)//2 and abs(dy)<(y1-y0)//2: continue
            if forb(Fi,x0+dx-8,y0+dy-8,x1+dx+8,y1+dy+8)>0: continue
            sw=wfrac(x0+dx,y0+dy,x1+dx,y1+dy)
            if abs(sw-rw)>0.35: continue
            c=np.abs(out[ys+dy,xs+dx].astype(np.int16)-tgt).mean()+0.03*(abs(dx)+abs(dy))+60*abs(sw-rw)
            if best is None or c<best[0]: best=(c,dx,dy)
    return best
def paste(region_mask,dx,dy,feather=9):
    global out
    m=cv2.GaussianBlur(cv2.dilate(region_mask,np.ones((5,5),np.uint8)).astype(np.float32),(feather,feather),0)[...,None]
    sh=np.roll(np.roll(out,-dy,0),-dx,1)  # sh[y,x]=out[y+dy,x+dx]
    out=(sh*m+out*(1-m)).astype(np.uint8)
def clean(region_mask,bbox,clear_box):
    b=best_offset(region_mask,bbox)
    if b is None: b=best_offset(region_mask,bbox,maxd=420,step=20)
    if b is None:
        global out; out=cv2.inpaint(out,(region_mask*255).astype(np.uint8),7,cv2.INPAINT_TELEA); print('preenchido por interpolação',bbox); return
    paste(region_mask,b[1],b[2])
    cv2.rectangle(F,(clear_box[0]-8,clear_box[1]-8),(clear_box[2]+8,clear_box[3]+8),0,-1)  # limpo: agora pode servir de fonte
    for x,y,r in KEEP: cv2.circle(F,(x,y),r+10,1,-1)
for x,y,r in ICONS+TOWERS:
    m=np.zeros((H,W),np.uint8);cv2.circle(m,(x,y),r+3,1,-1);bb=(x-r-3,y-r-3,x+r+3,y+r+3);clean(m,bb,bb)
for bb in LABELS:
    x0,y0,x1,y1=bb;m=np.zeros((H,W),np.uint8);cv2.rectangle(m,(max(0,x0),y0),(min(W-1,x1),y1),1,-1);clean(m,bb,bb)
for bb in UI:
    x0,y0,x1,y1=bb;m=np.zeros((H,W),np.uint8);cv2.rectangle(m,(x0,y0),(min(W-1,x1),min(H-1,y1)),1,-1);clean(m,bb,bb)
# legenda (grande): mar copiado de cima, com emenda suave
x0,y0,x1,y1=LEG;m=np.zeros((H,W),np.uint8);cv2.rectangle(m,(x0,y0),(x1,y1),1,-1);paste(m,0,-262,feather=41)
cv2.imwrite('mapa_limpo.png',out);cv2.imwrite('mapa_limpo.webp',out,[cv2.IMWRITE_WEBP_QUALITY,84])
import os;print(os.path.getsize('mapa_limpo.webp'))
