import datetime
import errno
import json
import requests
import ssl
import websocket

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

        self._team_id = None
        self.load_initial_data(team)

    @property
    def user(self):
        return self._user

    @property
    def _headers(self):
        return {'Authorization': 'Bearer %s' % self._token}

    def get(self, request, use_token=True, raise_for_status=False, **kwargs):
        kwargs['verify'] = self._ssl_verify
        if use_token:
            kwargs['headers'] = self._headers

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
        response = self.get('/config/client', params={'format': 'old'}).json()
        self._api_version = tuple(map(int,
            response['Version'].split('.')[:2]))

        teams = self.get('/users/{}/teams'.format(self._user['id'])).json()
        for team in teams:
            if team['name'] == team_name:
                self._team_id = team['id']
                break
        else:
            raise SystemExit('Invalid team: %s.' % team_name)

    def channel_msg(self, channel_id, message):
        create_at = datetime.datetime.now().strftime('%s')
        data = {
            'channel_id': channel_id,
            'message': message
        }

        return self.post('/posts', data=data).json()

    def connect_websocket(self):
        url = '{}/websocket'.format(self._url.replace('http', 'ws'))
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

    def get_channels(self):
        route = '/users/%s/teams/%s/channels' % (self._user['id'], self._team_id)
        return self.get(route).json()

    def get_users(self):
        user_ids = [
            i['user_id'] for i in
            self.get('/teams/%s/members' % self._team_id).json()
        ]

        return self.post('/users/ids', data=user_ids).json()

    def ping(self):
        self._websocket.ping()
