import re

from prime.bot.groups import GroupsMgr
from prime.bot.exceptions import InvalidEntity

SLACK_LINK_RE = r'\<[%s](?P<entity>.+?)(\|.*)?\>'
SLACK_LINK_USER_RE = re.compile(SLACK_LINK_RE % '\@')
SLACK_LINK_CHANNEL_RE = re.compile(SLACK_LINK_RE % '\#')


class SlackGroupsMgr(GroupsMgr):
    def _validate_user(self, user):
        match = SLACK_LINK_USER_RE.match(user)
        if not match:
            raise InvalidEntity('Invalid user: %r' % user)
        return match.group('entity')

    def _validate_channel(self, channel):
        match = SLACK_LINK_CHANNEL_RE.match(channel)
        if not match:
            raise InvalidEntity('Invalid channel: %r' % channel)
        return match.group('entity')

    def add_user_to_group(self, user, group):
        user = self._validate_user(user)
        return super(SlackGroupsMgr, self).add_user_to_group(user, group)

    def add_channel_to_group(self, channel, group):
        channel = self._validate_channel(channel)
        return super(SlackGroupsMgr, self).add_channel_to_group(
            channel, group)

    def remove_user_from_group(self, user, group):
        user = self._validate_user(user)
        return super(SlackGroupsMgr, self).remove_user_from_group(
            user, group)

    def remove_channel_from_group(self, channel, group):
        channel = self._validate_channel(channel)
        return super(SlackGroupsMgr, self).remove_channel_from_group(
            channel, group)

    def list_user_groups(self, user=None):
        if user is not None:
            user = self._validate_user(user)
        for i in super(SlackGroupsMgr, self).list_user_groups(user):
            yield '<@{0}>'.format(i[0]), i[1]

    def list_channel_groups(self, channel=None):
        if channel is not None:
            channel = self._validate_channel(channel)
        for i in super(SlackGroupsMgr, self).list_channel_groups(channel):
            yield '<#{0}>'.format(i[0]), i[1]

    def users_in_groups(self, *groups):
        for i in super(SlackGroupsMgr, self).users_in_groups(*groups):
            yield '<@{0}>'.format(i)

    def channels_in_groups(self, *groups):
        for i in super(SlackGroupsMgr, self).channels_in_groups(*groups):
            yield '<#{0}>'.format(i)
