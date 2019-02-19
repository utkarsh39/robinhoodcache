#! /bin/bash
cd /usr/local && sudo curl -O https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz
cd /usr/local && sudo tar -xvf go1.8.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin