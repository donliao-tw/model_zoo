# head_base v11:大笑重做(使用者在滑桿網頁調定)+ 中性下顎後退 4.7mm

2026-11-05,Claude。狀態:**大笑使用者已核可**(在滑桿網頁上自己調好送出)。v10 的閉眼瑕疵還沒修,見「已知問題」。

## 從哪版來

- 上一版:v10(`head_base/v10/head_base_v10.blend`)。網格、UV、骨架都沒改,頂點數一樣。
- 來源:3D_model_design main `3d49ab8`,設定 `versions/v11.json`、`versions/v11_laugh.json`、`versions/v11_presets.json`。
  - `head_base_v11.fbx` SHA `6b13e9db…`(建置輸出原名 `head_base_v11_game.fbx`)。

| 檔案 | 內容 |
|---|---|
| `head_base_v11.fbx` | 遊戲用 FBX;骨架、權重同 v10 |
| `head_base_v11.blend` | 母檔,貼圖已打包;所有形態鍵預設 0 |
| `head_base_v11_tex.glb`／`_clay.glb` | 貼皮／灰模交換檔,有骨架和形態鍵 |
| `skins/skin_{normal,thin,lean,muscular,fat}.png` | 五型皮膚,口腔內部依新大笑重新上色 |
| `basecolor.png`、`eyebrow.png`、`eye.png`、`lashes.png`、`body_paint_balanced.png`、`body_joints.json` | 和 v10 相同 |
| `expressions.json` | ak_ 鍵清單、微笑／大笑組合、`ex_laugh` 的配方 |
| `compare_vs_v10.png` | 中性、微笑、大笑和 v10 同鏡頭比較 |
| `review/` | 檢查圖 |

## 改了什麼

1. **大笑改成一個鍵 `ex_laugh`**(Body、Brows、Lashes、Mouth 都有)。`expressions.json` 的 `presets.laugh` = `{"ex_laugh": 1}`。
   - 內容是使用者在滑桿網頁上調好送出的組合:MakeHuman laugh01 0.98、嘴角往兩側 0.9、下顎往前 1.5、下巴縮短 0.87,加上嘴唇控制點等,完整權重見 `expressions.json` 的 `ex_laugh.recipe_weights`。
   - MakeHuman 的骨頭動作單元,這次是**在這張臉上**(v5 `shape_final` + 下顎後退)擺骨頭量的。以前是在 MakeHuman 原人體上量,再搬過來。骨頭轉動的位移和點的位置有關,搬到別的臉上,上唇中間會出現一個 V(`review/上唇中間V_修正前後.png`)。
   - 唇內側和口腔面跟著正前方的外皮走,不會從下唇下方穿出來。
   - 上排牙同名鍵整排往後 11.32mm、往上 3.36mm(位置由使用者調定)。**沒有下排牙**(使用者決定先拿掉)。
2. **中性臉下顎後退 4.7mm**:MPFB `chin-prognathism-decr` × 0.6,加到 Body 的基底和所有形態鍵(相對位移不變)。只動到下巴附近 483 個點,最多 4.74mm。使用者已核可下巴形狀。
3. 上排牙用目前的 `mouthparts` 重做(沿弧長排、每側 7 顆),Mouth 頂點 288 → 336。`ak_jawOpen` 時牙齒往後 5mm、`ak_mouthFunnel` 時往後 3mm,避免從臉頰穿出來。

沒變的部分:骨架 52 根;Body 頂點 70583,和 v10 一樣;v10 的 149 個 Body 鍵全部保留,只多了 `ex_laugh`。

形態鍵數量:

| 物件 | v10 | v11 |
|---|---|---|
| Body | 149 | 150 |
| Brows | 95 | 96 |
| Lashes | 85 | 86 |
| EyeL／EyeR | 42 | 42 |
| Mouth | 6 | 9 |

## 已驗證

