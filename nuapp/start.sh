#! /bin/bash
if [[ $DEBUG ]]
then
    sleep 20d
elif [[ ! $SKIP_UNPACK ]]
then
    sleep 10m
fi
eth0=$(ifconfig | grep eth1 -A 2 | grep "inet" | awk '{print $2}')
pushd src
# curl -L ${CONFIG_URL}/${CONFIG}.tar.gz -o ${CONFIG}.tar.gz
# tar -xzvf ${CONFIG}.tar.gz
# mv config /config
rm -f redis.conf
touch redis.conf
echo "maxmemory 1gb" >> redis.conf
echo "maxmemory-samples 5" >> redis.conf
echo "maxmemory-policy allkeys-lru" >> redis.conf
echo "appendonly no" >> redis.conf
echo "save \"\"" >> redis.conf

redis-server redis.conf&
# ./start_controller.sh ${eth0} &
./start_cache.sh ${eth0} &
./start_app_server.sh ${eth0} &
popd

wait
