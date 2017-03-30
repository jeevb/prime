from peewee import CharField
from playhouse.fields import ManyToManyField
from prime.storage.database import GroupsBaseModel


class User(GroupsBaseModel):
    name = CharField(unique=True)


class Channel(GroupsBaseModel):
    name = CharField(unique=True)


class Group(GroupsBaseModel):
    name = CharField(unique=True)
    users = ManyToManyField(User, related_name='groups')
    channels = ManyToManyField(Channel, related_name='groups')


UserGroups = Group.users.get_through_model()
ChannelGroups = Group.channels.get_through_model()
