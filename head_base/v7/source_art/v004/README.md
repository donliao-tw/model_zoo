# v04：壯碩大腿與小腿陰影候選

2026-10-29 Codex；art開始基準d816375，main觀察9599364。使用者授權補大小腿；尚非全體型美術定案。v03原檔保留。

## 本輪新增

大腿前側股四頭肌、後側及側面長形淡面，小腿後側腓腸肌與側面過渡。ImageGen三個來源在sources，實際prompt一同保存；工具內建、模型版本未知。以現有髖／膝／踝座標及TPS手動標記對位，不採生成腿長。左右側使用同一來源。來源模型授權沿既有provenance，本輪未獨立重驗第三方授權。

原生Blender4.5.3：腿骨權重分區、世界Z約0.075至0.900m，膝附近減淡峰值65%、踝／腿根淡出，5px柔邊。腿根／骨盆過渡刻意少畫，不新增臀或胯部陰影。腳不新增筆觸，模型幾何、UV、骨架、體型鍵都不動。

四方向灰階1730×2400 Raw線性，white=無陰影。先把腿層烘到獨立B遮罩，再分別乘1.45／2，與對應v03 atlas用max合併。不是在v03整張上再乘一次。R/G/A逐像素一致、腿遮罩外所有像素一致；源FBX／Skin／BodyPaint／GLB SHA均保持。資料與區域驗證見final_validation、merge_validation、source_checkpoint。

## 實際檢查

- 遊戲四組：v03/v04 × 1.45／2，各18張，共72張，兩場景、三距離、正斜背。相同存檔副本和相機；待機時序不同，非逐像素同姿勢。現用建置只提供18個鏡位，90度側面另由Blender檢查，勿宣稱遊戲側面也跑過。
- 原生Blender12張：修改前、修改後、灰模 × 正／斜／側／背。採最終2048UV貼圖，不是生成圖直接當模型；燈光是檢查用，不等於Unity shader。native/和before_after_legs_native.png有清楚標示。
- 遊戲5.5m看得到全腿，0.8／2m鏡頭多數腿在畫外；不能拿近鏡頭通過當腿細節驗收。review.html預設5.5m，提供同強度前後及Blender近照。

判讀：原本平白腿部有了長形肌肉明暗，膝／踝未加整圈刻線，正斜側背無明顯大面貼圖穿插；側面亮暗仍受現有幾何及燈光影響。個別長線仍有筆觸感，最細層次遠看會消失，2倍較明顯；使用者尚未驗收。不改v03原有胸肩、腋下與腹部場景硬陰影；固定姿勢查光需求仍有效。

未驗：所有戰鬥動畫、屈膝極端、任意體型混合、服裝遮罩。未畫其他四體型，不宣稱完整創角或全套完成，roadmap維持進行中。

## 重現與交付

project_layers.py／projection_source.blend出腿部層；bake_and_review.py用35c6594固定工具快照烘焙、合併及啟動現有遊戲；render_inspection.py出原生近照；validate_delivery.py／capture_review.py驗證與保存前後圖。檔案含本機絕對路徑，換機依SETUP調整；不取代Claude維護的正式工具。

交付inbox：body_muscular_paint_test_v04，兩張預乘強度atlas、獨立legs_only、四面圖層、相機／manifest／整合說明與前後圖。Claude只合併B至最新主線，不覆蓋最新其他通道；BodyPaintStrength=1，sRGB off。正式Unity素材沒有替換，沒有新FBX，不需回復模型。預設強度仍由使用者驗收後定。
