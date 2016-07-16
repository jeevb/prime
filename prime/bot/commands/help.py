from prime.bot.command import Command
from prime.bot.decorators import description


@description('Shows a list of commands.')
class Help(Command):
    triggers = ('commands',)

    def get_usable_commands(self, query):
        template = '{:15s}\t{:60s}'
        yield template.format('Command', 'Description')
        yield template.format('-------', '-----------')
        for cmd in self.manager.commands:
            if self.manager.is_authorized(cmd, query):
                yield template.format(
                    cmd.prog.lower(),
                    cmd.description
                ).strip()

    def handle(self, query, args):
        query.reply_within_block('\n'.join(self.get_usable_commands(query)))
