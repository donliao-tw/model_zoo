# V2 R3 鼻底貼圖候選 v002（研究用）

2026-10-28。以使用者暫時選用的 Claude `head_nose_r3.glb` 為基準。原版在 `../../head_base_v3_tex.glb`；未覆蓋。

## 本次處理與觀察
鼻底面片 UV 遮罩內做 16 像素半徑、45% 強度的羽化模糊，參數比前次（50 像素、90%）保守；這仍是區域模糊，**不是逐一辨識並重繪髒污**，所以不能說已達成精準重繪。正面與仰視鼻底碎色稍微淡化，但改善有限，部分紋理仍在；鼻孔明暗保留比前次較多，外觀仍待使用者確認。`before_after.png` 左修前、右修後；兩排分別為正面及仰視，皆為 Blender 渲染，不是 Unity toon shader。

畫面左鼻翼黑影為獨立問題：單色材質時仍存在；使用者認為目前 Unity toon 實拍不明顯，這次沒有修改它。

## 資料與限制
- `texture_v002.glb`(原 `head_nose_r3_texture_v002.glb`,與 `../../../v4/head_base_v4_tex.glb` 逐位元相同)僅替換 skin basecolor 圖片，GLB 原 buffer 前綴逐位元保留；mesh、accessor、node、skin、animation、material、texture 的 JSON 相同。`validation.json` 記錄；這不是 Blender 往返、滑桿動畫、Unity 或 shader 驗證。
- 有 50,532 像素變化，遮罩外 0；含模糊羽化與原 JPEG 解碼。素材採 Pillow 與 NumPy 處理；`repair_texture.py` 是原始實驗腳本，含當時本機路徑，移機需修改。原 V2 仍保留。
- 遮罩按鼻底幾何面片範圍選取，並非髒污的像素級分割；未作手繪風格重繪，也尚未用遊戲鏡頭比較。此為候選，不交付 Unity 正式角色。


## 完整頭部與耳朵檢視
使用 Blender Cycles、16 samples，模型形態鍵歸零，在同一個鏡頭和燈光輸出 `full_head_5views.png`（鼻底候選版）及 `full_head_before_after.png`（左 R3、右候選，正面／側面）。本次未改耳朵。側面可見耳朵上緣與耳後輪廓不夠平順；影像不足以斷言成因，尚未做耳部細節、捏臉或 Unity 驗收。頭部保留 v005 修過耳上突出頭型，但非耳朵完整修復。`render_full.py` 為實際使用的渲染腳本，輸出路徑需依工作環境調整。
