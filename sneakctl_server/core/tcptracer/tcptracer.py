from datetime import datetime

from sneakctl_server.core.utils import get_all_process_instances
from sneakctl_server.core.tcptracer.cmd import tcptracer_options


class TcptracerInstance:
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

        self.options = self.cmdline.split('tcptracer')[1].strip()
        for option, meta in tcptracer_options.items():
            self.__set_option(option, meta)

    def __set_option(self, option_name: str, option_meta: dict):
        # TODO: rather loop through the cmdline and match the found options to the specified known args
        option_name = 'tcptracer_' + option_name
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


class Tcptracer:
    def __init__(self):
        self.instances = set()
        self.load_instances()

    def load_instances(self):
        self.instances.clear()
        for instance in get_all_process_instances('tcptracer'):
            self.instances.add(TcptracerInstance(instance))

    def to_json(self):
        json_instances = []
        for i in self.instances:
            json_instances.append(i.to_json())

        return json_instances


tcptracer_adapter = None
