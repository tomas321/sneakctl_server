from dbus import SystemBus, Interface, DBusException


class Systemd:
    def __init__(self):
        bus = SystemBus()
        systemd = bus.get_object(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1'
        )

        self.manager = Interface(
            systemd,
            'org.freedesktop.systemd1.Manager'
        )
        self.supported_operations = ['stop', 'start', 'restart']

    def run(self, operation: str, names):
        """
        Run a bulk request on a list of services.

        :param operation: one of [stop, start, restart]
        :param names: a single or a list of services
        :return: tuple of (number of successful operations, status list)
        """
        if type(names) is not list:
            names = [names]
        if operation.lower() not in self.supported_operations:
            return -1, f'error: unsupported action {operation.lower()}'

        status = []
        count = 0
        for name in names:
            # msg = {'status': 'operation failed'}

            if not name.endswith('.service'):
                name = f'{name}.service'

            if operation.lower() == 'stop':
                rc, msg = self.stop(name)
            elif operation.lower() == 'start':
                rc, msg = self.start(name)
            elif operation.lower() == 'restart':
                rc, msg = self.restart(name)

            if rc == 0:
                count += 1

            msg.update({'name': name})
            print(msg)
            status.append(msg)

        return {'services': status, 'successful': count, 'failed': len(names) - count}

    def __list_units(self):
        return self.manager.ListUnits()

    def start(self, name: str) -> (int, str):
        """
        Start the service.

        :param name: service name (e.g. database.service)
        :return: tuple of (return code, status message)
        """
        try:
            self.manager.StartUnit(name, 'replace')
            return 0, {'status': 'started'}
        except DBusException as e:
            return 1, {'error': str(e)}

    def stop(self, name: str) -> (int, str):
        """
        Stop the service.

        :param name: service name (e.g. database.service)
        :return: tuple of (return code, status message)
        """
        try:
            self.manager.StopUnit(name, 'replace')
            return 0, {'status': 'stopped'}
        except DBusException as e:
            return 1, {'error': str(e)}

    def restart(self, name: str) -> (int, str):
        """
        Try to restart the service.

        :param name: service name (e.g. database.service)
        :return: tuple of (return code, status message)
        """
        try:
            self.manager.TryRestartUnit(name, 'replace')
            return 0, {'status': 'restarted'}
        except DBusException as e:
            return 1, {'error': str(e)}

    def get_all_systemd_units(self, service_name_regex: str = None):
        def map_values(unit_dbus_data) -> dict:
            return {
                'name': str(unit_dbus_data[0]).replace('.service', ''),
                'description': str(unit_dbus_data[1]),
                'load_state': str(unit_dbus_data[2]),
                'active_state': str(unit_dbus_data[3]),
                'sub_state': str(unit_dbus_data[4]),
                'next_unit': str(unit_dbus_data[5]),
                'unit_obj_path': str(unit_dbus_data[6]),
                'queued_job_id': int(unit_dbus_data[7]),
                'queued_job_type': str(unit_dbus_data[8]),
                'queued_job_path': str(unit_dbus_data[9])
            }

        units_original = self.__list_units()
        units = []
        if not service_name_regex:
            units = [map_values(unit) for unit in units_original]
        else:
            for unit in units_original:
                if str(unit[0]).startswith(service_name_regex):
                    units.append(map_values(unit))

        return units
