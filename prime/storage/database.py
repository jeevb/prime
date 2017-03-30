from peewee import SqliteDatabase, Model

GROUPS_DB = SqliteDatabase(None)


class GroupsBaseModel(Model):
    class Meta:
        database = GROUPS_DB
