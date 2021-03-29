from flask import Flask

from sneakctl_server.flaskr.settings import prod as prod_cfg, dev as dev_cfg
from sneakctl_server.flaskr import db, routes


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.app_context().push()

    if app.config['ENV'] == 'production':
        app_cfg = prod_cfg.ProdConfig()
    else:
        app_cfg = dev_cfg.DevConfig()

    app.config.update(app_cfg.get_config())

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    app.register_blueprint(routes.db_blueprint)

    db.init_app(app)

    return app
