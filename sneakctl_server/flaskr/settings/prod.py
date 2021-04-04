from sneakctl_server.flaskr.settings.base import BaseConfig, CONFIG_DIR_PROD


class ProdConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.config['CONFIG_DIR'] = CONFIG_DIR_PROD

        self._load_config(CONFIG_DIR_PROD)
