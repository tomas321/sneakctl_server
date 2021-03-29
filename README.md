# sneakctl server

Server handling requests from sneakctl client tool.

## DEV setup
- clone the repo
- run the [configure.sh](configure.sh) script
```bash
DEST=/opt/sneakctl_server
git clone https://github.com/tomas321/sneakctl_server $DEST

pushd $DEST || exit 1
./configure.sh && popd && exit 0
```

### Docker
- assuming
    - you ran the `configure.sh` script
    - docker is ran on a remote host (e.g. LXC, VM)
    - the VM is accessible over ssh via host `user@host` or `ssh-config-host`

- this setups a docker container with all depenedencies (i.e. redis container)
```bash
./test-docker.sh user@host
# OR
./test-docker.sh ssh-config-host
```

## License

MIT

## Author

Tomas Bellus
