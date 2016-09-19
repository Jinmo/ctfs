from pwn import *
import subprocess

HOST, PORT = 'misc.chal.csaw.io', 8001

r = remote(HOST, PORT)
r.recvline()
while True:
	regex = r.recvline()[:-1]
	regex = regex.replace(r'\W', ':')
	regex = regex.replace(r'\w', 'a')
	regex = regex.replace(r'\d', '0')
	print regex
	p = subprocess.Popen(['/home/jinmo/.cabal/bin/genex', regex], stdout=subprocess.PIPE)
	s = ''
	while '\n' not in s:
		s += p.stdout.read(1)
	p.kill()
	s = s[3:-2]
	r.sendline(s)
	print s