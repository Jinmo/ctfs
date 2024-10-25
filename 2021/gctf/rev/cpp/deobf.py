import hashlib
lines = list(open('cpp.c', 'r'))
i = 0
def _(x):
    return x.split(' ')[-1].strip()

def assign(lines):
    if len(lines) != 8:
        return

    prev = _(lines[0])[:1]
    result = 0
    if prev == 'S':
        return

    for l in lines:
        if _(l)[:1] != prev:
            return

        op = l.strip().split(' ')[0]
        try:
            op = ['#define', '#undef'].index(op)
        except ValueError:
            return
        result |= (1 - op) << int(l.strip()[-1])
    return '%s = 0x%02x;\n' % (prev, result)

def if_zero(lines):
    if len(lines) != 18:
        return

    prev = _(lines[0])[:1]
    result = 0
    if prev == 'S':
        return

    for l in lines[:8]:
        if _(l)[:1] != prev:
            return

        op = l.strip().split(' ')[0]
        if op != '#ifndef':
            return

    return 'if(%s == 0) goto %d;\n' % (prev, int(_(lines[9])))

rom = [0] * 128
while i < len(lines) - 8:
    line = lines[i]
    op = line.lstrip()
    if op.startswith('#define ROM_'):
        addr, bit = op.split(' ')[1].split('_')[1:]
        addr = int(addr, 2)
        bit = int(bit)
        if addr < 0x80:
            print(addr)
            rom[addr] |= int(_(op)) << bit
    if op.startswith('#if S == '):
        if '#undef c' in lines[i + 3]:
            chunks = lines[i:i + 205]
            dest = _(chunks[7])[:1]
            arg0 = _(chunks[4])[:1]
            arg1 = _(chunks[5])[:1]
            assert dest == arg0
            chunks = ''.join(chunks[4:]).replace(dest, 'DEST').replace(arg0, 'ARG0').replace(arg1, 'ARG1')
            print(_(op), hashlib.md5(chunks.encode()).hexdigest(), dest, arg0, arg1)
            open('state' + _(op) + '.c', 'w').write(chunks)
            lines[i + 1:i + 204] = [
                '        %s += %s;\n' % (dest, arg1)
            ]
        elif '#ifdef' in lines[i + 3] and '#define' in lines[i + 4]:
            chunks = lines[i:i + 44]
            dest = _(lines[i + 4])[:1]
            src = _(lines[i + 3])[:1]
            chunks = ''.join(chunks[3:]).replace(src, 'A').replace(dest, 'B')
            print(repr(chunks))
            lines[i + 1:i + 43] = [
                '        %s = %s;\n' % (dest, src)
            ]
        elif '#ifdef' in lines[i + 3] and '#undef' in lines[i + 4]:
            chunks = lines[i:i + 44]
            dest = _(lines[i + 4])[:1]
            src = _(lines[i + 3])[:1]
            chunks = ''.join(chunks[3:]).replace(src, 'A').replace(dest, 'B')
            print(repr(chunks))
            lines[i + 1:i + 43] = [
                '        %s = ~%s;\n' % (dest, src)
            ]
        elif assign(lines[i + 3:i + 11]):
            lines[i + 1:i + 11] = [
                '        ' + assign(lines[i + 3:i + 11])
            ]
        elif if_zero(lines[i + 3:i + 21]):
            assert int(_(lines[i + 2])) == int(_(op)) + 1
            lines[i + 1:i + 21] = [
                '        ' + if_zero(lines[i + 3:i + 21])
            ]
        elif '#ifndef' in lines[i + 3] and '#ifdef' in lines[i + 4] and '#define' in lines[i + 5]:
            chunks = lines[i:i + 44]
            print(chunks)
            dest = _(lines[i + 5])[:1]
            src = _(lines[i + 4])[:1]
            assert dest == _(lines[i + 3])[:1]
            lines[i + 1:i + 43] = [
                '        %s |= %s;\n' % (dest, src)
            ]
        elif '#ifdef' in lines[i + 3] and '#ifndef' in lines[i + 4] and '#undef' in lines[i + 5]:
            chunks = lines[i:i + 44]
            print(chunks)
            dest = _(lines[i + 5])[:1]
            src = _(lines[i + 4])[:1]
            assert dest == _(lines[i + 3])[:1]
            lines[i + 1:i + 43] = [
                '        %s &= %s;\n' % (dest, src)
            ]
        elif '#undef l0' in lines[i + 3]:
            chunks = lines[i:i + 92]
            addr = _(lines[i + 4])[:1]
            dest = _(lines[i + 52])[:1]
            print(lines[i + 92])
            print(addr, dest)
            lines[i + 1:i + 91] = [
                '        %s = LD(%s);\n' % (dest, addr)
            ]
        elif '#ifdef' in lines[i + 3] and '#ifdef' in lines[i + 4] and '#undef' in lines[i + 5]:
            chunks = lines[i:i + 60]
            print(chunks)
            dest = _(lines[i + 5])[:1]
            src = _(lines[i + 3])[:1]
            assert dest == _(lines[i + 4])[:1]
            lines[i + 1:i + 59] = [
                '        %s ^= %s;\n' % (dest, src)
            ]
        elif '#undef S' in lines[i + 3] and '#define S' in lines[i + 4]:
            lines[i + 1:i + 5] = [
                '        goto %s;\n' % _(lines[i + 4])
            ]

    i += 1

open('cpp.c', 'w').write(''.join(lines))
print(bytes(rom).hex())