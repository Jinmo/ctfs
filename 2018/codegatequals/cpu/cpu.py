literal = lambda x: eval(x, labels)

labels = {}
import struct
def sub_4022D6(a1):

  a2 = a1 >> 24;
  if ( a2 <= 0x20 ):
    if ( a2 == 1 ):
      a3 = (a1 & 0xF00000) >> 20;
      a4 = 0;
      a5 = 0;
      a6 = a1 & 0xFFFFF;
    else:
      a3 = (a1 & 0xF00000) >> 20;
      a4 = (a1 & 0xF0000) >> 16;
      a5 = (a1 & 0xF000) >> 12;
      a6 = a1 & 0xFFF;
  else:
    print("Invalid instruction");
    return
  return a2, a3, a4, a5, a6

def reg(x):
  return int(x.lstrip('r'))

def encode(op, a1=0, a2=0, a3=0, a4=0):
  if op == 1:
    a1, a4, a2, a3 = reg(a1), literal(a2), 0, 0
  elif op == 2:
    a2, a1, a4, a3 = a1, a2, a3, 0
  elif op == 3:
    a1, a2, a4, a3 = a1, a2, a3, 0
  elif op == 4:
    a4, a1, a2, a3 = literal(a1), 0, 0, 0
  elif op == 5:
    a1, a2, a3, a4 = reg(a1), 0, 0, 0
  elif op == 6:
    a1, a2, a3, a4 = reg(a1), 0, 0, 0
  elif op in (7, 8, 9, 10, 11, 12):
    a1, a2, a4, a3 = reg(a1), reg(a2), literal(a3), 0
  elif op in (13, 14):
    a2, a1, a3, a4 = reg(a1), reg(a2), reg(a3), 0
  elif op == 15:
    a2, a1, a3, a4 = reg(a1), reg(a2), 0, 0
  elif op in (16, 22):
    a2, a1, a4, a3 = reg(a1), reg(a2), literal(a3), 0
  elif op == 17:
    a2, a1, a3, a4 = reg(a1), reg(a2), 0, 0
  elif op == 18:
    a1, a2, a3, a4 = reg(a1), reg(a2), 0, 0
  elif op == 23:
    a1, a2, a3, a4 = literal(a1), 0, 0, 0
  elif op == 20:
    a1, a2, a4, a3 = literal(a1), reg(a2), literal(a3), 0
  elif op == 21:
    a1, a2, a3, a4 = 0, 0, 0, 0
  else:
    print 'handle', op
    a1, a2, a3, a4 = 0, 0, 0, 0
  r = op << 24
  r |= a1 << 20
  r |= a2 << 16
  r |= a3 << 12
  r |= a4 & 0xfff
  return r

opmap = {
  'nop': 0,
  'li': 1,
  'ldr': 2,
  'str': 3,
  'syscall': 21,
  'add': 13,
  'sub': 14,
  'mov': 15,
  'shl': 16,
  'shr': 22,
  'lnop': 19,
  'ldx': 17,
  'stx': 18,
  'exception': 23,
  'cache': 20,
  'printint': 6,
  'printchar': 5,
  'jnz': 7,
  'jz': 8,
  'jmp': 4,
  'mov': 15
}
def asm(lines):
  lines = lines.strip()
  lines = lines.split('\n')
  lines = map(lambda x: x.strip(), lines)
  r = []
  skip = set()
  offset = 0
  for line in lines:
    if line.endswith(':'):
      skip.add(line)
      labels[line.rstrip(':').strip()] = offset * 4
      print labels
    else:
      offset += 1
  for line in lines:
    if line in skip:
      continue
    op, args = (line + ' ').split(' ', 1)
    args = args.strip()
    if op.startswith('op'):
      opcode = int(op[2:])
    else:
      opcode = opmap[op]
    args = args.split(',')
    args = map(lambda x: x.strip(), args)
    r += [encode(opcode, *args)]
  r = r + list(struct.unpack("<L", "flag"))
  r += [0]
  print 'asm:', `r`
  return ' '.join(map(str, r))

open('cpu.bin', 'wb').write(asm('''
  li r1, 10
  li r3, 1
  li r13, 0
  exception 2
  li r10, 0x400
  shl r10, r10, 7
  li r7, 0x35000 / 64
  shl r7, r7, 6
  li r12, 7
  li r8, 0
  li r5, 8
  c:
    cache 15, r9, 0
    add r9, r7, r8
    cache 4, r9, 0
    li r14, 0
    li r4, 255
    a:
      jz r4, r4, equals
      shl r2, r4, 12
      ldx r6, r2
      jnz r14, r13, equals
      sub r4, r4, r3
      jmp a
    equals:
    printint r4
    printchar r1
    printint r8
    printchar r1
    printint r4
    printchar r1
    printchar r1
    jz r5, r13, complete
    add r8, r8, r3
    stx r4, r10
    add r10, r10, r3
    sub r5, r5, r3
    jmp c
  complete:
  cache 15, r9, 0
  shl r2, r2, 31
  li r9, 0x100
  li r9, 0x100
  li r9, 0x100
  shl r9, r9, 9
  ldx r6, r9
  li r8, 4
  add r9, r9, r8
  ldx r7, r9
  li r0, 3
  li r1, hey
  li r2, 0
  syscall
  printint r5
  printint r5
  printint r5
  printint r5
  printint r5
  mov r1, r5
  li r0, 1
  mov r2, r10
  li r3, 256
  syscall
  li r0, 2
  li r1, 1
  li r3, 256
  syscall
  li r0, 0
  syscall
  hey:
  ''') + '\n')