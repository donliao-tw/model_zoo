import bpy,json,numpy as np
from pathlib import Path
from mathutils.kdtree import KDTree
S=Path('D:/workspace/ideal_hero_art/work/zoo_v7_stage')
def load(kind,p):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 if kind=='fbx':bpy.ops.import_scene.fbx(filepath=str(p))
 else:bpy.ops.import_scene.gltf(filepath=str(p))
 result={};bones={}
 for o in bpy.data.objects:
  if o.type=='ARMATURE':bones[o.name]=len(o.data.bones)
  if o.type!='MESH':continue
  name={'Body':'body','Brows':'brows','EyeL':'eye_L','EyeR':'eye_R','Lashes':'lashes'}.get(o.name,o.name);M=o.matrix_world
  result[name]={'P':np.array([tuple(M@v.co)for v in o.data.vertices]),'keys':{k.name:np.array([tuple(M@v.co)for v in k.data])for k in o.data.shape_keys.key_blocks}if o.data.shape_keys else {},'defaults':{k.name:float(k.value)for k in o.data.shape_keys.key_blocks[1:]}if o.data.shape_keys else {},'colors':[c.name for c in o.data.color_attributes]}
 return result,bones
A,ab=load('fbx',S/'head_base_v7_game.fbx');report={'fbx_bones':ab,'exports':{}}
for file in ['head_base_v7_tex.glb','head_base_v7_clay.glb','head_base_v7_muscular_preview.glb']:
 B,bb=load('glb',S/file);r={'bones':bb,'objects':{}}
 for name,a in A.items():
  b=B[name];target=a['keys'].get('body_muscular',a['P'])if 'preview'in file else a['P'];tree=KDTree(len(target))
  for i,p in enumerate(target):tree.insert(p,i)
  tree.balance();match=[tree.find(p)for p in b['P']];idx=np.array([m[1]for m in match]);err=max(m[2]for m in match);assert err<2e-5,(file,name,err)
  missing=[]if 'preview'in file else sorted(set(a['keys'])-set(b['keys']));assert not missing
  morph_error=0
  if 'preview'not in file:
   for k in b['keys']:morph_error=max(morph_error,float(np.linalg.norm(a['keys'][k][idx]-b['keys'][k],axis=1).max()))
   assert morph_error<2e-5,(file,name,morph_error)
   assert not any(abs(x)>1e-6 for x in b['defaults'].values())
  r['objects'][name]={'fbx_vertices':len(a['P']),'export_vertices':len(b['P']),'basis_or_preview_nearest_max_m':err,'morph_max_error_m':morph_error if 'preview'not in file else None,'export_keys':len(b['defaults']),'missing_keys':missing,'all_defaults_zero':not any(abs(x)>1e-6 for x in b['defaults'].values()),'fbx_color_layers':a['colors'],'export_color_layers':b['colors']}
 report['exports'][file]=r
(S/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('V7_READBACK_OK',json.dumps(report))
