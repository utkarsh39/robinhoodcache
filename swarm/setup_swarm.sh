#! /bin/bash
sudo snap enable docker
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
    scp -i ~/rh2.pem install.sh $mgr:~/
    ssh -i ~/rh2.pem $mgr ./install.sh
    ssh -i ~/rh2.pem $mgr "sudo snap enable docker"
    ssh -i ~/rh2.pem $mgr $ADD_MGR
done
for worker in $(cat workers.txt)
do
    echo "adding worker $worker"
    scp -i ~/rh2.pem install.sh $worker:~/
    ssh -i ~/rh2.pem $worker ./install.sh
    ssh -i ~/rh2.pem $worker "sudo snap enable docker"
    echo $ADD_WORKER
    ssh -i ~/rh2.pem $worker $ADD_WORKER
done
