# Set the base image to Ubuntu
FROM ubuntu:18.04
# File Author / Maintainer
MAINTAINER Utkarsh
ENV DEBIAN_FRONTEND=noninteractive
# Update the sources list
RUN apt-get update
RUN apt-get -qq install -y git curl socat net-tools emacs-nox tar procps
RUN apt-get -qq install -y build-essential tcl
WORKDIR /tmp
RUN git clone https://github.com/utkarsh39/redis.git
RUN cd redis && git checkout group_get
RUN cd redis && make && make install
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

CMD ./start.sh
