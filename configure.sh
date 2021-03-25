#!/bin/bash

# create the desired config.yml file from the example config
pushd config/etc/sneakctl_server/ || exit 1
cp config_example.yml config.yml
popd && exit 0