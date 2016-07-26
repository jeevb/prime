from collections import defaultdict
from peewee import DoesNotExist
from prime.bot.constants import OWNER_GROUP, ADMIN_GROUP
from prime.bot.models import User, Channel, Group, UserGroups, ChannelGroups
from prime.storage.database import PRIME_DB as db


class GroupsMgr(object):
    def __init__(self):
        self._db_cache = defaultdict(lambda: defaultdict(set))
        self._check_db()
        self._load()

    def _check_db(self):
        db.connect()
        db.create_tables(
            [User, Channel, Group, UserGroups, ChannelGroups],
            safe=True
        )

    def _load(self):
        for entity_type in (User, Channel):
            for entity in entity_type.select():
                for group in entity.groups:
                    self._db_cache[entity_type][entity.name].add(group.name)

    def _add_to_group(self, entity_type, entity, group):
        _entity, _ = entity_type.get_or_create(name=entity)
        _group, _ = Group.get_or_create(name=group)
        if _group in _entity.groups:
            return False
        _entity.groups.add(_group)
        self._db_cache[entity_type][entity].add(group)
        return True

    def _remove_from_group(self, entity_type, entity, group):
        try:
            _entity = entity_type.get(entity_type.name == entity)
            _group = Group.get(Group.name == group)
        except DoesNotExist:
            return False
        else:
            _entity.groups.remove(_group)
            self._db_cache[entity_type][entity].remove(group)
            return True

    def _in_group(self, entity_type, entity, group):
        return group in self._db_cache[entity_type][entity]

    def _list_in_groups(self, entity_type, groups):
        for entity, entity_groups in self._db_cache[entity_type].items():
            if set(groups).intersection(entity_groups):
                yield entity

    def _list_groups(self, entity_type, entity=None):
        for name, groups in self._db_cache[entity_type].items():
            if groups and (entity is None or entity == name):
                yield name, groups

    def _is_authorized(self, entity_type, entity, groups):
        if groups:
            for group in groups:
                if self._in_group(entity_type, entity, group):
                    break
            else:
                return False
        return True

    def add_user_to_group(self, user, group):
        return self._add_to_group(User, user, group)

    def add_channel_to_group(self, channel, group):
        return self._add_to_group(Channel, channel, group)

    def remove_user_from_group(self, user, group):
        return self._remove_from_group(User, user, group)

    def remove_channel_from_group(self, channel, group):
        return self._remove_from_group(Channel, channel, group)

    def user_in_group(self, user, group):
        return self._in_group(User, user, group)

    def channel_in_group(self, channel, group):
        return self._in_group(Channel, channel, group)

    def users_in_groups(self, *groups):
        return self._list_in_groups(User, groups)

    def channels_in_groups(self, *groups):
        return self._list_in_groups(Channel, groups)

    def list_user_groups(self, user=None):
        return self._list_groups(User, user)

    def list_channel_groups(self, channel=None):
        return self._list_groups(Channel, channel)

    def can_modify_group(self, user, group):
        if group not in (OWNER_GROUP, ADMIN_GROUP,):
            if self.is_admin(user) or self.user_in_group(user, group):
                return True;
        return self.is_owner(user)

    def is_owner(self, user):
        return self.user_in_group(user, OWNER_GROUP)

    def is_admin(self, user):
        return self.user_in_group(user, ADMIN_GROUP)

    def is_authorized_user(self, user, groups):
        if not OWNER_GROUP in (groups or []):
            if self.is_admin(user) or self._is_authorized(User, user, groups):
                return True
        return self.is_owner(user)

    def is_authorized_channel(self, channel, groups):
        return self._is_authorized(Channel, channel, groups)
