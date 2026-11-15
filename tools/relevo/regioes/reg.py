"""Biblioteca comum para as regiões de detalhe do Atlas (relevo, textura, luz, modelos, embutir)."""
import numpy as np, cv2, json, math, os, base64
from PIL import Image
ME='/tmp/claude-0/me/'
HSW=46*1.35
def sstep(a,b,x): t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def gauss(cx,cy,s,X,Y): return np.exp(-((X-cx)**2+(Y-cy)**2)/(2*s*s))
C=lambda r,g,b: np.array([r,g,b],np.float32)/255
_h492=None;_tex=None;_lm=None
def base_maps():
    global _h492,_tex,_lm
    if _h492 is None:
        hm=np.asarray(Image.open(ME+'height_hi.png').convert('RGB')).astype(np.float32)
        _h492=((hm[...,0]*256+hm[...,1])/65535*1.25-0.05)
        _tex=np.asarray(Image.open(ME+'me_tex.webp').convert('RGB')).astype(np.float32)/255
        _lm=np.asarray(Image.open(ME+'light_hi.png').convert('RGB')).astype(np.float32)/255
    return _h492,_tex,_lm
class Region:
    def __init__(s,name,X0,Y0,X1,Y1,PX=40,GR=5,seed=1,out='.'):
        s.name=name;s.X0,s.Y0,s.X1,s.Y1=X0,Y0,X1,Y1;s.PX=PX;s.GR=GR;s.out=out
        s.TW,s.TH=int((X1-X0)*PX),int((Y1-Y0)*PX);s.GW,s.GH=int((X1-X0)*GR)+1,int((Y1-Y0)*GR)+1
        assert s.GW*s.GH<65000,('malha grande demais',s.GW*s.GH)
        s.rng=np.random.default_rng(seed)
        ux=np.linspace(X0,X1,s.TW,dtype=np.float32);uy=np.linspace(Y0,Y1,s.TH,dtype=np.float32);s.UX,s.UY=np.meshgrid(ux,uy)
        gx=np.linspace(X0,X1,s.GW);gy=np.linspace(Y0,Y1,s.GH);s.GX,s.GY=np.meshgrid(gx,gy)
        h492,tex,lm=base_maps()
        fx=s.GX/984*491;fy=s.GY/877*437;i0=np.floor(fx).astype(int);j0=np.floor(fy).astype(int);u=fx-i0;v=fy-j0
        s.hb=((h492[j0,i0]*(1-u)+h492[j0,i0+1]*u)*(1-v)+(h492[j0+1,i0]*(1-u)+h492[j0+1,i0+1]*u)*v).astype(np.float32)
        s.fade=np.clip(np.minimum.reduce([s.GX-X0,X1-s.GX,s.GY-Y0,Y1-s.GY])/4.0,0,1)
        s.MOD=[];s.TREES=[];s.TOPS=[];s.PL={}
    # ruído em textura (grid=False) ou na malha (grid=True)
    def noise(s,base,octv,seed,grid=False):
        w,h=(s.GW,s.GH) if grid else (s.TW,s.TH)
        r=np.random.default_rng(seed);out=np.zeros((h,w),np.float32);a=1;t=0
        for o in range(octv):
            n=r.standard_normal((int(base*2**o*h/w)+2,base*2**o+2)).astype(np.float32);out+=cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
        return out/t
    def tp(s,x,y): return (int(round((x-s.X0)*s.PX)),int(round((y-s.Y0)*s.PX)))
    def set_height(s,hd):
        hd=hd*s.fade+s.hb*(1-s.fade);hd=np.maximum(hd,-0.04).astype(np.float32);s.hd=hd
        enc=np.clip((hd+0.05)/1.25,0,1)*65535
        Image.fromarray(np.dstack([(enc//256).astype(np.uint8),(enc%256).astype(np.uint8),np.zeros((s.GH,s.GW),np.uint8)]),'RGB').save(os.path.join(s.out,s.name+'_h.png'),optimize=True)
        s.HT=cv2.resize(hd,(s.TW,s.TH),interpolation=cv2.INTER_CUBIC)
        s.slope=np.hypot(*np.gradient(cv2.GaussianBlur(s.HT,(0,0),2)*HSW,1/s.PX,1/s.PX))
    def soften(s,hd,k=0.55,sig=8.0):
        m=cv2.GaussianBlur(hd.astype(np.float32),(0,0),sig*s.GR);return m+(hd-m)*k
    def gz(s,x,y):
        hd=s.hd;fx=(x-s.X0)*s.GR;fy=(y-s.Y0)*s.GR;i=int(min(s.GW-2,max(0,fx)));j=int(min(s.GH-2,max(0,fy)));uu=min(1,max(0,fx-i));vv=min(1,max(0,fy-j))
        return float(((hd[j,i]*(1-uu)+hd[j,i+1]*uu)*(1-vv)+(hd[j+1,i]*(1-uu)+hd[j+1,i+1]*uu)*vv)*HSW)
    def at(s,m,x,y): px,py=s.tp(x,y);return m[min(s.TH-1,max(0,py)),min(s.TW-1,max(0,px))]
    def base_tex(s,blur=0):
        _,tex,_=base_maps();b=cv2.resize(tex[int(s.Y0*2):int(s.Y1*2),int(s.X0*2):int(s.X1*2)],(s.TW,s.TH),interpolation=cv2.INTER_CUBIC)
        return cv2.GaussianBlur(b,(0,0),blur) if blur else b
    def line_mask(s,pts,w,blur=0.9,closed=False):
        m=np.zeros((s.TH,s.TW),np.float32);cv2.polylines(m,[np.array([s.tp(x,y) for x,y in pts],np.int32)],closed,1.0,max(1,int(w*s.PX)),cv2.LINE_AA)
        return cv2.GaussianBlur(m,(0,0),blur) if blur else m
    def paint(s,img,m,col,a=1.0):
        m=np.clip(m*a,0,1)[...,None];return img*(1-m)+np.asarray(col,np.float32)*m
    def road(s,img,pts,w,col,ecol):
        m=s.line_mask(pts,w);e=np.clip(cv2.dilate(m,np.ones((5,5),np.uint8))-m,0,1)
        img=s.paint(img,e,ecol,0.4);img=s.paint(img,m,col);return img,m
    def light(s,img,amb=0.62,dif=0.55,tint=None):
        hf=cv2.GaussianBlur(s.HT,(0,0),3)*HSW
        gy_,gx_=np.gradient(hf,1/s.PX,1/s.PX)
        Lv=np.array([-0.62,-0.55,0.56]);Lv/=np.linalg.norm(Lv)
        nn=np.dstack([-gx_,-gy_,np.ones_like(hf)]);nn/=np.linalg.norm(nn,axis=2,keepdims=True)
        lam=np.clip(nn@Lv,0,1);flatL=float(Lv[2])
        Lt=(amb+dif*(lam-flatL)+0.42*flatL)*np.clip(1-(cv2.GaussianBlur(hf,(0,0),30)-hf)*0.04,0.65,1)
        cool=np.array([0.55,0.62,0.82]);warm=np.array([1.10,1.02,0.88]);mixw=np.clip(Lt,0,1.2)[...,None]/1.2
        fin=img*(cool*(1-mixw)+warm*mixw)*Lt[...,None]
        if tint is not None: fin=fin*np.asarray(tint)
        return fin
    def save_tex(s,fin):
        _,tex,lm=base_maps()
        def crop_up(a_,sc): return cv2.resize(a_[int(s.Y0*sc):int(s.Y1*sc),int(s.X0*sc):int(s.X1*sc)],(s.TW,s.TH),interpolation=cv2.INTER_CUBIC)
        cool=np.array([0.55,0.62,0.82]);warm=np.array([1.10,1.02,0.88])
        bt=crop_up(tex,2);bl=crop_up(lm,1);Lb=bl[...,0]*1.3;mb=np.clip(Lb,0,1.2)[...,None]/1.2
        base=bt*(cool*(1-mb)+warm*mb)*Lb[...,None];wcb=bl[...,2][...,None]*0.8;sky=np.array([0.62,0.70,0.76]);base=base*(1-wcb)+(bt*0.3+sky*0.38)*wcb
        bw=np.clip((np.minimum.reduce([s.UX-s.X0,s.X1-s.UX,s.UY-s.Y0,s.Y1-s.UY])-0.5)/5.0,0,1)[...,None]**1.5
        out=np.clip(fin*bw+base*(1-bw),0,1)
        cv2.imwrite(os.path.join(s.out,s.name+'_tex.webp'),cv2.cvtColor((out*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_WEBP_QUALITY,88])
        Image.fromarray((out*255).astype(np.uint8)).resize((s.TW//2,s.TH//2)).save(os.path.join(s.out,'prev.png'))
    def base_water(s,thr=0.45,soft=0.08):
        w=np.load(ME+'water.npy');crop=w[int(s.Y0*2):int(s.Y1*2),int(s.X0*2):int(s.X1*2)]
        up=cv2.resize(crop,(s.TW,s.TH),interpolation=cv2.INTER_CUBIC)
        return cv2.GaussianBlur(np.clip((up-thr)/soft,0,1),(0,0),0.9)
    def base_water_grid(s):
        w=np.load(ME+'water.npy');crop=w[int(s.Y0*2):int(s.Y1*2),int(s.X0*2):int(s.X1*2)]
        return cv2.resize(crop,(s.GW,s.GH),interpolation=cv2.INTER_AREA)
    def tree(s,x,y,sz,t,c): s.TREES.append([round(x,2),round(y,2),round(sz,2),t,round(float(c[0]),2),round(float(c[1]),2),round(float(c[2]),2)])
    def save_json(s):
        def _c(o):
            if isinstance(o,(list,tuple,np.ndarray)): return [_c(v) for v in o]
            if isinstance(o,(np.floating,float)): return round(float(o),3)
            if isinstance(o,np.integer): return int(o)
            return o
        json.dump({'rect':[s.X0,s.Y0,s.X1,s.Y1],'models':_c(s.MOD),'trees':_c(s.TREES),'tops':_c(s.TOPS),'places':{k:[round(float(x),2),round(float(y),2)] for k,(x,y) in s.PL.items()}},open(os.path.join(s.out,s.name+'.json'),'w'),separators=(',',':'))
        print(s.name,'modelos',len(s.MOD),'árvores',len(s.TREES),{f:os.path.getsize(os.path.join(s.out,s.name+f)) for f in ['_tex.webp','_h.png','.json']})
    # ---- modelos de terreno ----
    def ribbon(s,pts,hw,col,minrise=0.0,step=0.15,pad=0.03):
        """Fita apoiada no relevo (água, lava, cachoeira)."""
        for (ax,ay),(bx,by) in zip(pts[:-1],pts[1:]):
            n=max(1,int(math.hypot(bx-ax,by-ay)/step));rot=math.atan2(by-ay,bx-ax)
            for k in range(n):
                x0_,y0_=ax+(bx-ax)*k/n,ay+(by-ay)*k/n;x1_,y1_=ax+(bx-ax)*(k+1)/n,ay+(by-ay)*(k+1)/n
                za,zb=s.gz(x0_,y0_),s.gz(x1_,y1_)
                if abs(za-zb)>=minrise: s.MOD.append(['boxA',(x0_+x1_)/2,(y0_+y1_)/2,math.hypot(x1_-x0_,y1_-y0_)/2+0.01,hw,min(za,zb)-pad,max(za,zb)+pad,rot,col,None])
def dense(pts,step=0.04):
    o=[];sv=[];acc=0
    for (ax,ay),(bx,by) in zip(pts[:-1],pts[1:]):
        L=math.hypot(bx-ax,by-ay);n=max(1,int(L/step))
        for k in range(n): o.append((ax+(bx-ax)*k/n,ay+(by-ay)*k/n));sv.append(acc+L*k/n)
        acc+=L
    o.append(pts[-1]);sv.append(acc);return np.array(o),np.array(sv)
INDEX='/home/claude/atlas-terra-media/index.html'
def embed(dirp,name,sid,title):
    d=lambda f,t:'data:image/'+t+';base64,'+base64.b64encode(open(f,'rb').read()).decode()
    s=open(INDEX,encoding='utf-8').read();sj=json.load(open(os.path.join(dirp,name+'.json')))
    det={'name':title,'rect':sj['rect'],'hm':d(os.path.join(dirp,name+'_h.png'),'png'),'tex':d(os.path.join(dirp,name+'_tex.webp'),'webp'),'models':sj['models'],'trees':sj['trees'],'tops':sj['tops']}
    tag=f'<script id="atlas-detail-{sid}">window.ATLAS_DETAILS=window.ATLAS_DETAILS||[];window.ATLAS_DETAILS.push('+json.dumps(det,separators=(',',':'),ensure_ascii=False)+');</script>'
    key=f'<script id="atlas-detail-{sid}">'
    if key in s:
        i=s.index(key);j=s.index('</script>',i)+9;s=s[:i]+tag+s[j:]
    else: s=s.replace('<script id="atlas-v86-relevo">',tag+'\n<script id="atlas-v86-relevo">',1)
    open(INDEX,'w',encoding='utf-8').write(s);print('embed',sid,round(len(s.encode())/1e6,2),'MB')
def integrate(places,SUB,basekey,deepz,route_key=None,route_js=None,option=None):
    """Acrescenta os nomes de perto (P, PINS, SUBK), o mergulho e a rota. Idempotente por chave."""
    s=open(INDEX,encoding='utf-8').read()
    def rep(a,b):
        nonlocal s; assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
    i=s.index('const P={Condado:');j=s.index('};',i)
    K=[x[1] for x in SUB]
    for k in K: assert (','+k+':[') not in s[i:j],('já existe',k)
    s=s[:j]+','+','.join(f'{k}:[{places[k][0]},{places[k][1]}]' for k in K)+s[j:]
    i=s.index("const PINS=[");j=s.index("];",i);s=s[:j]+','+','.join(json.dumps([n,k,None,d,w],ensure_ascii=False) for n,k,d,w in SUB)+s[j:]
    i=s.index("const SUBK=new Set([");j=s.index("]);",i);s=s[:j]+','+','.join(json.dumps(k) for k in K)+s[j:]
    if basekey:
        rep("(SUBK.has(k)?deep:!(deep&&(","(SUBK.has(k)?deep:!(deep&&(k==="+json.dumps(basekey).replace('"',"'")+"||")
        rep("const deepZ=key==='Condado'?zFit*11:","const deepZ=key==='Condado'?zFit*11:key==="+json.dumps(basekey).replace('"',"'")+f"?zFit*{deepz}:")
    if route_key:
        rep(" cerco:{title:'O cerco de Minas Tirith',",f" {route_key}:"+route_js+",\n cerco:{title:'O cerco de Minas Tirith',")
        rep('<option value="cerco">O cerco de Minas Tirith (de perto)</option>',f'<option value="cerco">O cerco de Minas Tirith (de perto)</option><option value="{route_key}">{option} (de perto)</option>')
    open(INDEX,'w',encoding='utf-8').write(s);print('integrado',len(SUB),'lugares')
def route_js(title,icon,z,steps):
    return "{title:"+json.dumps(title,ensure_ascii=False).replace('"',"'")+",icon:'"+icon+"',z:"+str(z)+",steps:[\n"+",\n".join("  "+json.dumps(st,ensure_ascii=False) for st in steps)+"]}"
