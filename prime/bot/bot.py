import traceback

from .command import CommandMgr
from .constants import SYSTEM_USER, SYSTEM_CHANNEL
from .listener import ListenerMgr
from .job import JobsMgr
from .query import Query
from .utils import strip
from gevent import Greenlet, sleep, spawn_raw, spawn_later
from gevent.event import Event
from greenlet import GreenletExit
from prompt_toolkit import prompt, AbortAction


class GenericBot(object):
    command_mgr_class = CommandMgr
    listener_mgr_class = ListenerMgr
    jobs_mgr_class = JobsMgr

    query_class = Query

    def __init__(self, ping_interval=3):
        super(GenericBot, self).__init__()
        self._greenlet = None
        self._prompt_greenlet = None
        self._command_mgr = self.command_mgr_class(self)
        self._listener_mgr = self.listener_mgr_class(self)
        self._jobs_mgr = self.jobs_mgr_class(self)
        self._stop_event = Event()
        self._stop_event.set()

        # For pinging server
        self._ping_interval = ping_interval

    def handle_cmd(self, query):
        self._command_mgr.handle(query)

    def start(self):
        self._stop_event.clear()
        if not self._greenlet:
            self._greenlet = Greenlet(self.run)
            self._greenlet.start()

        if not self._prompt_greenlet:
            self._prompt_greenlet = Greenlet(self.prompt)
            self._prompt_greenlet.start()

    def join(self, timeout=None):
        try:
            self._stop_event.wait(timeout)
        except KeyboardInterrupt:
            pass

    def stop(self):
        self._stop_event.set()

        self._greenlet.kill()
        self._greenlet = None

        self._prompt_greenlet.kill()
        self._prompt_greenlet = None

    def prompt(self):
        while True:
            try:
                message = prompt('>>> ')
            except (GreenletExit, KeyboardInterrupt, SystemExit):
                self.stop()
            except:
                traceback.print_exc()
            else:
                if message:
                    query = Query(SYSTEM_USER, SYSTEM_CHANNEL, message)
                    query.is_targeting_me = True
                    query.is_private = True
                    query.send_handler = (
                        lambda _, m: self._send_helper(print, m))
                    spawn_raw(self._listener_mgr.handle, query)
            finally:
                sleep(.5)

    def run(self):
        while True:
            try:
                self._connect()
                self.poll()
            except (GreenletExit, KeyboardInterrupt, SystemExit):
                self.stop()
            except:
                traceback.print_exc()
                sleep(10)

    def poll(self):
        raise NotImplementedError(
            '%r should implement the `poll` method.'
            % self.__class__.__name__
        )

    def _send_helper(self, handler, message):
        message = strip(message)
        if isinstance(message, (str, bytes)):
            if message:
                handler(message)
        elif hasattr(message, '__iter__'):
            for chunk in message:
                if chunk:
                    sleep(.5)
                    handler(chunk)

    def send(self, channel, message):
        raise NotImplementedError(
            '%r should implement the `send` method.'
            % self.__class__.__name__
        )

    def on_query(self, query):
        query.send_handler = self.send
        self._listener_mgr.handle(query)

    def _ping(self):
        self.ping()
        spawn_later(self._ping_interval, self._ping)

    def _connect(self):
        self.connect()
        self._ping()

    def connect(self):
        raise NotImplementedError(
            '%r should implement the `connect` method.'
            % self.__class__.__name__
        )

    def ping(self):
        raise NotImplementedError(
            '%r should implement the `ping` method.'
            % self.__class__.__name__
        )
