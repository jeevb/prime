from prime.bot.command import Command
from prime.bot.decorators import description, trigger, timeout


@timeout(10)
@trigger('hi', 'hey', 'yo', 'hola')
@description('Say hello to Prime.')
class Hello(Command):
    def handle(self, query, args):
        query.reply_with_one_of(
            'Hello there!',
            'Well, hello!',
            'Hi there!',
            'Hey you!',
            'Hey there!'
        )
