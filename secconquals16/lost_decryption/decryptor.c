#include <dlfcn.h>
#include <stdio.h>

void swap(long long *a1) {
long long tmp = a1[1];
a1[1] = a1[0];
a1[0] = tmp;
}

int main() {
char *d = dlopen("./libencrypt.so", RTLD_NOW);
FILE *keyfp = fopen("key.bin", "rb");
FILE *flagfp = fopen("flag.enc", "rb");
long long key[2];
long long block[2];
d = dlsym(d, "encrypt");
d -= 0x8a0;
long long (*F)(long long, long long) = d + 0x700;
long long roundkeys[14][2];
memset(roundkeys, 0, sizeof(roundkeys));
fread(key, 1, 16, keyfp);
int rounds = 14;
int i = 0;
do {
memcpy(roundkeys[i], key, 16);
key[1] = F(key[1], 0x9104F95DE694DC50LL);
swap(key);
rounds--;
i++;
} while(rounds);
// write(1, roundkeys, sizeof(roundkeys));
while(fread(block, 1, 16, flagfp) == 16) {
long long lr;
rounds = 14;
i = 13;
do {
// printf("%p\n", roundkeys[i][1]);
lr = F(block[1], roundkeys[i][1]);
block[0] ^= lr;
swap(block);
rounds--;
i--;
} while(rounds);
write(1, block, 16);
}
}
