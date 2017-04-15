import os

##
## User-defined modules
##

USER_DIR = os.path.expanduser(os.path.join('~', '.prime'))
CONFIG_FILE_PATH = os.path.join(USER_DIR, 'config.yml')
USER_COMMANDS_DIR = os.path.join(USER_DIR, 'commands')
USER_LISTENERS_DIR = os.path.join(USER_DIR, 'listeners')
USER_JOBS_DIR = os.path.join(USER_DIR, 'jobs')
USER_FIXTURES_DIR = os.path.join(USER_DIR, 'fixtures')
DB_DIR = os.path.join(USER_DIR, 'db')
