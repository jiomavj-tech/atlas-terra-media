import json,re
INDEX='/home/claude/atlas-terra-media/index.html'
D=json.load(open('/tmp/claude-0/fam/family.json'))
RACE={'Hobbit':'Hobbit','Hobbits':'Hobbit','Man':'Homem','Men':'Homem','Woman':'Mulher','Elf':'Elfo','Elves':'Elfo','Dwarf':'Anão','Dwarves':'Anão','Ainur':'Ainur','Vala':'Vala','Valar':'Vala','Maia':'Maia','Maiar':'Maia',
'Half-elven':'Meio-elfo','Half-elf':'Meio-elfo','Ent':'Ent','Orc':'Orc','Orcs':'Orc','Dragon':'Dragão','Spider':'Aranha','Noldo':'Elfo (Noldor)','Noldor':'Elfo (Noldor)','Sinda':'Elfo (Sindar)','Sindar':'Elfo (Sindar)',
'Vanya':'Elfo (Vanyar)','Teler':'Elfo (Teleri)','Nando':'Elfo (Nandor)','Silvan':'Elfo (silvestre)','Edain':'Homem (Edain)','Dunedain':'Homem (Dúnedain)','Dúnedain':'Homem (Dúnedain)','Numenorean':'Homem (Númenor)',
'Gondorian':'Homem (Gondor)','Rohirrim':'Homem (Rohan)','Rohirric':'Homem (Rohan)','Beorning':'Homem (beornida)','Drúedain':'Homem (Drúedain)','Easterling':'Homem (Lestense)','Haradrim':'Homem (Harad)'}
for x in D['n']:
    r=x[1] or '';x[1]=RACE.get(r,RACE.get(r.capitalize(),r))
