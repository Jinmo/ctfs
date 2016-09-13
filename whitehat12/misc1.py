import requests, urllib, urllib2

LOGIN_URL = 'http://misc001.whitehat.vn/Login.php'
SIGNUP_URL = 'http://misc001.whitehat.vn/Signup.php'

def Encrypt(string2):
    string3 = "";
    n2 = len(string2);
    n3 = 0;
    n4 = 0;
    for n in range(n2):
        string3 = string3 + string2[n];
        string3 = string3 + chr(ord(string2[n]) + 1);
        string3 = string3 + chr(ord(string2[n]) + 2);
        string3 = string3 + chr(ord(string2[n]) + 3);
    n2 = len(string3);
    n5 = n2 % 6;
    n = n2 / 6 if n5 == 0 else n2 / 6 + 1;
    arrstring= [''] * n;
    if (n5 == 0):
        for n3 in range(n):
            arrstring[n3] = string3[n4:n4 + 6];
            n4 += 6
    else:
        for n4 in range(n):
            if (n3 + 6 > n2 / 6 * 6):
                arrstring[n4] = string3[n3:n2 % 6 + n3];
                n3 += 6;
            else:
                arrstring[n4] = string3[n3:n3 + 6];
                n3 += 6;
    string2 = "";
    while (n > 0):
        string2 = string2 + arrstring[n - 1];
        n -= 1
    return string2;

data = {
    "Username": "1",
    "Password": Encrypt("1")
}

r = requests.post(LOGIN_URL, data="action="+urllib2.quote(Encrypt(urllib.urlencode(data))))
print r.text