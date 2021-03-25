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

## License

MIT

## Author

Tomas Bellus