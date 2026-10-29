# Head Base V6（2026-10-29）

V6 是 V5 後「遊戲目前模型」的可回退工作快照；V5 保留。來源為 ideal_hero main 7a86892 的 Unity HeadBaseV5.fbx 與同資料夾貼圖，來源檔 SHA-256 見 params.json。模型以 Blender 4.5.3 從該 FBX 匯入後重新包裝，非重新雕刻；遊戲 Unity 工程未改。

## 與 V5 的變化

- 使用遊戲模型中烘入的眼窩前推及睫毛位置調整、眼下與耳後的既有處理。
- 右眼球角膜殼切除方式修正，兩隻眼球各 276 頂點。
- 原 V5 眉毛換為遊戲中的手繪眉網格；GLB 是單一目前形狀，不包括遊戲程式的三種眉型切換。
- 五部件各 42 個形態鍵（V5 的28個加14個眼皮、眼尾、眉毛控制），預設全0；52根身體骨骼。morphs.json 前28配方沿用V5來源紀錄，新增14鍵只記名稱、配方尚未重建。
- **頭部1.15** 由 Unity 執行時骨骼控制，沒有烘入這份模型；Unity toon shader與描邊也不包含。basecolor.png 是遊戲當時貼圖，含 Claude 五官投影測試筆觸與眼角清理，不是最終五官美術。
- 先前未通過的嘴唇及體型試驗未納入；微笑、表情骨架、肌肉體型皆未完成。

## 檔案

- head_base_v6_game.fbx：從 Unity 複製的原始 FBX，與來源 SHA 相同；遊戲頂點色／骨架資料的權威副本。
- head_base_v6_tex.glb、head_base_v6_clay.glb：貼圖與灰模 GLB；.blend 是打包貼圖的 Blender 編輯副本。GLB 為重新匯出，並非 Unity 材質逐像素一致；FBX頂點色用途是否完整保留到 GLB 尚未驗。
- basecolor.png、eyebrow.png、eye.png、lashes.png：來源 Unity 貼圖副本。
- params.json、morphs.json、validation.json、visible_reconstruction.json 記錄來源、限制和回讀。
- compare_vs_v5.png：Blender Cycles 同鏡頭、燈光的 V5/V6 正、斜、側及鼻部裁切；兩者材質不同，此圖不是 Unity toon 的 A/B。
- shape_final_visible_rebuilt.npz：以 V5 的可見頂點映射，重建 V6 13,380 個可見身體點；接縫複製點差0。**另外 5,778 個輔助點及 HV 沒重建，沒有完整的 shape_final.npz，不可將這份部分資料當完整包裝源。**

## 驗證與限制

重新讀入 FBX／貼圖 GLB：5 個部件均保留42鍵，預設0；對應頂點與各鍵逐索引最大位置差約0.0015mm，左右眼276點；詳 validation.json。已看正、斜、側及灰模預覽；非完整動作、表情、組合、Unity匯入或效能驗收。GLB 控制鍵與原FBX的骨架／權重完整語意及頂點色遮罩尚未全驗。使用者尚未確認 V6 為最終美術。來源及原始模型不可覆蓋。

- Blender 比較圖中手繪眉附近可見淺色條紋及接合問題，可能涉及材質、光線或網格；原因未做受控測試，與 Unity 外觀是否一致未驗證，需後續處理。
