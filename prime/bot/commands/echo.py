from prime.bot.command import Command
from prime.bot.decorators import arg, description


@description('Echoes a message.')
@arg('message', help='Message to echo.', nargs='+')
class Echo(Command):
    def handle(self, query, args):
        message = ' '.join(args.message)
        query.reply(message)
