from flask import Blueprint, request
from werkzeug.exceptions import BadRequest, BadRequestKeyError

from sneakctl_server.core.utils import str_to_bool
from sneakctl_server.core.core import interface

fswatch_blueprint = Blueprint('fswatch_blueprint', __name__, url_prefix='/fswatch')


@fswatch_blueprint.route('/status', methods=['GET'])
def status():
    """
    Get status on all fswatch processes. Use URL parameter 'reload' to reload the instances and get the current
    status. It defaults to true.

    :return: list of process_info dicts
    """
    status_response = {'response': {}}
    if str_to_bool(request.args.get('reload', default='true')):
        interface.fswatch_adapter.load_instances()

    status_response['request'] = '/fswatch/status'
    status_response['response']['process_instances'] = interface.fswatch_adapter.to_json()
    status_response['response']['count'] = len(status_response['response']['process_instances'])

    return status_response


@fswatch_blueprint.route('/services', methods=['GET'])
def services():
    """
    Get all execsnoop systemd services, that are manageable by this server.

    :return: list of services
    """
    if request.method == 'GET':
        units = interface.systemd_adapter.get_all_systemd_units('fswatch@')
        return {
            'request': '/fswatch/services',
            'response': units
        }


@fswatch_blueprint.route('/services/<name>', methods=['GET', 'POST'])
def services_modify(name):
    """
    Get, stop or restart an fswatch service by name or all (<name> == '_all')

    json body:
    { "action": on of ["start", "stop", "restart"] }

    :param name: fswatch service name or '_all' for addressing all execsnoop services
    :return: status of changes made or requested service info
    """
    ALL_SERVICES = '_all'
    ALLOWED_ACTIONS = ['start', 'stop', 'restart']
    DEFAULT_STATUS_CODE = 200

    contents = {}
    response = {'request': f'/fswatch/services/{name}'}
    msg = {}
    status_code = DEFAULT_STATUS_CODE

    if request.method == 'POST':
        # GET a single service is allowed without body
        try:
            data = request.get_json(force=True)
            if 'action' not in data.keys():
                msg = {'message': 'error: bad body'}
                status_code = 400
                raise BadRequestKeyError()

            if 'action' in data.keys() and data['action'] not in ALLOWED_ACTIONS:
                msg = {'message': 'error: bad action'}
                status_code = 400
                raise BadRequestKeyError()
        except BadRequestKeyError:
            return msg, status_code
        except BadRequest:
            return {'message': 'error: missing data'}, 400

    elif request.method != 'GET':
        return {}, 400

    if status_code == DEFAULT_STATUS_CODE:
        units = interface.systemd_adapter.get_all_systemd_units('fswatch@')
        if request.method == 'GET':
            # resolve the GET request and return a single service
            if name == ALL_SERVICES:
                # ALL_SERVICES is allowed only for POST method
                msg = {'message': "info: use the designated API endpoint '/fswatch/services' or use POST"}
            else:
                found_service = [unit for unit in units if unit['name'] == name]
                if len(found_service) > 0:
                    contents = {'response': found_service[0]}
                if not contents:
                    msg = {'message': 'error: unknown service name'}
                    status_code = 404

        elif request.method == 'POST':
            names = [u['name'] for u in units]
            if name == ALL_SERVICES:
                contents = {'response': interface.systemd_adapter.run(data['action'], names)}
            else:
                for unit_name in names:
                    if unit_name.rstrip('.service') == name.rstrip('.service'):
                        contents = {'response': interface.systemd_adapter.run(data['action'], name)}
                        break

                if not contents and data['action'] == 'start':
                    # if no service was found and the action is start
                    contents = {'response': interface.systemd_adapter.run('start', name)}

            if not contents:
                msg = {'message': 'no services modified'}

    response.update(contents)
    response.update(msg)
    return response, status_code
