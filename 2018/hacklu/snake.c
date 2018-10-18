int main() {
  char v5; // bl
  char v9; // al
  char v10; // dl
  char v11; // bl
  char input[100] = {0, };
  char table[] = "\x01\x95\x66\x3e\x1b\x56\x64\x2c\x28\x0a\x9a\x04\xad\x0c\xc8\xd9";
  for(int i = 0; i < 16; i++) {
  	for(input[i] = 0; input[i] < 128; input[i]++) {
  		if(i == 0) {
  			v5 = input[i];
  		} else {
  		}
  		v9 = input[i];
  		v10 = (32 * (((v5 >> 2) | (v5 << 6)) ^ 0xAE) | ((unsigned short)(char)(((v5 >> 2) | (v5 << 6)) ^ 0xAE) >> 3)) ^ 0x66;
  		v11 = v9 ^ ~((v10 >> 1) | (v10 << 7) | (v9 >> 4));
  		if(v11 == table[i]) {
			v5 = ~v11;
			break;
  		}
  	}
  }
  puts(input);

}