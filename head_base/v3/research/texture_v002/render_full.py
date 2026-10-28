import bpy,sys
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];source,tag=args;out=Path('C:/Users/user/Documents/Codex/full_head_review');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=source);s=bpy.context.scene
for o in s.objects:
 if o.type=='MESH' and o.data.shape_keys:
  for k in o.data.shape_keys.key_blocks[1:]:k.value=0
cam=bpy.data.objects.new('HeadCamera',bpy.data.cameras.new('HeadCamera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=.31;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=720;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.world=bpy.data.worlds.new('HeadWorld');s.world.color=(.18,.18,.18);s.view_settings.view_transform='AgX';center=Vector((0,-.08,1.55))
def lamp(name,pos,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
lamp('Key',(-.6,-1.3,2.3),8,1.5);lamp('Fill',(.9,-1.,1.8),5,1.8);lamp('Rim',(.4,.7,2.2),4,1.)
for view,direction in [('front',(0,-3,0)),('left_quarter',(-1.6,-3,0)),('right_quarter',(1.6,-3,0)),('left_side',(-3,0,0)),('right_side',(3,0,0))]:
 cam.location=center+Vector(direction);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(out/f'{tag}_{view}.png');bpy.ops.render.render(write_still=True)
