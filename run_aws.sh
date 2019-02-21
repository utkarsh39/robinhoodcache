#! /bin/bash
. aws_env.sh && ./deploy/aws_deploy.sh $(cat swarm/managers.txt | grep "#" | sed 's/#//g')
