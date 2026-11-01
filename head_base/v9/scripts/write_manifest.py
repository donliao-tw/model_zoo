"""write head_base/<ver>/manifest.json in the shared zoo format (see head_base/README.md).
The descriptive fields come from a small JSON spec; sha256 of every file in the folder is computed here.
usage: python write_manifest.py <version_dir> <spec.json>
"""
import hashlib
import json
import sys
from pathlib import Path

d, spec = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'))
ORDER = ['version', 'date', 'made_by', 'previous', 'status', 'source', 'bones', 'meshes',
         'changes', 'verified', 'not_verified', 'known_issues', 'extra']
m = {k: spec[k] for k in ORDER if k in spec}
missing = [k for k in ORDER[:-1] if k not in spec]
if missing: sys.exit(f'missing fields: {missing}')
m['files'] = {p.relative_to(d).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(d.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
(d / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('MANIFEST_OK', d.name, len(m['files']), 'files')
