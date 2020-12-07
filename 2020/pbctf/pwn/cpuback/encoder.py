import base64
import textwrap
b = base64.b64encode(open('test', 'rb').read()).decode()
for x in textwrap.wrap(b):
	print('echo "%s" >> a' % x)