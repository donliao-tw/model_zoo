# Head Base V4

2026-10-28：使用者指定將目前看到的鼻底貼圖候選存為 model_zoo V4。此資料夾保存 V4 的現有交付快照，不覆蓋 v1、v1_1、v2 或研究版本。

## 檔案

- `head_base_v4_tex.glb`：實際使用者查看的 V2 頭型 v005 → Claude 鼻部 R3 → Codex 鼻底貼圖 v002 的模型。GLB 含 body 等網格，不是切離身體的獨立頭部；來源 SHA256 `90cfad66c8c3b2f3c0a141643ad1a406163134dfd734ad83a8f91ca592be8a02`。
- `basecolor.png`：從上面 GLB 實際嵌入的皮膚貼圖提取；不是另外重繪的貼圖。
- `full_head_5views.png`：同一模型完整頭部正面、雙斜面、雙側面；`full_head_before_after.png` 與 `nose_before_after.png` 為修前／修後比較，Blender 渲染。
- `texture_validation.json`：與 Claude R3 原版的靜態 GLB JSON 和原 buffer 比對。

## 來源與限制

來源研究 `../v2_nose_r3_research/` 及 `../v2_nose_r3_texture_v002/`，前者保留 Claude R3 和其來源資訊；理想圖是 2D 參考。V4 沒有獨立 `.blend`、灰模 GLB 或對應的新 `shape_final.npz`／params，請勿把 v2 的檔案冒充成 V4 來源。GLB 保留 R3 的形態鍵，但鼻尖向下拉滿外觀不自然；混合滑桿、動畫、實際 Unity 遊戲情境尚未驗證。V4 的鼻底貼圖只是局部保守模糊，碎色仍有，並非完成手繪重畫。耳上頭型沿用之前修整，耳朵上緣／耳後尚有不平順，本次未修耳。左側鼻影在現有 Unity toon 近拍比較不明顯，但未在所有光照下驗證。
