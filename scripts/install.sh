#!/bin/bash
pwd=$( aws ecr get-login-password )
docker container stop $(docker container ls -aq)
docker login -u AWS -p $pwd https://xxxxxxxxxxxxx.dkr.ecr.sa-east-1.amazonaws.com
docker pull xxxxxxxxxx.dkr.ecr.sa-east-1.amazonaws.com/MYAPP

