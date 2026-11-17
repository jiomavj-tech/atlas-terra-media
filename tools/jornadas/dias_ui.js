(()=>{'use strict';
const stage=document.getElementById('m3Stage'),plane=document.getElementById('m3Plane'),btn=document.getElementById('m3BtnDias');if(!stage||!plane||!btn)return;
const DATA=window.ATLAS_DIAS;if(!DATA)return;
let on=false,modo='guerra',dia=DATA.guerra.inicio,timer=0,last=null;
const cv=document.createElement('canvas');cv.id='m3Dias';cv.setAttribute('aria-hidden','true');
const svg=document.getElementById('m3Svg');svg?plane.insertBefore(cv,svg):plane.appendChild(cv);
const ctx=cv.getContext('2d');
const box=document.createElement('div');box.id='m3DiaBox';box.className='m3-dia';box.hidden=true;stage.appendChild(box);
['pointerdown','pointermove','pointerup','wheel','touchstart','touchmove','click'].forEach(t=>box.addEventListener(t,e=>e.stopPropagation(),{passive:true}));
const M=()=>DATA[modo];
/* posição de um grupo num dia: interpola entre as paradas conhecidas */
function pos(t,d){const p=t.pts;if(d<p[0][0]||d>p[p.length-1][0])return null;let lab=t.nome,i=0;
  for(;i<p.length;i++){if(p[i][3]&&p[i][0]<=d)lab=p[i][3];if(p[i][0]>=d)break}
  let k=p.length-1;while(k>0&&p[k][0]>d)k--;               /* última parada até hoje */
  const a=p[k],b=p[Math.min(p.length-1,k+1)];
  if(a[0]===d||b[0]===a[0])return {x:a[1],y:a[2],lab,k};
  const f=(d-a[0])/(b[0]-a[0]);return {x:a[1]+(b[1]-a[1])*f,y:a[2]+(b[2]-a[2])*f,lab,k}}
function evento(d){return M().ev[d]||''}
function panel(){const m=M(),n=m.cal.length;
  const ativos=m.tracks.map(t=>[t,pos(t,dia)]).filter(x=>x[1]);
  box.innerHTML=`<div class="rb-eras" role="group" aria-label="Escolher a história">${Object.entries(DATA).map(([k,v])=>`<button type="button" data-m="${k}" aria-pressed="${k===modo}">${v.nome}</button>`).join('')}</div>
  <div class="dd-top"><button type="button" class="dd-prev" aria-label="Dia anterior">◀</button><strong>${m.cal[dia]}</strong><button type="button" class="dd-next" aria-label="Próximo dia">▶</button><button type="button" class="dd-play" aria-pressed="${!!timer}">${timer?'⏸ Pausar':'▶ Reproduzir'}</button></div>
  <input type="range" min="0" max="${n-1}" value="${dia}" aria-label="Escolher o dia">
  <div class="rb-chips">${ativos.map(([t,q])=>`<button type="button" data-t="${m.tracks.indexOf(t)}"><i style="background:${t.cor}"></i>${t.ic} ${q.lab}</button>`).join('')||'<small>Ninguém em viagem neste dia.</small>'}</div>
  <p class="dd-ev">${evento(dia)||'<span>Sem acontecimento registrado neste dia: a viagem continua.</span>'}</p><small class="rb-src">${m.nota}</small>`;
  box.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{stop();modo=b.dataset.m;dia=M().inicio;panel();fit()});
  const r=box.querySelector('input');r.oninput=()=>{stop();dia=+r.value;upd()};
  box.querySelector('.dd-prev').onclick=()=>{stop();dia=Math.max(0,dia-1);upd()};
  box.querySelector('.dd-next').onclick=()=>{stop();dia=Math.min(M().cal.length-1,dia+1);upd()};
  box.querySelector('.dd-play').onclick=()=>{if(timer){stop();panel()}else play()};
  box.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{const t=M().tracks[+b.dataset.t],q=pos(t,dia),A=window.AtlasMapa3D;if(q&&A&&A.fly)A.fly({x:q.x,y:q.y-12,z:A.zFit()*3,t:50},1000)})}
