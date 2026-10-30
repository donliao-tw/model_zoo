# Head Base V7：現用模型與核可壯碩身體畫層

> **2026-10-30 更新（Claude）**：換成 ideal_hero da407ae 的遊戲模型。
> - FBX 重建：肩／肘／膝權重平滑（重綁），body 新增 10 個舉手修正鍵 `fix_armup_<normal|thin|lean|muscular|fat>_<L|R>`，共 56 鍵（42 五官＋4 體型＋10 修正）；其他部件仍 42 鍵，52 骨不變。
> - 修正鍵不是玩家滑桿：遊戲依上臂抬起角度（90→150°）自動套用目前體型那一個，其餘保持 0。
> - 新增 `body_joints.json`：各體型骨頭位置偏移，遊戲執行時（BodyRig）搬動關節並重算綁定姿勢；鎖骨分擔舉手 35%、頭前後 0.92 也是執行時做，沒有烘進 FBX。
> - 貼圖（皮膚、眉、眼、睫毛、肌肉畫層）和 10/29 版雜湊相同，沒有變。
> - 靜止姿勢和 10/29 版完全一樣（`compare_vs_v7_before.png`，像素差 0）；差別只在動作時，見 `review/blender_armup_cmp.png`（Blender 舉手 150°）、`review/ingame_cmp.png`（遊戲中）。
> - 依 Codex 原腳本重跑打包與回讀驗證（V7_PACKAGE_OK、V7_READBACK_OK）；`scripts/zoo_v7_render_update.py` 是改成新舊 v7 對照的渲染腳本。下文「46鍵」等描述指 10/29 版。

2026-10-29。使用者已核可胸背、手臂、大小腿畫層並要求發布進版；整個頭臉、全體型或動畫不是因此全部定案。V6原檔保留。1.45與2倍都收錄，沒有擅自選正式預設。

## 選哪個檔案

|檔案|用途|
|---|---|
|head_base_v7_game.fbx|遊戲現用來源的原樣副本；骨架、權重、頂點色的權威檔|
|head_base_v7.blend|從原FBX打包貼圖的可編輯母檔；所有形態預設0|
|head_base_v7_tex.glb / head_base_v7_clay.glb|中性貼皮／灰模交換檔；有骨架與形態鍵；不包含Unity卡通shader|
|head_base_v7_muscular_preview.glb|壯碩體型＋1.45畫層的**靜態展示**；沒有骨架或滑桿，不能代替母檔進遊戲|
|basecolor.png / eyebrow.png / eye.png / lashes.png|來源皮膚與部件貼圖原樣副本|
|body_paint_balanced.png / body_paint_strong.png|2048RGBA線性資料，v03上半身＋v04腿，分別已乘1.45／2；勿當BaseMap|
|body_paint_legs_unscaled.png|v04新增腿部的未乘強度B遮罩；供回復／增量合併|
|muscular_preview_basecolor.png|Blender以平衡B與tint(.55,.46,.41)乘入基礎色的展示圖；不是新的權威Skin|

params／morphs／structure／validation／source_audit／manifest記錄版本與驗證。review.html、compare_vs_v6.png為上一版比較；review內另附本輪實際遊戲及腿部前後圖。原腳本一併封存，使用本機暫存路徑，重現前調整根目錄。

## 與V6的變化

V6來自ideal_hero 7a86892；V7模型／Skin取目前9599364時可核對的原始資產，身體畫層取美術4e0f660（發布開始202b406）。不是本輪重新雕刻模型。

- 現用body為70,583個來源頂點（GLB因接縫拆分成71,538），46鍵：42五官＋4個體型；其餘眉、眼、睫毛各42鍵。52骨。拓撲已不同於V6，不可逐索引互換V6形態或重建npz。
- 收錄body_thin／lean／muscular／fat；中性為四鍵全0，單體型各1。不建議任意全部拉滿混用。新增體型只套body，其他部件沒有這四鍵。
- 皮膚沿用目前遊戲來源；本輪核可的是壯碩畫層，不包含宣布五官所有問題修好。沒有烘入執行時頭部縮放或新表情綁定。
- V03精簡胸肩、胸腹中線，V04補前後側大腿和小腿；膝／踝減淡，臀胯及腳未新增筆觸。其他體型新畫層尚未畫。

## Claude整合

只把選定版本的 **B通道** 合併到最新V5_BodyPaint，R/G/A保持最新主線。PNG以線性資料匯入（sRGB off、A當資料、不作透明），BodyPaintStrength=1，兩檔已含強度。不要再將整張或v03上身乘一次。這輪畫層不需要換FBX；有模型需求時使用原FBX並先驗收，勿拿static preview替換rig。

frame/Unity測試證據在review與validation副本；主線正式素材未由Codex覆蓋，Claude仍須匯入／驗動作／記整合提交。原腋下紅棕與腹部移動陰影在關閉BodyPaint時仍存在，請固定姿勢查光照／接收投影／ShadowColor，勿用亮貼圖抵銷。

## 驗證與限制

中性tex／clay獨立回讀：52骨、body46鍵及部件42鍵皆在且預設0；basis／各鍵以最近點對應最大誤差約0.0015mm。這不是逐索引拓撲相同證明。static preview另對源body_muscular=1座標驗證；沒有骨或鍵是刻意設計。

GLB輸出曾提示頂點色／材質採樣警告；回讀有Color層，但NoseShade各通道語意、蒙皮權重／骨軸及動畫尚未完整比對，故原FBX為權威。中性GLB只顯示基礎貼皮，Unity獨立身體畫層不會自動生效；請看展示GLB或遊戲圖。Blender比較光照不是Unity toon，也沒有執行時頭部縮放。

身體貼圖已實測72張遊戲前後與12張Blender腿部檢查圖；其他體型／完整屈膝、戰鬥、任意混形、衣服遮罩未驗。不宣稱新V7在Unity重新匯入完成，也不重建不存在的完整19158點shape_final.npz/HV。V6部分npz不能沿用V7。

來源模型沿專案既有MPFB/MakeHuman hm08 CC0紀錄；混合生成貼圖來源沿ideal_hero provenance，本輪未重新獨立驗全體授權。ImageGen實際提示詞、三個腿部輸入和前輪上身紀錄，見source_art/README.md的可回溯路徑與版本。
