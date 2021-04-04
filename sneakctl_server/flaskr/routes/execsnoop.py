from flask import Blueprint, request

import sneakctl_server.core.execsnoop.execsnoop as execsnoop
from sneakctl_server.core.utils import str_to_bool

execsnoop_blueprint = Blueprint('execsnoop_blueprint', __name__, url_prefix='/execsnoop')


@execsnoop_blueprint.route('/process/<proc>', methods=['GET'])
def process_status(proc):
    """
    Get status of each process matching the name. URL parameter 'full'
    specifies the verbosity of the output

    :param proc: process name for the called 'pgrep' command
    :return: list of matched processes with info
    """
    status_response = dict(response={})
    full_status = str_to_bool(request.args.get('full', default='false'))
    if full_status is None:
        return {'error': 'bad arg format'}
    status_response['response']['process_instances'] = execsnoop.get_all_instances(proc, full_status)
    status_response['count'] = len(status_response['response']['process_instances'])

    return status_response


@execsnoop_blueprint.route('/status', methods=['GET'])
def status():
    """
    Get status on all execsnoop processes

    :return: list of process_info dicts
    """
    status_response = dict(response={}, count=0)
    if execsnoop.execsnoop_adapter:
        status_response['response']['process_instances'] = execsnoop.execsnoop_adapter.to_json()
    else:
        status_response['response']['process_instances'] = []
    status_response['count'] = len(status_response['response']['process_instances'])

    return status_response


@execsnoop_blueprint.route('/load', methods=['POST'])
def load():
    """
    Load all execsnoop current processes. Use URL parameter 'force' to reload

    :return: operation status
    """
    rc = 200
    if not execsnoop.execsnoop_adapter or str_to_bool(request.args.get('force', default='false')):
        execsnoop.execsnoop_adapter = execsnoop.Execsnoop()
        rc = 201

    return {'response': 'OK'}, rc
