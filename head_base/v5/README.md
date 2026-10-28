# Head Base V5(2026-10-28)

從 V4 出發的修正版。V4 原檔不變。

## 做了什麼
1. **重建 V4 的 `shape_final.npz`**:V4 只有 glb;glTF 在 UV 接縫拆頂點,用 UV 把 14,517 個 glb 頂點對回 MPFB 的 13,380 個身體頂點(全部對到、接縫兩側位置一致)。用它重新打包後與原 V4 同鏡頭渲染,平均差 0.5/255。重建檔另存 `../v4/shape_final_rebuilt.npz`。
2. **鼻翼黑影**:不是形狀也不是貼圖,是 V4 glb 在角色右側鼻翼/鼻孔有 14 個頂點的法線存錯(最大偏 109°)。重新計算法線後消失。見 `v4_rebuild_check.png`(左 V4、中 V5、右差異 ×4)。
3. **耳朵**:耳輪折角、耳後稜線來自之前頭型收窄時耳朵頂點各自位移。以「MPFB 原版耳朵 + 已確認的耳朵滑桿」為準把多餘位移平滑掉;位置不變。見 `ear_before_after.png`(上 V4 灰模、中 V5 灰模、下 V5 貼皮)。
4. **眼皮細線**:AI 眼線比 MPFB 眼皮邊緣高約 2 mm,中間隔一條皮膚,看起來像蓋在眼白上的第二條線。把眼線往下接到眼皮邊緣(只疊在 V4 貼圖上,不重新烘,V4 的鼻底貼圖保留)。見 `eye_before_after.png`(上 V4、中 睫毛 0.5、下 睫毛 0.35 = V5)。
5. **睫毛**:0.5 → 0.35。
7. **鼻子整體更挺(2026-10-28 選 D)**:鼻根往前墊 4 mm(避開眼睛)+ MPFB `nose-scale-depth-incr` 0.6。鼻尖比眉心突出 4.4 → 9.6 mm,鼻根凹陷 12.3 → 5.6 mm;0 新翻面。選項比較 `nose_options.png`(由上:原 v5 / C2 / C3 / D)。
6. **眉毛左右對稱**:MPFB eyebrow004 的貼圖左右是兩條不同的眉毛,位置也因皮膚左右差約 1.4 mm 而歪。右眉改成左眉(眉尾上揚那條)的鏡像,形狀與圖案都對稱;離皮膚的距離做平滑修正(逐點貼皮會折疊三角形)。見 `brow_before_after.png`。

## 檔案
同 `../README.md` 的格式:`head_base_v5_tex.glb`、`head_base_v5_clay.glb`、`head_base_v5.blend`、`basecolor.png`、`shape_final.npz`、`params.json`(含已知問題)、`morphs.json`。

## 驗證
- glb 與 .blend 的 28 個 morph 預設值都是 0(打開就是原形)。`morph_check.png`:預設 / nose_big / nose_tip_up。
- glb 重新匯入:body / brows / eye_L / eye_R / lashes 各 28 個 morph,eyes_big / nose_big / ears_big 時眼球、眉毛、睫毛跟著走。
- 鼻、嘴、耳灰模與貼皮近拍:`nose_mouth_closeups.png`、`ear_before_after.png`。
- 未驗證:Unity toon 實機、滑桿組合、動畫。

## 已知問題
見 `params.json` 的 `known_issues`:唇縫內側 8 個翻面面、耳孔前小凹口(MPFB 原生)、睫毛下方仍可見、眼線偏粗、耳輪上緣淡色斑塊(沿用 V4 貼圖)。
