import sys
import json
import PIL.Image as Image

p = json.load(open('lights.json', 'rb'))
row = list()
rows = list()
rgb = {}
def binary(x):
	return ''.join(map(lambda x: bin(x)[2:].zfill(8), x))

for c in p:
	if 'http' in c['_source']['layers']:
		http = c['_source']['layers']['http']
		url = http['http.request.full_uri']
		if 'data' in http:
			data = http['data']['data.data']
			data = data.replace(':', '').decode('hex')
			data = json.loads(data)
			if 'groups' not in url:
				index = url.split('lights/')[1].split('/')[0]
				index = int(index)
				if index in rgb:
					exit()
				rgb[index] = data['sat']
				if len(rgb.keys()) == 3:
					row.append((rgb[1], rgb[2], rgb[3]))
					x = binary([rgb[1], rgb[2], rgb[3]])
					sys.stdout.write(chr(rgb[1]^rgb[2]^rgb[3]))
					rgb = {}
			else:
				rows.append(row)
				row = list()
				print
			# print data

print rows
w = len(rows[0])
h = len(rows)
im = Image.new('RGB', (w, h))
for i in range(w):
	for j in range(h):
		im.putpixel((i, j), rows[j][i])

im.save('image.png')