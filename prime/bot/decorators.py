from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from prime.bot.constants import (
    COMMAND_ARGS,
    COMMAND_DESC,
    COMMAND_ALIASES,
    COMMAND_TIMEOUT,
    COMMAND_DMONLY,
    COMMAND_USER_GROUPS,
    COMMAND_CHANNEL_GROUPS,
    JOB_TRIGGER,
    JOB_BROADCAST_GROUPS,
)


##
## Command decorators
##

def arg(*args, **kwargs):
    def wrapper(cls):
        command_args = getattr(cls, COMMAND_ARGS, [])
        kwargs['option_strings'] = args
        command_args.append(kwargs)
        setattr(cls, COMMAND_ARGS, command_args)
        return cls
    return wrapper

def description(text):
    def wrapper(cls):
        setattr(cls, COMMAND_DESC, text)
        return cls
    return wrapper

def alias(*what):
    def wrapper(cls):
        aliases = getattr(cls, COMMAND_ALIASES, set())
        for val in what:
            aliases.add(val)
        setattr(cls, COMMAND_ALIASES, aliases)
        return cls
    return wrapper

def timeout(seconds):
    def wrapper(cls):
        setattr(cls, COMMAND_TIMEOUT, seconds)
        return cls
    return wrapper

def dm_only(cls):
    setattr(cls, COMMAND_DMONLY, True)
    return cls

def user_group(*groups):
    def wrapper(cls):
        user_groups = getattr(cls, COMMAND_USER_GROUPS, set())
        for group in groups:
            user_groups.add(group)
        setattr(cls, COMMAND_USER_GROUPS, user_groups)
        return cls
    return wrapper

def channel_group(*groups):
    def wrapper(cls):
        channel_groups = getattr(cls, COMMAND_CHANNEL_GROUPS, set())
        for group in groups:
            channel_groups.add(group)
        setattr(cls, COMMAND_CHANNEL_GROUPS, channel_groups)
        return cls
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
