"""打包 head_base v8:v7 + MPFB 表情單元形態鍵(ex_ 開頭,預設 0)。
輸出 .blend、貼皮 / 灰模 glb、遊戲用 fbx(Blender 重新匯出,需在 Unity 驗收)。
用法: blender -b --python package_v8.py -- <v7.blend> <expr.npz> <輸出資料夾>
"""
import os
import sys
import bpy
import numpy as np

src, npz, outd = sys.argv[sys.argv.index('--') + 1:][:3]
SKIP = {'neck-platysma'}          # 脖子轉移範圍邊界有接縫,這版不收
bpy.ops.wm.open_mainfile(filepath=src)
X = np.load(npz)
added = {}
for k in X.files:
    on, n = k.split('__')
    if n in SKIP: continue
    o = bpy.data.objects[on]; me = o.data
    base = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', base)
    kn = 'ex_' + n.replace('-', '_')
    sk = o.shape_key_add(name=kn, from_mix=False)
    sk.data.foreach_set('co', base + X[k].ravel())
    added.setdefault(on, []).append(kn)
# Blender 5 新增的形態鍵預設值是 1 → 全部歸零後才存檔 / 匯出
for o in bpy.data.objects:
    if o.type == 'MESH' and o.data.shape_keys:
        for kb in o.data.shape_keys.key_blocks: kb.value = 0
os.makedirs(outd, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=f'{outd}/head_base_v8.blend')
bpy.ops.export_scene.gltf(filepath=f'{outd}/head_base_v8_tex.glb', export_format='GLB', export_animations=False)
bpy.ops.export_scene.fbx(filepath=f'{outd}/head_base_v8_game.fbx', use_selection=False, add_leaf_bones=False,
                         bake_anim=False, mesh_smooth_type='FACE', path_mode='COPY', embed_textures=False)
for o in bpy.data.objects:
    if o.type == 'MESH':
        m = bpy.data.materials.new('Clay_' + o.name); m.diffuse_color = (.55, .55, .55, 1)
        o.data.materials.clear(); o.data.materials.append(m)
bpy.ops.export_scene.gltf(filepath=f'{outd}/head_base_v8_clay.glb', export_format='GLB', export_animations=False)
print('V8_PACKAGE_OK', {k: len(v) for k, v in added.items()})
