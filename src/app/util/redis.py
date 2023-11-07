from flask_redis import FlaskRedis


# Wrapper functionality for the Flask Redis Client
class Redis:

    def __init__(self, app):
        self.client = FlaskRedis(app)

    def get(self, key):
        return self.client.get(key).decode('utf-8')
        # Get an element by its key and decode in utf-8 format

    def set(self, key, value):
        return self.client.set(key, value)
        # Sets a key-value element
