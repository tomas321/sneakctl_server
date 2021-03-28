#!/bin/bash

project_dir="sneakctl_server"

[ $# -ge 1 ] || echo "usage: SSH_HOST"

ssh_host="$1"
dest="$ssh_host:$project_dir"
version=$(python3 -c "from sneakctl_server.version import __version__; print(__version__)")

ssh $ssh_host DIR=$project_dir 'bash -s' <<-"ENDSSH"
    [[ -d $DIR ]] && mkdir -p $DIR
ENDSSH

rsync --progress -ar "." "$dest"

ssh $ssh_host DIR=$project_dir VERSION=$version "bash -s"  <<-"ENDSSH"
    cd $DIR && ./docker/build.sh "$VERSION"
ENDSSH