- 4 個檔案回讀(blend、fbx、兩個 glb):骨架 52 根,鍵數如上表,預設值全部 0。靜止姿勢和建置基底比:blend 0 mm、FBX 0.0008 mm。
- `ex_laugh` 和網頁上各單元相加的結果:最大差 0.0001mm,也就是網頁上看到的樣子就是這個鍵。
- 捏臉極值 × 大笑(`review/check/捏臉極值x大笑_*.png`):12 個嘴／下巴／下顎／臉型鍵各拉到 1。和 v11 調查版(方案 A)比,鼻下自相交 7 → 2、下巴縮短 × 大笑的下巴自相交 14 → 8。
- 閉嘴類 ak_ 鍵、中性、微笑看不到牙;`mouthUpperUp` 會露牙,這是那個鍵本來的作用(`review/check/閉嘴類_眨眼x大笑_五體型x大笑.png`)。
- 眨眼 0.5 / 1.0 × 大笑、五型體型 × 大笑:正常。
- 和預想圖並排:`review/預想圖vs_v10_v11.png`。

## 未驗證

- Unity 實機匯入、遊戲卡通 shader 外觀。
- 多個捏臉鍵疊加後再大笑;`body_round` 以外的組合。
- 其他 `ex_` 表情鍵、大部分 `ak_` 鍵在下顎後退之後沒有逐一重看(數學上相對位移不變)。

## 已知問題

1. **下巴最長(`chin_long`)× 大笑**:口腔裡露出幾個暗色的尖三角形(口腔內面),舊版也有。
2. **上唇在大笑時往內捲**:從下往上看,唇內側和口腔的交界是鋸齒狀;正面看上唇邊緣有一點小波浪。原因是上唇往內捲的那條邊,只有幾個 3~4mm 的大三角形。試過沿唇平滑位移,沒有用,要動網格才能根治。
3. **大笑嘴部的自相交總數**比調查版多(218 對、調查版 18 對),大多是口腔裡本來就貼在一起的面。看圖沒有破面,這個數字目前不當驗收依據。
4. **glb 的材質是 BLEND(半透明)**:three.js 等網頁檢視器會把貼皮畫成碎片。要在網頁上用,得在載入後把皮膚、眼睛設成不透明,眉毛、睫毛用 alphaTest(v10 也一樣)。
5. 大笑用到的部分單元是外插(下顎往前 1.5、好幾個負值),只在這一組權重下看過,單獨拉開不保證好看。
6. 從 v10 沿用:閉眼時上眼皮眼線露出三角形、外眼角尖折,以及 v10 README 列的其他項目。

## 下一步

| 要改什麼 | 誰改 | 開始條件 |
|---|---|---|
| 已知問題 2:上唇內捲、小波浪(上唇邊緣加細網格) | 3D_model_design | 先調查再動手 |
| 下排牙(依下唇位置自動放) | 3D_model_design | 使用者決定要不要 |
| v10 閉眼兩處瑕疵 | 待定 | 使用者決定做法 |
| Unity 實機匯入測試 | 待定 | 無 |

做完任何一項就開新版本(v12),不覆蓋 v11。

## 怎麼重做

在 3D_model_design(commit `3d49ab8`),腳本說明見 `tools/v11_laugh/README.md`:

```
# 1. 由滑桿網頁的模型(build/v11a/sliderweb3/slider.blend)依權重相加出大笑位移
blender -b --python tools/v11_laugh/bake_laugh.py -- build/v11a/sliderweb3/slider.blend versions/v11_laugh.json build/v11/mh_laugh.npz
# 2. 建置
python3 tools/build_version.py v11 --steps dump,prebase
blender -b --python tools/v11_laugh/make_cand.py -- build/v11/pre_nojaw.blend build/v11a/jaw/jawback.npz 0.6 build/v11/pre.blend   # 先把 pre.blend 改名成 pre_nojaw.blend
python3 tools/build_version.py v11 --steps package,interior,paint,package,assets,verify,review
```

輸出在 `build/v11/out/`:`head_base_v11_game.fbx` 改名成這裡的 `head_base_v11.fbx`,其他檔名相同。
