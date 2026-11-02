# head_base v8：v7 加上表情形態鍵

2026-10-30，Codex。狀態：**保留；表情鍵研究快照**（閉眼已由 v9 取代）。

## 從哪版來

- 上一版：v7。從 v7 母檔出發，只新增臉部表情形態鍵。
- 骨架、捏臉鍵、體型鍵、舉手修正鍵、貼圖都和 v7 一樣。

| 檔案 | 內容 |
|---|---|
| `head_base_v8.blend` | 可編輯母檔，所有形態鍵預設 0 |
| `head_base_v8_game.fbx` | 由 Blender 從母檔重新匯出，**沒有在 Unity 驗收**；骨架和權重以 v7 的 FBX 為準 |
| `head_base_v8_tex.glb`／`_clay.glb` | 貼皮／灰模交換檔，有骨架和形態鍵 |
| `expressions.json` | 每個表情鍵的來源、適用物件、最大位移、建議上限，以及 6 個表情組合 |
| 各 png、`body_joints.json` | 和 v7 相同的副本 |
| `compare_vs_v7.png`、`review/units_*.png` | 比較圖與每個表情單元近拍 |

## 改了什麼

- **33 個表情形態鍵**，名稱都以 `ex_` 開頭，預設 0。
  - 來源：MPFB 內建的表情單元（expression/units/asian，MakeHuman 原雕，CC0）。
  - 分布：眼睛 6、眉毛 8、嘴巴 13、鼻子 6。
  - body 33 個、brows 15 個、lashes 14 個；同名的鍵要同時設到這三個物件。
  - 眼球沒有表情鍵：眼球轉向直接轉 eye 物件。
- **轉移方法**：v7 每個頂點投影到 v5 MPFB 網格最近的表面，再用重心座標內插 MPFB 的表情位移。v7 臉部大多和 v5 頂點重合，這些點拿到的就是原始位移。
- **6 個表情組合（presets）**：

| 名稱 | 組成 |
|---|---|
| blink | 左右 closure 各 1 |
| smile | corner_puller 0.8 + 左右 slit 0.3 |
| laugh | corner_puller 0.9 + mouth_open 0.35 + slit 0.5 + 挑眉 0.3 |
| sad | 左右眉頭上抬 1 + mouth_depression 0.6 |
| angry | 左右皺眉 1 + mouth_compression 0.5 + 鼻翼上提 0.4 |
| surprise | 挑眉 1 + 睜大 1 + mouth_open 0.3 |

## 已驗證

- `.blend` 靜止姿勢和 v7 逐頂點相同，差 0 mm。
- FBX 重新匯入 Blender：骨頭 52 根，形態鍵數量和預設 0 都正確，靜止姿勢和 v7 最大差 0.0005 mm。
- glb：JSON 內預設權重全部 0。各物件形態鍵數：body 89、brows 57、eye 42、lashes 56。
- `compare_vs_v7.png`：v7 中性臉加 6 個組合；正面貼皮、斜側貼皮、正面灰模。

## 未驗證

- FBX 沒有在 Unity 實機測過。
- 42 個捏臉鍵和表情鍵疊加，例如眼睛放大後再閉眼。
- 表情只在中性體型上看過（4 種體型鍵不影響頭部）。

## 已知問題

1. **閉眼時上眼皮是一片深色。** 閉眼形狀是對的（灰模上眼皮完整蓋住眼球），原因是 v7 的粗眼線畫在上眼皮皮膚上：睜眼時那片皮膚被壓扁看起來是眼線，閉眼時轉到正面露出整片。調形態鍵或權重修不掉。（v9 已重做。）
2. **張嘴**：嘴裡只有原本淺淺的口腔內袋，看得到平坦的後壁；牙齒、舌頭、口腔零件沒做。`ex_mouth_open` 滿值 41 mm（尖叫），建議上限 0.5。
3. **neck-platysma 沒收**：脖子在轉移範圍邊界有接縫。

做過但沒採用：自己寫公式算臉部骨頭和權重，眼睛試 6 次、嘴巴試 3 次都失敗（眼皮撕裂、閉眼黑塊、嘴裡鋸齒、嘴角撕裂），最後改用 MPFB 現成的雕刻表情。

## 下一步

| 要改什麼 | 誰改 | 開始條件 |
|---|---|---|
| 閉眼上眼皮深色 | 美術 session | 已完成，見 v9 |
| 牙齒、口腔、笑臉 | 美術 session | 進行中，見 v9「下一步」 |
| 其他表情鍵重審、捏臉鍵疊加 | 美術 session | 見 v9「下一步」 |
| neck-platysma 接縫 | 未排 | 用到脖子表情時 |

## 怎麼重做

```
python scripts/transfer_mpfb_expr.py <v7dump.npz> <v5 shape_final.npz> <wrap_in.npz> <expr_units.npz> <expr.npz>
blender -b --python scripts/package_v8.py -- <v7.blend> <expr.npz> <輸出資料夾>
blender -b --python scripts/verify_v8.py  -- <v7.blend> <輸出資料夾>
```

表情組合定義在 `scripts/presets.json`。
