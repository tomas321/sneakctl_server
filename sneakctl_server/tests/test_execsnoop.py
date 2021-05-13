from copy import deepcopy
from datetime import datetime
import unittest
from unittest.mock import patch

from sneakctl_server.core.execsnoop.execsnoop import Execsnoop

execsnoop_dicts = [
    {
        "cmdline": "/usr/bin/python /usr/share/bcc/tools/execsnoop -t -u root",
        "cpu_percent": 0.0,
        "create_time": 1617374949.67,
        "exe": "/usr/local/bin/python3.6",
        "memory_percent": 0.14426940640952218,
        "pid": 7,
        "ppid": 1,
        "status": "sleeping",
        "username": "root"
    },
    {
        "cmdline": "/usr/bin/python /usr/share/bcc/tools/execsnoop -t -T -u tomas",
        "cpu_percent": 0.0,
        "create_time": 1617374950.04,
        "exe": "/usr/local/bin/python3.6",
        "memory_percent": 0.15903539981076925,
        "pid": 10,
        "ppid": 7,
        "status": "sleeping",
        "username": "root"
    }
]

expected_execsnoop_instances = deepcopy(execsnoop_dicts)
for i in range(len(execsnoop_dicts)):
    for k, v in execsnoop_dicts[i].items():
        if k == 'create_time':
            expected_execsnoop_instances[i][k] = datetime.fromtimestamp(v)


class MyTestCase(unittest.TestCase):
    def __test_execsnoop_obj_has_all_attributes(self, index):
        i = index
        with patch('sneakctl_server.core.execsnoop.execsnoop.get_all_process_instances', return_value=[execsnoop_dicts[i]]):
            execsnoop = Execsnoop()
            execsnoop_test_instance = execsnoop.instances.pop()
            for k, v in expected_execsnoop_instances[i].items():
                self.assertEqual(getattr(execsnoop_test_instance, k), v)

            self.assertEqual(execsnoop_test_instance.options,
                             expected_execsnoop_instances[i]['cmdline'].split('execsnoop')[1].strip())

            return execsnoop_test_instance

    def test_execsnoop_obj0_has_all_attributes(self):
        execsnoop_instance = self.__test_execsnoop_obj_has_all_attributes(0)

        self.assertEqual(execsnoop_instance.execsnoop_time, True)
        self.assertEqual(execsnoop_instance.execsnoop_username, 'root')

    def test_execsnoop_obj1_has_all_attributes(self):
        execsnoop_instance = self.__test_execsnoop_obj_has_all_attributes(1)

        self.assertEqual(execsnoop_instance.execsnoop_time, True)
        self.assertEqual(execsnoop_instance.execsnoop_timestamp, True)
        self.assertEqual(execsnoop_instance.execsnoop_username, 'tomas')


if __name__ == '__main__':
    unittest.main()
