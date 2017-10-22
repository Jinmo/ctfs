import sys
c = d = g = 0
def p_drawText(a, b, c, d):
  sys.stdout.write(a)
def b(f2):
    n2 = 0;
    n3 = 0;
    n4 = 0;
    while True:
      if (n3 >= 1000 or f2 == ord(['!', '@', '`', 'A', 'a', '\"', 'B', 'b', '#', 'C', 'c', 'd', 'D', '$', 'E', '%', 'e', 'F', 'f', '&', '\'', 'G', 'g', 'h', 'H', '(', ')', 'I', 'i', 'j', 'J', '*', '+', 'K', 'k', ',', 'l', 'L', '-', 'M', 'm', 'n', '.', 'N', 'O', 'o', '/', '0', '1', '2', 'P', 'p', 'Q', 'q', 'R', 'r', '3', 'S', 's', 't', 'T', '4', '5', '6', '7', '8', 'U', 'V', 'W', 'X', 'u', 'v', 'w', 'x', '9', 'Y', 'y', ':', 'Z', 'z', ';', '[', '{', '|', '\\', '<', '=', ']', '}', '_', '^', '~', '>', '?'][n3])):
        break
      n4 += 1;
      n3 += 1;
    f2 = n4;
    n4 = 33;
    n3 = n2;
    while True:
      if (n3 >= 1000 or f2 == ord(['Z', '\x0e', '\x11', '\x0b', '\f', '\x06', '\x1d', '\x1c', '\'', '.', '*', ')', '6', '@', '?', 'P', 'N', 'L', 'G', '=', ':', ',', '\x1f', '\x10', '\x13', '\x01', '\x04', '-', '9', 'E', 'O', 'R', 'V', 'Q', 'S', '\\', ']', ';', '1', '!', '\x16', '\r', '\n', '\x12', '\x03', '\x00', '\x05', '<', '>', 'F', 'K', 'J', 'W', '[', '4', '\x1b', '\x1a', '2', '/', 'C', 'H', 'X', '\x02', '\t', '\b', '\x07', '+', '(', '7', 'M', 'T', 'U', '\x14', '%', '5', '\x1e', '\"', 'A', 'D', 'I', '#', '\x15', 'Y', '\x18', '0', 'B', '\x17', '\x0f', '&', '8', '\x19', ' ', '$', '3'][n3])):
          f3 = n4;
          if (f3 < ord('!') or f3 > ord('/')):
            break;
          return f3 + 64.0
      n4 += 1;
      n3 += 1;
    if (f3 >= ord('a') and f3 <= ord('o')):
        return f3 - 32.0
    if (f3 >= ord('A') and f3 <= ord('O')):
        return f3 - 32.0
    if (f3 >= ord('0') and f3 <= ord(':')):
        return f3 + 32.0
    if (f3 >= ord('P') and f3 <= ord('Z')):
        return f3 + 32.0
    f2 = f3;
    if (f3 < ord('p')):
      return f2;
    f2 = f3;
    if (f3 > ord('z')):
      return f2;
    return f3 - 64.0
def a(x):
  return chr(int(b(x)))
# p_drawText("H", c / 2, d * 36 / 46, g);
# p_drawText("HS", c / 2, d * 36 / 46, g);
p_drawText("HS{", c / 2, d * 36 / 46, g);
p_drawText("" + a(81), c / 2, d * 36 / 46, g);
p_drawText("" + a(83), c / 2, d * 36 / 46, g);
p_drawText("" + a(85), c / 2, d * 36 / 46, g);
p_drawText("" + a(87), c / 2, d * 36 / 46, g);
p_drawText("" + a(89), c / 2, d * 36 / 46, g);
p_drawText("" + a(92), c / 2, d * 36 / 46, g);
p_drawText("" + a(95), c / 2, d * 36 / 46, g);
p_drawText("" + a(98), c / 2, d * 36 / 46, g);
p_drawText("" + a(105), c / 2, d * 36 / 46, g);
p_drawText("" + a(109), c / 2, d * 36 / 46, g);
p_drawText("" + a(111), c / 2, d * 36 / 46, g);
p_drawText("}", c / 2, d * 36 / 46, g);
print