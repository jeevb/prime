from prime.bot.command import Command
from prime.bot.decorators import description, alias, timeout


@timeout(10)
@alias('hi', 'hey', 'yo', 'hola')
@description('Say hello.')
class Hello(Command):
    def handle(self, query, args):
        query.reply_with_one_of(
            'Hello there!',
            'Well, hello!',
            'Hi there!',
            'Hey you!',
            'Hey there!'
        )
