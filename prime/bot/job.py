from apscheduler.schedulers.gevent import GeventScheduler
from prime.bot.constants import (
    BASE_DIR_JOIN,
    JOB_TRIGGER,
    JOB_BROADCAST_GROUPS
)
from prime.bot.manager import Module, ModuleMgr
from prime.storage.local_storage import USER_JOBS_DIR


class Job(Module):
    @property
    def trigger(self):
        return getattr(self, JOB_TRIGGER, None)

    @property
    def broadcast_groups(self):
        return getattr(self, JOB_BROADCAST_GROUPS, [])

    def broadcast(self):
        message = self.handle()
        for channel in self.bot.channels_in_groups(*self.broadcast_groups):
            channel = self.bot.validate_channel(channel)
            self.bot.send(channel, message)

    def handle(self):
        raise NotImplementedError(
            '%r should implement the `handle` method.'
            % self.__class__.__name__
        )


class JobsMgr(ModuleMgr):
    module_class = Job
    module_specs = [
        ('prime_user_jobs', USER_JOBS_DIR),
    ]

    def __init__(self, bot):
        super(JobsMgr, self).__init__(bot)
        self._scheduler = GeventScheduler()
        self._scheduler.start()
        self._add_jobs()

    def _add_jobs(self):
        for module in self._modules:
            task = (
                module.broadcast
                if module.broadcast_groups else
                module.handle
            )
            self._scheduler.add_job(task, trigger=module.trigger)
