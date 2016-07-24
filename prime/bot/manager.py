import importlib
import os
import re
import sys

from gevent import Greenlet
from prime.bot.constants import PACKAGE_RE

def load(dirnames):
    for module_root, dirname in dirnames:
        if not os.path.isdir(dirname):
            continue
        for fn in os.listdir(dirname):
            match = PACKAGE_RE.match(fn)
            if not match:
                continue
            module_name = '{}.{}'.format(module_root, match.group('package'))
            spec = importlib.util.spec_from_file_location(
                module_name,
                os.path.join(dirname, match.group())
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


class Module(object):
    def __init__(self, manager):
        super(Module, self).__init__()
        self._manager = manager

    @property
    def manager(self):
        return self._manager

    @property
    def bot(self):
        return self.manager.bot


class ModuleMgr(object):
    module_class = None
    modules_specs = None

    def __init__(self, bot):
        super(ModuleMgr, self).__init__()
        print('Initializing {0}...'.format(self.__class__.__name__))
        self.bot = bot
        self._modules = set()
        self._load_modules()

    def _get_module_class(self):
        assert self.module_class is not None, (
            '%r should either include a `module_class` attribute, '
            'or override the `_get_module_class()` method.'
            % self.__class__.__name__
        )
        return self.module_class

    def _get_module_specs(self):
        assert self.module_specs is not None, (
            '%r should either include a `module_specs` attribute, '
            'or override the `_get_module_specs()` method.'
            % self.__class__.__name__
        )
        return self.module_specs

    def _get_subclasses(self):
        yield from self._get_module_class().__subclasses__()

    def _load_modules(self):
        load(self._get_module_specs())
        for module_subclass in self._get_subclasses():
            module = module_subclass(self)
            self._modules.add(module)
        print('[{0}] {1} {2}(s) loaded.'.format(
            self.__class__.__name__,
            len(self._modules),
            self._get_module_class().__name__.lower()
        ))

    def _on_error(self, exc):
        if isinstance(exc, Greenlet):
            exc = exc.exception
        # TODO(jeev): Implement logger to handle these errors
        print(exc, file=sys.stderr)
