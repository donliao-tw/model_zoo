import bpy,sys,json,numpy as np
from pathlib import Path
from mathutils.kdtree import KDTree
p=Path('C:/Users/user/Documents/Codex/zoo_v6_stage'); src=Path('D:/workspace/ideal_hero/unity/IdealHero/Assets/Characters/HeadBaseV5_v01/HeadBaseV5.fbx')
def load(kind,path):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 if kind=='fbx':bpy.ops.import_scene.fbx(filepath=str(path))
 else:bpy.ops.import_scene.gltf(filepath=str(path))
 out={}
 for o in bpy.data.objects:
  if o.type!='MESH':continue
  name={'Body':'body','Brows':'brows','EyeL':'eye_L','EyeR':'eye_R','Lashes':'lashes'}.get(o.name,o.name)
  keys=o.data.shape_keys.key_blocks if o.data.shape_keys else []
  mat=o.matrix_world
  out[name]={'n':len(o.data.vertices),'P':np.array([tuple(mat@v.co) for v in o.data.vertices]),'keys':{k.name:np.array([tuple(mat@v.co) for v in k.data]) for k in keys},'values':{k.name:float(k.value) for k in keys},'colors':len(o.data.color_attributes)}
 return out,len([x for x in bpy.data.objects if x.type=='ARMATURE'])
a,aa=load('fbx',src);b,bb=load('glb',p/'head_base_v6_tex.glb');report={'armatures_fbx':aa,'armatures_glb':bb,'objects':{}}
for name in a:
 if name not in b:report['objects'][name]={'missing':True};continue
 x=a[name];y=b[name];tree=KDTree(y['n'])
 for i,v in enumerate(y['P']):tree.insert(v,i)
 tree.balance();nearest=[tree.find(v) for v in x['P']]
 d=max(t[2] for t in nearest);common=set(x['keys']) & set(y['keys'])
 # Matching basis positions alone is not enough to validate morphs at seams; compare same index only when exact correspondence.
 same=bool(x['n']==y['n'] and np.max(np.linalg.norm(x['P']-y['P'],axis=1))<1e-5)
 kerr=max((float(np.max(np.linalg.norm(x['keys'][k]-y['keys'][k],axis=1))) for k in common),default=0) if same else None
 report['objects'][name]={'fbx_vertices':x['n'],'glb_vertices':y['n'],'basis_nearest_max_m':d,'same_order':same,'morph_max_diff_m_if_same_order':kerr,'fbx_keys':len(x['keys'])-1,'glb_keys':len(y['keys'])-1,'missing_keys':sorted(set(x['keys'])-set(y['keys'])),'defaults_nonzero':{k:v for k,v in y['values'].items() if abs(v)>1e-6},'fbx_color_layers':x['colors'],'glb_color_layers':y['colors']}
(p/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))

