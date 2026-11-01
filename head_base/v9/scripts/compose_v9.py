import sys
from PIL import Image, ImageDraw
d = sys.argv[1]
cols = ['front', 'quarter', 'side', 'blink', 'body', 'clay']
S = 350
g = Image.new('RGB', (40 + S * len(cols), 30 + S * 2), (30, 30, 30)); dr = ImageDraw.Draw(g)
for c, n in enumerate(cols): dr.text((40 + c * S + 8, 8), n, fill=(230, 230, 230))
for r, v in enumerate(('v8', 'v9')):
    dr.text((8, 30 + r * S + S // 2), v, fill=(230, 230, 230))
    for c, n in enumerate(cols): g.paste(Image.open(f'{d}/review/{v}_{n}.png').convert('RGB').resize((S, S)), (40 + c * S, 30 + r * S))
g.save(f'{d}/compare_vs_v8.png')
r = Image.new('RGB', (S * 3, S), (30, 30, 30))
for i, n in enumerate(('body', 'round_front', 'round_side')): r.paste(Image.open(f'{d}/review/v9_{n}.png').convert('RGB').resize((S, S)), (i * S, 0))
r.save(f'{d}/review/body_round_sheet.png')
print('OK')
