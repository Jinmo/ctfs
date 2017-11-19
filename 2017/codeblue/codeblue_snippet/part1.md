### CODE BLUE Snippet (part 1)

This is web challenge. In top of index.php:

```php
<?php
include('config.php');
if (file_exists($USER_DIR . '/is_admin')) {
  exit($FLAG);
}
?>
```

The $USER_DIR is generated as below:

```php
session_start();
$USER_DIR = md5($SALT . $_SERVER['REMOTE_ADDR'] . session_id());
```

And it's known to user. SALT is secret.

```php
<?php
include('config.php');

$filename = strtolower($_POST['filename']);
if ($filename == 'is_admin' || preg_match('/\./', $filename)) {
  die('Hello hacker :)');
}

@mkdir($USER_DIR);
file_put_contents($USER_DIR . '/' . basename($_POST['filename']), $_POST['contents']);

header('Location: /');

```

Filename "is_admin" is filtered, but the real filename was basename(filename). If user uploads a/is_admin, "a/is_admin" != "is_admin", and the uploaded file was "is_admin". Got flag: **CBCTF{plz fix PHP Bug #72374}**.

After few hours, the challenge was fixed for this vulnerability. [Part 2](part2.md)