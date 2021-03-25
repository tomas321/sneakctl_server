#!/usr/bin/env python3
from flask import Flask

from sneakctl_server.settings.base import BaseConfig

app = Flask(__name__)
app_config = BaseConfig()


@app.route('/config')
def config():
    return app_config.get_config()


if __name__ == '__main__':
    app.run()
