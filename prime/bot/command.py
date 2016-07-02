import inflection
import re
import shlex
import sys

from docopt import docopt, DocoptLanguageError, DocoptExit
from prime.bot.loaders import load_commands
from prime.bot.utils import SEPARATORS


class Command(object):
    manager = None
    triggers = None

    def __init__(self):
        super(Command, self).__init__()
        prefix = [self.__class__.__name__]
        if self.triggers is not None:
            prefix += list(self.triggers)
        self._pattern = re.compile(
            r'^(%s)[%s]*' % (
                '|'.join(inflection.underscore(i) for i in prefix),
                SEPARATORS
            ),
            re.I
        )

    @property
    def pattern(self):
        return self._pattern

    @property
    def bot(self):
        return self.manager.bot

    def handle(self, query, args):
        raise NotImplementedError(
            '%r should implement the `handle` method.'
            % self.__class__.__name__
        )


class CommandMgr(object):
    def __init__(self, bot):
        print('Initializing CommandMgr...')
        self.bot = bot
        self._commands = set()
        self._load_commands()

    def _load_commands(self):
        load_commands()
        for cmd_class in Command.__subclasses__():
            cmd = cmd_class()
            cmd.manager = self
            self._commands.add(cmd)
        print('[CommandMgr] {} command(s) loaded.'.format(len(self._commands)))

    def handle(self, query):
        for cmd in self._commands:
            match = cmd.pattern.search(query.message)
            if match:
                argv = shlex.split(cmd.pattern.sub('', query.message))
                try:
                    args = docopt(cmd.__doc__, help=False, argv=argv)
                except DocoptLanguageError:
                    print('Command with invalid docstring: %r' %
                            cmd.__class__.__name__, file=sys.stderr)
                    raise
                except DocoptExit:
                    if cmd.__doc__:
                        query.reply(cmd.__doc__)
                else:
                    cmd.handle(query, args)
                finally:
                    break
