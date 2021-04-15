from flask import Blueprint, request

import sneakctl_server.core.execsnoop.execsnoop as execsnoop
from sneakctl_server.core.utils import str_to_bool, get_all_systemd_units

execsnoop_blueprint = Blueprint('execsnoop_blueprint', __name__, url_prefix='/execsnoop')


@execsnoop_blueprint.route('/status', methods=['GET'])
def status():
    """
    Get status on all execsnoop processes. Use URL parameter 'reload' to reload the instances and get the current
    status. It defaults to true.

    :return: list of process_info dicts
    """
    status_response = dict(response={}, count=0)
    if not execsnoop.execsnoop_adapter:
        execsnoop.execsnoop_adapter = execsnoop.Execsnoop()
    if str_to_bool(request.args.get('reload', default='true')):
        execsnoop.execsnoop_adapter.load_instances()

    status_response['response']['process_instances'] = execsnoop.execsnoop_adapter.to_json()
    status_response['count'] = len(status_response['response']['process_instances'])

    return status_response


@execsnoop_blueprint.route('/services', methods=['GET'])
def services():
    """
    Get all execsnoop systemd services, that are manageable by this server.

    :return: list of services
    """
    units = get_all_systemd_units('execsnoop@')
    return {
        'response': units
    }
