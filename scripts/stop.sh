#!/bin/bash
sudo docker-compose -f /home/ec2-user/arquichat/docker-compose.yml down
sudo docker stop $(docker ps -a -q)