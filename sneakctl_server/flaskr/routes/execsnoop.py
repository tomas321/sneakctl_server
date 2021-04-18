from flask import Blueprint, request

from sneakctl_server.core.utils import str_to_bool
from sneakctl_server.core.core import interface

execsnoop_blueprint = Blueprint('execsnoop_blueprint', __name__, url_prefix='/execsnoop')


@execsnoop_blueprint.route('/status', methods=['GET'])
def status():
    """
    Get status on all execsnoop processes. Use URL parameter 'reload' to reload the instances and get the current
    status. It defaults to true.

    :return: list of process_info dicts
    """
    status_response = dict(response={}, count=0)
    if str_to_bool(request.args.get('reload', default='true')):
        interface.execsnoop_adapter.load_instances()

    status_response['response']['process_instances'] = interface.execsnoop_adapter.to_json()
    status_response['count'] = len(status_response['response']['process_instances'])

    return status_response


@execsnoop_blueprint.route('/services', methods=['GET'])
def services():
    """
    Get all execsnoop systemd services, that are manageable by this server.

    :return: list of services
    """
    units = interface.systemd_adapter.get_all_systemd_units('execsnoop@')
    return {
        'response': units
    }


@execsnoop_blueprint.route('/services/<name>', methods=['GET', 'POST'])
def services_modify(name):
    """
    Get, stop or restart an execsnoop service by name

    json body:
    :key action: on of [start, stop, restart]

    :param name: execsnoop service name
    :return: status message
    """
    allowed_actions = ['start', 'stop', 'restart']
    data = request.get_json(force=True)
    if not data or (data and 'action' not in data.keys()):
        return {'error': 'bad body'}, 404
    if 'action' in data.keys() and data['action'] not in allowed_actions:
        return {'error': 'bad action'}

    units = interface.systemd_adapter.get_all_systemd_units('execsnoop@')
    rc = -2
    msg = 'error: unable to modify service'
    if request.method == 'GET':
        return [unit for unit in units if unit['name'] == name][0]
    elif request.method == 'POST':
        for unit in units:
            if unit['name'] == name:
                rc, msg = interface.systemd_adapter.run(data['action'], name)
                break
        if rc == -2 and data['action'] == 'start':
            # if no service was found and the action is start
            rc, msg = interface.systemd_adapter.run('start', name)

    if msg.startswith('error'):
        return {'name': name, 'error': msg}, 404
    else:
        return {'name': name, 'response': msg}
