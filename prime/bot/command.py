import functools
import inflection
import re
import shlex
import sys

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from gettext import gettext as _
from gevent import Greenlet, with_timeout
from prime.bot.exceptions import CommandExit, CommandPrint
from prime.storage.local_storage import USER_COMMANDS_DIR
from prime.bot.manager import Module, ModuleMgr
from prime.bot.constants import (
    BASE_DIR_JOIN,
    SEPARATORS,
    COMMAND_ARGS,
    COMMAND_DESC,
    COMMAND_ALIASES,
    COMMAND_TIMEOUT,
    COMMAND_DMONLY,
    COMMAND_USER_GROUPS,
    COMMAND_CHANNEL_GROUPS
)


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


class Command(Module):
    def __init__(self, manager):
        super(Command, self).__init__(manager)
        # Initialize command parser
        self._parser = CommandParser(prog=self.prog,
                                     description=self.description)
        self.init_parser()

        # Initialize command pattern
        self._pattern = None
        self.init_pattern()

    # ===============
    # Override these methods, if necessary
    # ===============
    def init_parser(self):
        for kwargs in getattr(self, COMMAND_ARGS, []):
            args = kwargs.pop('option_strings')
            self._parser.add_argument(*args, **kwargs)

    def init_pattern(self):
        prefix = [self.prog]
        aliases = getattr(self, COMMAND_ALIASES, None)
        if aliases is not None:
            prefix += list(aliases)
        self._pattern = re.compile(
            r'^(%s)([%s]+)?' % (
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
    def prog(self):
        return inflection.underscore(self.__class__.__name__)

    @property
    def description(self):
        return getattr(self, COMMAND_DESC, self.prog)

    @property
    def timeout(self):
        return getattr(self, COMMAND_TIMEOUT, None)

    @property
    def direct_message_only(self):
        return getattr(self, COMMAND_DMONLY, False)

    @property
    def user_groups(self):
        return getattr(self, COMMAND_USER_GROUPS, None)

    @property
    def channel_groups(self):
        return getattr(self, COMMAND_CHANNEL_GROUPS, None)

    def handle(self, query, args):
        raise NotImplementedError(
            '%r should implement the `handle` method.'
            % self.__class__.__name__
        )


class CommandMgr(ModuleMgr):
    module_class = Command
    module_specs = [
        ('prime_default_commands', BASE_DIR_JOIN('commands')),
        ('prime_user_commands', USER_COMMANDS_DIR),
    ]

    @property
    def commands(self):
        return self._modules

    def is_authorized(self, cmd, query):
        # Validate user/channel for command use
        return (
            not cmd.direct_message_only or
            query.is_direct_message
        ) and self.bot.groups.is_authorized_user(
            query.user,
            cmd.user_groups
        ) and self.bot.groups.is_authorized_channel(
            query.channel,
            cmd.channel_groups
        )

    def handle(self, query):
        if not query.is_targeting_me:
            return
        for cmd in self._modules:
            match = cmd.pattern.search(query.message)
            if not match:
                continue
            if not self.is_authorized(cmd, query):
                continue
            argv = shlex.split(cmd.pattern.sub('', query.message))
            try:
                args, _ = cmd.parser.parse_known_args(argv)
            except CommandPrint as e:
                query.reply_within_block(str(e))
            except CommandExit:
                pass
            else:
                func = (
                    functools.partial(with_timeout,
                                      cmd.timeout,
                                      cmd.handle,
                                      timeout_value=None)
                    if cmd.timeout is not None
                    else cmd.handle
                )
                # Spawn a greenlet to handle command
                g = Greenlet(func, query, args)
                g.link_exception(self._on_error)
                g.start()
            finally:
                break
