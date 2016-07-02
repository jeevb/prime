from prime.bot.loaders import load_listeners


class Listener(object):
    manager = None

    @property
    def bot(self):
        return self.manager.bot

    def handle(self, query):
        raise NotImplementedError(
            '%r should implement the `handle` method.'
            % self.__class__.__name__
        )


class ListenerMgr(object):
    def __init__(self, bot):
        print('Initializing ListenerMgr...')
        self.bot = bot
        self._listeners = set()
        self._load_listeners()

    def _load_listeners(self):
        load_listeners()
        for listener_class in Listener.__subclasses__():
            listener = listener_class()
            listener.manager = self
            self._listeners.add(listener)
        print('[ListenerMgr] {} listener(s) loaded.'.format(
            len(self._listeners)))

    def handle(self, query):
        for listener in self._listeners:
            listener.handle(query)
