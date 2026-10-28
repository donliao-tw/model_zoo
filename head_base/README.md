# head_base:可捏臉的男性底模

## 每個版本資料夾的檔案

| 檔案 | 用途 |
|---|---|
| `head_base_vX_tex.glb` | 貼皮版(網頁 / 遊戲引擎直接載入) |
| `head_base_vX_clay.glb` | 灰模版 |
| `head_base_vX.blend` | Blender 原檔(貼圖已打包) |
| `basecolor.png` | 皮膚貼圖 4096²,MPFB UV |
| `shape_final.npz` | 最終頂點位置 `X`(MPFB 全部 19158 頂點,含輔助幾何)。重做時以它為準 |
| `params.json` | 全部參數:體型、各擬合階段的方法與滑桿值、修正、零件、已知問題 |
| `morphs.json` | 每個玩家滑桿由哪些 MPFB 目標組成 |

## 版本

| 版本 | 狀態 | 來源 |
|---|---|---|
| v1 | 停用 | 第一次擬合打包,鼻子破損 |
| v1.1 | 停用 | v1 只改貼圖 |
| v2 | 保留 | v1 + 眼袋、眉毛、畫風眼睛、腮紅 |
| v3 | 保留 | v2 頭型 v005 + Claude 鼻部 R3(ideal_hero) |
| v4 | 保留 | v3 + 鼻底貼圖 v002 |
| **v5** | **目前** | v4 + 法線 / 耳朵 / 眼線 / 睫毛 / 眉毛對稱 / 鼻子更挺 |

> **2026-10-28 修正**:v1、v1.1、v2、v5 的 glb / .blend 先前把 28 個捏臉 morph 的預設值存成 1(全部拉滿疊加),直接打開會看到巫婆鼻等變形。已全部改回 0(glb 只改 JSON 的預設權重,模型資料不變)。v4 沒有這個問題。對照 `v5/morph_default_fix.png`。

### v5(目前版本)
- 從 v4 出發:重建 shape_final.npz、修鼻翼黑影(法線)、耳朵平順化、眼線接到眼皮邊緣、睫毛 0.35、眉毛左右對稱、鼻子整體更挺(鼻根 +4 mm、鼻子深度 0.6)。詳見 [v5 說明](v5/README.md)。

### v4(保留)
- 目前完整頭部檢視使用的模型，承接 v005 頭型、Claude R3 鼻部及鼻底貼圖候選 v002。
- 實際可用檔案、來源及耳朵／滑桿／Unity 驗證限制見 [v4 說明](v4/README.md)。此版本目前只有 GLB 快照及提取貼圖，沒有新的 Blender 原檔或完整生成參數。2026-10-28 補上用 UV 對回 MPFB 編號重建的 `v4/shape_final_rebuilt.npz`(與原 glb 渲染一致)。


### v1(停用)
- 底模:MPFB 男、約 22 歲、亞洲 100%(肌肉 0.5、體重 0.35、比例 0.8、身高 0.6)。
- 擬合:照 AI 頭 head02 分階段(頭型 → 69 個五官特徵點 → 眼 / 鼻 / 嘴 / 耳 MPFB 滑桿),再把顱頂收窄 0.92、下巴加寬 0.25。
- 問題:**鼻子破損**。第 1 階段的平滑變形把鼻子擠窄,第 2 階段鼻翼特徵點深度不準造成翻面,第 3 階段鼻子滑桿把鼻尖削成楔形(鼻尖後 3 mm 只剩 6.8 mm 寬,AI 為 12.5 mm)。遠看正常,灰模近拍很明顯。見 `previews/v1_nose_closeup.png`。

### v1.1(停用)
- 形狀與 v1 完全相同,只把鼻孔附近的深色污漬拉回膚色。改善很小。

### v3(保留:另一專案 ideal_hero 做的 Claude 鼻部 R3)
- 從 v2 的 v005 頭型修出 R3 鼻子;貼圖試驗在 `v3/research/`。詳見 [v3 說明](v3/README.md)。原資料夾名 `v2_nose_r3_research/`、`v2_nose_r3_texture_v002/`。

### v2(保留)
從 v1 出發:
- 眼袋:拿掉 4 個 push 類眼睛滑桿(把下眼皮往前推的主因),加 eye-bag-decr 1.0、eye-bag-in 0.6。
- 眉毛:MPFB eyebrow004(可換,見 `parts/eyebrows/`)。
- 眼睛:畫風眼球貼圖 `parts/eyes/toon_eye_brown.png`。
- 貼圖:兩頰與鼻頭淡腮紅(0.5)、耳朵與鼻孔暗部拉回膚色、保留 AI 眼線。
- 預覽:`previews/v2_*.png`。

已知問題(未修):
1. 鼻子沿用 v1:鼻翼皺、鼻尖偏尖。
2. 上眼皮邊緣有一條細暗線蓋到眼白和瞳孔上緣。原因:AI 眼線比 MPFB 眼皮邊緣高約 2 mm,形成「眼線 + 眼皮邊緣」兩條線。正在改成在 MPFB 眼皮邊緣重畫眼線(已試 2 次未成功,第 3 次進行中)。
3. 睫毛從下方看仍偏長。
4. 耳下一小塊顏色偏淺。

## 玩家滑桿(v1 / v1.1 / v2 相同)

成對使用:一條 −1..1 的滑桿,負值給左欄、正值給右欄。

| 滑桿 | 負 | 正 | 建議上限 |
|---|---|---|---|
| 眼睛大小 | eyes_small | eyes_big | 1 |
| 眼睛高低 | eyes_down | eyes_up | 1 |
| 眼距 | eyes_together | eyes_apart | 1 |
| 眼尾 | eyes_corner_down | eyes_corner_up | 1 |
| 鼻子大小 | nose_small | nose_big | 1 |
| 鼻翼寬窄 | nose_narrow | nose_wide | 1 |
| 鼻尖 | nose_tip_down | nose_tip_up | 1 |
| 嘴寬 | mouth_narrow | mouth_wide | 1 |
| 嘴唇厚薄 | lips_thin | lips_full | 1 |
| 下巴寬窄 | chin_narrow | chin_wide | 0.5(1 會出現方形台階) |
| 下巴長短 | chin_short | chin_long | 0.6 |
| 下顎寬窄 | jaw_narrow | jaw_wide | 0.6 |
| 臉型 | face_slim | face_round | 1 |
| 耳朵大小 | ears_small | ears_big | 1 |

three.js:

```js
const set = (name, v) => root.traverse((m) => {
  const i = m.morphTargetDictionary?.[name];
  if (i !== undefined) m.morphTargetInfluences[i] = v;
});
set('eyes_big', 0.5);
```

注意:MPFB 的 `nose-scale-depth-decr` 目標套在原版 MPFB 上就會造成網格翻面,不要做成滑桿。
