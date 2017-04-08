from prime.bot.command import Command

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
    for c in command.manager.commands:
        if command.manager.is_authorized(c, query):
            yield template.format(
                c.prog.lower(),
                c.description
            ).strip()

@cmd.register
def main(command, query, args):
    query.reply_within_block('\n'.join(get_usable_commands(command, query)))
