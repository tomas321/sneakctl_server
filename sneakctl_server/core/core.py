from sneakctl_server.core.execsnoop.execsnoop import Execsnoop
from sneakctl_server.core.fswatch.fswatch import Fswatch
from sneakctl_server.core.systemd import Systemd
from sneakctl_server.core.tcptracer.tcptracer import Tcptracer


class Main:
    __instance = None

    def __init__(self):
        if Main.__instance is not None:
            raise Exception('this is a singleton class')
        else:
            self.__instance = self
        self.execsnoop_adapter = Execsnoop()
        self.systemd_adapter = Systemd()
        self.fswatch_adapter = Fswatch()
        self.tcptracer_adapter = Tcptracer()


interface = Main()
