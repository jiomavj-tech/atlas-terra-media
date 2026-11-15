/* Relevo 3D v2 do mapa ilustrado — WebGL puro, sem bibliotecas (funciona offline).
   Câmera em perspectiva real; terreno 492×438 com mapa de luz assado (sombras, oclusão, neve, água);
   construções e árvores em 3D. Dados: HM (altura 16 bits em R/G), LM (luz/neve/água), TEX (mapa sem nomes,
   ícones e torres pintadas), TREES (posições e cores das árvores). */
window.AtlasRelevo=(()=>{'use strict';
const HM='__HM__',LM='__LM__',TEX='__TEX__',TREES=__TREES__;
const MW=984,MH=877,HS=46,EX=1.35,FOV=40*Math.PI/180,BASE=-26;
let gl=null,cv=null,ok=false,GW=492,GH=438,heights=null,uintOK=false;
let pT=null,pM=null,bufT=null,ibT=null,nIdx=0,bufM=null,nM=0,texMap=null,texLight=null;
const SUN=(()=>{const v=[-0.62,-0.55,0.56],l=Math.hypot(...v);return v.map(x=>x/l)})();
function supported(){try{const c=document.createElement('canvas');return !!(c.getContext('webgl')||c.getContext('experimental-webgl'))}catch(e){return false}}
function load(src){return new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=rej;i.src=src})}
function prog(vs,fs){const mk=(t,s)=>{const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(o));return o};
  const p=gl.createProgram();gl.attachShader(p,mk(gl.VERTEX_SHADER,vs));gl.attachShader(p,mk(gl.FRAGMENT_SHADER,fs));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw new Error('link');
  p.u={};['T','R','Up','F','C','f','W','H','A','B','fog0','fog1','tMap','tLight','sun'].forEach(k=>p.u[k]=gl.getUniformLocation(p,k));return p}
/* câmera: mesma conta no sombreador e no JavaScript */
const CAMV=`uniform vec3 C,R,Up,F;uniform float f,W,H,A,B;
vec4 proj(vec3 p,out float zc){vec3 r=p-C;float x=dot(r,R),y=dot(r,Up);zc=dot(r,F);return vec4(x*2.0*f/W,y*2.0*f/H-0.16*zc,A*zc+B,zc);}`;
const VT=`attribute vec3 p;${CAMV}varying vec2 uv;varying float zc;varying float hz;
void main(){float z;gl_Position=proj(p,z);zc=z;uv=vec2(p.x/${MW}.0,p.y/${MH}.0);hz=p.z;}`;
const FT=`precision mediump float;uniform sampler2D tMap,tLight;uniform float fog0,fog1;varying vec2 uv;varying float zc;varying float hz;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
void main(){vec3 sky=vec3(0.62,0.70,0.76);vec3 col=texture2D(tMap,uv).rgb;vec3 lm=texture2D(tLight,uv).rgb;float L=lm.r*1.3;
 float g=hash(floor(uv*vec2(1600.0,1426.0)))*0.06-0.03;col+=g;
 vec3 lit=col*mix(vec3(0.55,0.62,0.82),vec3(1.10,1.02,0.88),clamp(L,0.0,1.2))*L;
 lit=mix(lit,vec3(0.94,0.96,1.0)*(0.55+0.5*L),lm.g*0.75);
 vec3 wcol=mix(col*0.55,sky*0.85,0.45)+vec3(0.10,0.12,0.12)*smoothstep(0.75,1.1,L);lit=mix(lit,wcol,lm.b*0.8);
 float fg=smoothstep(fog0,fog1,zc);gl_FragColor=vec4(mix(lit,sky,fg*0.85),1.0);}`;
