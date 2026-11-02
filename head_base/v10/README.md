# head_base v10：微笑／大笑重做＋上排牙與口腔＋ARKit 表情鍵

2026-11-02，Claude。狀態：**目前工作快照**（微笑、大笑 G 版、牙齒、ARKit 眨眼使用者已核可；閉眼的兩處瑕疵**待修**，見「已知問題」1、2）。

## 從哪版來

- 上一版：v9（`head_base/v9/head_base_v9.blend`）。
- 來源：3D_model_design main `7bd32ee`，設定 `versions/v10.json`、`versions/v10_presets.json`，由 `tools/build_version.py v10` 產生。
  - `head_base_v10.fbx` SHA `bee4a327…`（建置輸出原名 `head_base_v10_game.fbx`）。

| 檔案 | 內容 |
|---|---|
| `head_base_v10.fbx` | 遊戲用 FBX；骨架、權重同 v9 |
| `head_base_v10.blend` | 母檔，貼圖已打包；所有形態鍵預設 0 |
| `head_base_v10_tex.glb`／`_clay.glb` | 貼皮／灰模交換檔，有骨架和形態鍵；貼皮用普通型皮膚 |
| `skins/skin_{normal,thin,lean,muscular,fat}.png` | 五型手繪皮膚（4096²），v9 的皮膚加上口腔內部上色、大笑嘴角黑線補色、耳背灰褐色團改平 |
| `basecolor.png`、`eyebrow.png`、`eye.png`、`lashes.png`、`body_paint_balanced.png`、`body_joints.json` | 和 v9 相同 |
| `expressions.json` | ak_ 鍵清單、哪些審過、微笑／大笑組合 |
| `compare_vs_v9.png` | 和 v9 同鏡頭比較（Blender Cycles，不是遊戲畫面） |
| `review/` | 檢查圖，見「已驗證」 |

預想照：沿用 `../v9/reference/expr_smile_laugh_v001.png`（左微笑、右大笑），使用者以它為目標；和 v10 並排在 `review/預想圖vs_v10.png`。

## 改了什麼

1. **ARKit 表情鍵**：新增 51 個 `ak_` 鍵（ARKit 52 鍵命名，沒有 `tongueOut`）。
   - 從 MPFB faceunits01（CC0）轉移；Body 51、Brows 32、Lashes 23。
   - `ak_eyeBlinkLeft/Right` 不用 MPFB 轉來的形狀，直接等於 v9 核可的 `ex_eye_{left,right}_closure`（轉來的會把眼線壓成一大塊黑色）。
2. **微笑／大笑組合**（`expressions.json` 的 `presets`）：
   - 微笑：嘴角上揚 0.75、臉頰上提 0.7、瞇眼 0.35。
   - 大笑（使用者選定 G 版）：張嘴 0.42、下唇下拉 0.8、嘴角拉寬 0.95、嘴角上提 0.8、瞇眼 1.0 等，不做到月牙眼。
3. **局部平滑修正**：微笑嘴角倒勾（`ex_mouth_corner_puller`）、左臉頰上提時左下眼皮撕裂（`ak_cheekSquintLeft`）。
4. **新物件 `Mouth`**：上排 12 顆牙（每側 6 顆，最外兩顆調暗），掛頭骨。
   - 只有 6 個捏臉鍵（跟著嘴型寬窄等走；嘴窄時外側臼齒內縮），做表情時牙齒不動。
   - 閉嘴、微笑都看不到牙。
5. **皮膚貼圖**：張嘴才看得到的口腔面塗深色，加舌頭色與唇色漸層；大笑嘴角外側的深色唇線補膚色；耳背灰褐色團改平（五型都改）。

沒變的部分：骨架 52 根；靜止姿勢和 v9 比 .blend 差 0 mm、FBX 差 0.0008 mm；v9 的 98 個 Body 鍵原樣保留。

形態鍵數量：

| 物件 | v9 | v10 |
|---|---|---|
| Body | 98 | 149 |
| Brows | 63 | 95 |
| Lashes | 62 | 85 |
| EyeL／EyeR | 42 | 42 |
| Mouth（新） | — | 6 |

## 已驗證

