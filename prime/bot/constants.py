import os
import re


##
## Loading modules
##

PACKAGE_RE = re.compile(r'^(?P<package>.+)\.py$')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR_JOIN = lambda *p : os.path.join(BASE_DIR, *p)


##
## Query parsing
##

SEPARATORS = re.escape(',.:;!? ')
SHORTHAND_TRIGGERS = '!'
SHORTHAND_TRIGGERS_ESC = re.escape(SHORTHAND_TRIGGERS)
SHORTHAND_TRIGGER_RE = re.compile(r'^[%s]+' % SHORTHAND_TRIGGERS_ESC, re.I)


##
## ACLs
##

# Privileged users
SYSTEM_USER = 'system'

# Privilged channels
SYSTEM_CHANNEL = 'system'

# Privileged groups
OWNER_GROUP = 'owner'
ADMIN_GROUP = 'admin'


##
## Command attributes
##

COMMAND_ALIASES = '__COMMAND_ALIASES__'
COMMAND_TIMEOUT = '__COMMAND_TIMEOUT__'
COMMAND_DMONLY = '__COMMAND_DMONLY__'
COMMAND_USER_GROUPS = '__COMMAND_USER_GROUPS__'
COMMAND_CHANNEL_GROUPS = '__COMMAND_CHANNEL_GROUPS__'
COMMAND_PARSER_ARGS = '__COMMAND_PARSER_ARGS__'


##
## Job attributes
##

JOB_TRIGGER = '__JOB_TRIGGER__'
JOB_BROADCAST_GROUPS = '__JOB_BROADCAST_GROUPS__'
