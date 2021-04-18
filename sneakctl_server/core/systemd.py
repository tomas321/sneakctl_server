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
        self.operations = ['stop', 'start', 'restart']

    def run(self, operation: str, name: str):
        rc = -1
        msg = 'error'
        if not name or operation.lower() not in self.operations:
            return rc, msg

        if not name.endswith('.service'):
            name = f'{name}.service'

        try:
            if operation.lower() == 'stop':
                self.manager.StopUnit(name, 'replace')
                msg = 'stopped'
            elif operation.lower() == 'start':
                self.manager.StartUnit(name, 'replace')
                msg = 'started'
            elif operation.lower() == 'restart':
                self.manager.TryRestartUnit(name, 'replace')
                msg = 'restarted'
            rc = 0
        except DBusException as e:
            rc = 1
            msg = f'error: {str(e)}'

        return rc, msg

    def __list_units(self):
        return self.manager.ListUnits()

    def start(self, name: str):
        return self.run('start', name)

    def stop(self, name: str):
        return self.run('stop', name)

    def restart(self, name: str):
        return self.run('restart', name)

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
