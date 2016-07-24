from prime.bot.query import Query


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
        if message and not self.is_direct_message:
            message = '{0}: {1}'.format(self.user_link, message)
        return super(SlackQuery, self).reply(message)
