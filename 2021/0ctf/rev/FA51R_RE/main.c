#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#define __fastcall
#define _DWORD int32_t
#define _QWORD uint64_t
#define _WORD uint16_t
#define __int64 long
#define __int16 short
#define __int8 char

#include <stdarg.h>

uint64_t qword_700000008, seed;
unsigned __int16 Table[] = {0, 1, 16, 17, 256, 257, 272, 273, 4096, 4097, 4112, 4113, 4352, 4353, 4368, 4369};
unsigned __int16 values, values2[5];

__int64 __fastcall do_79958b70_transform(unsigned __int16 a1)
{
	return (2 * a1) & 0xEEEE | (a1 >> 3) & 0x1111u;
}

//----- (0000000700075000) ----------------------------------------------------
__int64 __fastcall do_c8ec4eba_dart(int mask, unsigned int row, char dart, char col)
{
	return (Table[row] << col) | (mask << (4 * dart));
}

__int64 do_188db852_rand()
{
  unsigned int v1; // [rsp+0h] [rbp-4h]

  v1 = (1103515245 * (uint32_t)(seed) + 12345) & 0x7FFFFFFF;
  seed = v1;
  return v1;
}

//----- (0000000700024000) ----------------------------------------------------
__int64 __fastcall do_2eef166f_transform(unsigned __int16 a1)
{
	return (unsigned __int16)((a1 >> 12) | (16 * a1));
}

//----- (000000070002A000) ----------------------------------------------------
char __fastcall do_31a8b2bb_isspace(int a1)
{
	return a1 == 32 || (a1 - 9) <= 4;
}

//----- (0000000700033000) ----------------------------------------------------
void __fastcall do_3e11029d(unsigned int a1, __int16 a2)
{
  while ( (int)a1 > 0 )
  {
    values2[a1] &= ~a2;
    values2[a1] |= a2 & values2[a1 - 1];
    --a1;
  }
}

__int64 do_30e23ac2()
{
  int v0; // ebx
  unsigned __int16 v2; // [rsp+3Eh] [rbp-22h]
  int a1; // [rsp+40h] [rbp-20h]
  int v4; // [rsp+44h] [rbp-1Ch]
  int i; // [rsp+48h] [rbp-18h]
  int j; // [rsp+4Ch] [rbp-14h]

  a1 = 4;
  while ( a1 )
  {
    v4 = 0;
    v2 = values2[a1];
    for ( i = 0; i <= 3; ++i )
    {
      v0 = 15 << (4 * i);
      if ( (_WORD)v0 == (v2 & (unsigned __int16)v0) )
      {
        v4 = 1;
        ++qword_700000008;
        do_3e11029d(a1, v0);
        v2 = values2[a1];
      }
    }
    for ( j = 0; j <= 3; ++j )
    {
      if ( (unsigned __int16)(0x1111 << j) == (v2 & (unsigned __int16)(0x1111 << j)) )
      {
        v4 = 1;
        ++qword_700000008;
        do_3e11029d(a1, 0x1111 << j);
        v2 = values2[a1];
      }
    }
    if ( !v4 )
      --a1;
  }
  return 0LL;
}

//----- (000000070003B000) ----------------------------------------------------
char do_5f66dd0c_win()
{
	return qword_700000008 > 0x96uLL;
}

//----- (000000070003F000) ----------------------------------------------------
char __fastcall do_632a2fa6_isnumeric(int a1)
{
	return (a1 - 48) <= 9;
}

unsigned __int16 __fastcall do_6adf580f_(__int16 value)
{
  unsigned __int16 result; // ax
  int i; // [rsp+10h] [rbp-4h]

  result = value;
  for ( i = 0; i <= 3; ++i )
  {
    result = value & values2[i + 1];
    if ( result )
    {
      result = value | values2[i];
      values2[i] = result;
      break;
    }
  }
  if ( i == 4 )
  {
    result = value | values2[4];
    values2[4] = result;
  }
  return result;
}

