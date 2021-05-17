#!/usr/bin/env python3
from json import dumps

from sneakctl_server.flaskr.app import create_app
from sneakctl_server.version import __version__

app = create_app()


@app.route('/config')
def config():
    return dumps(app.config, default=str)


@app.route('/')
def default():
    return {'version': __version__}


if __name__ == '__main__':
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
