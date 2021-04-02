from sneakctl_server.core.utils import pgrep, process_info


def get_all_instances(pname: str = "execsnoop", full: bool = False):
    pids = pgrep(pname)
    processes = []
    for pid in pids:
        processes.append(process_info(pid, full))

    return processes