//----- (0000000700055000) ----------------------------------------------------
__int64 do_92e99fe8_random_dart()
{
  unsigned int v1; // [rsp+38h] [rbp-18h]

  v1 = do_188db852_rand();
  return do_c8ec4eba_dart(v1 & 0xF, (v1 & 0xff) >> 4, ((v1 >> 8) & 0xff) & 3, (((v1 >> 8) & 0xF) >> 2) & 3);
}

//----- (000000070005D000) ----------------------------------------------------
__int64 __fastcall do_a113ccb9()
{
	if ( values2[0] )
	{
		return -1;
	}
	return 0;
}

//----- (000000070005F000) ----------------------------------------------------
__int64 do_a351539e()
{
	return 0LL;
}
// 70005F000: using guessed type __int64 __fastcall do_a351539e();

//----- (0000000700073000) ----------------------------------------------------
void do_c7d66329_srand(unsigned int a1)
{
	seed = a1;
}

//----- (000000070007B000) ----------------------------------------------------
__int64 __fastcall do_e4036573(unsigned __int16 value, unsigned int inp)
{
  int upper; // [rsp+4Ch] [rbp-24h]
  int lower; // [rsp+50h] [rbp-20h]
  int i; // [rsp+54h] [rbp-1Ch]
  int j; // [rsp+58h] [rbp-18h]

  upper = 0;
  lower = 0;
  for ( i = 0; i <= 3; ++i )
  {
    if ( ((inp >> (i + 4)) & 1) != 0 )
    {
      value = do_2eef166f_transform(value);
      ++upper;
    }
  }
  for ( j = 0; j <= 3; ++j )
  {
    if ( ((inp >> j) & 1) != 0 )
    {
      value = do_79958b70_transform(value);
      ++lower;
    }
  }
  return value;
}

//----- (0000000700059000) ----------------------------------------------------
__int64 __fastcall do_957fd0e7(unsigned __int8 a1, unsigned __int16 value)
{
  int v3; // [rsp+6Ah] [rbp-6h]

  v3 = (unsigned __int16)do_e4036573(value, a1);
  do_6adf580f_(v3);
  if(do_a113ccb9()) return -1;
  do_30e23ac2();
  return 0LL;
}

//----- (0000000700035000) ----------------------------------------------------
__int64 __fastcall do_41c24acb(char *input, __int64 len)
{
  unsigned __int16 v3; // [rsp+56h] [rbp-2Ah]
  unsigned int i; // [rsp+58h] [rbp-28h]
  unsigned __int8 c; // [rsp+5Ch] [rbp-24h]

  for ( i = 0; len > i; ++i )
  {
  	if ( do_5f66dd0c_win() )
  		return 10000000;
  	c = input[i];
  	v3 = do_92e99fe8_random_dart();
  	if(do_957fd0e7(c, v3)) return -1;
  }
  return qword_700000008;
}

int main(int argc, char *argv[]) {
	__int64 max = -1;
	int seed = atoi(argv[1]);
	char inp[0x100] = {0};
	srand(clock());
	for(int j = 0; j < sizeof(inp); j++) {
		char target = 0;
		for(int i = 0; i < (1 << 8); i++) {
			do_c7d66329_srand(seed);
			memset(values2, 0, sizeof(values2));
			values = 0;
			qword_700000008 = 0;
			inp[j] = rand();
			if(inp[j] == 10) inp[j]++;
			else if(inp[j] == 0) inp[j]++;
			__int64 score = do_41c24acb(inp, j + 1);
			if(score == -1) continue;
			if(score > max) {
				max = score;
				target = inp[j];
				if(score == 10000000) {
					puts("solved!");
					int fd = open("/tmp/payload", O_CREAT|O_WRONLY, 0777);
					write(fd, inp, j + 1);
					close(fd);
					exit(0);
				}
			}
		}
		if(max == -1) return 0;
		printf("%d %ld %d\n", j, max, target);
		max = -1;
		inp[j] = target;
	}
}