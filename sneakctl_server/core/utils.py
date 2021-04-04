import sys
from collections import namedtuple
import os
import psutil
from psutil._common import addr, pconn
from psutil._pslinux import pcputimes


class ProcessAttributes:
    @staticmethod
    def get_all_attribute_names():
        return [key for key, value in ATTRIBUTES.items()]

    @staticmethod
    def get_attribute_names():
        return [key for key, value in ATTRIBUTES.items() if not value.verbose]

    @staticmethod
    def parse_attributes(attributes: dict):
        attrs = dict()
        for key, value in attributes.items():
            if ATTRIBUTES[key].func:
                # parsing function is present
                attrs[key] = ATTRIBUTES[key].func(value)
            else:
                attrs[key] = value

        return attrs

    @staticmethod
    def parse_connections(conns):
        if not conns:
            return conns

        connections = []
        for conn in conns:
            laddr = raddr = None
            if conn[3]:
                laddr = dict(addr(*conn[3])._asdict())
            if conn[4]:
                raddr = dict(addr(*conn[4])._asdict())

            connection_dict = dict(pconn(conn[0], conn[1], conn[2], laddr, raddr, conn[5])._asdict())
            print(connection_dict, file=sys.stderr)

            connections.append(connection_dict)
            
        return connections


ATTR = namedtuple('ATTR', ['verbose', 'func'])
ATTRIBUTES = {
    # (ATTR, VERBOSE, [parsing_func])
    'cmdline': ATTR(False, lambda x: ' '.join(x)),
    'connections': ATTR(True, ProcessAttributes.parse_connections), # requires additional parsing
    'cpu_num': ATTR(True, None),
    'cpu_percent': ATTR(False, None),
    'cpu_times': ATTR(True, lambda x: dict(pcputimes(*x)._asdict())), # requires additional parsing
    'create_time': ATTR(False, None),
    'cwd': ATTR(True, None),
    'environ': ATTR(True, None),
    'exe': ATTR(False, None),
    'memory_percent': ATTR(False, None),
    'name': ATTR(True, None),
    'num_fds': ATTR(True, None),
    'num_threads': ATTR(True, None),
    'open_files': ATTR(True, None),
    'pid': ATTR(False, None),
    'ppid': ATTR(False, None),
    'status': ATTR(False, None),
    'username': ATTR(False, None)
}


def get_all_instances(pname: str, full: bool = False):
    pids = pgrep(pname)
    processes = []
    for pid in pids:
        processes.append(process_info(int(pid), full))

    return processes


def pgrep(proc_pattern: str):
    """run 'pgrep' for given pattern of process and return
    a list of processes matching **proc_pattern** pattern
    """
    # TODO: fix Command Injection vulnerab !!!
    commandline = 'pgrep %s' % proc_pattern
    out = os.popen(commandline).read().strip()
    return list(out.splitlines())


def process_info(pid: int, full: bool = False):
    process = psutil.Process(pid)
    process_info_dict = process.as_dict(attrs=ProcessAttributes.get_all_attribute_names()) if full else process.as_dict(
        attrs=ProcessAttributes.get_attribute_names())
    return ProcessAttributes.parse_attributes(process_info_dict)


def str_to_bool(s: str):
    if s.lower() in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s.lower() in ['false', '0', 'f', 'n', 'no']:
        return False
    return None
