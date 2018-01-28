from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from time import ctime
from Crypto import Random
from hexdump import *
import socket
# from Secret import __HIDDEN__, __SECRET__
__HIDDEN__ = ' jinmo123 !'
__SECRET__ = 'secret'

BLOCK_SIZE = 16

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def xor(dest, src):
    if len(dest) == 0:
        return src
    elif len(src) == 0:
        return dest
    elif len(dest) >= len(src):
        return ''.join(chr(ord(dest[i])^ord(src[i])) for i in range(len(src)))
    else:
        return ''.join(chr(ord(dest[i])^ord(src[i])) for i in range(len(dest)))


class AES_CNV:
    
    def __init__(self, key):
        assert len(key) == BLOCK_SIZE
        self.key = key

    def encrypt(self, plain_text, iv):
        assert len(iv) == 16
        plain_text = pad(plain_text)
        assert len(plain_text)%BLOCK_SIZE == 0
        cipher_text = ''
        aes = AES.new(self.key, AES.MODE_ECB)
        h = iv
        hexdump(plain_text)
        for i in range(len(plain_text)//BLOCK_SIZE):
            block = plain_text[i*16:i*16+16]
            block = xor(block, h)
            cipher_block = aes.encrypt(block)
            cipher_text += cipher_block
            h = md5(cipher_block).digest()
        return iv+cipher_text

    def decrypt(self, cipher_text):
        assert len(cipher_text)%BLOCK_SIZE == 0
        iv = cipher_text[:16]
        cipher_text = cipher_text[16:]
        aes = AES.new(self.key, AES.MODE_ECB)
        h = iv
        plain_text = ''
        for i in range(len(cipher_text)//BLOCK_SIZE):
            block = cipher_text[i*16:i*16+16]
            plain_block = aes.decrypt(block)
            print `plain_block`, `h`
            plain_block = xor(plain_block, h)
            print '=', `plain_block`
            plain_text += plain_block
            h = md5(block).digest()
            print '>', `h`
        return unpad(plain_text)

class Cookie:

    def __init__(self, key):
        assert len(key) == BLOCK_SIZE
        self.key = key
    
    def register(self, name, username):
        name = pad(name)
        iv = xor(name, md5(__HIDDEN__).digest())
        cookie = "CNVService" + "*" + "user="+ username + "*" + ctime() + "*" + __SECRET__
        aescnv = AES_CNV(self.key)
        cookie = aescnv.encrypt(cookie, iv)
        return b64encode(cookie)

    def authentication(self, cookie):
        cookie = b64decode(cookie)
        name = cookie[:16]
        name = xor(name, md5(__HIDDEN__).digest())
        if ord(name[-1]) < 16:
            name = unpad(name) 
        aescnv = AES_CNV(self.key)
        print hexdump(cookie)
        cookie = aescnv.decrypt(cookie)
        print hexdump(cookie)
        info = cookie.split("*")
        if info[0] != "CNVService":
            return None, None, None
        elif info[-1] != __SECRET__:
            return None, None, None
        elif "user=" != info[1][:5]:
            return None, None, None
        elif len(info[1].split("=")) == 2:
            return name, info[1].split("=")[1], info[2]
        else:
            return None, None, None

key = Random.new().read(BLOCK_SIZE)
cookie = Cookie(key)

decode = lambda x: hexdump(x)

class RemoteCookie(object):
    def recvuntil(self, x):
        d = ''
        while x not in d:
            c = self.s.recv(1)
            if c == '':
                print d
                print 'socket error'
                exit()
            d += c
        return d

    def __init__(self):
        self.s = socket.create_connection(('cnvservice.acebear.site', 1337))
        pass

    def register(self, name, username):
        self.recvuntil('choice: ')
        self.s.send('1')
        print self.recvuntil(': ')
        self.s.send(name + '\x00' * 100)
        print self.recvuntil(': ')
        self.s.send(username)
        self.recvuntil('Cookie: ')
        return self.recvuntil('\n')
    def authentication(self, cookie):
        self.recvuntil('choice: ')
        self.s.send('2')
        print self.recvuntil(': ')
        self.s.send(cookie)
        data = self.recvuntil('**Menu')
        print data

cookie = RemoteCookie()
text = 'Root------------'
x = cookie.register('', text).decode('base64')
print decode(x)
print len(x)
print len(x[:16] * 2 + x[16:32] + x[32:])
m = x[16:32]
m = bytearray(m)
m = str(m)
next_iv = md5(x[16:32]).digest()
next_iv2 = md5(x[32:48]).digest()
prev = x[:16]
print `next_iv`, '!'
print `next_iv2`, '!'
print `prev`
target = xor(text, 'root**------------')
y = cookie.register('', text + xor(xor(xor(text, next_iv), next_iv2), target)).decode('base64')
print hexdump(y)
print cookie.authentication((prev + m + y[48:64] + x[32:]).encode('base64'))