import functools
import inflection
import io
import re
import shlex
import sys

from argh.assembling import set_default_command, add_commands
from argh.constants import PARSER_FORMATTER, ATTR_EXPECTS_NAMESPACE_OBJECT
from argh.dispatching import dispatch
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from gettext import gettext as _
from gevent import Greenlet, with_timeout
from prime.bot.exceptions import CommandExit, CommandPrint
from prime.storage.local_storage import USER_COMMANDS_DIR
from prime.bot.manager import Module, ModuleMgr
from prime.bot.constants import (
    BASE_DIR_JOIN,
    SEPARATORS,
    SHORTHAND_TRIGGERS_ESC,
    COMMAND_ALIASES,
    COMMAND_TIMEOUT,
    COMMAND_DMONLY,
    COMMAND_USER_GROUPS,
    COMMAND_CHANNEL_GROUPS,
    COMMAND_PARSER_ARGS
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


class ShorthandCommandMixin(object):
    def init_pattern(self):
        self._pattern = re.compile(
            r'^[%s]+(%s)([%s]+)?' % (
                SHORTHAND_TRIGGERS_ESC,
                self.prefixes,
                SEPARATORS
            ), re.I
        )


class Command(Module):
    __command_handlers__ = None

    @classmethod
    def create(cls,
               name,
               aliases=None,
               timeout=None,
               direct_message_only=False,
               user_groups=None,
               channel_groups=None,
               allow_shorthand=False,
               **parser_args):
        bases = (ShorthandCommandMixin, cls,) if allow_shorthand else (cls,)
        return type(
            name,
            bases,
            {
                COMMAND_ALIASES: aliases,
                COMMAND_TIMEOUT: timeout,
                COMMAND_DMONLY: direct_message_only,
                COMMAND_USER_GROUPS: user_groups,
                COMMAND_CHANNEL_GROUPS: channel_groups,
                COMMAND_PARSER_ARGS: parser_args
            }
        )

    @classmethod
    def register(cls, func):
        if cls.__command_handlers__ is None:
            cls.__command_handlers__ = []
        cls.__command_handlers__.append(func)
        return func

    def __init__(self, manager):
        super(Command, self).__init__(manager)
        # Initialize command pattern
        self._pattern = None
        self.init_pattern()

    def init_pattern(self):
        self._pattern = re.compile(
            r'^(%s)([%s]+)?' % (self.prefixes, SEPARATORS), re.I)

    def _wrap(self, query, func):
        @functools.wraps(func)
        def wrapper(args):
            result = func(self, query, args)
            return result
        setattr(wrapper, ATTR_EXPECTS_NAMESPACE_OBJECT, True)
        return wrapper

    @staticmethod
    def _concat_errors(stdout=None, stderr=None):
        if stderr:
            stderr = 'ERROR:\n{}'.format(stderr)
        return '\n\n'.join((stdout, stderr)).strip()

    def get_command_handlers(self, query):
        assert bool(self.__class__.__command_handlers__), (
            '%r should contain at least one registered command handler, '
            'or override the `get_command_handlers()` method.'
            % self.__class__.__name__
        )

        return [
            self._wrap(query, func)
            for func in self.__class__.__command_handlers__
        ]

    def __call__(self, query):
        try:
            argv = shlex.split(self.pattern.sub('', query.message))
        except ValueError as e:
            query.reply_within_block('Error parsing arguments: %s' % str(e))
            return

        parser = CommandParser(prog=self.prog, **self.parser_args)

        handlers = self.get_command_handlers(query)
        if len(handlers) == 1:
            set_default_command(parser, handlers[0])
        else:
            add_commands(parser, handlers)

        output_file = io.StringIO()
        errors_file = io.StringIO()

        try:
            dispatch(parser,
                     argv=argv,
                     raw_output=True,
                     output_file=output_file,
                     errors_file=errors_file)

            error_msg = self._concat_errors(
                output_file.getvalue(), errors_file.getvalue())
            if error_msg:
                raise CommandPrint(error_msg)
        except CommandPrint as e:
            query.reply_within_block(str(e))
        except CommandExit:
            pass

    @property
    def aliases(self):
        return getattr(self, COMMAND_ALIASES, None)

    @property
    def pattern(self):
        return self._pattern

    @property
    def prog(self):
        return inflection.underscore(self.__class__.__name__).lower()

    @property
    def prefixes(self):
        def _helper():
            yield self.prog
            if self.aliases is not None:
                yield from self.aliases
        return '|'.join(inflection.underscore(i) for i in _helper())

    @property
    def parser_args(self):
        return getattr(self, COMMAND_PARSER_ARGS, {})

    @property
    def description(self):
        return self.parser_args.get('description', self.prog)

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
        if not self.bot.is_authorized_user(query.user, cmd.user_groups):
            return False

        if not query.is_private and (
                cmd.direct_message_only or
                not self.bot.is_authorized_channel(
                    query.channel, cmd.channel_groups)
        ):
            return False

        return True

    def handle(self, query):
        # Find a valid command that matches query
        cmd = next(
            filter(
                lambda c: c.pattern.search(query.message),
                self._modules
            ),
            None
        )

        # If the command exists and is authorized, execute it.
        if cmd is not None and self.is_authorized(cmd, query):
            func = (
                functools.partial(with_timeout,
                                  cmd.timeout,
                                  cmd,
                                  timeout_value=None)
                if cmd.timeout is not None
                else cmd
            )
            # Spawn a greenlet to handle command
            g = Greenlet(func, query)
            g.link_exception(self._on_error)
            g.start()
