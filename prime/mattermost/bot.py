import json
import re
import time

from .cache import UserCache, ChannelCache
from .client import MattermostClient
from .groups import MMGroupsMixin
from .query import MattermostQuery
from gevent import sleep, spawn_later, spawn_raw
from prime.bot.bot import GenericBot
from prime.bot.constants import SEPARATORS


class MattermostBot(MMGroupsMixin, GenericBot):
    query_class = MattermostQuery

    def __init__(self, cfg, cache_refresh_interval=600, ssl_verify=False):
        super(MattermostBot, self).__init__()
        self._client = MattermostClient(cfg.mattermost_url,
                                        cfg.mattermost_team,
                                        cfg.mattermost_email,
                                        cfg.mattermost_password,
                                        ssl_verify=ssl_verify)

        self._cache_refresh_interval = cache_refresh_interval

        # Local caches
        self._user_cache = UserCache()
        self._channel_cache = ChannelCache()

    def _handle_post_edited(self, event):
        return self._handle_posted(event)

    def _handle_posted(self, event):
        data = event['data']
        post = json.loads(data['post'])

        message = post['message']
        if not message:
            return

        message, is_targeting_me, shorthand = self._is_targeting_me(message)
        user_id = post['user_id']
        channel_id = post['channel_id']

        # In edited message, if user/channel is not in cache
        # ignore the message
        try:
            user = (
                data.get('sender_name') or
                self._user_cache[user_id]['username']
            )
            channel_type = (
                data.get('channel_type') or
                self._channel_cache[channel_id]['type']
            )
        except KeyError:
            return

        query = self.query_class(user,
                                 channel_id,
                                 message,
                                 channel_type == 'D')
        query.is_targeting_me = (is_targeting_me or
                                 shorthand or
                                 query.is_direct_message)
        if shorthand:
            query.is_private = True

        return self.on_query(query)

    def _handle_event(self, event):
        event_type = event.get('event')
        handler = getattr(self, '_handle_{}'.format(event_type), None)
        if handler:
            spawn_raw(handler, event)

    def _update_caches(self):
        self._user_cache.load(self._client.get_users())
        self._channel_cache.load(self._client.get_channels())
        spawn_later(self._cache_refresh_interval, self._update_caches)

    def poll(self):
        while True:
            data = self._client.get_messages()
            for event in data:
                self._handle_event(event)
            sleep(.5)

    def ping(self):
        self._client.ping()

    def connect(self):
        self._client.connect_websocket()

        # Cache pattern to determine if incoming message is targeting bot
        mentions = (
            self._client.user
            .get('notify_props', {})
            .get('mention_keys', 'prime')
        ).split(',')

        self._targeting_me_re = re.compile(
            r'^(%s)[%s]+' % ('|'.join(mentions), SEPARATORS), re.I)

        # Update caches
        self._update_caches()

    def send(self, channel, message):
        handler = lambda m: self._client.channel_msg(channel, m)
        return self._send_helper(handler, message)
