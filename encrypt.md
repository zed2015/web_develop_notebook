### rsa
- 公钥私钥的表现形式
> `http://github.tiankonguse.com/blog/2017/07/01/ASN1-SRA.html`

### ca
```
openssl genrsa  -out ca.key 2048

openssl req -sha256 -new -x509 -days 36500 -key ca.key -out ca.crt -subj "/C=CN/ST=BJ/L=BJ/O=zhang/OU=chi/CN=selfRoot"


openssl req -new \
    -sha256 \
    -key server.key \
    -subj "/C=CN/ST=BJ/L=BJ/O=zhang/OU=chi/CN=ainnovation.com" \
    -reqexts SAN \
    -config <(cat /home/zc/anaconda3/ssl/openssl.cnf \
        <(printf "[SAN]\nsubjectAltName=DNS.1:*.ainnovation.com,IP.1:127.0.0.1,IP.2:39.104.65.219")) \
    -out server.csr


openssl ca -in server.csr \
        -md sha256 \
        -keyfile ca.key \
    -cert ca.crt \
    -extensions SAN \
    -config <(cat /home/zc/anaconda3/ssl/openssl.cnf\
        <(printf "[SAN]\nsubjectAltName=DNS.1:*.ainnovation.com,IP.1:127.0.0.1,IP.2:39.104.65.219")) \
    -out server.crt
```
