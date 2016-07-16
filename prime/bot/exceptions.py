class PrimeException(Exception):
    def __init__(self, what):
        super(PrimeException, self).__init__(what)
        self._what = what

    @property
    def what(self):
        return self._what

    def __str__(self):
        return what


class CommandExit(Exception):
    pass


class CommandPrint(PrimeException):
    pass


class InvalidEntity(PrimeException):
    pass
