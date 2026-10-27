# styles:渲染風格

## toon_disney(動漫 / 偏迪士尼)— v2 預覽使用中

Blender EEVEE,`pipeline/blender/wrap_final_render.py`:
- 皮膚:漫射 → Shader to RGB → 柔邊三階色階(陰影帶暖紫)× 貼圖,飽和度 1.2,淡輪廓光。
- 描邊:反轉外殼(Solidify,厚度 1.2 mm,翻轉法向 + 背面剔除);眼睛 1.6 cm 內厚度 0(否則外殼會從眼皮邊緣露出、蓋到眼球)。
- 眼睛:畫風貼圖,幾乎不吃明暗。
- 腮紅:兩頰與鼻頭,`BLUSH=0.5`。

指令範例:

```
BROW=eyebrow004 BLUSH=0.5 STYLE=disney EYE_TEX=parts/eyes/toon_eye_brown.png LASH_LEN=0.5 \
  scripts/blender.sh -b --factory-startup --python pipeline/blender/wrap_final_render.py -- \
  models/head02/head.glb models/wrap02/wrap_in.npz head_base/v2/shape_final.npz <輸出資料夾>
```

網頁端對應:three.js `MeshToonMaterial` 或 three-vrm 的 MToon(MIT)。

## real(寫實光)

同一張貼圖用 Cycles Principled BSDF,用來檢查形狀與貼圖瑕疵。
