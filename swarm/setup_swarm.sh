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
    scp -o StrictHostKeyChecking=no -i ~/robinhood.pem install.sh $mgr:~/
    ssh -o StrictHostKeyChecking=no -i ~/robinhood.pem $mgr ./install.sh
    ssh -o StrictHostKeyChecking=no -i ~/robinhood.pem $mgr $ADD_MGR
done
for worker in $(cat workers.txt)
do
    echo "adding worker $worker"
    scp -o StrictHostKeyChecking=no -i ~/robinhood.pem install.sh $worker:~/
    ssh -o StrictHostKeyChecking=no -i ~/robinhood.pem $worker ./install.sh
    ssh -o StrictHostKeyChecking=no -i ~/robinhood.pem $worker $ADD_WORKER
done
