import re
f='/home/claude/atlas-terra-media/index.html';s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s;assert s.count(a)==cnt,(a[:60],s.count(a));s=s.replace(a,b)
rep("return {details:()=>DEFS.map(","return {projector:(cam,W,H)=>{const k=camera(cam,W,H);return (x,y)=>{const r0=x-k.C[0],r1=y-k.C[1],r2=height(x,y)*EX-k.C[2];const zc=r0*k.F[0]+r1*k.F[1]+r2*k.F[2];if(zc<k.near)return [0,0,0];return [W/2+(r0*k.R[0]+r1*k.R[1]+r2*k.R[2])*k.f/zc,H*0.58-(r0*k.Up[0]+r1*k.Up[1]+r2*k.Up[2])*k.f/zc,1]}},details:()=>DEFS.map(")
rep("window.AtlasRelevo.draw(cam,W,H);placeRelief();if(tour)drawRoute();","window.AtlasRelevo.draw(cam,W,H);window.AtlasReinos&&window.AtlasReinos.draw(cam,W,H,true,zFit);placeRelief();if(tour)drawRoute();")
rep("plane.style.setProperty('--sw',(3.2/cam.z).toFixed(3));\n  compass.firstChild.style.transform=`rotate(${cam.h}deg)`}","plane.style.setProperty('--sw',(3.2/cam.z).toFixed(3));window.AtlasReinos&&window.AtlasReinos.draw(cam,W,H,false,zFit);\n  compass.firstChild.style.transform=`rotate(${cam.h}deg)`}")
rep("cam:()=>({...cam}),startTour,","cam:()=>({...cam}),render:()=>render(),zFit:()=>zFit,startTour,")
rep('<button type="button" id="m3BtnArda">🌐 Ver Arda</button></div>','<button type="button" id="m3BtnArda">🌐 Ver Arda</button><button type="button" id="m3BtnReinos" aria-pressed="false">👑 Reinos e Eras</button></div>')
css=r'''<style id="atlas-reinos-css">
#m3Reinos{position:absolute;left:0;top:0;pointer-events:none;display:none}
#m3RealmBox{position:absolute;left:8px;top:8px;right:62px;max-height:calc(100% - 50px);overflow:auto;z-index:3;background:#0f2621ee;border:1px solid #8c784b;border-radius:12px;padding:8px;color:#f1e2bb;font-size:13px;box-shadow:0 4px 18px #0008}
#m3RealmBox .rb-eras{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}
#m3RealmBox .rb-eras button{flex:1 1 auto;min-height:34px;padding:5px 8px;font-size:12.5px;background:#18372e;border:1px solid #8c784b;border-radius:9px;color:#f1e2bb}
#m3RealmBox .rb-eras button[aria-pressed="true"]{background:#d4b16a;color:#102b25;font-weight:700}
#m3RealmBox .rb-chips{display:flex;flex-wrap:wrap;gap:4px}
#m3RealmBox .rb-chips button{min-height:30px;padding:3px 9px;font-size:12.5px;background:#173129;border:1px solid #5c5236;border-radius:15px;color:#f1e2bb;display:inline-flex;align-items:center;gap:5px}
#m3RealmBox .rb-chips button.on{border-color:#e8d39a;background:#2a4a3e;font-weight:700}
#m3RealmBox .rb-chips i{width:11px;height:11px;border-radius:50%;display:inline-block;border:1px solid #fff8}
#m3RealmBox .rb-card{position:relative;margin-top:8px;padding:8px 10px;background:#162f28;border-radius:10px;border:1px solid #5c5236}
#m3RealmBox .rb-card h4{margin:0 26px 2px 0;font-size:16px;color:#f6dfa0}
#m3RealmBox .rb-card small{color:#c9b98e}
#m3RealmBox .rb-card p{margin:6px 0;line-height:1.4}
#m3RealmBox .rb-card dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:3px 8px}
#m3RealmBox .rb-card dt{color:#d4b16a;font-weight:700}#m3RealmBox .rb-card dd{margin:0}
#m3RealmBox .rb-x{position:absolute;right:6px;top:6px;width:28px;height:28px;min-height:0!important;padding:0!important;border-radius:50%;background:#18372e;border:1px solid #8c784b;color:#f1e2bb}
#m3RealmBox small.rb-src{display:block;margin-top:6px;font-size:11px;color:#a99d7e}
</style>'''
dados=open('/tmp/claude-0/realm/build/dados.js',encoding='utf-8').read()
js=open('/tmp/claude-0/realm/build/reinos.js',encoding='utf-8').read()
anchor="relief:v=>setRelief(v),reliefOn:()=>reliefOn,"
k=s.index(anchor);k=s.index('</script>',k)+len('</script>')
s=s[:k]+'\n'+css+'\n<script id="atlas-reinos-dados">\n'+dados+'\n</script>\n<script id="atlas-reinos-script">\n'+js+'\n</script>'+s[k:]
cred='<small class="fam-src">O Atlas é um projeto pessoal, sem fins lucrativos'
rep(cred,'''<p><b>Reinos e Eras</b> (botão "👑 Reinos e Eras" no Mapa): fichas dos reinos traduzidas e adaptadas do
<a href="https://github.com/grot666/middle-earth-atlas" target="_blank" rel="noopener">Middle-earth Interactive Atlas</a> (Middle-earth Interactive Atlas contributors, licença MIT). As fronteiras foram redesenhadas à mão sobre o mapa do Atlas e são aproximadas.</p>
'''+cred)
s=s.replace("window.ATLAS_VERSAO='12.6'","window.ATLAS_VERSAO='12.7'")
open(f,'w',encoding='utf-8').write(s);print('ok')
