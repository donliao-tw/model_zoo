"""same-camera Blender renders of v8 and v9 for compare_vs_v8.png (Cycles, not Unity toon).
usage: blender -b --factory-startup --python render_v9.py -- <v8.blend> <v9.blend> <review_dir>
"""
import math
import sys
import bpy
from mathutils import Vector

v8, v9, outd = sys.argv[sys.argv.index('--') + 1:][:3]
VIEWS = [('front', 0, 1.53, .48, {}), ('quarter', 35, 1.53, .48, {}), ('side', 90, 1.53, .48, {}),
         ('blink', 0, 1.60, .22, {'ex_eye_left_closure': 1, 'ex_eye_right_closure': 1}),
         ('body', 0, .84, 1.88, {}), ('clay', 35, 1.53, .48, {})]
ROUND = [('round_front', 0, .84, 1.88, {'body_round': 1}), ('round_side', 90, .84, 1.88, {'body_round': 1})]


def setkeys(vals):
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.data.shape_keys:
            for kb in o.data.shape_keys.key_blocks: kb.value = vals.get(kb.name, 0)


for ver, f in (('v8', v8), ('v9', v9)):
    bpy.ops.wm.open_mainfile(filepath=f)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'; s.cycles.samples = 16; s.cycles.use_denoising = True
    s.render.resolution_x = s.render.resolution_y = 700; s.render.image_settings.file_format = 'PNG'
    s.view_settings.view_transform = 'Standard'; s.render.film_transparent = False
    w = bpy.data.worlds.new('Cmp'); w.use_nodes = True
    bg = w.node_tree.nodes.get('Background'); bg.inputs[0].default_value = (.25, .25, .25, 1); bg.inputs[1].default_value = .6; s.world = w
    ld = bpy.data.lights.new('Key', 'AREA'); ld.energy = 250; ld.size = 4
    li = bpy.data.objects.new('Key', ld); s.collection.objects.link(li); li.location = (-2, -3, 4)
    li.rotation_euler = (Vector((0, 0, 1)) - li.location).to_track_quat('-Z', 'Y').to_euler()
    cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); s.collection.objects.link(cam); s.camera = cam; cam.data.type = 'ORTHO'
    for name, yaw, z, scale, keys in VIEWS + (ROUND if ver == 'v9' else []):
        setkeys(keys)
        if name == 'clay':
            for o in bpy.data.objects:
                if o.type == 'MESH':
                    m = bpy.data.materials.new('Gray'); m.use_nodes = True
                    b = m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value = (.45, .45, .45, 1); b.inputs['Roughness'].default_value = .8
                    o.data.materials.clear(); o.data.materials.append(m)
        c = Vector((0, 0, z)); a = math.radians(yaw)
        cam.location = c + Vector((3 * math.sin(a), -3 * math.cos(a), 0))
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = scale
        s.render.filepath = f'{outd}/{ver}_{name}.png'; bpy.ops.render.render(write_still=True)
print('V9_RENDER_OK')
