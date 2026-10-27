# 其他實驗(未採用)

這些模型只記錄結論,檔案留在 `3D_model_design` 專案裡,不放進 model_zoo。

| 模型 / 方法 | 專案路徑 | 結果 | 為什麼沒採用 |
|---|---|---|---|
| AI 生成頭 head02 | `models/head02/` | 臉部好看,是 head_base 的擬合目標 | 網格不固定、五官不能換;顱頂偏大(頭頂→眼 : 眼→下巴 = 1.25) |
| TRELLIS(微軟,MIT)單張 / 多張 | `models/trellis_test/` | 多張 multidiffusion 最乾淨 | 臉部貼圖不夠銳利,網格不固定 |
| MPFB 調參頭(輪廓擬合) | `models/mpfb_head01–04` | 形狀接近參考圖 | 寫實人臉,動畫感出不來 |
| MPFB 社群動漫臉型 | `models/mpfb_anime_A/B` | — | 套在男性底模上不理想 |
| VRoid CC0 範例 | `models/vroid_cc0/` | 授權可商用,零件分開 | 臉型千篇一律、解析度低 |
| Blender Studio Human Base Meshes(CC0) | `models/blender_base/` | — | 美式卡通臉或雕刻起點,不適用 |
| 模板擬合第 1、2 次(一次全包) | `models/wrap01`、`wrap02` | 失敗 | 沒有五官對應,眼球浮在額頭;另有形狀鍵重複疊加的 bug |
| 鼻子修復分支(放鬆 / 移植 / 原生鼻 / 鼻尖選項) | `models/wrap03/nose_*`、`nv*` | 失敗 | 鼻翼腫、多一層唇、巫婆鼻;已回到 v1 鼻子 |
