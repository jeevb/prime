import re

from prime.bot.groups import GroupsMixin
from prime.bot.exceptions import InvalidEntity

MM_LINK_RE = r'[%s](?P<entity>[^\s]+)'
MM_LINK_USER_RE = re.compile(MM_LINK_RE % '\@')
MM_LINK_CHANNEL_RE = re.compile(MM_LINK_RE % '\~')


class MMGroupsMixin(GroupsMixin):
    database_name = 'mattermost_groups'

    def _find_in_user_cache(self, user):
        try:
            user = self._user_cache[user]
        except KeyError:
            raise InvalidEntity('Invalid user: %r' % user)
        return user

    def _find_in_channel_cache(self, channel):
        try:
            channel = self._channel_cache[channel]
        except KeyError:
            raise InvalidEntity('Invalid channel: %r' % channel)
        return channel

    def _validate_user(self, user):
        match = MM_LINK_USER_RE.match(user)
        if match:
            user = match.group('entity')
        return self._find_in_user_cache(user)['id']

    def _validate_channel(self, channel):
        match = MM_LINK_CHANNEL_RE.match(channel)
        if match:
            channel = match.group('entity')
        return self._find_in_channel_cache(channel)['id']

    def _user_display(self, user):
        user = self._find_in_user_cache(user)
        return '@{0}'.format(user['username'])

    def _channel_display(self, channel):
        channel = self._find_in_channel_cache(channel)
        return '~{0}'.format(channel['name'])
