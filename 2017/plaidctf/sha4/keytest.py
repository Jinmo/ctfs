from Crypto.Cipher import DES
plain_text = 'asdfghij'
print 'plain Text: ', plain_text

des = DES.new('82514145', DES.MODE_ECB)
cipher_text = des.encrypt(plain_text)
print 'the cipher text is ', `cipher_text`

des = DES.new('93505044', DES.MODE_ECB)
print 'the decrypted text is: ', `des.decrypt(cipher_text)`