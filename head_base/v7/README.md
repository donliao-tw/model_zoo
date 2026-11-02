# head_base v7：當時的遊戲模型＋核可壯碩身體畫層

2026-10-29 Codex 發布，2026-10-30 Claude 更新。狀態：**保留；壯碩胸背、手臂、大小腿畫層使用者已核可**（整個頭臉、全體型、動畫不是因此定案）。

## 從哪版來

- 上一版：v6（ideal_hero 7a86892）。
- 10-29 版：模型與皮膚取 ideal_hero 9599364，身體畫層取 art 4e0f660。不是重新雕刻。
- 10-30 更新：換成 ideal_hero da407ae 的模型（FBX SHA `df782d…`）。

| 檔案 | 內容 |
|---|---|
| `head_base_v7_game.fbx` | 來源 FBX 原樣副本；骨架、權重、頂點色以它為準 |
| `head_base_v7.blend` | 從 FBX 打包貼圖的母檔；所有形態鍵預設 0 |
| `head_base_v7_tex.glb`／`_clay.glb` | 中性貼皮／灰模交換檔，有骨架和形態鍵 |
| `head_base_v7_muscular_preview.glb` | 壯碩體型＋1.45 倍畫層的**靜態展示**，沒有骨架和滑桿 |
| `basecolor.png`、`eyebrow.png`、`eye.png`、`lashes.png` | 皮膚與部件貼圖 |
| `body_paint_balanced.png`／`_strong.png` | 2048 RGBA 線性資料，肌肉畫層已乘 1.45／2 倍；不是基礎色 |
| `body_paint_legs_unscaled.png` | 腿部未乘強度的 B 遮罩 |
| `muscular_preview_basecolor.png` | 展示檔用的合成色，不是新的皮膚 |
| `body_joints.json` | 各體型關節偏移（10-30 新增） |
| `params.json`、`morphs.json`、`structure.json`、`validation.json`、`source_audit.json` | 參數、滑桿組成、結構、驗證、來源稽核 |
| `compare_vs_v6.png`、`compare_vs_v7_before.png`、`review/`、`review.html` | 比較圖 |
| `source_art/` | 身體畫層的生圖提示詞與輸入 |

## 改了什麼

- 換成當時的遊戲模型，拓撲和 v6 不同：body 70,583 點，不能逐點沿用 v6 的形態或 npz。
- 4 個體型鍵 `body_thin/lean/muscular/fat`，只在 body 上。中性是四鍵全 0，單體型設 1；不建議全部拉滿混用。
- 壯碩身體畫層：v03 精簡胸肩、胸腹中線；v04 補前後側大腿和小腿。膝、踝減淡；臀胯和腳沒有新增筆觸。1.45 與 2 倍都收錄，沒有選定正式強度。
- 10-30 更新：
  - 肩、肘、膝權重平滑（重綁）。
  - body 新增 10 個舉手修正鍵 `fix_armup_<normal|thin|lean|muscular|fat>_<L|R>`，共 56 鍵（42 捏臉＋4 體型＋10 修正）。修正鍵依上臂抬起角度（90°→150°）自動套用目前體型那一個，不是玩家滑桿。
  - 新增 `body_joints.json`。
  - 貼圖和 10-29 版雜湊相同。

## 已驗證

- tex／clay 回讀：52 骨，body 46 鍵（10-29 版）、其他部件 42 鍵，全部預設 0。
- basis 和各鍵以最近點對應，最大誤差約 0.0015 mm（不是逐點拓撲相同的證明）。
- 10-30 更新後靜止姿勢和 10-29 版像素差 0（`compare_vs_v7_before.png`）；差別只在動作，見 `review/blender_armup_cmp.png`。
- 展示檔另對 `body_muscular=1` 的座標驗證過。
- 主 GLB 和 strong 畫層另從遠端全新下載核對 SHA。

## 未驗證

- 其他體型的畫層、完整屈膝、戰鬥動作、任意混形、衣服遮罩。
- NoseShade 各通道語意、蒙皮權重和骨軸沒有逐項比對，所以以 FBX 為準。
- 比較圖是 Blender 光照，不是卡通 shader。

## 已知問題

1. 沒有完整 19,158 點的 `shape_final.npz`：拓撲已改，v6 的部分 npz 不能沿用，也沒有偽造。
2. GLB 匯出時有頂點色／材質採樣警告；回讀有 Color 層。
3. 中性 GLB 只顯示基礎皮膚，看不到肌肉畫層；要看請開展示檔。

## 下一步

| 要改什麼 | 誰改 | 開始條件 |
|---|---|---|
| 表情鍵 | 美術 | 已做，見 v8、v9 |
| 其他體型的皮膚 | 美術 | 已做五型手繪皮膚，見 v9 |
| 肌肉畫層正式強度（1.45 或 2 倍） | 使用者決定 | 未決 |

## 怎麼重做

```
blender -b --python scripts/zoo_v7_build.py
blender -b --python scripts/zoo_v7_verify.py
blender -b --python scripts/zoo_v7_render.py          （和 v6 比較）
blender -b --python scripts/zoo_v7_render_update.py   （10-30 新舊 v7 比較）
```

腳本裡寫的是當時的本機暫存路徑，重做前要改成實際路徑。執行紀錄在 `scripts/*.log`。

生圖提示詞與輸入：`source_art/README.md`。來源模型沿用 MPFB／MakeHuman hm08 CC0。
