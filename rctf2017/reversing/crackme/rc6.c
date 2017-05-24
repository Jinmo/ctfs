// from http://webcache.googleusercontent.com/search?q=cache:iMqTMnspPxsJ:www.fobwaimao.com/thread-213714.htm+&cd=1&hl=ko&ct=clnk&gl=kr

#include <stdint.h>
#include <string.h>
typedef char bool;
typedef unsigned int DWORD;

typedef struct _context
{
	unsigned int unkonwn1;
	unsigned int *sn;
	int len;
	unsigned int key_a;
	unsigned int key_b;
	unsigned int key_table[32];
	unsigned int key_d;
	unsigned int key_e;
}context;

unsigned int shrl(unsigned int a1, char a2)
{
	return (a1 << a2) | (a1 >> (32 - a2));
}

unsigned int inner_log(int a1)
{
	return (unsigned int)(a1 << (32 - (uint64_t)8LL)) >> (32- (uint64_t)8LL);
}

unsigned int shlr(unsigned int a1, char a2)
{
	return (a1 >> a2) | (a1 << (32 - a2));
}


unsigned char data[] = {
202, 244, 96, 22, 220, 183, 47, 113, 61, 234, 125, 243, 200, 46, 168, 23, 46, 58, 71, 206, 51, 133, 227, 16, 79, 177, 133, 93, 135, 176, 5, 132, 252, 202, 143, 137, 244, 54, 23, 189, 225, 141, 241, 137, 91, 63, 55, 228, 39, 38, 239, 209, 106, 223, 177, 218, 240, 99, 4, 143, 215, 121, 80, 34, 77, 212, 102, 208, 225, 224, 204, 18, 58, 251, 229, 4, 218, 36, 98, 202, 51, 197, 212, 149, 77, 168, 129, 129, 68, 32, 243, 186, 57, 119, 38, 68, 247, 189, 97, 107, 108, 132, 29, 37, 56, 115, 95, 118, 209, 224, 43, 87, 27, 194, 155, 54, 246, 35, 186, 130, 170, 246, 114, 79, 211, 177, 103, 24
};

/*
0xF5, 0x9B, 0x55, 0x20, 0xF6, 0x01, 0xB5, 0x69, 0x98, 0x4F, 0xD1, 0xA9,
	0x70, 0x40, 0x9E, 0xDC, 0x2B, 0x7D, 0xB9, 0x1F, 0x1F, 0xB2, 0xA0, 0x14, 0x5F, 0x49, 0xE1, 0xEA,
	0x50, 0x1E, 0x41, 0xD8, 0xEA, 0x22, 0xD6, 0x94, 0xE5, 0x8F, 0x56, 0xCD, 0x36, 0x63, 0x10, 0x32,
	0x1F, 0xF0, 0xF7, 0x09, 0xD9, 0xF6, 0x5C, 0x5E, 0xA0, 0x25, 0x2F, 0xBE, 0x92, 0x63, 0x9C, 0x2E,
	0xD1, 0x6D, 0xEA, 0xBB, 0x6D, 0x07, 0xAF, 0x7F, 0x4C, 0xFA, 0xD7, 0x9B
};
*/

