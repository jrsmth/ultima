from flask_redis import FlaskRedis


def init_redis(app):
    return FlaskRedis(app)


# Get an element by its key and decode in utf-8 format
def get(client: FlaskRedis, key):
    return client.get(key).decode('utf-8')
