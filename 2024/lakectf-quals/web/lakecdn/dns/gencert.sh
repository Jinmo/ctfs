# self-signed certificate generation script for localhost

# Generate a private key
openssl genrsa -out localhost.key 2048

# Generate a certificate signing request
openssl req -new -key localhost.key -out localhost.csr -subj "/C=US/ST=CA/L=San Francisco/O=My Company/CN=localhost"

# Generate a self-signed certificate
openssl x509 -req -days 365 -in localhost.csr -signkey localhost.key -out localhost.crt
