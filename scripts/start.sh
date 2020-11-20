#!/bin/bash
sudo ./init-letsencrypt.sh
sudo docker-compose -f /home/ubuntu/arquichat/docker-compose.production.yml up -d



# sudo docker-compose -f /home/ec2-user/arquichat/docker-compose.production.yml up -d

