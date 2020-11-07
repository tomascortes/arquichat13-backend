#!/bin/bash
pwd=$( aws ecr get-login-password )
docker container stop $(docker container ls -aq)
docker login -u AWS -p $pwd https://374139594143.dkr.ecr.us-east-2.amazonaws.com
docker pull 374139594143.dkr.ecr.us-east-2.amazonaws.com/arquichat
