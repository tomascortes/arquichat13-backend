#!/bin/bash
sudo docker-compose -f /home/ubuntu/arquichat/docker-compose.yml down
sudo docker stop $(docker ps -a -q)