const VM=`attribute vec3 p;attribute vec3 n;attribute vec4 c;${CAMV}uniform vec3 sun;varying vec4 vc;varying float zc;
void main(){float z;gl_Position=proj(p,z);zc=z;float d=max(dot(normalize(n),sun),0.0);vc=vec4(mix(c.rgb*(0.38+0.85*d),c.rgb*1.15,c.a),1.0);}`;
const FM=`precision mediump float;uniform float fog0,fog1;varying vec4 vc;varying float zc;
void main(){vec3 sky=vec3(0.62,0.70,0.76);float fg=smoothstep(fog0,fog1,zc);gl_FragColor=vec4(mix(vc.rgb,sky,fg*0.85),1.0);}`;
/* ---- altura ---- */
function hAt(i,j){i=Math.max(0,Math.min(GW-1,i));j=Math.max(0,Math.min(GH-1,j));return heights[j*GW+i]}
function height(x,y){if(!heights)return 0;const fx=Math.max(0,Math.min(GW-1.001,x/MW*(GW-1))),fy=Math.max(0,Math.min(GH-1.001,y/MH*(GH-1)));const i=fx|0,j=fy|0,u=fx-i,v=fy-j;
  return ((hAt(i,j)*(1-u)+hAt(i+1,j)*u)*(1-v)+(hAt(i,j+1)*(1-u)+hAt(i+1,j+1)*u)*v)}
/* ---- construções ---- */
const M=[];let LAND=[];
function tri(a,b,c,col){const u=[b[0]-a[0],b[1]-a[1],b[2]-a[2]],v=[c[0]-a[0],c[1]-a[1],c[2]-a[2]];let n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];if(n[2]<-1e-6&&Math.abs(n[2])>Math.hypot(n[0],n[1])*2)n=n.map(x=>-x);
  for(const p of [a,b,c])M.push(p[0],p[1],p[2],n[0],n[1],n[2],col[0],col[1],col[2],col[3]||0)}
function quad(a,b,c,d,col){tri(a,b,c,col);tri(a,c,d,col)}
function cyl(x,y,z0,z1,r0,r1,n,col,capCol){for(let k=0;k<n;k++){const a0=k/n*Math.PI*2,a1=(k+1)/n*Math.PI*2;
  const p=(r,a,z)=>[x+Math.cos(a)*r,y+Math.sin(a)*r,z];quad(p(r0,a0,z0),p(r0,a1,z0),p(r1,a1,z1),p(r1,a0,z1),col);
  if(r1>0.01)tri([x,y,z1],p(r1,a0,z1),p(r1,a1,z1),capCol||col)}}
function box(x,y,sx,sy,z0,z1,col,rot=0,roofCol){const c=Math.cos(rot),s=Math.sin(rot);const P=(dx,dy,z)=>[x+dx*c-dy*s,y+dx*s+dy*c,z];
  const a=P(-sx,-sy,z0),b=P(sx,-sy,z0),cc=P(sx,sy,z0),d=P(-sx,sy,z0),A=P(-sx,-sy,z1),B=P(sx,-sy,z1),C=P(sx,sy,z1),D=P(-sx,sy,z1);
  quad(a,b,B,A,col);quad(b,cc,C,B,col);quad(cc,d,D,C,col);quad(d,a,A,D,col);
  if(roofCol){const r1=P(0,-sy,z1+sx*0.9),r2=P(0,sy,z1+sx*0.9);quad(A,r1,r2,D,roofCol);quad(B,C,r2,r1,roofCol);tri(A,B,r1,roofCol);tri(C,D,r2,roofCol)}else quad(A,B,C,D,col)}
