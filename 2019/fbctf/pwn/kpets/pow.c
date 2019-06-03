#include <openssl/md5.h>

int main(int argc, char *argv[]) {
	long i = 0;
	char buf[100];
	char md[16];
	while(1){
		sprintf(buf,"%08x", i++);
		MD5(buf,8,md);
		if(memcmp(md,argv[1],3)==0){
			printf("%s", buf);
			return 0;
		}
	}
}
