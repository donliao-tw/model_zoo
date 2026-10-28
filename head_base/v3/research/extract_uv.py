import bpy,json
from pathlib import Path
import numpy as np
S=Path('D:/workspace/ideal_hero/.claude/worktrees/jolly-newton-530a10/outputs/unity_v01/nose_rebuild_v001/head_nose_r3.glb'); O=Path('C:/Users/user/Documents/Codex/nose_repair_work');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(S));o=bpy.data.objects['body'];o.data.calc_loop_triangles();uv=o.data.uv_layers.active.data; groups={}
for t in o.data.loop_triangles:
 coords=np.array([tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices]);c=coords.mean(0);x,y,z=c
 for name,test in [('nose',abs(x)<.023 and 1.506<z<1.531 and y<-.115),('under',abs(x)<.020 and 1.510<z<1.522 and y<-.135)]:
  if test:groups.setdefault(name,[]).append([list(uv[i].uv) for i in t.loops])
(O/'uv_triangles.json').write_text(json.dumps(groups),encoding='utf-8');print({k:len(v) for k,v in groups.items()})
