from prime.api.generics import PostAPIRequest


class PrimeNotifyAPI(PostAPIRequest):
    base_url = 'https://{host}:{port}'
    endpoint = '/notify/'

    def __init__(self, host, port, token, cert):
        self._host = host
        self._port = port
        self._token = token
        self._cert = cert

    def __call__(self, text, to=None):
        return self.response(
            url_args={'host': self._host, 'port': self._port},
            headers={'Authorization': 'Token {}'.format(self._token)},
            data={'text': text, 'to': to or []},
            verify=self._cert
        )
