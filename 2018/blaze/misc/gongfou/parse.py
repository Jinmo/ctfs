from PIL import Image
import sys

img = Image.open('data.png')
for i in range(46):
	flag = ''
	for j in range(7):
		flag += '%d'%((img.getpixel((i * 34 + 17, j * 98 + 115)))[0] > 180)
	print i, flag,
	print chr(int(flag,2))