function g(x,y){return height(x,y)*EX}
const DARK=[0.13,0.12,0.13],BLACK=[0.07,0.07,0.08],WHITE=[0.88,0.86,0.80],PALE=[0.62,0.70,0.62],GOLD=[0.86,0.66,0.26],WOOD=[0.42,0.28,0.16],FIRE=[1.0,0.45,0.08,1],GLOW=[0.55,1.0,0.6,1];
function buildModels(P){M.length=0;LAND=[];
  const land=(k,top)=>{const p=P[k];if(p)LAND.push([p[0],p[1],top])};
  // Barad-dûr: fortaleza escura em degraus, torre alta, chifres e o Olho
  {const [x,y]=P.BaradDur,z=g(x,y)-2;cyl(x,y,z,z+14,16,13,8,DARK);cyl(x,y,z+14,z+30,10,8,8,DARK);cyl(x,y,z+30,z+66,6.5,3.6,8,BLACK);
   for(const a of [0.4,2.0]){const xx=x+Math.cos(a)*3,yy=y+Math.sin(a)*3;cyl(xx,yy,z+62,z+78,1.6,0,4,BLACK)}
   cyl(x,y,z+66,z+70,2.6,3.2,8,FIRE);cyl(x,y,z+70,z+72,3.2,0,8,FIRE);land('BaradDur',78)}
  // Orthanc: torre negra de quatro chifres no anel de Isengard
  {const [x,y]=P.Isengard,z=g(x,y)-1;cyl(x,y,z,z+3,22,22,24,[0.30,0.30,0.28]);cyl(x,y,z+3,z+3.2,19,19,24,[0.22,0.26,0.20]);
   box(x,y,4,4,z,z+44,BLACK,0.3);for(let k=0;k<4;k++){const a=0.3+k*Math.PI/2+Math.PI/4;cyl(x+Math.cos(a)*3.4,y+Math.sin(a)*3.4,z+44,z+53,1.3,0.2,4,BLACK)}land('Isengard',53)}
  // Minas Tirith: sete anéis brancos, a Torre de Ecthelion e o esporão de pedra
  {const [x,y]=P.MinasTirith,z=g(x,y)-2;for(let k=0;k<7;k++)cyl(x,y-k*0.8,z+k*4.2,z+k*4.2+4.6,17-k*1.9,16.4-k*1.9,20,k%2?[0.84,0.83,0.78]:WHITE);
   box(x+6,y-3,1.5,8,z+4,z+28,[0.80,0.79,0.74],0.5);cyl(x,y-5.6,z+29,z+52,1.6,1.2,8,WHITE);cyl(x,y-5.6,z+52,z+57,1.7,0,8,[0.9,0.9,0.95]);land('MinasTirith',57)}
  // Minas Morgul: torre pálida com brilho esverdeado
  {const [x,y]=P.MinasMorgul,z=g(x,y)-1;cyl(x,y,z,z+10,9,8,10,PALE);cyl(x,y,z+10,z+38,3.6,2.6,8,PALE);cyl(x,y,z+30,z+33,2.9,2.9,8,GLOW);cyl(x,y,z+38,z+46,2.8,0,8,PALE);land('MinasMorgul',46)}
  // Portão Negro: muralha entre duas torres
  {const [x,y]=P.PortaoNegro,z=g(x,y)-1;box(x,y,16,2.2,z,z+13,BLACK,0.15);for(const s of [-1,1]){const xx=x+s*17*Math.cos(0.15),yy=y+s*17*Math.sin(0.15);cyl(xx,yy,z,z+26,3.6,2.8,8,BLACK);cyl(xx,yy,z+26,z+32,3.0,0,8,BLACK)}land('PortaoNegro',32)}
  // Montanha da Perdição: cratera de lava e fluxo
  {let bx=P.MontePerdicao[0],by=P.MontePerdicao[1],bh=-1;for(let dx=-14;dx<=14;dx+=2)for(let dy=-14;dy<=14;dy+=2){const h=g(bx+dx,by+dy);if(h>bh){bh=h}}
   let px=bx,py=by;for(let dx=-14;dx<=14;dx+=2)for(let dy=-14;dy<=14;dy+=2)if(g(bx+dx,by+dy)>=bh-0.01){px=bx+dx;py=by+dy}
   cyl(px,py,bh-4,bh+1,6.5,4.5,10,[0.20,0.10,0.07]);cyl(px,py,bh+0.6,bh+0.8,4.3,0,10,FIRE);
   for(let k=0;k<6;k++){const a=-1.0+k*0.08;const x0=px+Math.cos(a)*5,y0=py+Math.sin(a)*5;const x1=px+Math.cos(a)*16,y1=py+Math.sin(a)*16;
     quad([x0-0.6,y0,g(x0,y0)+0.6],[x0+0.6,y0,g(x0,y0)+0.6],[x1+0.4,y1,g(x1,y1)+0.4],[x1-0.4,y1,g(x1,y1)+0.4],FIRE)}land('MontePerdicao',8)}
  // Carn Dûm (Angmar)
  {const [x,y]=P.Angmar,z=g(x,y)-1;cyl(x,y,z,z+8,9,8,8,DARK);cyl(x,y,z+8,z+34,3.4,2.4,6,BLACK);cyl(x,y,z+34,z+42,2.6,0,6,BLACK);land('Angmar',42)}
  // Cirith Ungol
  {const p=P.CirithUngol;if(p){const [x,y]=p,z=g(x,y)-1;cyl(x,y,z,z+18,3,2.2,6,DARK);cyl(x,y,z+18,z+23,2.4,0,6,DARK)}}
  // Edoras: Meduseld dourado sobre a colina
  {const [x,y]=P.Edoras,z=g(x,y);cyl(x,y,z-3,z+3,10,7,12,[0.45,0.52,0.30]);box(x,y,6,2.6,z+3,z+7,WOOD,0.6,GOLD);for(let k=0;k<5;k++){const a=k*1.26;box(x+Math.cos(a)*8.5,y+Math.sin(a)*8.5,1.6,1.2,z,z+2.6,WOOD,a,[0.55,0.42,0.18])}land('Edoras',12)}
  // Valfenda: casas élficas no vale
  {const [x,y]=P.Valfenda,z=g(x,y);[[0,0,0.3],[6,3,1.2],[-5,4,2.1],[2,-6,0.9]].forEach(([dx,dy,r],k)=>box(x+dx,y+dy,2.6,1.6,z,z+3.2+k%2,[0.86,0.82,0.70],r,[0.55,0.35,0.22]));land('Valfenda',7)}
  // Condado: tocas de hobbit (portas redondas) e moinho
  {const [x,y]=P.Condado,z=g(x,y);for(let k=0;k<6;k++){const a=k*1.05,xx=x+Math.cos(a)*7,yy=y+Math.sin(a)*7;cyl(xx,yy,z-1,z+2.5,3,1.2,8,[0.36,0.55,0.24]);cyl(xx+Math.cos(a)*2.6,yy+Math.sin(a)*2.6,z,z+1.6,0.9,0.9,6,[0.15,0.35,0.15])}box(x+11,y-4,1.4,1.4,z,z+6,WOOD,0,[0.5,0.2,0.15]);land('Condado',4)}
  // Bri: casinhas
  {const p=P.Bri;if(p){const [x,y]=p,z=g(x,y);[[0,0],[4,2],[-3,3],[2,-4]].forEach(([dx,dy],k)=>box(x+dx,y+dy,1.8,1.3,z,z+2.2,[0.62,0.52,0.36],k,[0.35,0.22,0.14]));land('Bri',5)}}
  // Erebor: o portão na encosta
  {const [x,y]=P.Erebor;let z=g(x,y+12);box(x,y+12,3.5,0.8,z-1,z+6,[0.40,0.34,0.26],0);land('Erebor',8)}
  // árvores
  const n=TREES.length;for(let k=0;k<n;k++){const t=TREES[k],x=t[0],y=t[1],z=g(x,y);if(z>HS*EX*0.45)continue;const s=0.8+((k*7919)%100)/220,dark=0.62;
    const col=[t[2]*dark+0.02,t[3]*dark+0.05,t[4]*dark],trunk=[0.25,0.17,0.10];cyl(x,y,z-0.3,z+1.4*s,0.35*s,0.3*s,4,trunk);cyl(x,y,z+1.2*s,z+7.5*s,2.4*s,0,6,col,col)}
  return new Float32Array(M)}
