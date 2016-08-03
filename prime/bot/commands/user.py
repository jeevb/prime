from prime.bot.command import Command
from prime.bot.decorators import (
    reply_with_exception,
    arg,
    description,
    user_group
)
from prime.bot.exceptions import InvalidEntity
from prime.bot.constants import ADMIN_GROUP


@arg('-g', '--group', required=True, type=str.lower,
     help='Group to add user(s) to or remove from.')
@arg('-r', '--remove', action='store_true', default=False,
     help='Remove users from group instead.')
@arg('users', help='Users to add to (or remove from) group.', nargs='+')
@description('Adds/Removes user(s) to/from group.')
class Usermod(Command):
    @reply_with_exception
    def handle(self, query, args):
        if not self.bot.groups.can_modify_group(query.user, args.group):
            query.reply('Only administrators or group members may do that.')
            return

        handler = (
            self.bot.groups.add_user_to_group
            if not args.remove else
            self.bot.groups.remove_user_from_group
        )

        added_or_removed = [
            user for user in args.users
            if handler(user, args.group)
        ]
        if added_or_removed:
            query.reply(
                'The following users have '
                'been successfully {0} group "{1}": {2}'.format(
                    'removed from' if args.remove else 'added to',
                    args.group.lower(),
                    ', '.join(added_or_removed)
                )
            )


@user_group(ADMIN_GROUP)
@description('Lists user groups.')
class Usergroups(Command):
    def init_parser(self):
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument('-g',
                           '--group',
                           help='Only list users in this group.')
        group.add_argument('-u',
                           '--user',
                           help='Only list groups for this user.')

    def get_user_groups(self, user):
        for i in self.bot.groups.list_user_groups(user):
            yield '{0}: {1}'.format(i[0], ','.join(i[1]))

    def list_group_users(self, query, group):
        users = list(self.bot.groups.users_in_groups(group))
        if users:
            query.reply_within_block('{0}: {1}'.format(group, ','.join(users)))
        else:
            query.reply('No group users found.')

    @reply_with_exception
    def handle(self, query, args):
        if args.group is not None:
            return self.list_group_users(query, args.group)

        groups = list(self.get_user_groups(args.user))
        if groups:
            query.reply_within_block('\n'.join(groups))
        else:
            query.reply('No user groups found.')


@description('Lists groups that you are a part of.')
class Groups(Command):
    def handle(self, query, args):
        _, groups = next(self.bot.groups.list_user_groups(query.user_link))
        if groups:
            query.reply('You are in the following groups:\n{0}'.format(
                ', '.join(groups)))
        else:
            query.reply('You are currently not in any group.')
