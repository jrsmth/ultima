from pyjavaproperties import Properties


def load_messages():
    messages = Properties()
    messages.load(open('../resources/message.properties'))

    return messages
