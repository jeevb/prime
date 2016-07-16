from prime.bot.constants import COMMAND_ARGS, COMMAND_DESC

def arg(*args, **kwargs):
    def wrapper(cls):
        command_args = getattr(cls, COMMAND_ARGS, [])
        kwargs['option_strings'] = args
        command_args.append(kwargs)
        setattr(cls, COMMAND_ARGS, command_args)
        return cls
    return wrapper

def description(*args):
    def wrapper(cls):
        setattr(cls, COMMAND_DESC, ''.join(args))
        return cls
    return wrapper
