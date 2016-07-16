import importlib.util
import os
import re
import sys

from prime.storage.local_storage import (
    USER_DIR,
    USER_COMMANDS_DIR,
    USER_LISTENERS_DIR
)

PACKAGE_RE = re.compile(r'^(?P<package>.+)\.py$')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMAND_DIRS = [
    ('prime_default_commands', os.path.join(BASE_DIR, 'commands')),
    ('prime_user_commands', USER_COMMANDS_DIR)
]
LISTENER_DIRS = [
    ('prime_default_listeners', os.path.join(BASE_DIR, 'listeners')),
    ('prime_user_listeners', USER_LISTENERS_DIR)
]

def load(dirnames):
    for module_root, dirname in dirnames:
        if not os.path.isdir(dirname):
            continue
        for fn in os.listdir(dirname):
            match = PACKAGE_RE.match(fn)
            if not match:
                continue
            module_name = '{}.{}'.format(module_root, match.group('package'))
            if module_name in sys.modules:
                continue
            spec = importlib.util.spec_from_file_location(
                module_name,
                os.path.join(dirname, match.group())
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

def load_commands():
    return load(COMMAND_DIRS)

def load_listeners():
    return load(LISTENER_DIRS)
