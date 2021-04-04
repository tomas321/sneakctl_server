from flask import current_app, g
import redis


def get_db(redis_db: int = None):
    if 'db' not in g:
        g.db = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'],
            db=redis_db if redis_db else current_app.config['REDIS_DB'],
            username=current_app.config['REDIS_USER'],
            password=current_app.config['REDIS_PWD']
        )

    try:
        if not g.db.ping():
            raise redis.exceptions.ConnectionError()
    except redis.exceptions.RedisError:
        return None

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
