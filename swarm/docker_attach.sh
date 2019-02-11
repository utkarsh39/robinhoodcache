#! /usr/bin/bash
export PATH="${PATH}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
cmd="grep $1"
id=$(docker ps | $cmd | awk '{print $1}')
docker exec -it $id bash
