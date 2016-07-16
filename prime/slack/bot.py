import re
import sys
import time

from gevent import sleep
from prime.bot.bot import GenericBot
from prime.slack.groups import SlackGroupsMgr
from prime.slack.query import SlackQuery
from slackclient import SlackClient


class SlackBot(GenericBot):
    groups_mgr_class = SlackGroupsMgr

    def __init__(self, token, ping_interval=3):
        super(SlackBot, self).__init__()
        self._client = SlackClient(token)
        self._ping_interval = ping_interval
        self._last_ping = None

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
        channel = event.get('channel')
        query = SlackQuery(self._get_user(user),
                           self._get_channel(channel),
                           message)
        return self._on_query(query)

    def _handle_user_change(self, event):
        user_data = event.get('user')
        if user_data:
            user_id = user.get('id')
            tz = user.get('tz', 'unknown')
            name = user.get('name')
            real_name = user.get('real_name', name)
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
            handler(event)

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
        if not self._client.rtm_connect():
            print('Could not connect to Slack\'s RTM API.',
                  file=sys.stderr)
            self.stop()
        while True:
            try:
                data = self._client.rtm_read()
            except:
                self.stop()
            else:
                for event in data:
                    self._handle_event(event)
                self._ping()
                sleep(.5)

    def _ping(self):
        now = time.time()
        if not self._last_ping or now > self._last_ping + self._ping_interval:
            self._client.server.ping()
            self._last_ping = now

    def _send(self, channel, message):
        return self._client.rtm_send_message(channel, message)
