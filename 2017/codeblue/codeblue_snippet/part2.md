### CODE BLUE Snippet (part 2)

The flag indicated the bug number: [72374](https://bugs.php.net/bug.php?id=72374). This can be triggered in export.php (See <--):

```php
<?php
include('config.php');

$tmpfile = tempnam('/tmp', 'cbs');

if (preg_match('/\.|\\\\|^\//', $_GET['dir']) === 1) {
  die('hello hacker :(');
}

$zip = new ZipArchive();
$zip->open($tmpfile, ZipArchive::CREATE);
$options = array('remove_path' => $_GET['dir']); // <--

$dir = trim($_GET['dir'], '/');
$zip->addGlob($dir . '/*', 0, $options); // <--

$zip->close();

$hmac = hash_hmac('sha256', file_get_contents($tmpfile), $MY_SECRET);
header("Content-Disposition: attachment; filename='${hmac}.zip'");
readfile($tmpfile);

unlink($tmpfile);
```

The url `export.php?dir=(user_hash)` is exposed to user. The filename of the zip has HMAC-ed zip content value. And the php bug is:

```
Title: ZipArchive::addGlob remove_path option strips first char of filename

Description:
------------
After adding a file by addGlob using add_path and remove_path options, the first character of the filename is stripped in the archive.

```

That is, remove_path is option that indicates the zip archiver will remove the specified prefix.
What if the prefix is `(user_hash)/`, not `(user_hash)`? If I have a post titled with `iis_admin`, it becomes `is_admin`. In this way we could get HMAC-signed ZIP with is_admin file.

After exporting, we can upload a file named is_admin. Got the flag.