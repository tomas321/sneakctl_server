from flask import Blueprint, request

import sneakctl_server.core.execsnoop as execsnoop
from sneakctl_server.core.utils import str_to_bool

execsnoop_blueprint = Blueprint('execsnoop_blueprint', __name__, url_prefix='/execsnoop')


@execsnoop_blueprint.route('/process/<proc>')
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

    return status_response
