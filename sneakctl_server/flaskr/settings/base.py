from os import environ, path
import yaml

from sneakctl_server import ROOT_DIR

CONFIG_DIR_PROD = '/etc/sneakctl_server'
CONFIG_DIR_DEV = path.abspath(path.join(ROOT_DIR, '../config/etc/sneakctl_server'))

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_USER = None
REDIS_PWD = None
REDIS_DB = 0
HOST = '0.0.0.0'
PORT = 5000


class BaseConfig:
    def __init__(self):
        self.config = dict()
        self.config['FLASK_ENV'] = environ.get('FLASK_ENV')

    def _load_config(self, config_base_dir):
        with open(path.join(config_base_dir, 'config.yml'), 'r') as config_fp:
            full_config = yaml.full_load(config_fp)

        self.config['REDIS_HOST'] = full_config.get('redis', {}).get('host', REDIS_HOST)
        self.config['REDIS_PORT'] = full_config.get('redis', {}).get('port', REDIS_PORT)
        self.config['REDIS_USER'] = full_config.get('redis', {}).get('user', REDIS_USER)
        self.config['REDIS_PWD'] = full_config.get('redis', {}).get('password', REDIS_PWD)
        self.config['REDIS_DB'] = full_config.get('redis', {}).get('db', REDIS_DB)

        self.config['HOST'] = full_config.get('host', HOST)
        self.config['PORT'] = full_config.get('port', PORT)

    def get_config(self) -> dict:
        return self.config if self.config else None
