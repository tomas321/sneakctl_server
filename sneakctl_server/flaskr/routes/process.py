from flask import Blueprint, request

from sneakctl_server.core.utils import get_all_instances, process_info
from sneakctl_server.core.utils import str_to_bool

process_blueprint = Blueprint('process_blueprint', __name__, url_prefix='/process')


@process_blueprint.route('/<proc>', methods=['GET'])
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

    try:
        proc = int(proc)
        status_response['response']['process_instances'] = process_info(proc, full_status)
    except ValueError:
        status_response['response']['process_instances'] = get_all_instances(proc, full_status)
    status_response['count'] = len(status_response['response']['process_instances'])

    return status_response
