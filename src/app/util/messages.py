from pyjavaproperties import Properties


# Wrapper functionality for the Message Bundle
class Messages:

    def __init__(self, path):
        self.bundle = Properties()
        self.bundle.load(open(path))

    def load(self, key):
        return self.bundle[key]

    def load_with_params(self, key, parameters: list):
        message = self.bundle[key]
        for index in range(len(parameters)):
            message = message.replace('{'+str(index)+'}', parameters[index])

        return message
