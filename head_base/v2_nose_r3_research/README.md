# V2 鼻部 R3 與貼圖試驗（2026-10-28）

- `head_nose_r3.glb`：使用者暫時選用的 Claude 鼻部 R3 原版，來源 ideal_hero commit `6834d54`，完整流程與驗證見原專案 `outputs/unity_v01/nose_rebuild_v001/README.md`。來源 SHA256 `83328f7f2fe7dda6164bd74058c6d44079ffc27bb84d1f1f2593e99c5b429fdf`。這是從 ideal_hero 的 v005 基準修出，不是直接以 model_zoo 原始 v2 檔為輸入，v005 已修頭型。
- `head_nose_r3_texture_trial.glb`：Codex 局部貼圖試驗，依鼻底面片 UV 蒙版、羽化及模糊淡化舊暗色，並未重繪鼻孔。原始嵌入 JPEG 轉 PNG；現有 UV 島的位置受到保留，但有近 54,731 個蒙版影響像素。不是最終版，需使用者確認。
- 效果：鼻底碎色減淡；鼻孔層次也變淡。正面畫面左側黑影在中性材質仍可見，顯示單獨貼圖不能消除該黑影；尚未隔離究竟是幾何、法線或照明影響。無法宣稱完全修復。`review.html` 為原 R3 / 試驗多角度比較。
- 靜態 GLB 檢查：mesh、accessor、node、skin、animation、material、texture 項目相同，且原始二進位 buffer 被完整保留；只新增 bufferView 並替換 body 的 basecolor 圖片引用。詳見 validation.json。這不是 Blender 匯入往返或形態鍵運動完整測試。
- 目前未測滑桿組合、動畫、髮型和實際遊戲場景；沒有 Blender 工程檔、原始參數或新的可重建 shape_final.npz。故此資料夾是獨立實驗版本，不覆蓋原 `head_base/v2`，不可當成完整 v3 來源工程。
- `extract_uv.py` 與 `repair_texture.py` 為實際使用的研究腳本，路徑指向當時本機工作目錄；重現需依實際位置調整路徑。`uv_triangles.json`、`texture_mask.png` 是修色範圍記錄。
