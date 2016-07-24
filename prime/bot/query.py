import random


class Query(object):
    is_targeting_me = False

    def __init__(self, user, channel, message):
        super(Query, self).__init__()
        self._user = user
        self._channel = channel
        self._message = message
        self._send_handler = None

    @property
    def user(self):
        return self._user

    @property
    def channel(self):
        return self._channel

    @property
    def message(self):
        return self._message

    @property
    def is_direct_message(self):
        return self.user == self.channel

    @property
    def send_handler(self):
        return self._send_handler

    @send_handler.setter
    def send_handler(self, value):
        self._send_handler = value

    def reply(self, message):
        if message and self.send_handler:
            return self.send_handler(self.channel, message)

    def reply_with_one_of(self, *choices):
        return self.reply(random.choice(choices))

    def reply_within_block(self, message):
        return self.reply('\n```\n{0}\n```'.format(message))