/* ---- iniciar ---- */
async function init(stage){
  if(ok)return true;if(!supported())return false;
  cv=document.createElement('canvas');cv.id='m3Gl';stage.insertBefore(cv,stage.firstChild);
  gl=cv.getContext('webgl',{antialias:true,alpha:true,premultipliedAlpha:false})||cv.getContext('experimental-webgl');if(!gl){cv.remove();return false}
  cv.addEventListener('webglcontextlost',e=>{e.preventDefault();ok=false;document.dispatchEvent(new Event('atlas:relevo-perdido'))});
  uintOK=!!gl.getExtension('OES_element_index_uint');
  const [hm,lm,img]=await Promise.all([load(HM),load(LM),load(TEX)]);
  const c2=document.createElement('canvas');c2.width=hm.width;c2.height=hm.height;const x2=c2.getContext('2d');x2.drawImage(hm,0,0);const px=x2.getImageData(0,0,hm.width,hm.height).data;
  const FW=hm.width,FH=hm.height;const full=new Float32Array(FW*FH);for(let i=0;i<FW*FH;i++)full[i]=((px[i*4]*256+px[i*4+1])/65535*1.25-0.05)*HS;
  if(uintOK){GW=FW;GH=FH;heights=full}else{GW=FW>>1;GH=FH>>1;heights=new Float32Array(GW*GH);for(let j=0;j<GH;j++)for(let i=0;i<GW;i++)heights[j*GW+i]=full[(j*2)*FW+i*2]}
  const V=new Float32Array(GW*GH*3),dx=MW/(GW-1),dy=MH/(GH-1);
  for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const k=(j*GW+i)*3;V[k]=i*dx;V[k+1]=j*dy;V[k+2]=heights[j*GW+i]*EX}
  const I=uintOK?new Uint32Array((GW-1)*(GH-1)*6):new Uint16Array((GW-1)*(GH-1)*6);let m=0;
  for(let j=0;j<GH-1;j++)for(let i=0;i<GW-1;i++){const a=j*GW+i,b=a+1,c=a+GW,d=c+1;I[m++]=a;I[m++]=c;I[m++]=b;I[m++]=b;I[m++]=c;I[m++]=d}nIdx=m;
  pT=prog(VT,FT);pM=prog(VM,FM);
  bufT=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,bufT);gl.bufferData(gl.ARRAY_BUFFER,V,gl.STATIC_DRAW);
  ibT=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ibT);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,I,gl.STATIC_DRAW);
  const tex=(im,size)=>{const c=document.createElement('canvas');c.width=c.height=size;c.getContext('2d').drawImage(im,0,0,size,size);const t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,c);gl.generateMipmap(gl.TEXTURE_2D);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
    const ext=gl.getExtension('EXT_texture_filter_anisotropic')||gl.getExtension('WEBKIT_EXT_texture_filter_anisotropic');if(ext)gl.texParameterf(gl.TEXTURE_2D,ext.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(8,gl.getParameter(ext.MAX_TEXTURE_MAX_ANISOTROPY_EXT)));return t};
  const maxT=gl.getParameter(gl.MAX_TEXTURE_SIZE);texMap=tex(img,Math.min(2048,maxT));texLight=tex(lm,Math.min(1024,maxT));
  ok=true;gl.enable(gl.DEPTH_TEST);gl.clearColor(0,0,0,0);return true}
