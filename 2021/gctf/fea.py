a1 = [BitVec('x%d' % i, 32) for i in range(2)]

v1 = a1[1];
v2 = 7 * HIWORD(*a1);
if ( v2 )
  v3 = v2 - HIWORD(v2) - ((v2 - HIWORD(v2)) >> 16);
else
  v3 = -6 - HIWORD(*a1);
v4 = *a1 + 6;
v5 = HIWORD(v1) + 5;
v6 = 4 * v1;
if ( v6 )
  v1 = v6 - HIWORD(v6) - ((v6 - HIWORD(v6)) >> 16);
else
  LOWORD(v1) = -3 - v1;
v7 = 3 * (v3 ^ v5);
if ( v7 )
  v8 = v7 - HIWORD(v7) - ((v7 - HIWORD(v7)) >> 16);
else
  v8 = -2 - (v3 ^ v5);
v9 = (v8 + (v1 ^ v4));
if ( 2 * v9 )
  v10 = (2 * v9) - ((2 * v9) >> 16) - (((2 * v9) - ((2 * v9) >> 16)) >> 16);
else
  v10 = ~v9;
*a1 = (v5 ^ v10) | ((v10 ^ v3) << 16);
result = a1 + 1;
a1[1] = (((v10 + v8) ^ v4) << 16) | ((v10 + v8) ^ v1);
return result;