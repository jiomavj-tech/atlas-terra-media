f='/home/claude/atlas-terra-media/index.html';s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s;assert s.count(a)==1,(a[:70],s.count(a));s=s.replace(a,b)
rep('<button type="button" id="m3BtnReinos" aria-pressed="false">👑 Reinos e Eras</button>','<button type="button" id="m3BtnReinos" aria-pressed="false">👑 Reinos e Eras</button><button type="button" id="m3BtnDias" aria-pressed="false">📅 Dia a dia</button>')
rep("window.AtlasReinos&&window.AtlasReinos.draw(cam,W,H,true,zFit);","window.AtlasReinos&&window.AtlasReinos.draw(cam,W,H,true,zFit);window.AtlasDias&&window.AtlasDias.draw(cam,W,H,true);")
rep("window.AtlasReinos&&window.AtlasReinos.draw(cam,W,H,false,zFit);","window.AtlasReinos&&window.AtlasReinos.draw(cam,W,H,false,zFit);window.AtlasDias&&window.AtlasDias.draw(cam,W,H,false);")
rep("function setOn(v){on=v;btn.setAttribute('aria-pressed',String(on));box.hidden=!on;","function setOn(v){on=v;if(on&&window.AtlasDias&&window.AtlasDias.isOn())window.AtlasDias.setOn(false);btn.setAttribute('aria-pressed',String(on));box.hidden=!on;")
a=s.index('<style id="atlas-reinos-css">');b=s.index('</style>',a)
css=s[a+len('<style id="atlas-reinos-css">'):b].replace('#m3RealmBox','#m3DiaBox').replace('#m3Reinos{','#m3Dias{').replace('#m3Stage:has(#m3DiaBox','#m3Stage:has(#m3DiaBox')
css+='''#m3DiaBox .dd-top{display:flex;align-items:center;gap:5px;margin:2px 0}
#m3DiaBox .dd-top strong{flex:1;text-align:center;font-size:14px;color:#f6dfa0}
#m3DiaBox .dd-top button{min-height:32px;min-width:36px;padding:3px 8px;background:#18372e;border:1px solid #8c784b;border-radius:9px;color:#f1e2bb;font-size:13px}
#m3DiaBox .dd-top .dd-play[aria-pressed="true"]{background:#d4b16a;color:#102b25;font-weight:700}
#m3DiaBox input[type=range]{width:100%;margin:4px 0 6px;accent-color:#d4b16a;flex:none}
#m3DiaBox .dd-ev{margin:6px 0 0;line-height:1.4;overflow:auto;min-height:0}#m3DiaBox .dd-ev span{color:#b8ab88;font-style:italic}
'''
dados=open('/tmp/claude-0/jor/dias.js',encoding='utf-8').read();js=open('/tmp/claude-0/jor/dias_ui.js',encoding='utf-8').read()
k=s.index('</script>',s.index('<script id="atlas-reinos-script">'))+len('</script>')
s=s[:k]+'\n<style id="atlas-dias-css">'+css+'</style>\n<script id="atlas-dias-dados">\n'+dados+'\n</script>\n<script id="atlas-dias-script">\n'+js+'\n</script>'+s[k:]
rep('''<details><summary>Licença MIT do Middle-earth Interactive Atlas</summary>''','''<p><b>Dia a dia</b> (botão "📅 Dia a dia" no Mapa): os percursos foram adaptados dos pontos de viagem do <a href="https://github.com/kwoxer/Arda-Maps" target="_blank" rel="noopener">Arda-Maps</a> (CC BY-NC-SA 4.0) e encaixados no mapa do Atlas. As datas e os acontecimentos da Guerra do Anel seguem o Apêndice B de O Senhor dos Anéis.</p>
<details><summary>Licença MIT do Middle-earth Interactive Atlas</summary>''')
s=s.replace("window.ATLAS_VERSAO='12.7'","window.ATLAS_VERSAO='12.8'")
open(f,'w',encoding='utf-8').write(s);print('ok')
