from prime.bot.command import Command
from prime.bot.decorators import description


@description('Say hello to Prime.')
class Hello(Command):
    triggers = ('hi', 'hey', 'yo', 'hola',)

    def handle(self, query, args):
        query.reply_with_one_of(
            'Hello there!',
            'Well, hello!',
            'Hi there!',
            'Hey you!',
            'Hey there!'
        )
