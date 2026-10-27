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
| [head_base v1.1](head_base/v1_1/) | 停用 | 只改 v1 的貼圖(鼻孔污漬變淡),形狀同 v1 |
| [head_base v2](head_base/v2/) | **目前版本** | 眼袋修正、眉毛、畫風眼睛、淡腮紅;鼻子和眼皮細線仍待修 |

## 共通規格

- 網格:MPFB 2 標準人體(MakeHuman hm08 基礎網格,CC0),所有版本頂點數與 UV 相同,所以零件、貼圖、滑桿可以互換。
- 單位公尺;glb 為 Y 朝上。
- 物件:`body`(全身,無衣服頭髮)、`eye_L` / `eye_R`(眼球,原點在球心,轉物件即可轉眼珠)、`lashes`、v2 起有 `brows`。
- 玩家滑桿:28 個 morph target(14 對),同名 morph 要同時設到所有物件,眼球、睫毛、眉毛才會跟著走。對照表在各版本的 `morphs.json` 與 [`head_base/README.md`](head_base/README.md)。
- 皮膚貼圖:從 AI 生成的頭(head02)烘到 MPFB UV,4096²。

## 產生方式

所有檔案都由 `3D_model_design` 專案的 `pipeline/` 腳本產生(主要是 `pipeline/blender/package_head.py` 與 `pipeline/blender/wrap_final_render.py`),詳細過程記在該專案的 `docs/開發歷程.md`。
