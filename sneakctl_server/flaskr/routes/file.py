import os

from flask import Blueprint, request
from werkzeug.exceptions import BadRequestKeyError, BadRequest

from sneakctl_server.core.utils import get_file_stats

files_blueprint = Blueprint('files_blueprint', __name__, url_prefix='/file')


@files_blueprint.route('/stats', methods=['POST'])
def stats():
    """
    Get a file stats

    :return: file stats dict
    """
    try:
        msg = {'message': 'error: missing data'}
        data = request.get_json(force=True)
        if 'file' not in data.keys():
            msg = {'message': 'error: bad body'}
            raise BadRequestKeyError()
    except (BadRequestKeyError, BadRequest, Exception) as e:
        return msg, 400

    status_code = 200
    contents = {}
    msg = {}
    response = {'request': '/file/stats'}

    rc, result = get_file_stats(data['file'])
    if rc == 0:
        response['response'] = result
    else:
        msg = result
        status_code = 404

    response.update(contents)
    response.update(msg)
    return response, status_code
