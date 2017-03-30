from .exceptions import UnsupportedAPIVersion
from functools import wraps

def api_specific(func):
    def wrapper(obj, *args, **kwargs):
        handler = getattr(
            obj,
            '_{}_helper_{}_{}'.format(func.__name__, *obj.api_version),
            None
        )
        if handler is None:
            raise UnsupportedAPIVersion(obj._api_version)

        return handler(*args, **kwargs)
    return wrapper
