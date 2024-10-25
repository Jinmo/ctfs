#include <stdio.h>
#include <unistd.h>

int arginfo() {
	return 0;
}

int func(FILE *fp, char *payload, void **args) {
	write(1, payload, 20);
	return 0;
}

int main(int argc, char **argv) {
	char s[] = "CMSOXVNLREIU";
	for(int i = 0; i < sizeof(s) - 1; i++) {
		register_printf_function(s[i], func, arginfo);
	}
	printf(argv[1]);
}