function upd(){panel();redraw()}
function play(){if(dia>=M().cal.length-1)dia=M().inicio;timer=setInterval(()=>{if(dia>=M().cal.length-1){stop();panel();return}dia++;upd()},1100);panel()}
function stop(){clearInterval(timer);timer=0}
function fit(){const A=window.AtlasMapa3D;if(!A||!A.fly)return;let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;for(const t of M().tracks)for(const p of t.pts){x0=Math.min(x0,p[1]);x1=Math.max(x1,p[1]);y0=Math.min(y0,p[2]);y1=Math.max(y1,p[2])}
  const s=Math.max(x1-x0,y1-y0);A.fly({x:(x0+x1)/2,y:(y0+y1)/2-s*0.15,z:A.zFit()*Math.max(1.1,Math.min(4,820/s/2.2)),t:44,h:0},1100)}
function setOn(v){on=v;if(!on)stop();btn.setAttribute('aria-pressed',String(on));box.hidden=!on;cv.style.display=on?'block':'none';
  if(on){if(window.AtlasReinos&&window.AtlasReinos.isOn())window.AtlasReinos.setOn(false);panel();fit()}redraw()}
btn.onclick=()=>setOn(!on);
function redraw(){const A=window.AtlasMapa3D;if(A&&A.render)A.render();else if(last)draw(...last)}
function draw(cam,W,H,relief){last=[cam,W,H,relief];if(!on)return;
  const R=window.AtlasRelevo,useR=relief&&R&&R.projector,dpr=Math.min(1.5,window.devicePixelRatio||1),cw=useR?W:984,ch=useR?H:877;
  if(cv.width!==Math.round(cw*dpr)||cv.height!==Math.round(ch*dpr)){cv.width=Math.round(cw*dpr);cv.height=Math.round(ch*dpr)}
  cv.style.width=cw+'px';cv.style.height=ch+'px';ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,cw,ch);
  const pj=useR?R.projector(cam,W,H):(x,y)=>[x,y,1],k=useR?1:1/Math.max(.35,Math.min(3,cam.z));
  /* adensa cada trecho para o traço acompanhar o relevo */
  const line=(pts)=>{ctx.beginPath();let n=0;for(let i=0;i<pts.length;i++){const a=pts[i],b=pts[i+1]||a,m=b===a?1:Math.max(1,Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/4));
      for(let j=0;j<m;j++){const q=pj(a[0]+(b[0]-a[0])*j/m,a[1]+(b[1]-a[1])*j/m);if(!q[2]){n=0;continue}n++?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1])}}ctx.stroke()};
  const marks=[];
  for(const t of M().tracks){const P=t.pts.map(p=>[p[1],p[2]]),q=pos(t,dia);
    ctx.lineCap='round';ctx.lineJoin='round';
    ctx.setLineDash([4*k,5*k]);ctx.lineWidth=1.6*k;ctx.strokeStyle='rgba(255,250,235,.45)';line(P);ctx.setLineDash([]);
    let feito=null;if(q)feito=P.slice(0,q.k+1).concat([[q.x,q.y]]);else if(dia>t.pts[t.pts.length-1][0])feito=P;
    if(feito){ctx.lineWidth=5*k;ctx.strokeStyle='rgba(20,16,10,.55)';line(feito);ctx.lineWidth=3*k;ctx.strokeStyle=t.cor;line(feito)}
    if(q){const s=pj(q.x,q.y);if(s[2])marks.push([t,q,s])}}
  ctx.textAlign='center';ctx.textBaseline='middle';const r=useR?13:Math.max(4,Math.min(26,13/Math.max(.4,cam.z)));
  marks.forEach(([t,q,s],i)=>{const dy=marks.slice(0,i).filter(m=>Math.hypot(m[2][0]-s[0],m[2][1]-s[1])<r*2).length*r*2.3;const y=s[1]-dy;
    ctx.beginPath();ctx.arc(s[0],y,r,0,Math.PI*2);ctx.fillStyle='rgba(16,30,26,.92)';ctx.fill();ctx.lineWidth=r*.22;ctx.strokeStyle=t.cor;ctx.stroke();
    ctx.font=`${r*1.05}px sans-serif`;ctx.fillStyle='#fff';ctx.fillText(t.ic,s[0],y+r*.05);
    ctx.font=`700 ${r*.95}px Georgia,serif`;ctx.lineWidth=r*.3;ctx.strokeStyle='rgba(12,14,12,.9)';ctx.textAlign='left';ctx.strokeText(q.lab,s[0]+r*1.25,y);ctx.fillStyle='#fbefc8';ctx.fillText(q.lab,s[0]+r*1.25,y);ctx.textAlign='center'})}
window.AtlasDias={draw,setOn,isOn:()=>on};
})();
