from datetime import datetime

from sneakctl_server.core.utils import get_all_instances
from sneakctl_server.core.execsnoop.cmd import execsnoop_options


class ExecsnoopInstance:
    def __init__(self, process: dict):
        """

        :param process_info: psutil dict info of a process
        """
        self.attributes = []
        for k, v in process.items():
            self.attributes.append(k)
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

    def to_json(self):
        json_attrs = {}
        for attr in self.attributes:
            json_attrs[attr] = getattr(self, attr)

        return json_attrs


class Execsnoop:
    def __init__(self):
        self.instances = list()
        self.__load_instances()

    def __load_instances(self):
        for instance in get_all_instances('execsnoop'):
            self.instances.append(ExecsnoopInstance(instance))

    def to_json(self):
        json_instances = []
        for i in self.instances:
            json_instances.append(i.to_json())

        return json_instances


execsnoop_adapter = None
