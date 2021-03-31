#!/bin/bash

# MAIN VARS
project_dir="sneakctl_server"
network_name="sneakctl"

[ $# -lt 1 ] && echo "usage: $0 SSH_HOST" && exit 1
[ "$1" == "--help" ] && echo "usage: $0 SSH_HOST" && exit 0

ssh_host="$1"
dest="$ssh_host:$project_dir"
version=$(python3 -c "from sneakctl_server.version import __version__; print(__version__)")

ssh $ssh_host DIR=$project_dir 'bash -s' <<-"ENDSSH"
    [[ -d $DIR ]] && mkdir -p $DIR
ENDSSH

rsync --progress -ar "." "$dest"

ssh $ssh_host DIR=$project_dir VERSION=$version NET=$network_name "bash -s" <<-"ENDSSH"
    cd $DIR && ./docker/docker-setup.sh $NET && ./docker/build.sh "$VERSION" "$NET"
ENDSSH
