from prime.bot.query import Query
from prime.bot.utils import strip


class SlackQuery(Query):
    @property
    def user(self):
        return self._user.id

    @property
    def user_link(self):
        return '<@{0}>'.format(self._user.id)

    @property
    def channel(self):
        return self._channel.id

    @property
    def message(self):
        return self._message

    @property
    def is_direct_message(self):
        return self.channel.startswith('D')

    def reply(self, message):
        transform = lambda m, t: (
            '{0}: {1}'.format(self.user_link, m) if m and t else m)

        def from_iterable(iterable):
            first = True
            for val in iterable:
                if val:
                    yield transform(val, first and not self.is_direct_message)
                    first = False

        message = strip(message)
        if isinstance(message, (str, bytes)):
            if message:
                return super(SlackQuery, self).reply(
                    transform(message, not self.is_direct_message))
        elif hasattr(message, '__iter__'):
            return super(SlackQuery, self).reply(from_iterable(message))
