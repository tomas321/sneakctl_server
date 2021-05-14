from collections import namedtuple
from datetime import datetime
import os
import psutil
from psutil._common import addr, pconn
from psutil._pslinux import pcputimes
import pwd, grp


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
            # print(connection_dict, file=sys.stderr)

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


def get_all_process_instances(pname: str, full: bool = False):
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


def get_os_stats_dict(fname):
    file_stats = os.stat(fname)
    return {x: getattr(file_stats, x) for x in dir(file_stats) if x.startswith('st_')}


def get_file_stats(filename:  str):
    conversion_mapping = {
        "st_atime": lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'),
        "st_atime_ns": lambda x: datetime.fromtimestamp(x/10**9).strftime('%Y-%m-%d %H:%M:%S.%f'),
        "st_blksize": lambda x: int(x),
        "st_blocks": lambda x: int(x),
        "st_ctime": lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'),
        "st_ctime_ns": lambda x: datetime.fromtimestamp(x/10**9).strftime('%Y-%m-%d %H:%M:%S.%f'),
        "st_dev": lambda x: int(x),
        "st_gid": lambda x: grp.getgrgid(x).gr_name,
        "st_ino": lambda x: int(x),
        "st_mode": lambda x: str(oct(x))[2:],
        "st_mtime": lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'),
        "st_mtime_ns": lambda x: datetime.fromtimestamp(x/10**9).strftime('%Y-%m-%d %H:%M:%S.%f'),
        "st_nlink": lambda x: int(x),
        "st_rdev": lambda x: int(x),
        "st_size": lambda x: int(x),
        "st_uid": lambda x: pwd.getpwuid(x).pw_name
    }
    try:
        file_stats_dict = get_os_stats_dict(filename)
        parsed_dict = {}
        from sys import stderr
        for k, v in file_stats_dict.items():
            parsed_dict[k] = conversion_mapping[k](v)

        return 0, {'stats': parsed_dict, 'filename': filename}
    except FileNotFoundError as e:
        return 1, {'error': str(e)}
