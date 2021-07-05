int sub_DC5() {
  pc = 0;

  count = memory[pc];
  pc += 1;

  r27 = 0;
  valid = 0;

  while (r27 != count) {
    op0 = memory[pc++];
    op1 = memory[pc++];
    op2 = memory[pc++];

    switch (op0) {
    case 0:
      delta = 10;
      offset = op1;
      break;
    case 1:
      delta = -10;
      offset = 90 + op1;
      break;
    case 2:
      delta = 1;
      offset = 10 * op1;
      break;
    case 3:
      delta = -1;
      offset = 10 * (op1 + 1) - 1;
      break;
    default:
      return;
    }

    i = 0;
    j = 0;

    max = -1;
    bits = 0;
    while (i != 10) {
      r16 = 256 + offset;
      c = memory[r16];
      assert (1 <= c && c <= 10);
      r13 = 1 << (c - 1);
      bits |= r13;
      if (max < c) {
        max = c;
        j += 1;
      }
      offset += delta;
      i += 1;
    }
    if (1023 == bits && j == op2) {
      valid += 1;
    }
    r27 += 1;
  }

  if (*(_DWORD *)&memory[192])
    return;

  if (count == valid) {
    puts("Correct");
    fflush(stdout);
  }

  r9 = 256;
  r8 = 100;

  r9 += r8;
  r8 = *(unsigned __int16 *)&memory[r9];
  r7 = *(unsigned __int16 *)&memory[r9 + 2];
  *(_WORD *)&memory[r7] = r8;
}