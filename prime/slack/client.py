from slackclient.channel import Channel
from slackclient.client import SlackClient, SlackNotConnected
from slackclient.server import Server


class SlackChannel(Channel):
    def send_message(self, message, thread=None, reply_broadcast=False):
        '''
        Sends a message to a this Channel.
        Include the parent message's thread_ts value in `thread`
        to send to a thread.
        :Args:
            message (message) - the string you'd like to send to the channel
            thread (str or None) - the parent message ID, if sending to a
                thread
            reply_broadcast (bool) - if messaging a thread, whether to
                also send the message back to the channel
        :Returns:
            None
        '''
        message_json = {
            "id": self.server.event_uid,
            "type": "message",
            "channel": self.id,
            "text": message
        }

        if thread is not None:
            message_json["thread_ts"] = thread
            if reply_broadcast:
                message_json['reply_broadcast'] = True

        self.server.send_to_websocket(message_json)


class SlackServer(Server):
    def __init__(self, *args, **kwargs):
        super(SlackServer, self).__init__(*args, **kwargs)

        # UID for events sent from this server
        self._event_uid = None

    @property
    def event_uid(self):
        if self._event_uid is None:
            raise SlackNotConnected

        last_id = self._event_uid
        self._event_uid += 1
        return last_id

    def connect_slack_websocket(self, ws_url):
        # Reset UID counter
        self._event_uid = 0

        super(SlackServer, self).connect_slack_websocket(ws_url)

    def attach_channel(self, name, channel_id, members=None):
        if members is None:
            members = []
        if self.channels.find(channel_id) is None:
            self.channels.append(SlackChannel(self, name, channel_id, members))


class SlackClient2(SlackClient):
    def __init__(self, token):
        self.token = token
        self.server = SlackServer(self.token, False)
