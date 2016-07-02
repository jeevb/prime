from gevent import Greenlet, sleep, spawn_raw
from gevent.event import Event
from prime.bot.command import CommandMgr
from prime.bot.listener import ListenerMgr


class GenericBot(object):
    def __init__(self):
        self._greenlet = None
        self._cmd_mgr = CommandMgr(self)
        self._listener_mgr = ListenerMgr(self)
        self._stop_event = Event()
        self._stop_event.set()

    def start(self):
        self._stop_event.clear()
        if not self._greenlet:
            self._greenlet = Greenlet(self._run)
            self._greenlet.start()

    def join(self, timeout=None):
        self._stop_event.wait(timeout)

    def stop(self):
        self._stop_event.set()
        self._greenlet.kill()
        self._greenlet = None

    def handle_cmd(self, query):
        self._cmd_mgr.handle(query)

    def _run(self):
        while True:
            self._poll()
            sleep(10)

    def _poll(self):
        raise NotImplementedError(
            '%r should implement the `_poll` method.'
            % self.__class__.__name__
        )

    def _send(self, channel, message):
        raise NotImplementedError(
            '%r should implement the `_send` method.'
            % self.__class__.__name__
        )

    def _on_query(self, query):
        query.send_handler = self._send
        spawn_raw(self._listener_mgr.handle, query)
