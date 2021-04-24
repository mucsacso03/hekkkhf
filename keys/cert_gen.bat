rm *.crt
rm root -r
mkdir root
cd root
openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout root_key.pem -out root_cert.crt -subj "/O=Root/CN=root"
cd ..
openssl genrsa -aes128 -out server_key.pem 2048
openssl req -key server_key.pem -new -out server_req.csr -subj "/O=Server/CN=server"
openssl x509 -days 60 -req -in server_req.csr -CA .\root\root_cert.crt -CAkey .\root\root_key.pem -CAcreateserial -out server_cert.crt
rm server_req.csr
rm root/root_cert.srl
cp root/root_cert.crt .
rename root_cert.crt ca_cert.crt
openssl verify -CAfile .\root\root_cert.crt .\server_cert.crt