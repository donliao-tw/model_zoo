# head_base v12:大笑嘴唇重做、拿掉眉毛與睫毛、貼圖去眼線並上唇色

2026-11-07,Claude。狀態:**使用者已核可上架**。

## 從哪版來
- 上一版:v11。骨架 52 根和權重沒變;**Body 頂點數變了(70583 → 72907)**,而且**少了 Brows、Lashes 兩個物件**,Unity 的 prefab 要重新匯入。
- 來源:3D_model_design main `8bf2462`,設定 `versions/v12.json`、`versions/v12_laugh_d1.json`;貼圖腳本在 `tools/v12_d1/tex/`。
  - `head_base_v12.fbx` SHA `40d83558…`(建置輸出原名 `head_base_v12_game.fbx`)。

| 檔案 | 內容 |
|---|---|
| `head_base_v12.fbx` | 遊戲用 FBX |
| `head_base_v12.blend` | 母檔,貼圖已打包;所有形態鍵預設 0 |
| `head_base_v12_tex.glb`／`_clay.glb` | 貼皮／灰模交換檔 |
| `skins/skin_{normal,thin,lean,muscular,fat}.png` | 五型皮膚:去眼線、去眼頭陰影、上唇色、口腔內面重新上色 |
| `basecolor.png`、`eye.png`、`body_paint_balanced.png`、`body_joints.json` | 和 v11 相同 |
| `expressions.json` | ak_ 鍵清單、微笑／大笑組合、`ex_laugh` 的配方 |
| `compare_vs_v11.png` | 中性、微笑、大笑和 v11 同鏡頭比較(整臉、嘴部、3/4、灰模) |
| `review/` | 檢查圖(`v11_vs_v12_大笑x*` 是拿掉眉毛前拍的,幾何檢查仍有效) |

## 改了什麼
1. **大笑嘴唇**:Body 嘴唇一帶局部細分一刀(舊點編號不變),`ex_laugh` 換成使用者在滑桿網頁 D1 送出的值(磨順 1.5),修掉 v11 上唇往內捲和唇緣小波浪,露出較多上排牙。眉頭上揚、下眼皮上推歸零。
2. **拿掉 Brows(眉毛)、Lashes(睫毛)物件**與它們的形態鍵。眉毛之後另外做。
3. **皮膚貼圖(五型)**:去掉畫在眼皮上的黑眼線、眼頭上方兩塊深褐陰影;依使用者在中性圖上畫的唇線上唇色(上唇 RGB 165,105,98、下唇 185,118,112,保留原明暗、邊緣羽化)。
4. 口腔內面上色:射線改成也朝每個面中心打,細分後的小面不會漏掉(之前嘴角會有紫黑小點)。
5. tex glb 的皮膚材質改為 OPAQUE。
6. **大笑嘴角**(11-07 再修):嘴角翻出來的面原本被口腔深色畫黑 → 改回膚色;嘴角最外側暗點補平;使用者圈出的「唇色太大片」兩端與嘴角兩條側壁,羽化漸變成膚色(`review/嘴角柔化_側壁.png`、`review/大笑嘴角_修前修後_卡通.png`)。中性嘴唇兩端也因此略短。
7. `review/卡通近似渲染.png`:Blender 仿 Unity toon(兩階色帶、無自陰影、只畫外輪廓),**不是**遊戲實際 shader。

形態鍵:Body 150、EyeL／EyeR 42、Mouth 9(Brows、Lashes 物件已移除)。

## 已驗證
- 4 個檔案回讀:骨架 52、鍵數如上、預設值全 0;靜止姿勢 blend 0 mm、FBX 0.0008 mm。
- `tools/run_all_checks.sh v12`:morph、mouth、blink、body 全 PASS。
- 中性和其他 149 個鍵,在原有的點上和 v11 差 0.0000 mm。
- 中性／微笑／大笑整臉和嘴部近拍(灰模+貼皮)和 v11 並排看過;閉眼近拍看過。

## 未驗證
- Unity 實機匯入、遊戲卡通 shader 外觀。

## 已知問題
- 沒有眉毛(另做)、沒有下排牙。
- `chin_long` × 大笑口腔有暗三角(v11 就有)。
- v10 閉眼兩處瑕疵。
- tex glb 的眼睛材質仍是 BLEND。
