import bpy,sys,json,hashlib,shutil
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/user/Documents/Codex/zoo_v6_stage');R.mkdir(parents=True,exist_ok=True)
U=Path('D:/workspace/ideal_hero/unity/IdealHero/Assets/Characters/HeadBaseV5_v01')
F=U/'HeadBaseV5.fbx'; Z=Path('D:/workspace/model_zoo/head_base/v5/head_base_v5_tex.glb')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(F))
names={'Body':'body','Brows':'brows','EyeL':'eye_L','EyeR':'eye_R','Lashes':'lashes'}
textures={'Body':'V5_Skin.png','Brows':'V5_Brow.png','EyeL':'V5_Eye.png','EyeR':'V5_Eye.png','Lashes':'V5_Lashes.png'}
for n,file in textures.items():
 o=bpy.data.objects[n];o.name=names[n]
 img=bpy.data.images.load(str(U/file),check_existing=True);img.pack()
 mat=bpy.data.materials.new('V6_'+n);mat.use_nodes=True
 nodes=mat.node_tree.nodes;bs=nodes.get('Principled BSDF');tex=nodes.new('ShaderNodeTexImage');tex.image=img
 mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
 if n in ('Brows','Lashes'):
  mat.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);mat.surface_render_method='DITHERED'
 o.data.materials.clear();o.data.materials.append(mat)
for old,new in [('V5_Skin.png','basecolor.png'),('V5_Brow.png','eyebrow.png'),('V5_Eye.png','eye.png'),('V5_Lashes.png','lashes.png')]:shutil.copy2(U/old,R/new)
shutil.copy2(F,R/'head_base_v6_game.fbx')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'head_base_v6.blend'))
bpy.ops.export_scene.gltf(filepath=str(R/'head_base_v6_tex.glb'),export_format='GLB',export_animations=False)
# Independent clay material: shape keys and rig unchanged.
for o in bpy.data.objects:
 if o.type=='MESH':
  mat=bpy.data.materials.new('Clay_'+o.name);mat.diffuse_color=(.55,.55,.55,1);o.data.materials.clear();o.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=str(R/'head_base_v6_clay.glb'),export_format='GLB',export_animations=False)
print('PACKAGE_OK')

