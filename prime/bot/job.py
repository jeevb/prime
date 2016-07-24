from apscheduler.schedulers.gevent import GeventScheduler
from prime.bot.constants import BASE_DIR_JOIN, JOB_TRIGGER
from prime.bot.manager import ModuleMgr
from prime.storage.local_storage import USER_JOBS_DIR

class Job(object):
    manager = None

    @property
    def bot(self):
        return self.manager.bot

    @property
    def trigger(self):
        return getattr(self, JOB_TRIGGER, None)

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
            self._scheduler.add_job(module.handle, trigger=module.trigger)