- 4 個檔案回讀（blend、fbx、兩個 glb）：骨架 52 根；鍵數如上表；預設值全部 0。
- 和 v9 同鏡頭比較（`compare_vs_v9.png`）：中性臉正面、3/4、側面、灰模相同；微笑、大笑、閉眼並排。
- 捏臉極值配表情（`review/teeth/0_*`）：12 個嘴／下巴／下顎／臉型鍵各拉到 1，各配微笑和大笑；牙齒沒穿出嘴唇、嘴角沒撕裂、口腔上色沒露出。
- 牙齒（`review/teeth/3_*`）：一般、嘴寬、嘴窄、下巴長配大笑；閉嘴、微笑看不到牙。
- 五型體型（標準、瘦、精實、壯、胖）配對應皮膚，各看中性、微笑、大笑（`review/body/1_*`、`2_*`，Cycles）：體型對臉幾乎沒影響，沒有新問題。
- ARKit 眨眼修正前後（`review/body/6_*`）：半閉、閉眼正常。

## 未驗證

- 微笑、大笑、眨眼以外的 `ak_` 鍵沒有逐一重審。
- v8 沿用的其他 `ex_` 表情鍵（驚訝、生氣、難過等）沒有重審。
- 多個捏臉鍵疊加後再做表情；捏臉極值配閉眼。
- 超圓體型（`body_round`）配表情。
- Unity 實機匯入、遊戲卡通 shader 外觀。
- 背面比較圖。

## 已知問題（待修）

1. **閉眼時正面看，上眼皮的眼線露出一小片三角形**（`review/body/10_已知問題_閉眼眼線三角形.png`）。
   - 原因是貼圖：眼線畫在上眼皮皮膚上（貼圖裡是月牙形，中段最粗）。睜眼時那塊皮膚朝上被壓扁，看起來是粗眼線；閉眼時轉向正面，中段露出來。
   - 試過但沒採用：
     - 貼圖上把眼線修細：閉眼變成一條線，但睜眼的眼線變得斷斷續續。
     - 眼線改成獨立零件，閉眼時收成一條線：試 1 次，睜眼和原本一樣，但半閉、閉眼、大笑時眼線陷進皮膚。使用者決定不用。
2. **閉眼時外眼角上眼皮折出尖角**（`review/body/7_已知問題_閉眼外眼角尖折.png`）。v9 的閉眼鍵本來就有；眼線畫在那片面上，側面看像凸起。
   - 試過局部平滑 2 次：尖角變平，但外眼角的縫裂開、看得到眼白。沒採用。
3. 牙齒每顆比預想圖大，看得出一格一格；預想圖比較像一條細白帶。
4. 嘴型最窄（`mouth_narrow`）或嘴唇最厚（`lips_full`）配大笑時，灰模上嘴角有細小尖褶，貼皮幾乎看不出來。
5. 小瑕疵，打光／貼皮後看不出來：左耳背純貼圖上有淡淡的小圓圈；灰模上瞇眼時左眼外眼角有細碎起伏。
6. 從 v9 沿用：右眼內眼角凸塊；閉眼時上眼皮直條拉伸；`ex_mouth_open` 建議最大 0.5；超圓體型 2 處小三角形翻折、沒有專用皮膚。
7. FBX 的貼圖不是內嵌的：匯入時要自己指定 `skins/` 和同資料夾的 png。
8. glb 匯入 Blender 時會多出一個 `Icosphere`，是匯入器畫骨頭用的，不在檔案裡。

## 下一步

| 要改什麼 | 誰改 | 開始條件 |
|---|---|---|
| 已知問題 1、2：閉眼眼線三角形、外眼角尖折 | 待定（3D_model_design 或美術 session） | 使用者決定做法；不用眼線零件 |
| 其他表情（驚訝、生氣、難過）與 ak_ 鍵逐一重審 | 3D_model_design | 無 |
| Unity 實機匯入測試 | 待定 | 無 |
| 牙齒更細、更像一條白帶 | 3D_model_design | 使用者提出 |
| neck_platysma 接縫 | 3D_model_design | 無 |

做完任何一項就開新版本（v11），不覆蓋 v10。

## 怎麼重做

在 3D_model_design（commit `7bd32ee`）：

```
python3 tools/build_version.py v10                  # 全部步驟，約 10 多分鐘
python3 tools/build_version.py v10 --steps package,interior,paint,package,assets,verify,review
```

輸出在 `build/v10/out/`：`head_base_v10_game.fbx` 改名成這裡的 `head_base_v10.fbx`，其他檔名相同。上一版從 model_zoo 的 `head_base/v9/head_base_v9.blend` 讀；ARKit 鍵的來源是 MPFB faceunits01（`incoming/faceunits01/`）。