function setModels(P){if(!ok)return;const MV=buildModels(P);
  // laterais de maquete
  const W=[];const edge=[];for(let i=0;i<GW;i+=2)edge.push([i,0]);for(let j=0;j<GH;j+=2)edge.push([GW-1,j]);for(let i=GW-1;i>=0;i-=2)edge.push([i,GH-1]);for(let j=GH-1;j>=0;j-=2)edge.push([0,j]);edge.push([0,0]);
  const dx=MW/(GW-1),dy=MH/(GH-1);const before=M.length;
  for(let e=0;e<edge.length-1;e++){const [i0,j0]=edge[e],[i1,j1]=edge[e+1];const a=[i0*dx,j0*dy,hAt(i0,j0)*EX],b=[i1*dx,j1*dy,hAt(i1,j1)*EX];quad(a,b,[b[0],b[1],BASE],[a[0],a[1],BASE],[0.30,0.21,0.13])}
  const all=new Float32Array(M);bufM=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,bufM);gl.bufferData(gl.ARRAY_BUFFER,all,gl.STATIC_DRAW);nM=all.length/10}
/* ---- câmera ---- */
function camera(cam,W,H){const f=(H/2)/Math.tan(FOV/2),dist=f/cam.z,hr=cam.h*Math.PI/180,tr=cam.t*Math.PI/180;
  const U=[-Math.sin(hr),-Math.cos(hr)],R=[Math.cos(hr),-Math.sin(hr),0];const st=Math.sin(tr),ct=Math.cos(tr);
  const T=[cam.x,cam.y,height(cam.x,cam.y)*EX];const F=[U[0]*st,U[1]*st,-ct],Up=[U[0]*ct,U[1]*ct,st];
  const C=[T[0]-F[0]*dist,T[1]-F[1]*dist,T[2]-F[2]*dist];return {f,dist,R,Up,F,C}}
