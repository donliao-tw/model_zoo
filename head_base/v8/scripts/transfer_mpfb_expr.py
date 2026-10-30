"""把 MPFB 表情單元(在 v5 的 MPFB 頭上量的位移)轉移到 v7 各物件:
每個頂點投影到 v5 MPFB 網格(只用 body 三角形)最近的表面點,用該三角形的重心座標內插位移。
v7 臉部大多和 v5 頂點重合,這些點拿到的就是原位移。
用法: python3 transfer_mpfb_expr.py <v7dump.npz> <v5 shape_final.npz> <wrap_in.npz> <expr_units.npz> <輸出.npz>
輸出鍵 '<物件>__<表情>',可直接給 render_expr.py 加成形態鍵。
"""
import sys
import numpy as np
from scipy.spatial import cKDTree

dump, shp, wrap, units, out = sys.argv[1:6]
D = np.load(dump); X = np.load(shp)['X']; Wr = np.load(wrap); U = np.load(units)
F = Wr['F']; isb = Wr['is_body']
F = F[isb[F].all(1)]
if F.shape[1] == 4:
    F = np.vstack([F[:, [0, 1, 2]], F[:, [0, 2, 3]]])
vt = [[] for _ in range(len(X))]
for t, f in enumerate(F):
    for v in f: vt[v].append(t)
tree = cKDTree(X[np.unique(F)]); ids = np.unique(F)


def closest_bary(p, tri):
    a, b, c = X[F[tri, 0]], X[F[tri, 1]], X[F[tri, 2]]
    ab, ac, ap = b - a, c - a, p - a
    d00, d01, d11 = (ab * ab).sum(1), (ab * ac).sum(1), (ac * ac).sum(1)
    d20, d21 = (ap * ab).sum(1), (ap * ac).sum(1)
    den = d00 * d11 - d01 * d01 + 1e-20
    v = (d11 * d20 - d01 * d21) / den; w = (d00 * d21 - d01 * d20) / den
    v, w = np.clip(v, 0, 1), np.clip(w, 0, 1)
    s = v + w; over = s > 1; v[over] /= s[over]; w[over] /= s[over]
    q = a + v[:, None] * ab + w[:, None] * ac
    return np.c_[1 - v - w, v, w], np.linalg.norm(q - p, axis=1)


res = {}
for obj in ('body', 'brows', 'lashes', 'eye_L', 'eye_R'):
    P = D[obj + '_co'] + (D[obj + '_mw'][:3, 3] if obj.startswith('eye') else 0)
    sel = np.where(P[:, 2] > 1.38)[0]
    _, nn = tree.query(P[sel], k=6)
    T = np.zeros(len(sel), int); B = np.zeros((len(sel), 3)); dist = np.full(len(sel), np.inf)
    for i, row in enumerate(nn):
        cand = np.unique(np.concatenate([vt[ids[j]] for j in row]))
        bc, d = closest_bary(np.repeat(P[sel[i]][None], len(cand), 0), cand)
        k = d.argmin(); T[i], B[i], dist[i] = cand[k], bc[k], d[k]
    # 眼球整顆跟著它的中心走(MPFB 表情不轉眼球,只是保險)
    fade = np.clip(1 - (1.40 - P[sel, 2]) / 0.02, 0, 1)            # 脖子下緣淡出
    for n, dl in zip(U['names'], U['deltas']):
        d = np.zeros_like(P)
        d[sel] = (dl[F[T]] * B[:, :, None]).sum(1) * fade[:, None]
        if np.abs(d).max() > 1e-6: res[f'{obj}__{n}'] = d.astype(np.float32)
    print(obj, 'verts', len(sel), 'proj dist mm p50 %.2f p99 %.2f max %.2f' % tuple(np.percentile(dist, [50, 99, 100]) * 1000))
np.savez_compressed(out, **res)
print('keys', len(res))
