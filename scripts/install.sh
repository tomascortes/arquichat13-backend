#!/bin/bash
sudo apt install python3-pip
sudo pip install awscli 
pwd=$( aws ecr get-login-password )
sudo service docker start
# sudo docker container stop $(docker container ls -aq)
sudo docker login -u AWS -p $pwd https://374139594143.dkr.ecr.us-east-2.amazonaws.com/arquichat
sudo docker pull 374139594143.dkr.ecr.us-east-2.amazonaws.com/arquichat
