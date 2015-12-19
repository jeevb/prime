import requests

from prime.exceptions import APIError


class GenericAPIRequest(object):
    method = None
    base_url = None
    endpoint = None
    expected_codes = (requests.codes.OK,)

    def get_method(self):
        assert self.method is not None, (
            '%r should either include a `method` attribute, '
            'or override the `get_method()` method.'
            % self.__class__.__name__
        )

        return self.method

    def get_base_url(self):
        assert self.base_url is not None, (
            '%r should either include a `base_url` attribute, '
            'or override the `get_base_url()` method.'
            % self.__class__.__name__
        )

        return self.base_url

    def get_endpoint(self):
        assert self.endpoint is not None, (
            '%r should either include an `endpoint` attribute, '
            'or override the `get_endpoint()` method.'
            % self.__class__.__name__
        )

        return self.endpoint

    def api_call(self, url_args):
        return (self.get_base_url() + self.get_endpoint()).format(**url_args)

    def response(self, url_args=None, **kwargs):
        url = self.api_call(url_args or {})
        response = requests.request(self.get_method(), url, **kwargs)

        if response.status_code not in self.expected_codes:
            reason = response.json().get('detail') or response.reason
            raise APIError(response.status_code, reason)

        return response

    def __call__(self, *args, **kwargs):
        raise NotImplementedError(
            '%r should implement the `__call__()` method.'
            % self.__class__.__name__
        )


class HeadAPIRequest(GenericAPIRequest):
    method = 'HEAD'


class GetAPIRequest(GenericAPIRequest):
    method = 'GET'


class PostAPIRequest(GenericAPIRequest):
    method = 'POST'
