import json

from prime.bot.query import Query


class MattermostQuery(Query):
    def __init__(self, user, channel, message, is_direct_message=False):
        super(MattermostQuery, self).__init__(user, channel, message)
        self._is_direct_message = is_direct_message

    @property
    def user(self):
        return '@{0}'.format(self._user)

    @property
    def channel(self):
        return self._channel

    @property
    def is_direct_message(self):
        return self._is_direct_message
