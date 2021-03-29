from io import BytesIO
import unittest
from unittest.mock import patch

from sneakctl_server.flaskr.settings.base import CONFIG_DIR_PROD, CONFIG_DIR_DEV
from sneakctl_server.flaskr.settings.dev import DevConfig
from sneakctl_server.flaskr.settings.prod import ProdConfig


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


if __name__ == '__main__':
    unittest.main()
