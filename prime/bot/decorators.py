from prime.bot.constants import (
    COMMAND_ARGS,
    COMMAND_DESC,
    COMMAND_TRIGGERS,
    COMMAND_TIMEOUT,
    COMMAND_DMONLY,
    COMMAND_USER_GROUPS,
    COMMAND_CHANNEL_GROUPS
)

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

def trigger(*what):
    def wrapper(cls):
        triggers = getattr(cls, COMMAND_TRIGGERS, set())
        for val in what:
            triggers.add(val)
        setattr(cls, COMMAND_TRIGGERS, triggers)
        return cls
    return wrapper

def timeout(seconds):
    def wrapper(cls):
        setattr(cls, COMMAND_TIMEOUT, seconds)
        return cls
    return wrapper

def dm_only(cls):
    def wrapper(*args, **kwargs):
        setattr(cls, COMMAND_DMONLY, True)
        return cls
    return wrapper

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
