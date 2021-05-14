import unittest
from unittest.mock import patch

from sneakctl_server.core.utils import get_file_stats


example_file_stat = {
    "st_atime": 1620940299.475983,
    "st_atime_ns": 1620940299475983000,
    "st_blksize": 4096,
    "st_blocks": 8,
    "st_ctime": 1618662401.2761147,
    "st_ctime_ns": 1618662401276114700,
    "st_dev": 64769,
    "st_gid": 0,
    "st_ino": 3279562,
    "st_mode": 33188,
    "st_mtime": 1618662401.2641156,
    "st_mtime_ns": 1618662401264115500,
    "st_nlink": 1,
    "st_rdev": 0,
    "st_size": 697,
    "st_uid": 0
}
expected_file_stat_result = {
    "st_atime": '2021-05-13 23:11:39',
    "st_atime_ns": '2021-05-13 23:11:39.475983',
    "st_blksize": 4096,
    "st_blocks": 8,
    "st_ctime": '2021-04-17 14:26:41',
    "st_ctime_ns": '2021-04-17 14:26:41.276115',
    "st_dev": 64769,
    "st_gid": 'root',
    "st_ino": 3279562,
    "st_mode": '100644',
    "st_mtime": '2021-04-17 14:26:41',
    "st_mtime_ns": '2021-04-17 14:26:41.264116',
    "st_nlink": 1,
    "st_rdev": 0,
    "st_size": 697,
    "st_uid": 'root'
}


class TestFileStatConversion(unittest.TestCase):
    def test_data_from_os_stat_is_correctly_parsed(self):
        with patch('sneakctl_server.core.utils.get_os_stats_dict', return_value=example_file_stat) as os_stat_mock:
            rc, result = get_file_stats("dummy")
            self.assertDictEqual(result, expected_file_stat_result)


if __name__ == '__main__':
    unittest.main()
