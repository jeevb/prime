from prime.bot.listener import Listener


class CommandListener(Listener):
    def handle(self, query):
        self.bot.handle_cmd(query)
