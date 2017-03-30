import datetime
import errno
import itertools
import json
import requests
import ssl
import websocket

from .decorators import api_specific
from .exceptions import BotNotConnected


class MattermostClient(object):
    def __init__(self,
                 url,
                 team,
                 email,
                 password,
                 ssl_verify=True):
        self._url = url
        self._ssl_verify = ssl_verify
        self._websocket = None

        self._user = None
        self._token = None
        self.login(email, password)

        self._api_version = None
        self._team_id = None
        self.load_initial_data(team)

    @property
    def user(self):
        return self._user

    @property
    def api_version(self):
        return self._api_version

    @property
    def _headers(self):
        return {'Authorization': 'Bearer %s' % self._token}

    def get(self, request, use_token=True, raise_for_status=False):
        kwargs = {'verify': self._ssl_verify}
        if use_token:
            kwargs.update({'headers': self._headers})

        response = requests.get(self._url + request, **kwargs)
        if raise_for_status and response.status_code != requests.codes.OK:
            response.raise_for_status()

        return response

    def post(self,
             request,
             data=None,
             use_token=True,
             raise_for_status=False):
        kwargs = {'data': json.dumps(data) or {}, 'verify': self._ssl_verify}
        if use_token:
            kwargs.update({'headers': self._headers})

        response = requests.post(self._url + request, **kwargs)
        if raise_for_status and response.status_code != requests.codes.OK:
            response.raise_for_status()

        return response

    def login(self, email, password):
        data = {
            'login_id': email,
            'password': password
        }

        response = self.post(
            '/users/login',
            data=data,
            use_token=False,
            raise_for_status=True)
        self._user = response.json()
        self._token = response.headers['Token']

    def load_initial_data(self, team_name):
        response = self.get('/users/initial_load').json()
        self._api_version = tuple(map(int,
            response['client_cfg']['Version'].split('.')[:2]))

        for team in response['teams']:
            if team['display_name'] == team_name:
                self._team_id = team['id']
                break

    def channel_msg(self, channel_id, message):
        create_at = datetime.datetime.now().strftime('%s')
        route = '/teams/%s/channels/%s/posts/create' % (
            self._team_id, channel_id)
        data = {
            'user_id': self._user['id'],
            'channel_id': channel_id,
            'message': message,
            'create_at': int(create_at),
            'pending_post_id': '%s:%s' % (self._user['id'], create_at),
        }

        return self.post(route, data=data).json()

    def connect_websocket(self):
        url = '{}/users/websocket'.format(self._url.replace('http', 'ws'))
        self._connect_websocket(url)
        if self._websocket.getstatus() != 101:
            raise BotNotConnected

    def _connect_websocket(self, url):
        self._websocket = websocket.create_connection(
            url,
            header=[
                'Cookie: %s=%s' % ('MMAUTHTOKEN', self._token)
            ],
            sslopt={
                'cert_reqs': (
                    ssl.CERT_REQUIRED
                    if self._ssl_verify
                    else ssl.CERT_NONE
                )
            }
        )
        self._websocket.sock.setblocking(0)

    def websocket_safe_read(self):
        data = ''
        while True:
            try:
                data += '{0}\n'.format(self._websocket.recv())
            except ssl.SSLError as e:
                if e.errno == 2:
                    # errno 2 occurs when trying to read or write data, but more
                    # data needs to be received on the underlying TCP transport
                    # before the request can be fulfilled.
                    #
                    # Python 2.7.9+ and Python 3.3+ give this its own exception,
                    # SSLWantReadError
                    break
                raise
            except BlockingIOError as e:
                if e.errno == errno.EAGAIN:
                    break
                raise
            except websocket._exceptions.WebSocketException:
                self.connect_websocket()

        return data.rstrip()

    def get_messages(self):
        events = []

        data = self.websocket_safe_read()
        if data:
            for d in data.split('\n'):
                try:
                    _d = json.loads(d)
                    post = _d.get('data', {}).get('post')

                    # Skip messages from this bot
                    if post is not None:
                        _post = json.loads(post)
                        if self.user['id'] == _post['user_id']:
                            continue

                    events.append(_d)
                except ValueError:
                    pass

        return events

    def _get_channels_helper_3_4(self):
        route = '/teams/%s/channels/' % self._team_id
        return itertools.chain(
            self.get(route).json().get('channels', []),
            self.get('%s/more' % route).json().get('channels', [])
        )

    def _get_channels_helper_3_7(self):
        route = '/teams/%s/channels/' % self._team_id
        return itertools.chain(
            self.get(route).json(),
            self.get('%s/more' % route).json()
        )

    @api_specific
    def get_channels(self):
        pass

    def _get_users_helper_3_4(self):
        return self.get('/users/profiles/%s' % self._team_id).json()

    def _get_users_helper_3_7(self, pagination_size=100):
        profiles = {}

        start = 0
        while True:
            end = start + pagination_size
            route = '/teams/%s/users/%i/%i' % (self._team_id, start, end)
            page = self.get(route).json()
            profiles.update(page)

            if len(page) < pagination_size:
                break

            start = end

        return profiles

    @api_specific
    def get_users(self):
        pass

    def ping(self):
        self._websocket.ping()
