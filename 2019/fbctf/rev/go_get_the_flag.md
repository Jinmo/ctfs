# go_get_the_flag

```
Go get the flag!
```

A Mach-O binary compiled with Go is given. After running tools from [here](https://github.com/sibears/IDAGolangHelper), I could rename almost functions in the binary. There is `main_main`, `main_wrongpass`, `main_checkpassword`.

```c
void main_wrongpass() {
	puts("Wrong password!");
}
int main_checkpassword(char *c) {
	if(strlen(c) == 18 && strcmp(c, "s0_M4NY_Func710n2!") == 0) {
		print_flag();
	} else main_wrongpass();
}

int main() {
	main_checkpassword(argv[1]);
}
```

```
$ ./ggtf 's0_M4NY_Func710n2!'
fb{.60pcln74b_15_4w350m3}
```