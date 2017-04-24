import os
import PIL.Image as Image
try:os.mkdir('images')
except:
	pass
s = '''.oooooo. ........ .oooo... .oooo... .oooo... .oo.oo.. ........ .oo..... ........ .oo.oo.. .oooo... ........ .ooooo.. .oooooo. .ooooo.. ........ 
.oo..... .oo..... .oo.oo.. .oo..... .oo..... .oooo... ........ .oo..... ........ .ooo.oo. .oo.oo.. ........ .oo.oo.. .oo..... .oo.oo.. .oo.oo.. 
.oooo... .oo..... .oooooo. .oo.ooo. .ooo.... .oo..... ........ .oo.oo.. ........ .oo.ooo. .oo.oo.. ........ .ooooo.. .oooo... .ooooo.. .ooooo.. 
.oo..... .oo..... .oo.oo.. .oo.oo.. .oo..... .oo..... ........ .oo.oo.. ........ .oo.oo.. .oo.oo.. ........ .oo..... .oo..... .oo.oo.. .oo..... 
.oo..... .oooooo. .oo.oo.. .oooo... .oooo... .oo..... .oooooo. .oooo... .oooooo. .oo.oo.. .oooo... .oooooo. .oo..... .oooooo. .oo.oo.. .oo..... 
........ .oo.oo.. ........ .oooooo. .oooo... .oo..... ........ .oooo... .ooooo.. ........ .oooo... ........ .oo.oo.. .oooo... .oooooo. ........ 
.oo..... .ooo.oo. .oo.oo.. .oo..... .oo.oo.. .oo.oo.. .oo..... .oo.oo.. .oo.oo.. ........ .oo.oo.. .oo.oo.. .ooo.oo. .oo..... .oo..... .oo.oo.. 
.oooo... .oo.ooo. .oo.oo.. .oo..... .oo..... .oo.oo.. .oo..... .oooooo. .ooooo.. ........ .oo..... .oo.oo.. .oo.ooo. .oooo... .oo..... .ooooo.. 
.oo..... .oo.oo.. .oo.oo.. .oo..... .oo.oo.. .oo.oo.. .oo..... .oo.oo.. .oo.oo.. ........ .oo.oo.. .oo.oo.. .oo.oo.. .oo..... .oo..... .oo.oo.. 
.oooooo. .oo.oo.. .ooooo.. .oooooo. .oooo... .oooo... .oooooo. .oo.oo.. .oo.oo.. .oooooo. .oooo... .oooo... .oo.oo.. .oooo... .oo..... .oo.oo.. 
.oo..... ........ .oooooo. .oooooo. .oooo... .oo..... ........ ........         
.oo.oo.. .oo.oo.. .oo..... .oo..... .oo.oo.. .ooo.oo. .oo.oo.. .oo.....         
.oo.oo.. .oo..... .oo..... .oo..... .oo.oo.. .oo.ooo. .oo..... .ooo....         
.oo.oo.. .oo.oo.. .oo..... .oo..... .oo.oo.. .oo.oo.. .oo..... .oo.....         
.oooo... .oooo... .oo..... .oooooo. .oooo... .oo.oo.. .oo..... .oooo...         '''.replace('\n', '')
pad = 5
for i in range(9, len(s) / 5, 9):
	data = [s[j:j+i] for j in range(0, len(s) + i*2, i)]
	w = len(data[0])
	h = len(data)
	im = Image.new('RGB', (w+pad*2, h+pad*2))
	for x in range(w):
		for y in range(h):
			if len(data[y]) <= x or data[y][x] != 'o':
				c = (0, 0, 0)
			else:
				c = (255, 255, 255)
			im.putpixel((x+pad, y+pad), c)
	im.save('images/%d.png' % i)