class CachedObjects(dict):
    def __init__(self, **kwargs):
        super(CachedObjects, self).__init__(**kwargs)
        self._related = {}

    def __delitem__(self, key):
        if key in self:
            related = list(self._related.keys())
            for k in related:
                if self._related[k] == key:
                    del self._related[k]
            super(CachedObjects, self).__delitem__(key)
        else:
            del self._related[key]

    def __getitem__(self, key):
        try:
            return super(CachedObjects, self).__getitem__(key)
        except KeyError:
            return super(CachedObjects, self).__getitem__(self._related[key])

    def __setitem__(self, key, val):
        if isinstance(key, tuple):
            if not key:
                raise ValueError('Empty tuple used as key')
            key, others = key[0], key[1:]
            self._add_related(key, *others)

        super(CachedObjects, self).__setitem__(key, val)

    def _add_related(self, key, *others):
        for o in others:
            if o in self:
                raise ValueError('Key is primary: %r' % o)
            self._related[o] = key

    def add_related(self, key, *others):
        if not key in self:
            raise KeyError(key)
        self._add_related(key, *others)

    def load(self, data):
        raise NotImplementedError(
            '%r should implement the `load` method.'
            % self.__class__.__name__
        )


class UserCache(CachedObjects):
    def load(self, data):
        # Clear existing entries
        self.clear()

        for elem in data:
            self[elem['id'], elem['username']] = elem


class ChannelCache(CachedObjects):
    def load(self, data):
        # Clear existing entries
        self.clear()

        for elem in data:
            self[elem['id'], elem['name']] = elem

