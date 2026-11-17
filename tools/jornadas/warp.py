import json,re,numpy as np
from scipy.interpolate import RBFInterpolator
B='/home/claude/kwoxer/arda-maps/QGIS/third age/arda3/'
A={}
for fn in ['point_city','point_castletower','point_place','point_mount','point_ford','point_waterfall','point_bridge']:
    for f in json.load(open(B+fn+'.geojson'))['features']:
        n=f['properties'].get('eventname');A.setdefault(n,f['geometry']['coordinates'])
A['GreyHavens']=[0.02819,-0.01042]
WP={f['properties']['id']:f['geometry']['coordinates'] for f in json.load(open(B+'point_waypoint.geojson'))['features']}
s=open('/home/claude/atlas-terra-media/index.html',encoding='utf-8').read()
i=s.index('const P={Condado:');j=s.index('};',i)
P={k:(float(x),float(y)) for k,x,y in re.findall(r'(\w+):\[([\d.]+),([\d.]+)\]',s[i:j])}
CP={'BagEnd':'Bolsao','Bree':'Bri','Weathertop':'AmonSul','Rivendell':'Valfenda','FordOfBruinen':'VauBruinen','TomBertWilliam':'ColinasTrolls',
'DoorsOfDurin':'PortasDurin','CarasGaladhon':'CarasGaladhon','CerinAmroth':'CerinAmroth','AmonHen':'AmonHen','Rauros':'QuedasRauros','Argonath':'Argonath',
'Isengard':'Orthanc','HelmsDeep':'ForteTrombeta','Edoras':'Meduseld','Dunharrow':'FanoColina','MinasTirith':'MinasTirith','Osgiliath':'Osgiliath','Pelargir':'CidadePelargir',
'DolAmroth':'CasteloAmroth','MinasMorgul':'CidadeMorgul','TowerOfCirithUngol':'TorreCirithUngol','BaradDur':'TorreNegra','MountDoom':'CrateraOrodruin','HennethAnnun':'JanelaPoente',
'CirithGorgor':'Morannon','Carrock':'RochedoCarrocha','BeornsHall':'CasaBeorn','EaglesEyrie':'NinhoAguias','LakeTown':'Esgaroth','Dale':'ValleCidade','LonelyMountain':'PicoErebor',
'ElvenkingsHalls':'SalaoThranduil','DolGuldur':'FortalezaGuldur','FornostErain':'Fornost','GreyHavens':'Mithlond','BrandyHall':'SedeBrandevin','TomBombadil':'CasaBombadil',
'FordsOfIsen':'VausIsen','PathsOfTheDead':'PortaEscura','BrandywineBridge':'PonteBrandevin','GoblinGate':'MontanhasSombrias'}
CP.pop('GoblinGate')
src=np.array([A[k] for k in CP]);dst=np.array([P[v] for v in CP.values()])
tps=RBFInterpolator(src,dst,kernel='thin_plate_spline',smoothing=0.0)
res=np.hypot(*(tps(src)-dst).T);print('max resid',res.max())
def W(c):return [round(float(v),1) for v in tps(np.array([c]))[0]]
