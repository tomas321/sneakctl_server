from io import BytesIO
import os
import unittest
from unittest.mock import patch

from sneakctl_server.settings.base import BaseConfig, CONFIG_DIR_DEV, CONFIG_DIR_PROD


class TestBaseConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.env_prod = patch.dict('os.environ', {'FLASK_ENV': 'production'})
        self.env_dev = patch.dict('os.environ', {'FLASK_ENV': 'development'})

    def test_configuration_dir_is_correct_for_dev(self):
        with self.env_dev:
            config = BaseConfig()
            self.assertEqual(config.CONFIG_DIR, CONFIG_DIR_DEV)

    @unittest.mock.patch('sneakctl_server.settings.base.open')  # have to mock non-existing prod config
    def test_configuration_dir_is_correct_for_prod(self, open_mock):
        open_mock.return_value.__enter__.return_value = BytesIO(bytes('testing: aa', encoding='utf-8'))
        with self.env_prod:
            config = BaseConfig()
            self.assertEqual(config.CONFIG_DIR, CONFIG_DIR_PROD)


if __name__ == '__main__':
    unittest.main()
