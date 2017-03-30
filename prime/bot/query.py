import copy
import random

from prime.bot.utils import code_block
from prime.bot.utils import strip


class Query(object):
    is_targeting_me = False

    def __init__(self, user, channel, message):
        super(Query, self).__init__()
        self._user = user
        self._channel = channel
        self._message = message
        self._send_handler = None

        # Skip mentioning user
        self._treat_as_private = False

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
    def is_private(self):
        return self._treat_as_private or self.is_direct_message

    @is_private.setter
    def is_private(self, value):
        self._treat_as_private = value

    @property
    def is_direct_message(self):
        self.user == self.channel

    def update(self, user=None, channel=None, message=None):
        new_query = copy.copy(self)
        if user is not None:
            new_query._user = user
        if channel is not None:
            new_query._channel = channel
        if message is not None:
            new_query._message = message

        return new_query

    @property
    def send_handler(self):
        return self._send_handler

    @send_handler.setter
    def send_handler(self, value):
        self._send_handler = value

    def _reply_helper(self, message):
        if self.send_handler:
            return self.send_handler(self.channel, message)

    def reply(self, message, new_line_after_mention=False):
        transform = lambda m, t: (
            '{0}:{1}{2}'.format(
                self.user,
                '\n' if new_line_after_mention else ' ',
                m
            ) if m and t else m
        )

        def from_iterable(iterable):
            first = True
            for val in iterable:
                if val:
                    mention = first and not self.is_private
                    yield transform(val, mention)
                    first = False

        message = strip(message)
        if isinstance(message, (str, bytes)):
            if message:
                mention = not self.is_private
                return self._reply_helper(transform(message, mention))
        elif hasattr(message, '__iter__'):
            return self._reply_helper(from_iterable(message))

    def reply_with_one_of(self, *choices):
        return self.reply(random.choice(choices))

    def reply_within_block(self, message):
        return self.reply(code_block(message), new_line_after_mention=True)
