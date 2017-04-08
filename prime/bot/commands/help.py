from prime.bot.command import Command, ShorthandCommandMixin
from prime.bot.constants import SHORTHAND_TRIGGERS

cmd = Command.create(
    'help',
    aliases=('commands',),
    timeout=10,
    description='Shows a list of commands.'
)

def get_usable_commands(command, query):
    template = '{:15s}\t{:60s}'
    yield template.format('Command', 'Description')
    yield template.format('-------', '-----------')
    all_commands = sorted(
        command.manager.commands,
        key=lambda c: (
            not issubclass(c.__class__, ShorthandCommandMixin), c.prog)
    )
    for c in all_commands:
        if command.manager.is_authorized(c, query):
            prog = '{0}{1}'.format(
                (
                    SHORTHAND_TRIGGERS[0]
                    if issubclass(c.__class__, ShorthandCommandMixin)
                    else ''
                ),
                c.prog
            )
            yield template.format(
                prog,
                c.description
            ).strip()

@cmd.register
def main(command, query, args):
    query.reply_within_block('\n'.join(get_usable_commands(command, query)))
