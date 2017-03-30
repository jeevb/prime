from prime.bot.constants import SHORTHAND_TRIGGER_RE
from prime.bot.listener import Listener


class CommandListener(Listener):
    def handle(self, query):
        if query.is_targeting_me:
            self.bot.handle_cmd(query)


class ShorthandCommandListener(Listener):
    def handle(self, query):
        if SHORTHAND_TRIGGER_RE.match(query.message) is not None:
            # Here we are modifying the query, and this may
            # adversely affect other listeners, so just make a new one
            new_query = query.update(
                message=SHORTHAND_TRIGGER_RE.sub('', query.message))
            new_query.is_private = True
            self.bot.handle_cmd(new_query)
