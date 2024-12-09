#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

int (*tcg_gen_code)(void *s, void *tb, uint64_t pc_start);
int (*tcg_dump_ops)(void *s, FILE *a2, char a3);

int hook(void *s, void *tb, uint64_t pc_start) {
  tcg_dump_ops(s, stdout, 0);
  return tcg_gen_code(s, tb, pc_start);
}

__attribute__((constructor)) void startup(void) {
  // parse proc self maps to get address of executable
  FILE *fp = fopen("/proc/self/maps", "r");
  if (fp == NULL) {
    perror("fopen");
    exit(1);
  }
  char buf[4096];
  uint64_t base = 0;
  while (fgets(buf, sizeof(buf), fp)) {
    puts(buf);
    if (strstr(buf, "bash")) {
      return;
    }
    if (strstr(buf, "/qemu-")) {
      char *start = strtok(buf, "-");
      char *end = strtok(NULL, " ");
      unsigned long long start_addr = strtoull(start, NULL, 16);
      unsigned long long end_addr = strtoull(end, NULL, 16);
      printf("start: %llx, end: %llx\n", start_addr, end_addr);
      base = start_addr;
      break;
    }
  }
  // patch base+0x125460 to jump to our code
  void *stub =
      mmap((void *)(base - 0x1000), 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
           MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
  if (stub == MAP_FAILED) {
    perror("mmap");
    exit(1);
  }
  tcg_gen_code = (void *)(base + 0x17c900);
  tcg_dump_ops = (void *)(base + 0x17a4c0);
  // movabs rax, 0xdeadbeefcafebabe
  // jmp rax
  unsigned char payload[] = "\x48\xb8\xbe\xba\xfe\xca\xef\xbe\xad\xde\xff\xe0";
  *(uint64_t *)(payload + 2) = (uint64_t)hook;
  memcpy(stub, payload, sizeof(payload));
  uint64_t target = base + 0x125460;
  uint32_t i32 = (uint64_t)stub - ((uint64_t)target + 5);
  mprotect((void *)(target & ~0xfff), 0x1000,
           PROT_READ | PROT_WRITE | PROT_EXEC);
  memcpy((void *)(target + 1), &i32, 4);
}