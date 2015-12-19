import requests


class APIError(Exception):
    status_code = requests.codes.SERVER_ERROR
    message = 'A server error occurred.'

    def __init__(self, status_code=None, message=None):
        super(APIError, self).__init__(message)
        if status_code is not None:
            self.status_code = status_code
        if message is not None:
            self.message = message

    def __str__(self):
        return self.message
