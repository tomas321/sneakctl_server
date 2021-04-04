from flask import Blueprint

from sneakctl_server.flaskr.db import get_db

db_blueprint = Blueprint('db_blueprint', __name__, url_prefix='/db')


@db_blueprint.route('/test', methods=['GET'])
def test():
    db = get_db()
    if db:
        return {'message': 'OK'}
    else:
        return {'message': 'FAILED'}
