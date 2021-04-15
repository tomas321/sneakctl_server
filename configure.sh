#!/bin/bash
#
# USAGE: $0 (prod | dev)
#

usage="USAGE: $0 (prod | dev)"
[[ $# -lt 1 ]] && echo -e "error: missing argument\n$usage"

if [[ ! -f config/etc/sneakctl-server/config.yml ]]; then
    # create the desired config.yml file from the example config
    pushd config/etc/sneakctl-server/ || exit 2
    cp config_example.yml config.yml
    popd || exit 2
fi

case "$1" in
    dev)
        exit 0
        ;;
    prod)
        # create prod config dir and config.yml within it
        mkdir -p /etc/sneakctl-server
        pushd config/etc/sneakctl-server/ || exit 1
        cp config.yml /etc/sneakctl-server/config.yml
        popd && exit 0
        ;;
    *)
        echo -e "error: unknonwn arg '$1'\n$usage"
        exit 1
esac
