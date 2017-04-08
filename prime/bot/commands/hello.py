from prime.bot.command import Command

cmd = Command.create(
    'hello',
    aliases=('hi', 'hey', 'yo', 'hola',),
    timeout=10,
    description='Say hello.'
)

@cmd.register
def main(command, query, args):
    query.reply_with_one_of(
        'Hello there!',
        'Well, hello!',
        'Hi there!',
        'Hey you!',
        'Hey there!'
    )
