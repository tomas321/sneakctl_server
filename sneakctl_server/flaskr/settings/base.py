from os import environ, path
import yaml

from sneakctl_server import ROOT_DIR

CONFIG_DIR_PROD = '/etc/sneakctl_server'
CONFIG_DIR_DEV = path.abspath(path.join(ROOT_DIR, '../config/etc/sneakctl_server'))


class BaseConfig:
    def __init__(self):
        self.config = dict()
        self.config['FLASK_ENV'] = environ.get('FLASK_ENV')

    @staticmethod
    def _load_config(config_base_dir):
        with open(path.join(config_base_dir, 'config.yml'), 'r') as config_fp:
            return yaml.full_load(config_fp)

    def get_config(self) -> dict:
        return self.config if self.config else None
