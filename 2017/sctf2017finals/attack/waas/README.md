# 취약점

총 두개가 있습니다. 원인은 똑같은데요, frontend.py에서 불러오는 s.host는 헤더 기준이지만 path에 host가 있으면 flask, 즉 backend에서는 호스트값을 path에서 읽어서 불일치가 발생합니다. 이 취약점으로 아래와 같이 하면 admin 페이지가 불러와집니다.

```
GET http://admin.sctfwaas.com:8080/ HTTP/1.1
Host: lol
```

또한 역으로 이용하면 캐시 포이즈닝이 가능합니다. admin이 호스트에 들어가있는지 막는 것은 'admin.sctfwaas.com:8080'을 캐시에 등록한 후 응답을 보내는 과정에서 막는 것이므로 캐시 포이즈닝이 가능합니다.

```
GET http://my_api_key.sctfwaas.com:8080/ HTTP/1.1
Host: admin.sctfwaas.com:8080
```

admin 페이지의 특성은, 마지막으로 로그인한 시간과 현재 시간의 차이값을 초단위로 보여준다는 점입니다. admin 페이지를 반복적으로 불러왔을 때 이 값은 0~2까지 계속 반복되었으므로 계속해서 로그인 성공을 서버에서 시킨다는 것을 전제로 잡고 XSS를 시도했지만 자바스크립트를 실행하지 않는다는 점이 힌트에서 드러났고, form 태그를 잘 구성해서 서버로 오게 했더니 아이디 및 비밀번호가 오게 되었습니다. (hint/admin.py, solution/r.py 참고)

이제 첫 번째 응용을 이용하여 아이디, 비밀번호를 POST로 전송하면 플래그가 뜹니다.

플래그: SCTF{what_host_r_u_looking_for}