all:
	tar czvf target.tgz package
	sed 's/HASH/$(shell sha1sum target.tgz | cut -d " " -f 1)/' template > lodash
	# sha512-(base64)
	SHA512=sha512-`openssl dgst -sha512 -binary target.tgz | openssl enc -base64 -A`
	sed -i 's/SHA512/$(SHA512)/' lodash
