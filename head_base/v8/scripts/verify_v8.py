"""驗證 v8:重新匯入 fbx / glb,檢查骨頭數、各物件形態鍵數與預設值,並比較靜止姿勢頂點與 v7。
用法: blender -b --python verify_v8.py -- <v7.blend> <v8資料夾>"""
import sys
import bpy
import numpy as np
v7, d = sys.argv[sys.argv.index('--') + 1:][:2]


def grab():
    out = {}
    dg = bpy.context.evaluated_depsgraph_get()
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        e = o.evaluated_get(dg); m = e.to_mesh()
        c = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', c)
        out[o.name.split('.')[0]] = (np.array(o.matrix_world) @ np.c_[c.reshape(-1, 3), np.ones(len(m.vertices))].T)[:3].T
        e.to_mesh_clear()
    return out


bpy.ops.wm.open_mainfile(filepath=v7); A = grab()
for f, imp in ((f'{d}/head_base_v8.blend', None), (f'{d}/head_base_v8_game.fbx', bpy.ops.import_scene.fbx), (f'{d}/head_base_v8_tex.glb', bpy.ops.import_scene.gltf)):
    if imp is None: bpy.ops.wm.open_mainfile(filepath=f)
    else: bpy.ops.wm.read_factory_settings(use_empty=True); imp(filepath=f)
    B = grab()
    bones = sum(len(o.data.bones) for o in bpy.data.objects if o.type == 'ARMATURE')
    keys = {o.name: (len(o.data.shape_keys.key_blocks) - 1, max(k.value for k in o.data.shape_keys.key_blocks[1:])) for o in bpy.data.objects if o.type == 'MESH' and o.data.shape_keys}
    diff = {}
    for n, P in A.items():
        Q = next((v for k, v in B.items() if k.lower().replace('_', '') == n.lower().replace('_', '')), None)
        if Q is None: diff[n] = 'missing'; continue
        if len(Q) == len(P): diff[n] = '%.4f mm' % (np.abs(Q - P).max() * 1000)
        else:
            from scipy.spatial import cKDTree
            diff[n] = 'nn %.4f mm (%d vs %d verts)' % (cKDTree(P).query(Q)[0].max() * 1000, len(Q), len(P))
    print('VERIFY', f.split('/')[-1], 'bones', bones, 'keys(count,max value)', keys, 'rest diff vs v7', diff)
