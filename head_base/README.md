# head_base:可捏臉的男性底模

## 新版本怎麼上架（v7 起統一）

不管是哪個 session、哪個分支改的模型，上架都照這份。只寫模型本身，不寫遊戲怎麼整合。

### 資料夾

```
head_base/vN/
  README.md                固定 7 段，見下
  manifest.json            欄位見下；files 由 scripts/write_manifest.py 產生
  head_base_vN.fbx         來源 FBX 原樣副本（v7、v8 叫 head_base_vN_game.fbx）
  head_base_vN.blend       可編輯母檔，貼圖打包，所有形態鍵預設 0
  head_base_vN_tex.glb     貼皮交換檔
  head_base_vN_clay.glb    灰模交換檔
  *.png                    貼圖
  compare_vs_v<上一版>.png 同鏡頭比較：至少正面、斜側、側面、灰模
  review/                  其他檢查圖
  reference/               預想照（目標長相）與生圖提示詞；有才放
  scripts/                 重做用的腳本
```

**不覆蓋舊版**：改了就開新版本號。

### README 的 7 段

開頭一行寫標題、日期、誰做的、狀態（保留／目前工作快照／停用，以及使用者核可了什麼）。

1. **從哪版來**：上一版、來源 repo／commit／檔案和 SHA；附檔案表。有預想照就列出每張的內容和狀態（使用者選定／候選）。
2. **改了什麼**：和上一版比，逐項列；也寫沒變的部分。形態鍵數量有變就列表。
3. **已驗證**：實際跑過、看過的，附數字。
4. **未驗證**：沒做的檢查，照實寫。
5. **已知問題**：已知但沒修的。
6. **下一步**：表格「要改什麼／誰改／開始條件」。已被後續版本接手的寫「見 vN」。
7. **怎麼重做**：指令和腳本。

### manifest.json 欄位

| 欄位 | 內容 |
|---|---|
| `version`、`date`、`made_by`、`previous`、`status` | 同 README 開頭 |
| `source` | `repo`、`commit`、`file`、`sha256`（可加 `note`） |
| `bones` | 骨頭數 |
| `meshes` | 每個物件的 `verts`、`keys`（形態鍵數，不含 Basis） |
| `changes`、`verified`、`not_verified`、`known_issues`、`next` | 同 README 第 2～6 段的摘要 |
| `reference` | 選填，預想照：`{檔名: 內容與狀態}` |
| `extra` | 選填，該版特有的欄位 |
| `files` | 每個檔案的 SHA-256（腳本自動算；文字檔以 LF 換行計算，Windows 簽出成 CRLF 時會不同） |

產生方式：`python head_base/v9/scripts/write_manifest.py head_base/vN <spec.json>`，spec 寫上面除了 `files` 以外的欄位。

## 舊版資料夾的檔案（v1～v6）

V6／V7／V8／V9例外：完整shape_final.npz/HV未重建。V6僅有部分可見點；V7拓撲已改，不可沿用V6部分資料，以原FBX／Blender為準。詳各版README。

| 檔案 | 用途 |
|---|---|
| `head_base_vX_tex.glb` | 貼皮版(網頁 / 遊戲引擎直接載入) |
| `head_base_vX_clay.glb` | 灰模版 |
| `head_base_vX.blend` | Blender 原檔(貼圖已打包) |
| `basecolor.png` | 皮膚貼圖 4096²,MPFB UV |
| `shape_final.npz` | 最終頂點位置 `X`(MPFB 全部 19158 頂點,含輔助幾何)。重做時以它為準 |
| `params.json` | 全部參數:體型、各擬合階段的方法與滑桿值、修正、零件、已知問題 |
| `morphs.json` | 每個玩家滑桿由哪些 MPFB 目標組成 |
| `compare_vs_<上一版>.png` | 和上一版的比較(同鏡頭燈光;正面 / 斜側 / 側面 / 鼻子側面 / 鼻子斜側) |

## 版本

