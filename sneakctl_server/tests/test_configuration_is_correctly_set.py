from io import BytesIO
import unittest
from unittest.mock import patch

from sneakctl_server.flaskr.settings.base import CONFIG_DIR_PROD, CONFIG_DIR_DEV
from sneakctl_server.flaskr.settings.dev import DevConfig
from sneakctl_server.flaskr.settings.prod import ProdConfig

EXPECTED_KEYS_SET = {
    'REDIS_HOST', 'REDIS_PORT', 'REDIS_USER', 'REDIS_PWD', 'REDIS_DB', 'FLASK_ENV', 'CONFIG_DIR', 'HOST', 'PORT'
}


class TestBaseConfig(unittest.TestCase):
    def test_configuration_dir_is_correct_for_dev(self):
        with patch('sneakctl_server.flaskr.settings.base.open', create=True) as open_mock:
            open_mock.return_value.__enter__.return_value = BytesIO(bytes('testing: aa', encoding='utf-8'))
            cfg = DevConfig()

            self.assertEqual(cfg.get_config()['CONFIG_DIR'], CONFIG_DIR_DEV)

    def test_configuration_dir_is_correct_for_prod(self):
        with patch('sneakctl_server.flaskr.settings.base.open', create=True) as open_mock:
            open_mock.return_value.__enter__.return_value = BytesIO(bytes('testing: aa', encoding='utf-8'))
            cfg = ProdConfig()

            self.assertEqual(cfg.get_config()['CONFIG_DIR'], CONFIG_DIR_PROD)

    @patch('sneakctl_server.flaskr.settings.base.yaml.full_load')
    def test_config_has_all_required_keys_when_config_is_empty(self, yaml_load_mock):
        yaml_load_mock.return_value = dict()
        with patch('sneakctl_server.flaskr.settings.base.open', create=True) as open_mock:
            open_mock.return_value.__enter__.return_value = BytesIO(bytes('', encoding='utf-8'))
            cfg = DevConfig()

            self.assertSetEqual(set(cfg.get_config().keys()), EXPECTED_KEYS_SET)

    @patch('sneakctl_server.flaskr.settings.base.yaml.full_load')
    def test_config_has_all_required_keys(self, yaml_load_mock):
        yaml_load_mock.return_value = expected_config = {
            'redis': {
                'host': 'redis.local',
                'port': 6000,
                'user': 'redis',
                'password': 'redis',
                'db': 1
            }
        }
        with patch('sneakctl_server.flaskr.settings.base.open', create=True) as open_mock:
            open_mock.return_value.__enter__.return_value = BytesIO(bytes('', encoding='utf-8'))
            cfg = DevConfig()

            app_config = cfg.get_config()
            self.assertSetEqual(set(app_config.keys()), EXPECTED_KEYS_SET)
            self.assertEqual(app_config['REDIS_HOST'], expected_config['redis']['host'])


if __name__ == '__main__':
    unittest.main()
