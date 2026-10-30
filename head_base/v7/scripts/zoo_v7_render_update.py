import bpy,math
from pathlib import Path
from mathutils import Vector
S=Path('C:/Users/user/AppData/Local/Temp/claude/D--workspace-ideal-hero/10c51f56-1c77-42c4-8fed-691439bae1eb/scratchpad/zoo_v7');Q=Path('C:/Users/user/AppData/Local/Temp/claude/D--workspace-ideal-hero/10c51f56-1c77-42c4-8fed-691439bae1eb/scratchpad/zoo_v7/review');Q.mkdir(exist_ok=True)
for version,file in [('v7_before',S/'old'/'head_base_v7.blend'),('v7',S/'head_base_v7.blend'),('v7_preview',S/'head_base_v7_muscular_preview.glb')]:
 if file.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(file))
 else:bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(file))
 for o in bpy.data.objects:
  if o.type=='MESH'and o.data.shape_keys:
   for k in o.data.shape_keys.key_blocks:k.value=0
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.use_nodes=False;s.render.resolution_x=900;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.film_transparent=False
 w=bpy.data.worlds.new('Comparison');w.use_nodes=True;w.node_tree.nodes.get('Background').inputs[0].default_value=(.25,.25,.25,1);w.node_tree.nodes.get('Background').inputs[1].default_value=.6;s.world=w
 ld=bpy.data.lights.new('Key','AREA');ld.energy=250;ld.size=4;l=bpy.data.objects.new('Key',ld);bpy.context.collection.objects.link(l);l.location=(-2,-3,4);l.rotation_euler=(Vector((0,0,1))-l.location).to_track_quat('-Z','Y').to_euler()
 cam=bpy.data.objects.new('CompareCamera',bpy.data.cameras.new('CompareCamera'));bpy.context.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO'
 views=[('body',0,.84,1.88)] if version=='v7_preview'else[('front',0,1.53,.48),('quarter',35,1.53,.48),('side',90,1.53,.48),('body',0,.84,1.88),('clay',35,1.53,.48)]
 for name,yaw,z,scale in views:
  if name=='clay':
   for o in bpy.data.objects:
    if o.type=='MESH':
     mat=bpy.data.materials.new('InspectionGray');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.45,.45,.45,1);bs.inputs['Roughness'].default_value=.8;o.data.materials.clear();o.data.materials.append(mat)
  center=Vector((0,0,z));a=math.radians(yaw);cam.location=center+Vector((3*math.sin(a),-3*math.cos(a),0));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;s.render.filepath=str(Q/f'{version}_{name}.png');bpy.ops.render.render(write_still=True)
print('V7_REVIEW_RENDER_OK')
