#coding: utf8

"""

disassemble(co, lasti) in dis.py:
...
    while i < n:
        c = code[i]
        table = {
        0x99: 'LOAD_CONST',
        0x68: 'STORE_FAST',
        0x46: 'BINARY_MULTIPLY',
        0x61: 'LOAD_FAST',
        0x27: 'BINARY_ADD',
        0x88: 'MAKE_FUNCTION',
        0x91: 'STORE_GLOBAL',
        0x9b: 'LOAD_GLOBAL',
        0x60: 'LOAD_ATTR',
        0x53: 'RETURN_VALUE'
        }
        op = ord(c)
        if op in table: op = table[op]
        else: op = op
        if type(op) == str:
            op = opmap[op]
...
"""

import rotor # pip install rotor

def encrypt(data):
	key_a = '!@#$%^&*'
	key_b = 'abcdefgh'
	key_c = '<>{}:"'
	secret = key_a * 4 + '|' + (key_b + key_a + key_c) * 2 + '|' + key_b * 2 + 'EOF'
	print secret
	rot = rotor.newrotor(secret)
	return rot.encrypt(data)
def decrypt(data):
	key_a = '!@#$%^&*'
	key_b = 'abcdefgh'
	key_c = '<>{}:"'
	secret = key_a * 4 + '|' + (key_b + key_a + key_c) * 2 + '|' + key_b * 2 + 'EOF'
	rot = rotor.newrotor(secret)
	return rot.decrypt(data)

f = open('encrypted_flag', 'rb')
d = f.read()
print decrypt(d)
f.close()