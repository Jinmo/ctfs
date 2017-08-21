extern char buf[];
#include <sys/mman.h>

int initz() {
  munmap(0x10000, 0x10000);
  void *z = mmap(0x10000, 0x20000, 7, 34|MAP_FIXED, -1, 0);
  memcpy(z, buf, 2360);
#define patch(addr, start) extern char start[]; extern char start##_end[]; memcpy(addr, start, start##_end - start);

patch(0x100a4, getchar_);
patch(0x10070, putchar_);
}

