import re
import sys
import time
import traceback

from gevent import sleep, spawn_raw
from prime.bot.bot import GenericBot
from prime.bot.constants import SEPARATORS
from prime.bot.utils import strip
from prime.slack.groups import SlackGroupsMgr
from prime.slack.query import SlackQuery
from slackclient import SlackClient
from slackclient._client import SlackNotConnected
from slackclient._server import SlackConnectionError, SlackLoginError


class SlackBot(GenericBot):
    groups_mgr_class = SlackGroupsMgr

    def __init__(self, token, ping_interval=3):
        super(SlackBot, self).__init__()
        self._client = SlackClient(token)
        self._ping_interval = ping_interval
        # Pattern to determine if incoming messages are targeting bot
        self._targeting_me_re = None

    @property
    def _attrs(self):
        return self._client.server.login_data['self']

    def _on_connect(self):
        # Cache pattern to determine if incoming message is targeting bot
        link = re.escape('<@{0}>'.format(self._attrs.get('id')))
        name = re.escape(self._attrs.get('name'))
        self._targeting_me_re = re.compile(
            r'^(%s|%s)[%s]+' % (link, name, SEPARATORS), re.I)

    def _is_targeting_me(self, message):
        return (
            (self._targeting_me_re.sub('', message), True)
            if self._targeting_me_re.match(message) is not None
            else (message, False)
        )

    def _handle_message(self, event):
        message = event.get('text')
        user = event.get('user')
        # Handle case of edited message
        event_message = event.get('message')
        if not message and event_message:
            message = event_message.get('text')
            user = event_message.get('user')
        if not message:
            return
        message, is_targeting_me = self._is_targeting_me(message)
        channel = event.get('channel')
        query = SlackQuery(user=self._get_user(user),
                           channel=self._get_channel(channel),
                           message=message)
        query.is_targeting_me = is_targeting_me or query.is_direct_message
        return self._on_query(query)

    def _handle_user_change(self, event):
        user_data = event.get('user')
        if user_data:
            user_id = user_data.get('id')
            tz = user_data.get('tz', 'unknown')
            name = user_data.get('name')
            real_name = user_data.get('real_name', name)
            if not self._update_user(name=name,
                                     id=user_id,
                                     real_name=real_name,
                                     tz=tz):
                self._add_user(name, user_id, real_name, tz)

    def _handle_channel_left(self, event):
        self._remove_channel(event.get('channel'))

    def _handle_channel_joined(self, event):
        channel_data = event.get('channel')
        if channel_data:
            channel_id = channel_data.get('id')
            name = channel_data.get('name')
            members = channel_data.get('members')
            if not self._update_channel(name=name,
                                        id=channel_id,
                                        members=members):
                self._add_channel(name, channel_id, members)

    def _handle_channel_rename(self, event):
        channel_data = event.get('channel')
        if channel_data:
            self._update_channel(name=channel_data.get('name'),
                                 id=channel_data.get('id'))

    def _handle_event(self, event):
        event_type = event.get('type')
        handler = getattr(self, '_handle_{}'.format(event_type), None)
        if handler:
            spawn_raw(handler, event)

    def _add_user(self, *args, **kwargs):
        self._client.server.attach_user(*args, **kwargs)

    def _update_user(self, **kwargs):
        user = self._get_user(kwargs.get('id'))
        if not user:
            return False
        user.__dict__.update(**kwargs)
        return True

    def _get_user(self, user):
        return self._client.server.users.find(user)

    def _add_channel(self, *args, **kwargs):
        self._client.server.attach_channel(*args, **kwargs)

    def _remove_channel(self, channel_id):
        channel = self._get_channel(channel_id)
        if channel:
            self._client.server.channels.remove(channel)

    def _update_channel(self, **kwargs):
        channel = self._get_channel(kwargs.get('id'))
        if not channel:
            return False
        channel.__dict__.update(**kwargs)
        return True

    def _get_channel(self, channel):
        return self._client.server.channels.find(channel)

    def _poll(self):
        self._client.server.rtm_connect()
        self._on_connect()
        # Start a greenlet that will ping server on a specific interval
        spawn_raw(self._ping)
        while True:
            data = self._client.rtm_read()
            for event in data:
                self._handle_event(event)
            sleep(.5)

    def _ping(self):
        while True:
            self._client.server.ping()
            sleep(self._ping_interval)

    def send(self, channel, message):
        message = strip(message)
        if isinstance(message, (str, bytes)):
            if message:
                self._client.rtm_send_message(channel, message)
        elif hasattr(message, '__iter__'):
            for chunk in message:
                if chunk:
                    sleep(.5)
                    self._client.rtm_send_message(channel, chunk)
