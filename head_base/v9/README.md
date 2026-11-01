# head_base v9：閉眼重做＋超圓體型＋五型手繪皮膚

2026-11-02，Claude。狀態：**目前工作快照**（閉眼使用者已核可；其他表情鍵未重審）。

## 從哪版來

- 上一版：v8。
- 來源：ideal_hero main `a16d09f3`。
  - 模型：`unity/IdealHero/Assets/Characters/HeadBaseV5_v01/HeadBaseV5.fbx`，SHA `b7a236a6…`。
  - 遊戲裡的檔名 `HeadBaseV5` 是舊命名，跟 zoo 版本號無關。
- 這版不是重新雕刻，是把美術已交件、目前在用的模型原樣收進來。

| 檔案 | 內容 |
|---|---|
| `head_base_v9.fbx` | 來源 FBX 原樣副本；骨架、權重、頂點色以它為準 |
| `head_base_v9.blend` | 從 FBX 匯入、貼圖已打包的母檔；所有形態鍵預設 0 |
| `head_base_v9_tex.glb`／`_clay.glb` | 貼皮／灰模交換檔，有骨架和形態鍵；貼皮用普通型手繪皮膚 |
| `skins/skin_{normal,thin,lean,muscular,fat}.png` | 五型手繪皮膚（4096²） |
| `basecolor.png`、`eyebrow.png`、`eye.png`、`lashes.png` | 舊底皮膚與部件貼圖，和 v8 相同 |
| `body_paint_balanced.png` | 肌肉畫層，和 v7／v8 相同 |
| `body_joints.json` | 各體型關節偏移 |
| `garments/` | 基本內褲模型與貼圖 |
| `compare_vs_v8.png`、`review/` | 比較圖（Blender Cycles，不是遊戲畫面） |
| `validation.json` | 回讀驗證，以及和 v8 逐鍵比對的結果 |

## 改了什麼

和 v8 逐鍵比對（`validation.json` 的 `vs_v8`）：

1. **閉眼重做**：改了 `ex_eye_{left,right}_{closure,slit}` 4 個鍵（Body、Brows、Lashes 都有）。
   - 和 v8 的位移最大差：Body 9.2 mm、Lashes 14.5 mm。
   - 結果：上眼皮整片深色的問題（v8 已知問題 1）解決，閉眼只剩一條線加睫毛。
   - 睫毛縮短到 60%，眼線壓到 45%。
2. **新增 6 個閉眼修正鍵** `ex_corr_blink_{left,right}_{eyes_big,upper_lid_open,lower_lid_open}`。
   - Body、Brows、Lashes 都有。
   - 修正鍵的權重 = 該側閉眼值 × 對應捏臉鍵值。不是玩家滑桿。
3. **新增超圓體型**：`body_round` 加 2 個舉手修正鍵 `fix_armup_round_{L,R}`，只在 Body 上。
   - `body_joints.json` 只新增 `body_round` 一組，其他體型逐值相同。
4. **五型手繪皮膚**：新增 `skins/`。超圓型還沒有專用皮膚。
5. **新增內褲**：`garments/`。

沒變的部分：
- 靜止姿勢和 v8 差 0.0003 mm。
- 骨架仍是 52 根。
- Body 其餘 85 個鍵和 v8 相同：42 個捏臉、4 個體型、10 個舉手修正、v8 的另外 29 個表情鍵。

形態鍵數量：

| 物件 | v8 | v9 |
|---|---|---|
| Body | 89 | 98 |
| Brows | 57 | 63 |
| Lashes | 56 | 62 |
| EyeL／EyeR | 42 | 42 |

## 已驗證

- 4 個檔案都回讀檢查過（FBX、blend、兩個 glb）：
  - 骨架 52 根；
  - 鍵數如上表，全部預設 0；
  - 靜止姿勢和 FBX 比對：blend 差 0；glb 最近點最大 0.0013 mm（glb 會在 UV 接縫拆點，Body 71,538 點對 70,583 點）。
- 和 v8 同鏡頭比較（`compare_vs_v8.png`）：
  - 正面、35°、側面、閉眼特寫、全身、灰模都看過。
  - 臉形和 v8 一樣，閉眼明顯改善。
- 超圓體型灰模正面、側面（`review/body_round_sheet.png`）。

## 未驗證

- v8 的另外 29 個表情鍵（眉 8、嘴 13、鼻 6、睜大 2）原樣沿用，**沒有重新審過**。（美術交件寫「27 個」，實數是 33 − 4 = 29。）
- 多個捏臉鍵疊加後再閉眼；瞇眼配捏臉鍵（沒有修正鍵）。
- 閉眼疊其他表情；超圓體型疊表情。
- 超圓體型在動作中的關節轉軸。
- 背面沒有出比較圖。
- 比較圖是 Blender 預覽，不是遊戲裡的卡通 shader。

## 已知問題

1. 角色右眼內眼角有凸塊（底模本來就有）。
2. 閉眼時上眼皮皮膚有直條拉伸。
3. 嘴裡沒有牙齒和口腔內襯。笑臉改善（v11）還在研究，沒有收進這版。
4. `ex_mouth_open` 建議最大 0.5。
5. 超圓體型：
   - 還有 2 處單一小三角形翻折（左腋窩、右腳趾）；
   - 沒有專用皮膚。
6. glb 匯入 Blender 時會多出一個 `Icosphere`，是匯入器畫骨頭用的，不在檔案裡。

## 怎麼重做

用 Blender 4.5.3 執行。`<src>` 是 ideal_hero 的 `unity/IdealHero/Assets/Characters/HeadBaseV5_v01`。

```
copy <src>/HeadBaseV5.fbx head_base_v9.fbx
copy <src>/BodySkins/V5_Skin_<型>_Handpaint.png skins/skin_<型>.png
blender -b --factory-startup --python scripts/build_v9.py   -- <src>/HeadBaseV5.fbx skins/skin_normal.png .
blender -b --factory-startup --python scripts/verify_v9.py  -- ../v8/head_base_v8.blend . validation.json
blender -b --factory-startup --python scripts/render_v9.py  -- ../v8/head_base_v8.blend head_base_v9.blend review
python scripts/compose_v9.py .
```

`build_v9.py` 要讀來源資料夾的原 FBX，不能用複本：FBX 用相對路徑找貼圖。

閉眼和修正鍵的做法：ideal_hero art 分支 `outputs/art_library/research/v10_blink_smile_redo_v001/README.md`。超圓體型：同分支 `outputs/art_library/research/round_body_v001/README.md`。
