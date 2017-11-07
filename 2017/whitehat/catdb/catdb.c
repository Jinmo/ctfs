#include <openssl/blowfish.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
    FILE *stream = fopen("cat.db", "r");
    char magic[] = "MEOW";
    char *v7;
    unsigned short *ptr;
    char ivec[8];
    BF_KEY v9;
    fread(magic, 4, 1, stream);
    v7 = calloc(1uLL, 0x10000);
    while(!feof(stream)) {
        size_t size, v4, cur;
        ptr = (unsigned short *)calloc(1uLL, 0x14uLL);
        ivec[0] = 1;
        ivec[1] = 2;
        ivec[2] = 3;
        ivec[3] = 4;
        ivec[4] = 5;
        ivec[5] = 6;
        ivec[6] = 7;
        ivec[7] = 8;
        int fp = fread(ptr, 0x14uLL, 1uLL, stream);
        if ( fp == -1LL || !fp )
        return 0LL;
        BF_set_key(&v9, 2LL, ptr);
        BF_cbc_encrypt(ptr + 1, ptr + 1, 8LL, &v9, ivec, 0LL);
        BF_cbc_encrypt(ptr + 5, ptr + 5, 8LL, &v9, ivec, 0LL);
        size = ptr[9];
        v4 = 8 - (size & 7);
        printf("fileName: %s\n", ptr + 1);
        printf("comment: %s\n", ptr + 5);
        cur = size + v4;
        FILE *dest = fopen(ptr + 1, "wb");
        while(1) {
            fp = fread(v7, cur, 1uLL, stream);
            if(fp <= 0) {
                puts("?");
                exit(0);
            }
            printf("reading %d bytes\n", cur);
            BF_cbc_encrypt(v7, v7, cur, &v9, ivec, 0LL);
            fwrite(v7, cur, 1, dest);
            if(memmem(v7, cur, "\xff\xd9", 2)) {
                puts("read!");
                break;
            }
            for(int i = 0; i < 16; i++) {
                printf("%02x ", (unsigned char)v7[i]);
            }
            puts("");
            cur = 0x10000;
        }
    }
}
