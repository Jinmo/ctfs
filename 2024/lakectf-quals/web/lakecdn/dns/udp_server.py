# udp dnslib server

import socket
from dnslib import QTYPE, RCODE, RR, A, DNSRecord, DNSHeader, CNAME

# listen on 53, parse DNSRecord, return A record
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('172.26.14.204', 53))
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            request = DNSRecord.parse(data)
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            qname2 = b'registry.yarnpkg.com'
            qname3 = b'registry.npmjs.com'
            qname = request.q.qname
            qtype = request.q.qtype
            reply.q.qname = qname2
            if qtype == QTYPE.A:
                if qname == qname2 or 1:
                    new_var = A((3, 37, 52, 122))
                    reply.add_answer(RR(qname2, QTYPE.A, rdata=new_var))
                    reply.add_answer(RR(qname3, QTYPE.A, rdata=new_var))
                else:
                    new_var = CNAME(qname2)
                    reply.add_answer(RR(qname, QTYPE.CNAME, rdata=new_var))
            else:
                reply.header.rcode = RCODE.NXDOMAIN
            print(reply)
            sock.sendto(reply.pack(), addr)
        except Exception as e:
            import traceback
            
            traceback.print_exc()

if __name__ == '__main__':
    udp_server()
