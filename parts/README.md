# parts:可替換零件

所有零件都綁在 MPFB 網格上,底模換版本不用重做。

## eyes/
| 檔案 | 說明 | 狀態 |
|---|---|---|
| `toon_eye_brown.png` | 畫風眼球貼圖(1024²,MPFB high-poly 眼球 UV)。虹膜放大 1.25、上深下淺暖褐、深色外圈、右上大高光 + 左下小高光,眼白整片米白 | v2 使用中 |

替換方式:把眼球材質的 `DiffuseTexture` 換成這張(透明度貼圖 `AlphaMapTexture` 保持原本)。由 `pipeline/paint_toon_eye.py` 產生,顏色、虹膜大小、高光位置都是參數。

## eyebrows/
使用 MPFB 內建眉毛(CC0),目前候選 4 種,比較圖 `eyebrows/options.png`:

| 名稱 | 樣子 | 狀態 |
|---|---|---|
| eyebrow001 | 平直、眉尾略垂,溫和 | 候選 |
| eyebrow004 | 眉頭下壓、眉尾上揚,接近劍眉 | v2 使用中 |
| eyebrow008 | 粗、弧度柔和、成熟 | 候選 |
| eyebrow012 | 自然、毛流感明顯 | 候選 |

都是寫實毛髮貼圖,在動漫風下看起來偏鉛筆素描;之後可另畫平塗動漫眉毛。

## eyelashes/
MPFB eyelashes01,處理規則(`pipeline/blender/wrap_parts.py`):
- 拿掉下睫毛(原本被壓平貼在臉頰上像筆刷痕,也偏女性化)。
- 上睫毛以根部為準縮到 0.5 倍(`LASH_LEN`)。
- 狀態:從下方看仍偏長,待調。

## 待做
- 眼線:在 MPFB 眼皮邊緣重畫(做成可換的「妝」零件),取代 AI 頭畫的眼線。
- 頭髮、衣服、平塗動漫眉毛。
