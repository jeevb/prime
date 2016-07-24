from prime.bot.constants import BASE_DIR_JOIN
from prime.bot.manager import Module, ModuleMgr
from prime.storage.local_storage import USER_LISTENERS_DIR


class Listener(Module):
    def handle(self, query):
        raise NotImplementedError(
            '%r should implement the `handle` method.'
            % self.__class__.__name__
        )


class ListenerMgr(ModuleMgr):
    module_class = Listener
    module_specs = [
        ('prime_default_listeners', BASE_DIR_JOIN('listeners')),
        ('prime_user_listeners', USER_LISTENERS_DIR),
    ]

    def handle(self, query):
        for listener in self._modules:
            listener.handle(query)
