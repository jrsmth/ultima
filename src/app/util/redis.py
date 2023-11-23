from json import JSONDecodeError
import jsons
from flask_redis import FlaskRedis


# Wrapper functionality for the Flask Redis Client
class Redis:

    def __init__(self, app):
        self.client = FlaskRedis(app)

    # Get an element by its key and decode in utf-8 format
    def get(self, key):
        return self.client.get(key).decode('utf-8')

    # Set a key-value element
    def set(self, key, value):
        return self.client.set(key, value)

    # Set a complex key-value element by converting to json string
    def set_complex(self, key, complex_value):
        # FixMe :: bit dodgy
        json_value = str(jsons.dump(complex_value)).replace("False,", "false,").replace("True,", "true,")
        print("[set_complex] Successful conversion to JSON, setting value: " + json_value)  # TODO :: TRACE
        return self.client.set(key, json_value)

    # Get a complex key-value element by converting from json string
    def get_complex(self, key):
        json_value = self.client.get(key).decode('utf-8').replace("\'", "\"")  # FixMe :: bit dodgy
        try:
            return jsons.loads(json_value)
        except JSONDecodeError:
            raise Exception("[get_complex] Error parsing retrieved object: " + str(json_value))
