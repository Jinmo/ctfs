#coding: utf8

from Crypto.Cipher import AES
import sqlite3
import string
import time
import struct

path = r'RCTF_1.0.4.0_Debug_Test/RCTF_1.0.4.0_x86_x64_arm_Debug/RCTF_1.0.4.0_x64_Debug/Assets/flag.sqlite'
key = '26a6f9cc-d019-4f5d-8a1b-a352b7738f42'[:16]
iv = '0000000000000000'
get_aes = lambda: AES.new(key, AES.MODE_CBC, IV=iv)
C = []
base64chars = string.lowercase + string.uppercase + string.digits + '+/='
conn = sqlite3.connect(path)
c = conn.cursor()
c.execute('SELECT * FROM flag_table')
rows = c.fetchall()
print '\n'.join('%05d: %s' % (x[0], x[1]) for x in rows)

rows = map(lambda x: (x[0], x[1].decode('base64')), rows)
result = [None] * 9999
for index, row in enumerate(rows):
	aes = get_aes()
	s = aes.decrypt(row[1])
	if ord(s[-1]) <= 16 or 1:
		orig = s
		s = s[:-ord(s[-1])]
		if all(ord(c) < 128 for c in s) or 1:
			# print len(s),
			result[int(row[0])-1] = row[0], s
			# print s.encode('base64').replace('\n', '')
			# print `orig`
		else:
			print 'wtf'
			exit()

print filter(lambda x: x and 'rctf' in x[1].lower(), result)