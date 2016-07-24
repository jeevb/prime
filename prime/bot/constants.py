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


##
## Mandatory group definitions
##

# Privileged groups
OWNER_GROUP = 'owner'
ADMIN_GROUP = 'admin'


##
## Command attributes
##

COMMAND_ARGS = '__COMMAND_ARGS__'
COMMAND_DESC = '__COMMAND_DESC__'
COMMAND_ALIASES = '__COMMAND_ALIASES__'
COMMAND_TIMEOUT = '__COMMAND_TIMEOUT__'
COMMAND_DMONLY = '__COMMAND_DMONLY__'
COMMAND_USER_GROUPS = '__COMMAND_USER_GROUPS__'
COMMAND_CHANNEL_GROUPS = '__COMMAND_CHANNEL_GROUPS__'


##
## Job attributes
##

JOB_TRIGGER = '__JOB_TRIGGER__'
