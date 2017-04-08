from prime.bot.command import Command
from prime.bot.decorators import arg

cmd = Command.create(
    'echo',
    aliases=('parrot',),
    timeout=10,
    description='Echoes a message.'
)

@cmd.register
@arg('message', help='Message to echo.', nargs='+')
def main(command, query, args):
    message = ' '.join(args.message)
    query.reply(message)
