void L322();
void L261();
void L7();
void L200();
void L428();
void L653();
void L1262();
void L397();
void L337();
void L52();
void L500();
void L470();
void L405();
void L540();
void L253();
void L413();

volatile char mem[0x2000];
volatile int regs[5];


void L52(){// bytearray(b'%0.4096hhM%0.255llI%1.0lM%1.8llL%0.1lU%1.0lM%1.16llL%0.1lU%1.200llM%2.1788llM%7C%-6144.1701736302llM%0.200hhM%0.255llI%0.37llO%0200.0C')
  regs[0] = *(int *)&mem[0x1000]; // 0.4096hhM
  regs[0] &= 255; // 0.255llI
  regs[1] = regs[0]; // 1.0lM
  regs[1] <<= 8; // 1.8llL
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = regs[0]; // 1.0lM
  regs[1] <<= 16; // 1.16llL
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 200; // 1.200llM
  regs[2] = 1788; // 2.1788llM
  L7(); // 7C
  *(int *)&mem[1800] = 1701736302; // -6144.1701736302llM
  regs[0] = *(int *)&mem[0xc8]; // 0.200hhM
  regs[0] &= 255; // 0.255llI
  regs[0] -= 37; // 0.37llO
  if(regs[0] == 0) L200(); // 0200.0C
}
void L7(){// bytearray(b'%3.1hM%3.0lE%+1.3lM%1.4llS%3.1lM%3.2lO%-7.3C')
  regs[3] = *(int *)&mem[regs[1]]; // 3.1hM
  regs[3] ^= regs[0]; // 3.0lE
  *(int *)&mem[regs[1]] = regs[3]; // +1.3lM
  regs[1] += 4; // 1.4llS
  regs[3] = regs[1]; // 3.1lM
  regs[3] -= regs[2]; // 3.2lO
  if(regs[3] < 0) L7(); // -7.3C
}
void L200(){// bytearray(b'%4.5000llM%0.13200llM%337C%0.0llM%500C%1262C%0653.0C')
  regs[4] = 5000; // 4.5000llM
  regs[0] = 13200; // 0.13200llM
  L337(); // 337C
  regs[0] = 0; // 0.0llM
  L500(); // 500C
  L1262(); // 1262C
  if(regs[0] == 0) L653(); // 0653.0C
}
void L337(){// bytearray(b'%1.1llM%2.2llM%261C%+322.1C%0.1llS%1.13600llM%1.0lO%+337.1C')
  regs[1] = 1; // 1.1llM
  regs[2] = 2; // 2.2llM
  L261(); // 261C
  if(regs[1] > 0) L322(); // +322.1C
  regs[0] += 1; // 0.1llS
  regs[1] = 13600; // 1.13600llM
  regs[1] -= regs[0]; // 1.0lO
  if(regs[1] > 0) L337(); // +337.1C
}
void L500(){// bytearray(b'%2.0lM%2.4096llS%4.2hM%4.255llI%+540.4C')
  regs[2] = regs[0]; // 2.0lM
  regs[2] += 4096; // 2.4096llS
  regs[4] = *(int *)&mem[regs[2]]; // 4.2hM
  regs[4] &= 255; // 4.255llI
  if(regs[4] > 0) L540(); // +540.4C
}
void L1262(){// bytearray(b'%0.0llM%1.0llM%1.4500llS%1.1hM%2.0llM%2.1374542625llS%2.1686915720llS%2.1129686860llS%1.2lE%0.1lU%1.4llM%1.4500llS%1.1hM%2.0llM%2.842217029llS%2.1483902564llS%1.2lE%0.1lU%1.8llM%1.4500llS%1.1hM%2.0llM%2.1868013731llS%1.2lE%0.1lU%1.12llM%1.4500llS%1.1hM%2.0llM%2.584694732llS%2.1453312700llS%1.2lE%0.1lU%1.16llM%1.4500llS%1.1hM%2.0llM%2.223548744llS%1.2lE%0.1lU%1.20llM%1.4500llS%1.1hM%2.0llM%2.1958883726llS%2.1916008099llS%1.2lE%0.1lU%1.24llM%1.4500llS%1.1hM%2.0llM%2.1829937605llS%2.1815356086llS%2.253836698llS%1.2lE%0.1lU')
  regs[0] = 0; // 0.0llM
  regs[1] = 0; // 1.0llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 1374542625; // 2.1374542625llS
  regs[2] += 1686915720; // 2.1686915720llS
  regs[2] += 1129686860; // 2.1129686860llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 4; // 1.4llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 842217029; // 2.842217029llS
  regs[2] += 1483902564; // 2.1483902564llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 8; // 1.8llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 1868013731; // 2.1868013731llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 12; // 1.12llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 584694732; // 2.584694732llS
  regs[2] += 1453312700; // 2.1453312700llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 16; // 1.16llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 223548744; // 2.223548744llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 20; // 1.20llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 1958883726; // 2.1958883726llS
  regs[2] += 1916008099; // 2.1916008099llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
  regs[1] = 24; // 1.24llM
  regs[1] += 4500; // 1.4500llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[2] = 0; // 2.0llM
  regs[2] += 1829937605; // 2.1829937605llS
  regs[2] += 1815356086; // 2.1815356086llS
  regs[2] += 253836698; // 2.253836698llS
  regs[1] ^= regs[2]; // 1.2lE
  regs[0] |= regs[1]; // 0.1lU
}
void L653(){// bytearray(b'%0.123456789llM%1.0llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.846786818llS%2.0lE%1.0llM%1.6144llS%+1.2lM%1.4llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.1443538759llS%2.0lE%1.4llM%1.6144llS%+1.2lM%1.8llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.1047515510llS%2.0lE%1.8llM%1.6144llS%+1.2lM%1.12llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.359499514llS%2.1724461856llS%2.0lE%1.12llM%1.6144llS%+1.2lM%1.16llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.241024035llS%2.0lE%1.16llM%1.6144llS%+1.2lM%1.20llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.222267724llS%2.0lE%1.20llM%1.6144llS%+1.2lM%1.24llM%1.4096llS%1.1hM%0.1lE%2.0llM%2.844096018llS%2.0lE%1.24llM%1.6144llS%+1.2lM')
  regs[0] = 123456789; // 0.123456789llM
  regs[1] = 0; // 1.0llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 846786818; // 2.846786818llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 0; // 1.0llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
  regs[1] = 4; // 1.4llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 1443538759; // 2.1443538759llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 4; // 1.4llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
  regs[1] = 8; // 1.8llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 1047515510; // 2.1047515510llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 8; // 1.8llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
  regs[1] = 12; // 1.12llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 359499514; // 2.359499514llS
  regs[2] += 1724461856; // 2.1724461856llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 12; // 1.12llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
  regs[1] = 16; // 1.16llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 241024035; // 2.241024035llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 16; // 1.16llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
  regs[1] = 20; // 1.20llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 222267724; // 2.222267724llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 20; // 1.20llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
  regs[1] = 24; // 1.24llM
  regs[1] += 4096; // 1.4096llS
  regs[1] = *(int *)&mem[regs[1]]; // 1.1hM
  regs[0] ^= regs[1]; // 0.1lE
  regs[2] = 0; // 2.0llM
  regs[2] += 844096018; // 2.844096018llS
  regs[2] ^= regs[0]; // 2.0lE
  regs[1] = 24; // 1.24llM
  regs[1] += 6144; // 1.6144llS
  *(int *)&mem[regs[1]] = regs[2]; // +1.2lM
}
void L261(){// bytearray(b'%3.0lM%3.2lN%0253.3C%2.1llS%3.2lM%3.3lX%3.0lO%3.1llO%-261.3C')
  regs[3] = regs[0]; // 3.0lM
  regs[3] %= regs[2]; // 3.2lN
  if(regs[3] == 0) L253(); // 0253.3C
  regs[2] += 1; // 2.1llS
  regs[3] = regs[2]; // 3.2lM
  regs[3] *= regs[3]; // 3.3lX
  regs[3] -= regs[0]; // 3.0lO
  regs[3] -= 1; // 3.1llO
  if(regs[3] < 0) L261(); // -261.3C
}
void L322(){// bytearray(b'%+4.0lM%4.2llS')
  *(int *)&mem[regs[4]] = regs[0]; // +4.0lM
  regs[4] += 2; // 4.2llS
}
void L540(){// bytearray(b'%2.0lM%2.2llX%2.5000llS%2.2hM%2.255llI%4.2lE%0.1llS%2.0lM%470C%4.0lS%4.255llI%0.2lM%2.1llO%2.4500llS%+2.4lM%500C')
  regs[2] = regs[0]; // 2.0lM
  regs[2] *= 2; // 2.2llX
  regs[2] += 5000; // 2.5000llS
  regs[2] = *(int *)&mem[regs[2]]; // 2.2hM
  regs[2] &= 255; // 2.255llI
  regs[4] ^= regs[2]; // 4.2lE
  regs[0] += 1; // 0.1llS
  regs[2] = regs[0]; // 2.0lM
  L470(); // 470C
  regs[4] += regs[0]; // 4.0lS
  regs[4] &= 255; // 4.255llI
  regs[0] = regs[2]; // 0.2lM
  regs[2] -= 1; // 2.1llO
  regs[2] += 4500; // 2.4500llS
  *(int *)&mem[regs[2]] = regs[4]; // +2.4lM
  L500(); // 500C
}
void L253(){// bytearray(b'%1.0llM')
  regs[1] = 0; // 1.0llM
}
void L470(){// bytearray(b'%1.0lM%1.1llO%0397.1C%+428.1C')
  regs[1] = regs[0]; // 1.0lM
  regs[1] -= 1; // 1.1llO
  if(regs[1] == 0) L397(); // 0397.1C
  if(regs[1] > 0) L428(); // +428.1C
}
void L397(){// bytearray(b'%0.0llM')
  regs[0] = 0; // 0.0llM
}
void L428(){// bytearray(b'%1.0lM%1.2llN%0405.1C%+413.1C%470C%0.1llS')
  regs[1] = regs[0]; // 1.0lM
  regs[1] %= 2; // 1.2llN
  if(regs[1] == 0) L405(); // 0405.1C
  if(regs[1] > 0) L413(); // +413.1C
  L470(); // 470C
  regs[0] += 1; // 0.1llS
}
void L405(){// bytearray(b'%0.2llV')
  regs[0] /= 2; // 0.2llV
}
void L413(){// bytearray(b'%0.3llX%0.1llS')
  regs[0] *= 3; // 0.3llX
  regs[0] += 1; // 0.1llS
}

int main() {
	L52();
}


