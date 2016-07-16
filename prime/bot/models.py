from peewee import CharField
from playhouse.fields import ManyToManyField
from prime.storage.database import BaseModel


class User(BaseModel):
    name = CharField(unique=True)


class Channel(BaseModel):
    name = CharField(unique=True)


class Group(BaseModel):
    name = CharField(unique=True)
    users = ManyToManyField(User, related_name='groups')
    channels = ManyToManyField(Channel, related_name='groups')


UserGroups = Group.users.get_through_model()
ChannelGroups = Group.channels.get_through_model()
