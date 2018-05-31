from peewee import CharField, ManyToManyField
from prime.storage.database import GroupsBaseModel


class User(GroupsBaseModel):
    name = CharField(unique=True)


class Channel(GroupsBaseModel):
    name = CharField(unique=True)


class Group(GroupsBaseModel):
    name = CharField(unique=True)
    users = ManyToManyField(User, backref='groups')
    channels = ManyToManyField(Channel, backref='groups')


UserGroups = Group.users.get_through_model()
ChannelGroups = Group.channels.get_through_model()
