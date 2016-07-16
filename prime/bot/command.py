import inflection
import re
import shlex

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from gettext import gettext as _
from prime.bot.exceptions import CommandExit, CommandPrint
from prime.bot.loaders import load_commands
from prime.bot.constants import SEPARATORS, COMMAND_ARGS, COMMAND_DESC


class CommandParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs['formatter_class'] = ArgumentDefaultsHelpFormatter
        super(CommandParser, self).__init__(*args, **kwargs)

    # =====================
    # Override help-printing methods
    # =====================
    def print_usage(self, file=None):
        self._print_message(self.format_usage())

    def print_help(self, file=None):
        self._print_message(self.format_help())

    def _print_message(self, message, file=None):
        raise CommandPrint(message)

    # ===============
    # Override exiting methods
    # ===============
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message)
        raise CommandExit

    def error(self, message):
        args = {
            'usage': self.format_usage(),
            'prog': self.prog,
            'message': message
        }
        self._print_message(
            _('%(usage)s\n%(prog)s: Error: %(message)s\n') % args)


class Command(object):
    manager = None
    triggers = None
    direct_message_only = False
    required_user_groups = None
    required_channel_groups = None

    def __init__(self):
        super(Command, self).__init__()
        # Initialize command parser
        self._parser = CommandParser(prog=self.prog.lower())
        for kwargs in getattr(self.__class__, COMMAND_ARGS, []):
            args = kwargs.pop('option_strings')
            self._parser.add_argument(*args, **kwargs)

        # Initialize command pattern
        prefix = [self.prog]
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
    def parser(self):
        return self._parser

    @property
    def pattern(self):
        return self._pattern

    @property
    def bot(self):
        return self.manager.bot

    @property
    def prog(self):
        return inflection.underscore(self.__class__.__name__)

    @property
    def description(self):
        return getattr(self, COMMAND_DESC, self.prog)

    def handle(self, query, args):
        raise NotImplementedError(
            '%r should implement the `handle` method.'
            % self.__class__.__name__
        )


class CommandMgr(object):
    def __init__(self, bot):
        super(CommandMgr, self).__init__()
        print('Initializing CommandMgr...')
        self.bot = bot
        self._commands = set()
        self._load_commands()

    @property
    def commands(self):
        return self._commands

    def is_authorized(self, cmd, query):
        # Validate user/channel for command use
        return (
            not cmd.direct_message_only or
            query.is_direct_message
        ) and self.bot.groups.is_authorized_user(
            query.user,
            cmd.required_user_groups
        ) and self.bot.groups.is_authorized_channel(
            query.channel,
            cmd.required_channel_groups
        )

    def _load_commands(self):
        load_commands()
        for cmd_class in Command.__subclasses__():
            cmd = cmd_class()
            cmd.manager = self
            self._commands.add(cmd)
        print('[CommandMgr] {} command(s) loaded.'.format(len(self._commands)))

    def handle(self, query):
        if not query.is_valid:
            return
        for cmd in self._commands:
            match = cmd.pattern.search(query.message)
            if not match:
                continue
            if not self.is_authorized(cmd, query):
                continue
            argv = shlex.split(cmd.pattern.sub('', query.message))
            try:
                args, _ = cmd.parser.parse_known_args(argv)
            except CommandPrint as e:
                query.reply_within_block(e.what)
            except CommandExit:
                pass
            else:
                cmd.handle(query, args)
            finally:
                break