s=open(INDEX,encoding='utf-8').read()
DATA='<script id="atlas-familias-dados">/* Parentescos: Arda-Maps (kwoxer, CC BY-NC-SA 4.0) e Middle-Earth Genealogy Project (RobSis, CC BY-SA 4.0), combinados e revisados para o Atlas. n=[nome,povo,sexo,ficha]; p=[filho,pai/mãe]; s=[cônjuges]; b=[irmãos] */window.ATLAS_FAMILY='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';</script>'
CSS="""<style id="atlas-familias-css">
.fam-box{margin:14px 0;padding:12px;border:1px solid #51654b;border-radius:12px;background:rgba(15,35,28,.55)}
.fam-box h4{margin:0 0 8px;font-size:16px}.fam-row{margin:6px 0;display:flex;flex-wrap:wrap;gap:6px;align-items:center}.fam-row>b{min-width:70px;font-size:13px;color:#d4b16a}
.fam-chip{border:1px solid #6d7f61;border-radius:999px;padding:4px 10px;background:#172d24;color:#f1e8cf;font-size:13px;cursor:default}
button.fam-chip{cursor:pointer;background:#24453a;border-color:#d4b16a}.fam-box .fam-src{display:block;margin-top:8px;color:#b9c3ad;font-size:12px}
.fam-auto{display:none;margin:10px 0}.fam-auto.on{display:block}.fam-auto input{width:min(420px,100%)}
.fam-tree{display:grid;gap:10px;padding:8px 2px}.fam-gen{display:grid;gap:6px}.fam-gen>small{color:#d4b16a;font-weight:700;letter-spacing:.03em}
.fam-gen>div{display:flex;flex-wrap:wrap;gap:8px}.fam-card{border:1px solid #6d7f61;border-radius:10px;background:#172d24;color:#f1e8cf;padding:7px 10px;text-align:left;min-width:120px;cursor:pointer}
.fam-card small{display:block;color:#b9c3ad;font-size:11px}.fam-card.me{border:2px solid #d4b16a;background:#2b4a3a}.fam-card.sp{border-style:dashed}.fam-card.atl::after{content:' 📖';font-size:11px}
#familyGraph.fam-hide>*:not(.fam-tree){display:none}
</style>"""
JS=r"""<script id="atlas-familias-script">
/* v12.6: famílias para qualquer personagem (dados combinados de duas genealogias abertas) */
(()=>{'use strict';const F=window.ATLAS_FAMILY;if(!F)return;
const N=F.n,par={},chi={},spo={},sib={};const add=(o,a,b)=>{(o[a]=o[a]||new Set()).add(b)};
F.p.forEach(([c,p])=>{add(par,c,p);add(chi,p,c)});F.s.forEach(([a,b])=>{add(spo,a,b);add(spo,b,a)});F.b.forEach(([a,b])=>{add(sib,a,b);add(sib,b,a)});
for(const c in par)for(const p of par[c])for(const s of chi[p]||[])if(+s!==+c)add(sib,+c,s);
const byKey={};N.forEach((x,i)=>{if(x[3])byKey[x[3]]=i});const L=i=>[...(i||[])].map(Number).sort((a,b)=>N[a][0].localeCompare(N[b][0],'pt-BR'));
const openPerson=i=>document.dispatchEvent(new CustomEvent('atlas:open-person',{detail:{name:N[i][0]}}));
function chip(i){const atl=!!N[i][3];const e=document.createElement(atl?'button':'span');e.className='fam-chip';e.textContent=N[i][0];if(atl){e.type='button';e.title='Abrir a ficha';e.onclick=()=>openPerson(i)}return e}
window.atlasFamilyOf=key=>byKey[key];
window.atlasFamilyBlock=p=>{const i=byKey[p&&p.key];if(i===undefined)return null;const box=document.createElement('div');box.className='fam-box';
  const h=document.createElement('h4');h.textContent='🌳 Família';box.append(h);let any=false;
  for(const [lab,set] of [['Pais',par[i]],['Cônjuge',spo[i]],['Filhos',chi[i]],['Irmãos',sib[i]]]){const l=L(set);if(!l.length)continue;any=true;const r=document.createElement('div');r.className='fam-row';const b=document.createElement('b');b.textContent=lab;r.append(b,...l.map(chip));box.append(r)}
  if(!any)return null;const t=document.createElement('button');t.type='button';t.className='atlas-v50-link';t.textContent='🌳 Ver árvore completa';t.onclick=()=>window.atlasShowTree(i);box.append(t);
  const s=document.createElement('small');s.className='fam-src';s.textContent='Fontes: Arda-Maps e Middle-Earth Genealogy Project (licenças Creative Commons). 📖 = tem ficha no Atlas.';box.append(s);return box};
/* --- árvore automática na seção Genealogias --- */
const sel=document.getElementById('familySelect'),host=document.getElementById('familyGraph'),detail=document.getElementById('familyDetail');if(!sel||!host)return;
const opt=document.createElement('option');opt.value='auto';opt.textContent='🔎 Qualquer personagem (árvore automática)';sel.prepend(opt);sel.value=sel.options[1].value;
const tools=document.querySelector('.family-tools');const auto=document.createElement('div');auto.className='fam-auto';
auto.innerHTML='<label>Personagem <input id="famAutoInput" type="search" list="famAutoList" placeholder="Digite um nome: Aragorn, Frodo, Lúthien…" autocomplete="off"></label><datalist id="famAutoList"></datalist>';tools.after(auto);
const inp=auto.querySelector('input'),dl=auto.querySelector('datalist');N.map(x=>x[0]).sort((a,b)=>a.localeCompare(b,'pt-BR')).forEach(n=>{const o=document.createElement('option');o.value=n;dl.append(o)});
const norm=t=>String(t).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().trim();
function card(i,cls){const b=document.createElement('button');b.type='button';b.className='fam-card '+(cls||'')+(N[i][3]?' atl':'');b.textContent=N[i][0];const sm=document.createElement('small');sm.textContent=[N[i][1],N[i][2]==='F'?'♀':N[i][2]==='M'?'♂':''].filter(Boolean).join(' · ');b.append(sm);b.onclick=()=>cls==='me'&&N[i][3]?openPerson(i):tree(i);return b}
function gen(title,list,cls){if(!list.length)return null;const g=document.createElement('div');g.className='fam-gen';const s=document.createElement('small');s.textContent=title;const d=document.createElement('div');list.forEach(i=>d.append(card(i,cls)));g.append(s,d);return g}
function tree(i){const t=document.createElement('div');t.className='fam-tree';const P=L(par[i]),GP=L(new Set(P.flatMap(p=>[...(par[p]||[])]))),C=L(chi[i]),GC=L(new Set(C.flatMap(c=>[...(chi[c]||[])])));
  [gen('Avós',GP),gen('Pais',P),gen('Irmãos',L(sib[i])),(()=>{const g=gen('Personagem e cônjuge',[i]);L(spo[i]).forEach(s=>g.lastChild.append(card(s,'sp')));g.querySelector('.fam-card').classList.add('me');return g})(),gen('Filhos',C),gen('Netos',GC)].filter(Boolean).forEach(x=>t.append(x));
  host.classList.add('fam-hide');host.querySelector('.fam-tree')?.remove();host.append(t);inp.value=N[i][0];
  detail.textContent=N[i][0]+(N[i][3]?' — tem ficha no Atlas: toque no nome destacado para abrir.':'')+' Toque em outro parente para centralizar nele. Fontes: Arda-Maps e Middle-Earth Genealogy Project.'}
function pick(){const q=norm(inp.value);if(!q)return;let i=N.findIndex(x=>norm(x[0])===q);if(i<0)i=N.findIndex(x=>norm(x[0]).startsWith(q));if(i>=0)tree(i)}
inp.addEventListener('change',pick);inp.addEventListener('keydown',e=>{if(e.key==='Enter')pick()});
sel.addEventListener('change',e=>{if(sel.value==='auto'){e.stopImmediatePropagation();auto.classList.add('on');if(!host.querySelector('.fam-tree'))tree(byKey.Aragorn??0)}else{auto.classList.remove('on');host.classList.remove('fam-hide');host.querySelector('.fam-tree')?.remove()}},true);
window.atlasShowTree=i=>{const s=document.getElementById('atlasUxSelect');if(s){s.value='atlas-genealogia';s.dispatchEvent(new Event('change'))}sel.value='auto';sel.dispatchEvent(new Event('change'));tree(i);setTimeout(()=>document.getElementById('atlas-genealogia')?.scrollIntoView({block:'start'}),60)};
})();
</script>"""
CRED="""<div class="fam-box" id="atlasCreditosDados"><h4>📚 Dados abertos usados no Atlas</h4>
<p><b>Parentescos</b> (fichas e "Árvore automática" das Genealogias): combinados e revisados a partir de
<a href="https://github.com/kwoxer/Arda-Maps" target="_blank" rel="noopener">Arda-Maps</a> (kwoxer e colaboradores, licença
<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>) e
<a href="https://github.com/RobSis/middle-earth-genealogy-project" target="_blank" rel="noopener">Middle-Earth Genealogy Project</a> (RobSis, licença
<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br" target="_blank" rel="noopener">CC BY-SA 4.0</a>).
Os parentescos derivados desses dados são compartilhados sob a mesma licença CC BY-NC-SA 4.0. Algumas ligações das fontes foram corrigidas ou retiradas por conflito com os textos de Tolkien.</p>
<small class="fam-src">O Atlas é um projeto pessoal, sem fins lucrativos, e não tem ligação com a Tolkien Estate nem com a Middle-earth Enterprises.</small></div>"""
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
for sid in ('atlas-familias-dados','atlas-familias-script','atlas-familias-css'):
    if f'id="{sid}"' in s: raise SystemExit('já embutido: '+sid)
i=s.index('<section id="atlas-genealogia"');j=s.index('</script>',i)+9
s=s[:j]+'\n'+CSS+DATA+JS+s[j:]
rep('<p class="source-warning">Fontes primárias: textos de J. R. R. Tolkien,',CRED+'<p class="source-warning">Fontes primárias: textos de J. R. R. Tolkien,')
# ficha: bloco da família antes da nota
rep("content.append(h,intro,dl,note,map,document.createTextNode(' '),teia);","content.append(h,intro,dl);{const fb=window.atlasFamilyBlock&&window.atlasFamilyBlock(p);if(fb)content.append(fb)}content.append(note,map,document.createTextNode(' '),teia);")
open(INDEX,'w',encoding='utf-8').write(s);print('ok',round(len(s.encode())/1e6,2),'MB')
