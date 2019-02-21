#! /bin/bash
hostname=$1
aws --region $AWS_REGION ecr get-login --no-include-email --registry-ids $AWS_ECR_ID > ecr_login.sh
scp -i $AWS_KEY_PATH ecr_login.sh  $AWS_USER@$hostname:~/
rm ecr_login.sh
scp -i $AWS_KEY_PATH swarm/$COMPOSE_FILE $AWS_USER@$hostname:~/docker-compose.yml
scp -i $AWS_KEY_PATH swarm/swarm.sh $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/stop_swarm.sh  $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/docker_attach.sh $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/docker_bash.sh $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/utils.sh $AWS_USER@$hostname:~/
ssh -i $AWS_KEY_PATH $AWS_USER@$hostname "rm -f ~/robinhood.pem"
scp -i $AWS_KEY_PATH $AWS_KEY_PATH $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/managers.txt $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/workers.txt $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/install.sh $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH swarm/setup_swarm.sh $AWS_USER@$hostname:~/
scp -i $AWS_KEY_PATH aws_env.sh $AWS_USER@$hostname:~/swarm_env.sh
ssh -i $AWS_KEY_PATH $AWS_USER@$hostname bash install.sh 
ssh -i $AWS_KEY_PATH $AWS_USER@$hostname bash setup_swarm.sh
ssh -i $AWS_KEY_PATH $AWS_USER@$hostname bash swarm.sh $region $config