| 版本 | 狀態 | 來源 | 和上一版比較 |
|---|---|---|---|
| v1 | 停用 | 第一次擬合打包,鼻子破損 | — |
| v1.1 | 停用 | v1 只改貼圖 | [圖](v1.1/compare_vs_v1.png) |
| v2 | 保留 | v1 + 眼袋、眉毛、畫風眼睛、腮紅 | [圖](v2/compare_vs_v1.1.png) |
| v3 | 保留 | v2 頭型 v005 + Claude 鼻部 R3(ideal_hero) | [圖](v3/compare_vs_v2.png) |
| v4 | 保留 | v3 + 鼻底貼圖 v002 | [圖](v4/compare_vs_v3.png) |
| v5 | 保留 | v4 + 法線 / 耳朵 / 眼線 / 睫毛 / 眉毛對稱 / 鼻子更挺 | [圖](v5/compare_vs_v4.png) |
| v6 | 保留 | 以 Unity 現行 FBX 與貼圖封存，眼球修復、手繪眉、眼窩及睫毛調整；非最終美術 | [圖](v6/compare_vs_v5.png) |
| v7 | 保留；身體畫層已核可 | 現用遊戲模型與壯碩胸背手臂大小腿畫層，1.45／2倍；10/30 更新重綁權重與舉手修正鍵 | [圖](v7/compare_vs_v6.png) |
| v8 | 保留 | v7 + 33 個 MPFB 表情形態鍵（ex_*）；閉眼眼皮貼圖待重畫、口腔零件未做 | [圖](v8/compare_vs_v7.png) |
| v9 | 保留 | 遊戲現用模型：閉眼重做＋6 個閉眼修正鍵、超圓體型、五型手繪皮膚、內褲；其他 29 個表情鍵未重審 | [圖](v9/compare_vs_v8.png) |
| v10 | 保留 | v9 + 微笑／大笑重做、上排牙與口腔上色、51 個 ARKit ak_ 鍵；閉眼眼線三角形與外眼角尖折待修 | [圖](v10/compare_vs_v9.png) |
| **v11** | **目前工作快照** | v10 + 大笑重做（使用者在滑桿網頁調定，單一鍵 ex_laugh）、中性下顎後退 4.7 mm、上排牙重做；沒有下排牙；上唇內捲小波浪待修 | [圖](v11/compare_vs_v10.png) |

> **2026-10-28 修正**:v1、v1.1、v2、v5 的 glb / .blend 先前把 28 個捏臉 morph 的預設值存成 1(全部拉滿疊加),直接打開會看到巫婆鼻等變形。已全部改回 0(glb 只改 JSON 的預設權重,模型資料不變)。v4 沒有這個問題。對照 `v5/morph_default_fix.png`。

### v9 → v10 → v11 修了什麼(重點整理)

細節和驗證在各版的 README;這裡只列「修好了什麼」,以及到哪一版為止還沒修好。

**v9(以 v8 為基礎)**
- 閉眼重做:v8 閉眼時上眼皮整片深色,改成只剩一條線加睫毛(睫毛縮到 60%、眼線壓到 45%)。
- 新增 6 個閉眼修正鍵:大眼、上下眼皮張開的捏臉配閉眼時不會破。
- 新增超圓體型 `body_round`,加 2 個舉手修正鍵。
- 新增五型手繪皮膚、內褲。

**v10(以 v9 為基礎)**
- 微笑、大笑重做(大笑 G 版),新增 51 個 ARKit `ak_` 鍵。ARKit 眨眼直接用 v9 核可的閉眼形狀,不用轉來的(轉來的會把眼線壓成一塊黑)。
- 局部修正:微笑時嘴角的倒勾(`ex_mouth_corner_puller`)、左臉頰上提時左下眼皮撕裂(`ak_cheekSquintLeft`)。
- 新增上排牙 `Mouth`,閉嘴和微笑都看不到牙。
- 皮膚貼圖(五型都改):
  - 張嘴才看得到的口腔面塗深色,加舌頭色和唇色漸層。
  - 大笑時嘴角外側那條深色唇線,補成膚色。
  - **耳背的灰褐色團改平**:v9 手繪皮膚的兩邊耳背各有一大塊灰褐色。v10 在貼圖上把它換成周圍的膚色,但模糊時先轉成 8 位元,平滑的地方留下一圈圈淡淡的色階環(v10 README 已知問題 5「左耳背小圓圈」)。
- v10 還沒修好的:閉眼時上眼皮眼線露出三角形、外眼角尖折;嘴窄／唇厚配大笑時嘴角細尖褶。

**v11(以 v10 為基礎)**
- 大笑再重做,改成單一鍵 `ex_laugh`(使用者在滑桿網頁調定)。
  - MakeHuman 骨頭單元改在這張臉上量,**修好大笑時上唇中間的 V 形缺口**(以前是在 MakeHuman 原人體上量的)。
  - 唇內側跟著外皮走,**修好下唇下方穿出的白點**。
  - **修好上排牙凸在上唇前面、門牙頂端露出方形缺口**:牙齒位置由使用者調定。
- 中性臉下顎後退 4.7 mm(使用者核可的下巴形狀)。
- 上排牙重做:沿弧長排、每側 7 顆;張大嘴(`ak_jawOpen`)、嘟嘴(`ak_mouthFunnel`)時牙齒往後,不會從臉頰穿出。
- **耳背色階環修好**:同樣的去色團,改用浮點數模糊重算,一圈圈的色階環不見了(`v11/review/耳背貼圖_v9_v10_v11.png`:v9 色團 → v10 有環 → v11 平順)。
- 口腔內部依新的大笑重新上色(五型都改)。
- v11 還沒修好的:大笑時上唇往內捲、邊緣有小波浪;`chin_long` × 大笑口腔裡有暗色尖三角形;glb 材質是 BLEND;沒有下排牙;v10 的閉眼兩處瑕疵。

### v5(保留)
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
