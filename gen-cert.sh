#!/bin/bash
 
#Required
domain=$1
commonname=$domain
 
#Change to your company details
country=GB
state=Nottingham
locality=Nottinghamshire
organization=Jamescoyle.net
organizationalunit=IT
email=administrator@jamescoyle.net
 
#Optional
password=dummypassword
 
if [ -z "$domain" ]
then
    echo "Argument not present."
    echo "Useage $0 [common name]"
 
    exit 99
fi
 
echo "Generating key request for $domain"
 
#Generate a key
openssl genrsa -des3 -passout pass:$password -out ssl.key 2048 -noout
 
#Remove passphrase from the key. Comment the line out to keep the passphrase
echo "Removing passphrase from key"
openssl rsa -in ssl.key -passin pass:$password -out ssl.key
 
#Create the request
echo "Creating CSR"
openssl req -new -key ssl.key -out ssl.csr -passin pass:$password \
    -subj "/C=$country/ST=$state/L=$locality/O=$organization/OU=$organizationalunit/CN=$commonname/emailAddress=$email"

openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt
