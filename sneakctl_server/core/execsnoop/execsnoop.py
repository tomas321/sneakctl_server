from datetime import datetime

from sneakctl_server.core.utils import pgrep, process_info
from sneakctl_server.core.execsnoop.cmd import execsnoop_options


def get_all_instances(pname: str = "execsnoop", full: bool = False):
    pids = pgrep(pname)
    processes = []
    for pid in pids:
        processes.append(process_info(pid, full))

    return processes


class ExecsnoopInstance:
    def __init__(self, process: dict):
        """

        :param process_info: psutil dict info of a process
        """
        for k, v in process.items():
            if k == 'create_time':
                setattr(self, k, datetime.fromtimestamp(v))
            else:
                setattr(self, k, v)

        self.options = self.cmdline.split('execsnoop')[1].strip()
        for option, meta in execsnoop_options.items():
            self.__set_option(option, meta)

    def __set_option(self, option_name: str, option_meta: dict):
        # TODO: rather loop through the cmdline and match the found options to the specified known args
        option_name = 'execsnoop_' + option_name
        for arg in option_meta['variations']:
            if arg in self.options:
                if option_meta['has_arg']:
                    setattr(self, option_name, self.options.split(arg)[1].strip().split()[0])
                else:
                    setattr(self, option_name, True)


class Execsnoop:
    def __init__(self):
        self.instances = list()
        self.__load_instances()

    def __load_instances(self):
        for instance in get_all_instances():
            self.instances.append(ExecsnoopInstance(instance))


execsnoop_adapter = None
