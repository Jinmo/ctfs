from json import load

with open('cip.json') as f:
	obj = load(f)
result = ''
for item in obj:
	cip = item['_source']['layers'].get('cipcls')
	if not cip:
		continue
	data = cip['Command Specific Data']['cip.data']
	data = data.replace(':', '').decode('hex')
	if len(data) > 6:
		result += data[4:]

open('firmware.bin', 'wb').write(result)