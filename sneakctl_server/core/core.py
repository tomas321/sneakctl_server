from sneakctl_server.core.execsnoop.execsnoop import Execsnoop
from sneakctl_server.core.systemd import Systemd


class Main:
    __instance = None

    def __init__(self):
        if Main.__instance is not None:
            raise Exception('this is a singleton class')
        else:
            self.__instance = self
        self.execsnoop_adapter = Execsnoop()
        self.systemd_adapter = Systemd()


interface = Main()
