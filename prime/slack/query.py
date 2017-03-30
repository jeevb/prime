from prime.bot.query import Query
from prime.bot.utils import strip


class SlackQuery(Query):
    @property
    def user(self):
        return '<@{0}>'.format(self._user.id)

    @property
    def channel(self):
        return self._channel.id

    @property
    def is_direct_message(self):
        return self.channel.startswith('D')