const NEAR=2,FAR=40000,A=(FAR+NEAR)/(FAR-NEAR),B=-2*FAR*NEAR/(FAR-NEAR);
function uni(p,k,W,H){gl.uniform3fv(p.u.C,k.C);gl.uniform3fv(p.u.R,k.R);gl.uniform3fv(p.u.Up,k.Up);gl.uniform3fv(p.u.F,k.F);gl.uniform1f(p.u.f,k.f);gl.uniform1f(p.u.W,W);gl.uniform1f(p.u.H,H);gl.uniform1f(p.u.A,A);gl.uniform1f(p.u.B,B);
  gl.uniform1f(p.u.fog0,k.dist*1.15);gl.uniform1f(p.u.fog1,k.dist*4.5)}
function draw(cam,W,H){if(!ok)return;const dpr=Math.min(2,window.devicePixelRatio||1),w=Math.round(W*dpr),h=Math.round(H*dpr);if(cv.width!==w||cv.height!==h){cv.width=w;cv.height=h}
  gl.viewport(0,0,w,h);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);const k=camera(cam,W,H);
  gl.useProgram(pT);uni(pT,k,W,H);gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,texMap);gl.uniform1i(pT.u.tMap,0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,texLight);gl.uniform1i(pT.u.tLight,1);
  gl.bindBuffer(gl.ARRAY_BUFFER,bufT);const ap=gl.getAttribLocation(pT,'p');gl.enableVertexAttribArray(ap);gl.vertexAttribPointer(ap,3,gl.FLOAT,false,12,0);
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ibT);gl.drawElements(gl.TRIANGLES,nIdx,uintOK?gl.UNSIGNED_INT:gl.UNSIGNED_SHORT,0);gl.disableVertexAttribArray(ap);
  if(bufM){gl.useProgram(pM);uni(pM,k,W,H);gl.uniform3fv(pM.u.sun,SUN);gl.bindBuffer(gl.ARRAY_BUFFER,bufM);const L=['p','n','c'].map(n=>gl.getAttribLocation(pM,n));
    L.forEach(l=>gl.enableVertexAttribArray(l));gl.vertexAttribPointer(L[0],3,gl.FLOAT,false,40,0);gl.vertexAttribPointer(L[1],3,gl.FLOAT,false,40,12);gl.vertexAttribPointer(L[2],4,gl.FLOAT,false,40,24);
    gl.drawArrays(gl.TRIANGLES,0,nM);L.forEach(l=>gl.disableVertexAttribArray(l))}}
function topAt(x,y){for(const [lx,ly,t] of LAND)if(Math.hypot(lx-x,ly-y)<3)return t;return 0}
function project(x,y,cam,W,H){const k=camera(cam,W,H);const p=[x,y,height(x,y)*EX+topAt(x,y)];const r=[p[0]-k.C[0],p[1]-k.C[1],p[2]-k.C[2]];
  const xc=r[0]*k.R[0]+r[1]*k.R[1]+r[2]*k.R[2],yc=r[0]*k.Up[0]+r[1]*k.Up[1]+r[2]*k.Up[2],zc=r[0]*k.F[0]+r[1]*k.F[1]+r[2]*k.F[2];
  if(zc<NEAR)return [-9999,-9999,0,0];return [W/2+xc*k.f/zc,H*0.58-yc*k.f/zc,1,Math.max(-1900,Math.min(1900,1900-zc*0.3))]}
function show(on){if(cv)cv.style.display=on?'':'none'}
return {supported,init,draw,project,height:(x,y)=>height(x,y)*EX,setModels,show,TEX,get ok(){return ok},set exaggeration(v){}};
})();
