class BotNotConnected(Exception):
    pass


class UnsupportedAPIVersion(Exception):
    def __init__(self, version):
        message = 'Unsupported API Version: v%s' % '.'.join(map(str, version))
        super(UnsupportedAPIVersion, self).__init__(message)
