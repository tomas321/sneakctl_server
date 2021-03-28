#!/bin/bash
#
# usage: $0 DOCKER_IMAGE_TAG
#

usage="USAGE: $0 DOCKER_IMAGE_TAG"
[[ $# -lt 1 ]] && echo "$usage" && exit 1

name="sneakctl_server"
tag="$1"
image="$name:$tag"

# overwrite
echo "deleting old container"
sudo docker ps --all | grep $name && sudo docker rm $name -f

# docker image build and tagging
echo "building image: $image"
sudo docker build -t "$image" .
echo "tagging new image as latest"
sudo docker image tag "$image" "$name:latest"  # link image to 'latest' tag

# remove dangling images
images="$(sudo docker images -f 'dangling=true' -q)"
[[ "x$images" == "x" ]] || echo "removing dangling docker images: $images"
for i in $images; do
    sudo docker rmi "$i"
done

# docker run container
echo "running container"
sudo docker run -d --name $name -p 5000:5000 "$image"

echo Done