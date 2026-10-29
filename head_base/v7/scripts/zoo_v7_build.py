import bpy,json,shutil,hashlib
from pathlib import Path
S=Path('D:/workspace/ideal_hero_art/work/zoo_v7_stage');U=S/'source'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(U/'HeadBaseV5.fbx'))
names={'Body':'body','Brows':'brows','EyeL':'eye_L','EyeR':'eye_R','Lashes':'lashes'};textures={'Body':'V5_Skin.png','Brows':'V5_Brow.png','EyeL':'V5_Eye.png','EyeR':'V5_Eye.png','Lashes':'V5_Lashes.png'}
report={'objects':{},'bones':{}}
for old,file in textures.items():
 o=bpy.data.objects[old];o.name=names[old]
 if o.data.shape_keys:
  for k in o.data.shape_keys.key_blocks:k.value=0
 report['objects'][o.name]={'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'keys':[k.name for k in o.data.shape_keys.key_blocks[1:]] if o.data.shape_keys else [],'color_attributes':[a.name for a in o.data.color_attributes]}
 im=bpy.data.images.load(str(U/file),check_existing=True);im.pack();m=bpy.data.materials.new('V7_'+old);m.use_nodes=True;n=m.node_tree.nodes;bs=n.get('Principled BSDF');tex=n.new('ShaderNodeTexImage');tex.image=im;m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.8
 if old in ['Brows','Lashes']:m.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);m.surface_render_method='DITHERED'
 o.data.materials.clear();o.data.materials.append(m)
for o in bpy.data.objects:
 if o.type=='ARMATURE':report['bones'][o.name]=[b.name for b in o.data.bones]
for old,new in [('V5_Skin.png','basecolor.png'),('V5_Brow.png','eyebrow.png'),('V5_Eye.png','eye.png'),('V5_Lashes.png','lashes.png')]:shutil.copy2(U/old,S/new)
shutil.copy2(U/'HeadBaseV5.fbx',S/'head_base_v7_game.fbx')
for p in S.glob('body_paint*.png'):
 im=bpy.data.images.load(str(p));im.colorspace_settings.name='Non-Color';im.use_fake_user=True;im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(S/'head_base_v7.blend'))
bpy.ops.export_scene.gltf(filepath=str(S/'head_base_v7_tex.glb'),export_format='GLB',export_animations=False)
# Clay keeps geometry, morphs and skin; only materials replaced.
for o in bpy.data.objects:
 if o.type=='MESH':
  m=bpy.data.materials.new('Clay_'+o.name);m.diffuse_color=(.55,.55,.55,1);o.data.materials.clear();o.data.materials.append(m)
bpy.ops.export_scene.gltf(filepath=str(S/'head_base_v7_clay.glb'),export_format='GLB',export_animations=False)
(S/'structure.json').write_text(json.dumps(report,indent=2),encoding='utf8')
# Separate static muscular preview. It is explicitly not the editable master or a Unity shader reproduction.
bpy.ops.wm.open_mainfile(filepath=str(S/'head_base_v7.blend'));body=bpy.data.objects['body'];body.data.shape_keys.key_blocks['body_muscular'].value=1;bpy.context.view_layer.update()
m=body.data.materials[0];n=m.node_tree.nodes;n.clear();L=m.node_tree.links;out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');L.new(em.outputs[0],out.inputs[0]);uv=n.new('ShaderNodeUVMap');uv.uv_map=body.data.uv_layers[0].name;skin=n.new('ShaderNodeTexImage');skin.image=bpy.data.images.load(str(S/'basecolor.png'));L.new(uv.outputs[0],skin.inputs[0]);mask=n.new('ShaderNodeTexImage');mask.image=bpy.data.images.load(str(S/'body_paint_balanced.png'));mask.image.colorspace_settings.name='Non-Color';L.new(uv.outputs[0],mask.inputs[0]);sep=n.new('ShaderNodeSeparateColor');L.new(mask.outputs['Color'],sep.inputs[0]);tint=n.new('ShaderNodeMixRGB');L.new(sep.outputs['Blue'],tint.inputs[0]);tint.inputs[1].default_value=(1,1,1,1);tint.inputs[2].default_value=(.55,.46,.41,1);mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;L.new(skin.outputs['Color'],mul.inputs[1]);L.new(tint.outputs[0],mul.inputs[2]);L.new(mul.outputs[0],em.inputs[0])
image=bpy.data.images.new('MuscularDiffusePreview',width=2048,height=2048,alpha=False);image.colorspace_settings.name='sRGB';target=n.new('ShaderNodeTexImage');target.image=image;n.active=target
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body;scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=1;scene.render.bake.margin=8;bpy.ops.object.bake(type='EMIT');image.filepath_raw=str(S/'muscular_preview_basecolor.png');image.file_format='PNG';image.save()
n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.8;tex=n.new('ShaderNodeTexImage');tex.image=image;L.new(tex.outputs['Color'],bs.inputs['Base Color']);L.new(bs.outputs[0],out.inputs[0])
dg=bpy.context.evaluated_depsgraph_get()
for o in list(bpy.data.objects):
 if o.type=='MESH':
  ev=o.evaluated_get(dg);mesh=bpy.data.meshes.new_from_object(ev,depsgraph=dg);o.modifiers.clear();o.data=mesh
for o in list(bpy.data.objects):
 if o.type=='ARMATURE':bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.export_scene.gltf(filepath=str(S/'head_base_v7_muscular_preview.glb'),export_format='GLB',export_animations=False)
print('V7_PACKAGE_OK')
