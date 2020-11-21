#!/bin/bash

sudo docker-compose -f /home/ubuntu/arquichat/docker-compose.production.yml down

sleep 15

# sudo docker stop $(sudo docker ps -a -q)
