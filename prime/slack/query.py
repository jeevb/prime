import re

from prime.bot.query import Query
from prime.bot.constants import SEPARATORS

TARGETING_ME_RE = re.compile(r'^prime[%s]+' % SEPARATORS, re.I)


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
        return TARGETING_ME_RE.sub('', self._message)

    @property
    def is_direct_message(self):
        return self.channel.startswith('D')

    @property
    def is_targeting_me(self):
        return TARGETING_ME_RE.match(self._message) is not None

    @property
    def is_valid(self):
        return self.is_direct_message or self.is_targeting_me

    def reply(self, message):
        if message and not self.is_direct_message:
            message = '{0}: {1}'.format(self.user_link, message)
        return super(SlackQuery, self).reply(message)
