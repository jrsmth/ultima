from flask_redis import FlaskRedis
import json


# Wrapper functionality for the Flask Redis Client
class Redis:

    def __init__(self, app):
        self.client = FlaskRedis(app)

    def get(self, key):
        return self.client.get(key).decode('utf-8')
        # Get an element by its key and decode in utf-8 format

    def set(self, key, value):
        return self.client.set(key, value)
        # Set a key-value element

    def set_complex(self, key, complex_value):
        json_value = json.dumps(complex_value)
        return self.client.set(key, json_value)
    # Set a complex key-value element by converting to json string

    def get_complex(self, key):
        json_value = self.client.get(key).decode('utf-8')
        return json.loads(json_value)
    # Get a complex key-value element by converting from json string
