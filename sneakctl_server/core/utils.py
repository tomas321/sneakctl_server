import os
import psutil


full_process_attributes = [
    'cmdline',
    'connections',  # requires additional parsing
    'cpu_num',
    'cpu_percent',
    'cpu_times',  # requires additional parsing
    'create_time',
    'cwd',
    'environ',
    'exe',
    'memory_percent',
    'name',
    'num_fds',
    'num_threads',
    'open_files',
    'pid',
    'ppid',
    'status',
    'username'
]
process_attributes = [
    'cmdline',
    'pid',
    'ppid',
    'username',
    'cpu_percent',
    'memory_percent',
    'exe',
    'status',
    'create_time'
]


def pgrep(proc_pattern: str):
    """run 'pgrep' for given pattern of process and return
    a list of processes matching **proc_pattern** pattern
    """
    # TODO: fix Command Injection vulnerab !!!
    commandline = 'pgrep %s' % proc_pattern
    out = os.popen(commandline).read().strip()
    return list(out.splitlines())


def process_info(pid: int, full: bool = False):
    if type(pid) is not int:
        pid = int(pid)
    process = psutil.Process(pid)
    return process.as_dict(attrs=full_process_attributes) if full else process.as_dict(attrs=process_attributes)


def str_to_bool(s: str):
    if s.lower() in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s.lower() in ['false', '0', 'f', 'n', 'no']:
        return False
    return None
