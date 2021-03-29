#!/usr/bin/env python3
from json import dumps
from sneakctl_server.flaskr import create_app

app = create_app()


@app.route('/config')
def config():
    return dumps(app.config, default=str)


if __name__ == '__main__':
    app.run()
