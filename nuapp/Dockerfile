# Set the base image to Ubuntu
FROM ubuntu:18.04
# File Author / Maintainer
MAINTAINER Ben Berg
ENV DEBIAN_FRONTEND=noninteractive
# Update the sources list
RUN apt-get update
RUN apt-get -qq install -y memcached python python-pip git curl socat net-tools emacs-nox tar procps
RUN apt-get -qq install -y build-essential tcl
RUN cd /tmp && curl -O http://download.redis.io/redis-stable.tar.gz
RUN cd /tmp && tar xzvf redis-stable.tar.gz
RUN cd /tmp/redis-stable && make && make install
RUN mkdir /etc/redis
RUN cp /tmp/redis-stable/redis.conf /etc/redis

RUN cd /usr/local && curl -O https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz
RUN cd /usr/local && tar -xvf go1.8.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin
RUN echo $PATH

ADD ./src /nuapp/src
ADD ./start.sh /nuapp/start.sh

WORKDIR /nuapp

# src has to be subdir
RUN GOPATH=$(pwd) CGO_ENABLED=0 go get appserver
RUN GOPATH=$(pwd) CGO_ENABLED=0 go build appserver

# EXPOSE 6379
# EXPOSE 27001-27064
EXPOSE 80
RUN pip2 install -r /nuapp/src/requirements.txt

CMD ./start.sh
