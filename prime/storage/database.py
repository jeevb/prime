import os

from peewee import SqliteDatabase, Model
from prime.storage.local_storage import USER_DIR

PRIME_DB = SqliteDatabase(os.path.join(USER_DIR, 'prime.db'))


class BaseModel(Model):
    class Meta:
        database = PRIME_DB