void encrypt(context *ctx, bool encrypt)
{
	int *cur_dword; // esi@2
	unsigned int *tmp_key; // ebx@2
	int fourth_dword; // eax@3
	unsigned int v10; // ST28_4@3
	unsigned int v14; // eax@3
	bool v18; // zf@3
	signed int block_size; // [sp+24h] [bp-Ch]@2
	unsigned int offset = 0;

	if (ctx->len)
	{
		if (encrypt)
		{
			do
			{
				cur_dword = (int *)((unsigned char*)ctx->sn + offset);
				tmp_key = &ctx->key_table[31];
				block_size = 16;
				*cur_dword -= ctx->key_d;
				cur_dword[2] -= ctx->key_e;
				do
				{
					fourth_dword = cur_dword[3];
					cur_dword[3] = cur_dword[2];
					cur_dword[2] = cur_dword[1];
					cur_dword[1] = *cur_dword; 
					*cur_dword = fourth_dword; 

					v10 = shrl(cur_dword[1] * (2 * cur_dword[1] + 1), 8); // 调换前5个比特与后27个比特
					v14 = shrl((DWORD)cur_dword[3] * (2 * (DWORD)(cur_dword[3]) + 1), 8);
					
					*cur_dword = v10 ^ shlr(*cur_dword - *(tmp_key - 1), inner_log(v14));
					cur_dword[2] = ((DWORD)v14) ^ shlr(cur_dword[2] - *tmp_key, inner_log(v10));;

					tmp_key -= 2;
					v18 = block_size-- == 1;					
				} while (!v18);

				offset += 16;
				cur_dword[1] -= ctx->key_a;
				cur_dword[3] -= ctx->key_b;
			} while (offset < ctx->len);
		}
		else
		{
			do
			{
				cur_dword = (int *)((unsigned char*)ctx->sn + offset);
				tmp_key = &ctx->key_table[-1];
				block_size = 16;

				cur_dword[1] += ctx->key_a;
				cur_dword[3] += ctx->key_b;

				do
				{
					tmp_key += 2;

					v10 = shrl(cur_dword[1] * (2 * cur_dword[1] + 1), 8); // 调换前5个比特与后27个比特
					v14 = shrl((DWORD)cur_dword[3] * (2 * (DWORD)(cur_dword[3]) + 1), 8);

					int y = *cur_dword ^v10;
					int x = shrl(y, inner_log(v14));
					*cur_dword = x + *(tmp_key - 1);

					int n = cur_dword[2] ^ ((DWORD)v14);
					int m = shrl(n, inner_log(v10));
					cur_dword[2] = m + *tmp_key;

					fourth_dword = *cur_dword;
					*cur_dword = cur_dword[1];
					cur_dword[1] = cur_dword[2];
					cur_dword[2] = cur_dword[3];
					cur_dword[3] = fourth_dword;

					v18 = block_size-- == 1;
				} while (!v18);

				*cur_dword += ctx->key_d;
				cur_dword[2] += ctx->key_e;

				offset += 16;

			} while (offset < ctx->len);
		}
	}
}

char sn[33] = " \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00";

unsigned char g_data[64] = { // from preprocess.py
243, 56, 159, 56, 241, 33, 111, 152, 99, 239, 107, 106, 185, 26, 56, 181, 116, 137, 164, 250, 121, 22, 144, 200, 113, 46, 201, 99, 13, 223, 111, 77, 114, 127, 192, 105, 61, 118, 63, 238, 201, 35, 52, 118, 45, 183, 28, 56, 120, 247, 197, 41, 106, 19, 12, 188, 94, 179, 174, 182, 98, 188, 10, 56,
125, 52, 19, 249, 137, 7, 14, 255, 161, 59, 248, 250, 48, 20, 154, 183, 0, 72, 41, 120, 246, 50, 60, 49, 219, 26, 193, 198, 152, 46, 127, 186, 76, 233, 39, 129, 206, 254, 35, 93, 6, 66, 124, 80, 211, 7, 228, 86, 153, 234, 166, 210, 54, 157, 165, 82, 175, 117, 130, 204, 218, 20, 89, 217
};

int main(int argc, char* argv[])
{
	context ctx = { 0 };
	ctx.sn = (unsigned int*)g_data;
	ctx.len = 64;
	ctx.key_a = 0x5bf76637;
	ctx.key_b = 0x4748da7a;
	memcpy(ctx.key_table, data, 4 * 32);
	ctx.key_d = 0x7faf076d;
	ctx.key_e = 0x9bd7fa4c;
	encrypt(&ctx, 0);
	for(int i = 0; i < 64; i+=2)
		putchar(g_data[i]);

	ctx.sn = (unsigned int*)g_data;
	encrypt(&ctx, 0);
	return 0;
}

