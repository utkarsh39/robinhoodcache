#! /bin/bash
docker swarm init
ADD_MGR=$(docker swarm join-token manager | grep docker)
ADD_WORKER=$(docker swarm join-token worker | grep docker)

for mgr in $(cat managers.txt)
do
    if [[ $mgr == "#"* ]]
    then
        continue
    fi
    echo "adding manager $mgr"
    chmod 400 ~/robinhood.pem
    scp -i ~/robinhood.pem install.sh $mgr:~/
    ssh -i ~/robinhood.pem $mgr ./install.sh
    ssh -i ~/robinhood.pem $mgr $ADD_MGR
done
for worker in $(cat workers.txt)
do
    echo "adding worker $worker"
    scp -i ~/robinhood.pem install.sh $worker:~/
    ssh -i ~/robinhood.pem $worker ./install.sh
    ssh -i ~/robinhood.pem $worker $ADD_WORKER
done
