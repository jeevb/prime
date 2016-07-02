from prime.bot.command import Command


class Echo(Command):
    """
    Echo the specified message.
    Usage:
        echo (MESSAGE...)
    """

    def handle(self, query, args):
        message = ' '.join(args.get('MESSAGE'))
        query.reply(message)
