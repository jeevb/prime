import traceback

from gevent import Greenlet, sleep
from gevent.event import Event
from greenlet import GreenletExit
from prime.bot.command import CommandMgr
from prime.bot.listener import ListenerMgr
from prime.bot.job import JobsMgr
from prime.bot.groups import GroupsMgr


class GenericBot(object):
    command_mgr_class = CommandMgr
    listener_mgr_class = ListenerMgr
    jobs_mgr_class = JobsMgr
    groups_mgr_class = GroupsMgr

    def __init__(self):
        self._greenlet = None
        self._command_mgr = self.command_mgr_class(self)
        self._listener_mgr = self.listener_mgr_class(self)
        self._jobs_mgr = self.jobs_mgr_class(self)
        self._groups_mgr = self.groups_mgr_class()
        self._stop_event = Event()
        self._stop_event.set()

    @property
    def groups(self):
        return self._groups_mgr

    def handle_cmd(self, query):
        self._command_mgr.handle(query)

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

    def _run(self):
        while True:
            try:
                self._poll()
            except (GreenletExit, KeyboardInterrupt, SystemExit):
                self.stop()
            except:
                traceback.print_exc()
                sleep(10)

    def _poll(self):
        raise NotImplementedError(
            '%r should implement the `_poll` method.'
            % self.__class__.__name__
        )

    def send(self, channel, message):
        raise NotImplementedError(
            '%r should implement the `_send` method.'
            % self.__class__.__name__
        )

    def _on_query(self, query):
        query.send_handler = self.send
        self._listener_mgr.handle(query)
