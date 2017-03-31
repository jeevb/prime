import re

from prime.bot.groups import GroupsMixin
from prime.bot.exceptions import InvalidEntity

SLACK_LINK_RE = r'\<[%s](?P<entity>.+?)(\|.*)?\>'
SLACK_LINK_USER_RE = re.compile(SLACK_LINK_RE % '\@')
SLACK_LINK_CHANNEL_RE = re.compile(SLACK_LINK_RE % '\#')


class SlackGroupsMixin(GroupsMixin):
    database_name = 'slack_groups'

    def validate_user(self, user):
        match = SLACK_LINK_USER_RE.match(user)
        if not match:
            raise InvalidEntity('Invalid user: %r' % user)
        return match.group('entity')

    def validate_channel(self, channel):
        match = SLACK_LINK_CHANNEL_RE.match(channel)
        if not match:
            raise InvalidEntity('Invalid channel: %r' % channel)
        return match.group('entity')

    def _user_display(self, user):
        return '<@{0}>'.format(user)

    def _channel_display(self, channel):
        return '<#{0}>'.format(channel)
