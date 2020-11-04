#!/bin/bash
docker-compose -f /home/ec2-user/web/foku/docker-compose.production.yml down
docker stop $(docker ps -a -q)