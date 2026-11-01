"""verify head_base v9: read back fbx / blend / glb (bones, shape keys, defaults 0, rest pose vs fbx),
then compare every shape key with v8 so the README can say exactly which keys changed.
usage: blender -b --factory-startup --python verify_v9.py -- <v8.blend> <v9_dir> <out.json>
"""
import json
import sys
import bpy
import numpy as np
from mathutils.kdtree import KDTree

v8, d, out = sys.argv[sys.argv.index('--') + 1:][:3]


def load(f):
    if f.endswith('.blend'): bpy.ops.wm.open_mainfile(filepath=f); return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    (bpy.ops.import_scene.fbx if f.endswith('.fbx') else bpy.ops.import_scene.gltf)(filepath=f)


def meshes():
    return {o.name.split('.')[0].lower(): o for o in bpy.data.objects if o.type == 'MESH'}


def keys(o):
    """name -> (n,3) world-space absolute positions for Basis and every key"""
    M = np.array(o.matrix_world)
    res = {}
    for kb in (o.data.shape_keys.key_blocks if o.data.shape_keys else []):
        c = np.empty(len(kb.data) * 3); kb.data.foreach_get('co', c)
        res[kb.name] = (M @ np.c_[c.reshape(-1, 3), np.ones(len(kb.data))].T)[:3].T
    return res


def summary():
    bones = sum(len(o.data.bones) for o in bpy.data.objects if o.type == 'ARMATURE')
    ks = {}
    for n, o in meshes().items():
        kb = o.data.shape_keys.key_blocks if o.data.shape_keys else []
        ks[n] = {'verts': len(o.data.vertices), 'keys': len(kb) - 1 if kb else 0,
                 'max_default': max((k.value for k in kb[1:]), default=0)}
    return bones, ks


report = {'files': {}}
load(f'{d}/head_base_v9.fbx'); REF = {n: keys(o) for n, o in meshes().items()}
for f in ('head_base_v9.fbx', 'head_base_v9.blend', 'head_base_v9_tex.glb', 'head_base_v9_clay.glb'):
    load(f'{d}/{f}')
    bones, ks = summary()
    rest = {}
    for n, o in meshes().items():
        if n not in REF: rest[n] = 'not in fbx'; continue
        P = REF[n]['Basis']; Q = keys(o).get('Basis')
        if Q is None: rest[n] = 'no keys'; continue
        if len(P) == len(Q): rest[n] = round(float(np.abs(P - Q).max() * 1000), 4)
        else:  # glb splits uv seams; nearest-point distance instead of index match
            t = KDTree(len(P))
            for i, p in enumerate(P): t.insert(p, i)
            t.balance()
            rest[n] = 'nn %.4f (%d vs %d verts)' % (max(t.find(q)[2] for q in Q) * 1000, len(Q), len(P))
    report['files'][f] = {'bones': bones, 'meshes': ks, 'rest_diff_vs_fbx_mm': rest}
    print('VERIFY', f, bones, ks, rest)

# per-key comparison with v8 (same vertex order expected; checked)
load(v8); V8 = {n: keys(o) for n, o in meshes().items()}
cmp = {}
for n, K9 in REF.items():
    K8 = V8.get(n)
    if K8 is None: cmp[n] = 'missing in v8'; continue
    b9, b8 = K9['Basis'], K8['Basis']
    if len(b9) != len(b8): cmp[n] = 'vertex count differs %d vs %d' % (len(b9), len(b8)); continue
    c = {'basis_max_mm': round(float(np.abs(b9 - b8).max() * 1000), 4), 'added': [], 'removed': [], 'changed': {}, 'same': 0}
    for k in K9:
        if k == 'Basis': continue
        if k not in K8: c['added'].append(k); continue
        diff = float(np.abs((K9[k] - b9) - (K8[k] - b8)).max() * 1000)
        if diff > 0.01: c['changed'][k] = round(diff, 3)
        else: c['same'] += 1
    c['removed'] = [k for k in K8 if k != 'Basis' and k not in K9]
    cmp[n] = c
report['vs_v8'] = cmp
print('VS_V8', json.dumps(cmp))
json.dump(report, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('V9_VERIFY_OK')
