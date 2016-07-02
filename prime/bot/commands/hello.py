from prime.bot.command import Command


class Hello(Command):
    """
    Say hello.
    Usage:
        hello
    """

    triggers = ('hi',)

    def handle(self, query, args):
        query.reply_with_one_of(
            'Hello there!',
            'Well, hello!',
            'Hi there!',
            'Hey you!',
            'Hey there!'
        )
