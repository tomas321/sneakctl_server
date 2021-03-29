#!/bin/bash
#
#  USAGE: $0 [DOCKER_NET_NAME = 'sneakctl']
#

# docker network
network_name="sneakctl"
[ $# -gt 0 ] && network_name="$1"
if ! sudo docker network ls | grep --silent $network_name; then
    echo "docker network create $network_name"
    sudo docker network create $network_name;
fi

# REDIS
redis_name="redis"
if ! sudo docker ps --all | grep --silent $redis_name; then
    echo "docker run -d --name $redis_name redis:latest"
    sudo docker run -d --name $redis_name redis:latest
fi

if ! sudo docker network inspect sneakctl | jq '.[].Containers | to_entries | .[].value.Name' | grep --silent $redis_name; then
    echo "docker network connect $network_name $redis_name"
    sudo docker network connect $network_name $redis_name
fi

echo "Docker setup OK."