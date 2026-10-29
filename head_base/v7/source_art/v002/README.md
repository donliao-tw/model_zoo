# 壯碩上半身陰影 v02：實際遊戲比較與製作紀錄

2026-10-29，Codex。使用者尚未驗收畫風；不是完整五體型或正式模型替換。

本輪將密集胸腹漸層改成較疏暖棕筆觸，補肩臂／前臂、側腹和背。原 FBX、骨架、皮膚、頭臉與腿部未改。實際遊戲測過舊版、僅正面、多視角淡版、1.45倍、2倍共五組90張，正／斜／背、0.8／2／5.5m、大廳與遊戲。待機動作時序可能略不同，非逐像素比較。

## 給 Claude 的整合方式

1. 本包 `atlases/V5_BodyPaint_v02_readable.png` 是2倍強度的遠距可讀性候選；`balanced` 是1.45倍、`base` 是原始淡版。三張都已包含強度，`_BodyPaintStrength` 維持1，勿再乘一次。本包不決定正式預設，請先比較再由使用者驗收。
2. Atlas 2048×2048 RGBA，線性資料、sRGB關閉；R普通、G精瘦、B壯碩、A肥胖。只替換 **B**。R/G/A依35c6594時現用圖複製並驗證不變；若主線後來更新其他通道，請將B合併到最新圖，勿整張覆蓋新版本。
3. 不改 V5_Skin，不開回舊 Ink。這輪沒有新 FBX 或 .meta；Unity匯入由整合者處理。
4. 若重投影，`textures/muscular_{front,back,left,right}_gray.png` 是1730×2400 Raw線性資料，白=無陰影，mask=1-gray；四方向依template及body_muscular=1投影，以max合併，避免重疊加深。再只對B乘1.45或2。彩色層是引導用：RGB sRGB、直Alpha線性，勿與灰階雙重疊加。

## 已驗與未達

- 四方向彩色Alpha最大77/255；頭部與腰以下保護區Alpha為0。灰階與Alpha一致；原始多視角B最大77，均衡112，遠距154。R/G/A逐像素不變。
- 現用FBX、皮膚、BodyPaint與來源GLB仍符合開工SHA；前三組測試也記錄建置與真存檔未變。五組均使用存檔副本，未把測試圖寫進正式素材。
- 正／斜／背實際遊戲已自行看過；新版沒有模型改動，原灰模維持原樣。本輪不把這解讀為舊幾何所有問題已修復。
- 近看仍有平面筆觸與部分碎角，遠看腹肌較弱；最下排還不明確。沒有腿肌／其他體型新圖，尚未檢查所有戰鬥動畫、任意體型混合或第三方裝備遮罩。

## 來源、製作與回復

來源模型為現行r12：`outputs/unity_v01/body_paint_reference_v001/hero_v5_body_types.glb`；引用來源授權沿用專案原紀錄，本輪未重新授權。來源SHA見研究目錄source_checkpoint.json。

三張筆觸來源使用Codex內建ImageGen，實際模型版本未知；沒有使用外部API。實際提示詞與來源圖在研究目錄`sources/`。Blender4.5.3 LTS以現有關節／胸腹標記作薄板樣條對位，原生材質及遮擋正確的合成器出四方向，再用35c6594工具快照烘焙並啟動實際遊戲。最初透明幾何疊加造成側面Alpha過深，已改成渲染遮擋後由灰階取Alpha，重出全部圖層並重驗。

研究與90張原圖：`outputs/art_library/research/v5_body_paint_v002/`；入口review.html，可選強度／距離／燈光／方向。project_layers.py、projection_source.blend、bake_and_review.py、test_strength.py、validate_delivery.py、capture_review.py可查重現。工具快照含本機絕對路徑，換機須先調整ROOT並依SETUP重建環境；不取代Claude維護的正式工具。

舊v01未覆蓋；圖層初版檢查點592aa55。正式遊戲尚未替換，因此不需回復正式檔案。完整模型品質／全身畫風／玩家驗收未完成，看板維持進行中。
