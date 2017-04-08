from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from argh import arg
from functools import wraps
from prime.bot.constants import (
    COMMAND_TIMEOUT,
    COMMAND_DMONLY,
    COMMAND_USER_GROUPS,
    COMMAND_CHANNEL_GROUPS,
    JOB_TRIGGER,
    JOB_BROADCAST_GROUPS,
)

##
## Command handler decorators
##
def reply_with_exception(func):
    @wraps(func)
    def wrapper(command, query, args):
        try:
            func(command, query, args)
        except Exception as e:
            query.reply_within_block('Error: {0}'.format(str(e)))
    return wrapper


##
## Job decorators
##

def interval(*args, **kwargs):
    def wrapper(cls):
        trigger = IntervalTrigger(*args, **kwargs)
        setattr(cls, JOB_TRIGGER, trigger)
        return cls
    return wrapper

def cron(*args, **kwargs):
    def wrapper(cls):
        trigger = CronTrigger(*args, **kwargs)
        setattr(cls, JOB_TRIGGER, trigger)
        return cls
    return wrapper

def broadcast(*channel_groups):
    def wrapper(cls):
        setattr(cls, JOB_BROADCAST_GROUPS, channel_groups)
        return cls
    return wrapper
