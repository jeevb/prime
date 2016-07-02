import random


class Query(object):
    def __init__(self, channel, message, response_prefix=None):
        self.channel = channel
        self.message = message
        self.response_prefix = response_prefix
        self.send_handler = None

    def reply(self, message):
        if self.response_prefix:
            message = '{}{}'.format(self.response_prefix, message)
        if message and self.send_handler:
            return self.send_handler(self.channel, message)

    def reply_with_one_of(self, *choices):
        return self.reply(random.choice(choices))
