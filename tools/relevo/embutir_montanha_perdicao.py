import json,base64
d=lambda f,t:'data:image/'+t+';base64,'+base64.b64encode(open(f,'rb').read()).decode()
S='/tmp/claude-0/md/';p='/home/claude/atlas-terra-media/index.html'
s=open(p,encoding='utf-8').read();sj=json.load(open(S+'md.json'))
det={'name':'Montanha da Perdição','rect':sj['rect'],'hm':d(S+'md_h.png','png'),'tex':d(S+'md_tex.webp','webp'),'models':sj['models'],'trees':sj['trees'],'tops':sj['tops']}
tag='<script id="atlas-detail-montanha-perdicao">window.ATLAS_DETAILS=window.ATLAS_DETAILS||[];window.ATLAS_DETAILS.push('+json.dumps(det,separators=(',',':'),ensure_ascii=False)+');</script>'
if '<script id="atlas-detail-montanha-perdicao">' in s:
    i=s.index('<script id="atlas-detail-montanha-perdicao">');j=s.index('</script>',i)+9;s=s[:i]+tag+s[j:]
else: s=s.replace('<script id="atlas-v86-relevo">',tag+'\n<script id="atlas-v86-relevo">',1)
open(p,'w',encoding='utf-8').write(s);print('embed ok',round(len(s.encode())/1e6,2))
