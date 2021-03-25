import os
import yaml


from sneakctl_server import ROOT_DIR

CONFIG_DIR_PROD = '/etc/sneakctl_server'
CONFIG_DIR_DEV = os.path.abspath(os.path.join(ROOT_DIR, '../config/etc/sneakctl_server'))


class BaseConfig:
    def __init__(self):
        self.FLASK_ENV = os.environ.get('FLASK_ENV')
        self.CONFIG_DIR = CONFIG_DIR_PROD if self.FLASK_ENV == 'production' else CONFIG_DIR_DEV

        self.__load_config()

    def __load_config(self):
        with open(os.path.join(self.CONFIG_DIR, 'config.yml'), 'r') as config_fp:
            self.config = yaml.full_load(config_fp)

    def get_config(self) -> dict:
        return {
            "config": {
                "FLASK_ENV": self.FLASK_ENV,
                "config_dir": self.CONFIG_DIR,
                "other": self.config
            }
        }
