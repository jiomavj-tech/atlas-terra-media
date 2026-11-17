(()=>{'use strict';
const sec=document.getElementById('calendario-condado');if(!sec)return;
const MES=['Afteryule','Solmath','Rethe','Astron','Thrimidge','Forelithe','Afterlithe','Wedmath','Halimath','Winterfilth','Blotmath','Foreyule'];
const MNOS=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
const SEM=['Sterday','Sunday','Monday','Trewsday','Hevensday','Mersday','Highday'],SEMPT=['das Estrelas','do Sol','da Lua','das Duas Árvores','dos Céus','do Mar','dos Valar'];
const bis=a=>a%4===0&&a%100!==0;
/* monta o ano: lista de dias {t:'m'|'e', m, d, nome, sem} */
function ano(a){const L=[];const add=(o)=>L.push(o);add({t:'e',k:'2yule',nome:'2º Yule'});
  for(let m=0;m<12;m++){for(let d=1;d<=30;d++)add({t:'m',m,d});
    if(m===5){add({t:'e',k:'1lithe',nome:'1º Lithe'});add({t:'e',k:'meio',nome:'Meio-do-Ano',sw:1});if(bis(a))add({t:'e',k:'over',nome:'Overlithe',sw:1});add({t:'e',k:'2lithe',nome:'2º Lithe'})}}
  add({t:'e',k:'1yule',nome:'1º Yule'});let w=0;for(const o of L){if(o.sw)o.sem=-1;else o.sem=(w++)%7}return L}
const nomeDia=o=>o.t==='m'?`${o.d} de ${MES[o.m]}`:o.nome;
const semTxt=o=>o.sem<0?'sem dia da semana':`${SEM[o.sem]} (dia ${SEMPT[o.sem]})`;
/* nossa data ≈ índice num ano comum do Condado: 1º de janeiro = 9 de Afteryule */
function nossaParaIdx(dt){const y=dt.getFullYear(),j=Date.UTC(y,0,1);let n=Math.round((Date.UTC(y,dt.getMonth(),dt.getDate())-j)/864e5);
  const lp=(y%4===0&&y%100!==0)||y%400===0;if(lp&&n>=59)n--;return (n+9)%365}
function idxComum(o){const L=ano(1);return L.findIndex(x=>x.t===o.t&&(o.t==='m'?x.m===o.m&&x.d===o.d:x.k===(o.k==='over'?'meio':o.k)))}
function idxParaNossa(i){const d=new Date(Date.UTC(2001,0,1)+(i-9)*864e5);return `${d.getUTCDate()} de ${MNOS[d.getUTCMonth()]}`}
/* acontecimentos: os dias da jornada (Dia a dia) e datas fixas */
const EV={};const put=(a,key,txt,go)=>{(EV[a+'|'+key]=EV[a+'|'+key]||[]).push({txt,go})};
const keyOf=o=>o.t==='m'?o.m+'-'+o.d:o.k;
const D=window.ATLAS_DIAS;
if(D)for(const [modo,M] of Object.entries(D))M.cal.forEach((lab,i)=>{const tx=M.ev[i];if(!tx)return;let a,k,m;
  if(m=lab.match(/^(\d+) de (\S+) de (\d+)$/)){a=+m[3]-1600;k=MNOS.indexOf(m[2])+'-'+m[1]}
  else if(m=lab.match(/^1º Yule.*?(\d{4})/)){a=+m[1]-1600;k='1yule'}else if(m=lab.match(/^2º Yule.*?(\d{4})/)){a=+m[1]-1600;k='2yule'}
  else if(m=lab.match(/^1º Lithe de (\d+)/)){a=+m[1]-1600;k='1lithe'}else if(m=lab.match(/^Meio-do-Ano de (\d+)/)){a=+m[1]-1600;k='meio'}else if(m=lab.match(/^2º Lithe de (\d+)/)){a=+m[1]-1600;k='2lithe'}
  if(a)put(a,k,tx,[modo,i])});
put(1290,'8-22','Nasce Bilbo Bolseiro, em 22 de Halimath.');put(1368,'8-22','Nasce Frodo Bolseiro, no mesmo dia de aniversário de Bilbo.');
put(1401,'8-22','A Festa de Aniversário de Bilbo (111 anos) e de Frodo (33): Bilbo desaparece com o Anel e deixa o Condado.');
const anual={'8-22':'Aniversário de Bilbo e de Frodo.','meio':'Meio-do-Ano: festa no Condado, nos dias do Lithe.','over':'Overlithe: dia extra de festa, só nos anos bissextos.','2yule':'Ano-novo no Condado.'};
const $=id=>document.getElementById(id);
const nossa=$('ccNossa'),nossaOut=$('ccNossaOut'),inAno=$('ccAno'),conta=$('ccConta'),grade=$('ccGrade'),info=$('ccInfo'),anoOut=$('ccAnoOut');
const hoje=new Date();nossa.value=`${hoje.getFullYear()}-${String(hoje.getMonth()+1).padStart(2,'0')}-${String(hoje.getDate()).padStart(2,'0')}`;
function mostraNossa(){const v=nossa.value.split('-').map(Number);if(v.length<3||!v[0]){nossaOut.textContent='';return}const o=ano(1)[nossaParaIdx(new Date(v[0],v[1]-1,v[2]))];
  nossaOut.innerHTML=`<b>${nomeDia(o)}</b> — ${semTxt(o)}<small>No Condado, as datas ficavam uns 10 dias à frente das nossas. Conversão aproximada (Apêndice D).</small>`}
nossa.addEventListener('input',mostraNossa);mostraNossa();
function anoSR(){const n=+inAno.value||1;return conta.value==='TA'?n-1600:n}
function abreMapa(go){const s=document.getElementById('atlasUxSelect');if(s){s.value='mapas-originais';s.dispatchEvent(new Event('change'))}
  let n=0;const t=setInterval(()=>{if(window.AtlasDias&&window.AtlasDias.openAt&&document.body.dataset.view==='mapas-originais'){clearInterval(t);setTimeout(()=>window.AtlasDias.openAt(go[0],go[1]),400)}else if(++n>40)clearInterval(t)},150)}
function info1(o,a){const evs=(EV[a+'|'+keyOf(o)]||[]).slice(),an=anual[keyOf(o)];
  const i=idxComum(o);let h=`<b>${nomeDia(o)} de ${a} C.C.</b> (T.E. ${a+1600}) — ${semTxt(o)}<br><small>≈ ${idxParaNossa(i)} no nosso calendário</small>`;
  if(evs.length)h+=evs.map(e=>`<p>${e.txt}</p>`).join('');else if(an)h+=`<p>${an}</p>`;
  info.innerHTML=h;const g=evs.find(e=>e.go);if(g){const b=document.createElement('button');b.type='button';b.textContent='🗺️ Ver este dia no mapa';b.onclick=()=>abreMapa(g.go);info.append(b)}}
function desenha(){const a=anoSR();if(a<1){anoOut.textContent='Antes do ano 1 do Condado (T.E. 1601) não há Contagem do Condado.';grade.innerHTML='';return}
  const L=ano(a),hi=nossaParaIdx(new Date());const hk=keyOf(ano(1)[hi]);
  anoOut.innerHTML=`<b>Ano ${a} do Condado</b> = ano ${a+1600} da Terceira Era${a>=1422?` (ano ${a-1421} da Quarta Era)`:''} · ${bis(a)?'bissexto: 366 dias, com Overlithe':'365 dias'}`;
  grade.innerHTML='';let box=null,g=null;const esp=[];
  const btn=(o)=>{const b=document.createElement('button');b.type='button';b.className='cc-d';b.textContent=o.t==='m'?o.d:o.nome;const k=keyOf(o);
    if(EV[a+'|'+k]||(k==='8-22'))b.classList.add('ev');if(k===hk)b.classList.add('hj');b.title=nomeDia(o)+' — '+semTxt(o);
    b.onclick=()=>{grade.querySelectorAll('.sel').forEach(x=>x.classList.remove('sel'));b.classList.add('sel');info1(o,a);info.scrollIntoView({block:'nearest',behavior:'smooth'})};return b};
  const mbox=(titulo,sub)=>{box=document.createElement('div');box.className='cc-m';box.innerHTML=`<h4>${titulo}<small>${sub}</small></h4>`;g=document.createElement('div');g.className='cc-g';
    SEM.forEach(s=>{const sp=document.createElement('span');sp.textContent=s.slice(0,3);g.append(sp)});box.append(g);grade.append(box)};
  let pend=[];
  for(const o of L){if(o.t==='e'){pend.push(o);continue}
    if(o.d===1){mbox(MES[o.m],`${o.m+1}º mês · ≈ ${MNOS[o.m]}`);if(pend.length){const sp=document.createElement('div');sp.className='cc-sp';pend.forEach(p=>sp.append(btn(p)));g.append(sp);pend=[]}
      for(let k=0;k<o.sem;k++)g.append(document.createElement('i'))}
    g.append(btn(o))}
  if(pend.length){const sp=document.createElement('div');sp.className='cc-sp';pend.forEach(p=>sp.append(btn(p)));g.append(sp)}}
inAno.addEventListener('input',desenha);conta.addEventListener('change',()=>{const n=+inAno.value||0;inAno.value=conta.value==='TA'?n+1600:n-1600;desenha()});
$('ccAtalho').addEventListener('change',e=>{if(!e.target.value)return;conta.value='SR';inAno.value=e.target.value;e.target.value='';desenha()});
desenha();
})();
