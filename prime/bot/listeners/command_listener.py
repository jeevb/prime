from prime.bot.constants import SHORTHAND_TRIGGER_RE
from prime.bot.listener import Listener


class CommandListener(Listener):
    def handle(self, query):
        if query.is_targeting_me:
            self.bot.handle_cmd(query)
