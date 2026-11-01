"""head_base v9: package the source FBX into blend / tex glb / clay glb (all shape keys default 0).
The FBX itself is copied byte-for-byte outside this script; it stays the authority for bones and weights.
usage: blender -b --factory-startup --python build_v9.py -- <source.fbx> <skin_normal.png> <out_dir>
"""
import os
import sys
import bpy

src, skin, outd = sys.argv[sys.argv.index('--') + 1:][:3]
os.makedirs(outd, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=src)

# FBX import creates one image per material slot; collapse to one image per file
by_path = {}
for img in list(bpy.data.images):
    key = bpy.path.abspath(img.filepath).lower()
    if key in by_path:
        img.user_remap(by_path[key]); bpy.data.images.remove(img)
    else:
        by_path[key] = img
# Body uses the default (normal) hand-painted skin, the look the source model ships with for body type normal
body_img = next(i for i in bpy.data.images if i.name.startswith('V5_Skin'))
body_img.filepath = skin; body_img.name = 'skin_normal'; body_img.reload()

for o in bpy.data.objects:
    if o.type == 'MESH' and o.data.shape_keys:
        for kb in o.data.shape_keys.key_blocks: kb.value = 0
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=f'{outd}/head_base_v9.blend')
bpy.ops.export_scene.gltf(filepath=f'{outd}/head_base_v9_tex.glb', export_format='GLB', export_animations=False)
for o in bpy.data.objects:
    if o.type == 'MESH':
        m = bpy.data.materials.new('Clay_' + o.name); m.diffuse_color = (.55, .55, .55, 1)
        o.data.materials.clear(); o.data.materials.append(m)
bpy.ops.export_scene.gltf(filepath=f'{outd}/head_base_v9_clay.glb', export_format='GLB', export_animations=False)
print('V9_PACKAGE_OK', {o.name: len(o.data.shape_keys.key_blocks) - 1 for o in bpy.data.objects if o.type == 'MESH' and o.data.shape_keys})
