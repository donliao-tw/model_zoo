# model_zoo

SRAM 員工角色(捏臉系統)的模型與參數庫。每個模型都有版本、參數檔和目前進度。

## 目錄

| 分類 | 路徑 | 內容 |
|---|---|---|
| 底模(頭 + 全身) | [`head_base/`](head_base/) | 可捏臉的男性底模,依版本分資料夾 |
| 零件 | [`parts/`](parts/) | 可替換的零件:眼睛貼圖、眉毛、睫毛 |
| 風格 | [`styles/`](styles/) | 渲染風格設定(動漫 / 偏迪士尼) |
| 預覽圖 | [`previews/`](previews/) | 各版本的渲染與近拍 |
| 其他實驗 | [`experiments.md`](experiments.md) | 做過但沒採用的模型與原因(檔案不放這裡) |

## 進度總覽

| 模型 | 狀態 | 一句話 |
|---|---|---|
| [head_base v1](head_base/v1/) | 停用 | 第一次打包;鼻子破損(灰模近拍可見),不要拿來用 |
| [head_base v1.1](head_base/v1.1/) | 停用 | 只改 v1 的貼圖(鼻孔污漬變淡),形狀同 v1 |
| [head_base v2](head_base/v2/) | 保留 | 眼袋修正、眉毛、畫風眼睛、淡腮紅;鼻子和眼皮細線未修 |
| [head_base v3](head_base/v3/) | 保留 | v2 的 v005 頭型 + Claude 鼻部 R3(另一專案 ideal_hero) |
| [head_base v4](head_base/v4/) | 保留 | v3 + 鼻底貼圖 v002;只有 glb 快照 |
| [head_base v5](head_base/v5/) | 保留 | v4 + 鼻翼黑影(法線)、耳朵平順、眼線接到眼皮邊緣、睫毛 0.35、眉毛對稱、鼻子更挺 |
| [head_base v6](head_base/v6/) | 保留 | 遊戲模型快照：眼球修復、手繪眉、眼窩與睫毛調整；含已知限制 |
| [head_base v7](head_base/v7/) | 保留；壯碩畫層已核可 | 現用56鍵body（含10舉手修正鍵，10/30 更新）＋42鍵部件、52骨、各體型關節偏移，附胸背手臂大小腿畫層與兩強度 |
| [head_base v8](head_base/v8/) | **目前工作快照** | v7 + 33 個表情形態鍵（MPFB 表情單元，眨眼/微笑/張嘴/眉毛等）＋6 個表情組合；閉眼貼圖待重畫 |

## 共通規格

- 網格:MPFB 2 標準人體(MakeHuman hm08 基礎網格,CC0),V1–V5 基於相同人體；V6–V7 遊戲快照的眼球移除角膜殼、眉毛更換，不能假定所有部件頂點及零件互換，需實測。
- 單位公尺;glb 為 Y 朝上。
- 命名:每個版本資料夾 `head_base/vN/`,主檔 `head_base_vN_tex.glb`(貼皮)/ `_clay.glb`(灰模)/ `.blend`;研究或試驗放在該版本的 `research/`。
- 物件:`body`(全身,無衣服頭髮)、`eye_L` / `eye_R`(眼球,原點在球心,轉物件即可轉眼珠)、`lashes`、v2 起有 `brows`。
- 玩家滑桿:V1–V5 為 28 個 morph target(14 對)；V6有42鍵；V7 body有56鍵（42五官＋4體型＋10舉手修正，修正鍵由遊戲自動驅動），其他部件42鍵，組合仍待驗；V8 再加 ex_ 開頭的表情鍵（body 33、brows 15、lashes 14），見 `head_base/v8/expressions.json`。同名 morph 要同時設到所有物件,眼球、睫毛、眉毛才會跟著走。對照表在各版本的 `morphs.json` 與 [`head_base/README.md`](head_base/README.md)。
- 皮膚貼圖:從 AI 生成的頭(head02)烘到 MPFB UV,4096²。

## 產生方式

V1–V5 主要由 `3D_model_design` 專案的 `pipeline/` 腳本產生；V6–V7源於 ideal_hero 的 Unity 工作快照，見 V6 說明。V1–V5 主要腳本為 `pipeline/blender/package_head.py` 與 `pipeline/blender/wrap_final_render.py`，詳細過程記在該專案的 `docs/開發歷程.md`。
