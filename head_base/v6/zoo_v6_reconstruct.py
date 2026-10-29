import bpy,numpy as np,json
from mathutils.kdtree import KDTree
from pathlib import Path
P=Path('D:/workspace/model_zoo/head_base/v5');out=Path('C:/Users/user/Documents/Codex/zoo_v6_stage')
bpy.ops.import_scene.gltf(filepath=str(P/'head_base_v5_tex.glb'));o=bpy.data.objects['body'];A=np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices]);X=np.load(P/'shape_final.npz')['X'];tree=KDTree(13380)
for i,p in enumerate(X[:13380]):tree.insert(p,i)
tree.balance();match=[tree.find(p) for p in A];idx=np.array([x[1] for x in match]);assert len(set(idx))==13380 and max(x[2] for x in match)<1e-6
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath='D:/workspace/ideal_hero/unity/IdealHero/Assets/Characters/HeadBaseV5_v01/HeadBaseV5.fbx');o=bpy.data.objects['Body'];B=np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices]);D=np.zeros((13380,3));counts=np.zeros(13380,dtype=int)
for i,j in enumerate(idx):D[j]+=B[i];counts[j]+=1
D/=counts[:,None];err=np.linalg.norm(D[idx]-B,axis=1);maxerr=float(err.max());print('SEAM',maxerr,'mm',maxerr*1000)
assert maxerr<1e-5
np.savez_compressed(out/'shape_final_visible_rebuilt.npz',X_visible=D,source_v5_glb_to_mpfb=idx)
(out/'visible_reconstruction.json').write_text(json.dumps({'v5_match_max_m':float(max(x[2] for x in match)),'visible_mpfb_vertices':len(D),'mapped_source_vertices':len(idx),'max_duplicate_discrepancy_m':maxerr,'auxiliary_vertices_5778':'not reconstructed','coordinate_space':'Blender world metres'},indent=2),encoding='utf8')

