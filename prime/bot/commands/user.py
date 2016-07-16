from prime.bot.command import Command
from prime.bot.decorators import arg, description
from prime.bot.exceptions import InvalidEntity
from prime.bot.constants import ADMIN_GROUP


@description('Adds/Removes user(s) to/from group.')
@arg('-g', '--group', required=True,
     help='Group to add user(s) to or remove from.')
@arg('-r', '--remove', action='store_true', default=False,
     help='Remove users from group instead.')
@arg('users', help='Users to add to (or remove from) group.', nargs='+')
class Usermod(Command):
    required_user_groups = (ADMIN_GROUP,)

    def handle(self, query, args):
        handler = (
            self.bot.groups.add_user_to_group
            if not args.remove else
            self.bot.groups.remove_user_from_group
        )

        added_or_removed = []
        try:
            for user in args.users:
                if handler(user, args.group):
                    added_or_removed.append(user)
        except InvalidEntity as e:
            query.reply(
                '{0} is not a valid user identifier.'.format(e.what))
        else:
            query.reply(
                'The following users have '
                'been successfully {0} group "{1}": {2}'.format(
                    'removed from' if args.remove else 'added to',
                    args.group.lower(),
                    ', '.join(added_or_removed)
                )
            )


@description('Lists user groups.')
@arg('-u', '--user', help='List groups for this user.')
class Usergroups(Command):
    def get_user_groups(self, user):
        for i in self.bot.groups.list_user_groups(user):
            yield '{0}: {1}'.format(i[0], ','.join(i[1]))

    def handle(self, query, args):
        groups = list(self.get_user_groups(args.user))
        if groups:
            query.reply_within_block('\n'.join(groups))
        else:
            query.reply('No user groups exist.')


@description('Lists groups that you are a part of.')
class Groups(Command):
    def handle(self, query, args):
        _, groups = next(self.bot.groups.list_user_groups(query.user_link))
        if groups:
            query.reply('You are in the following groups:\n{0}'.format(
                ', '.join(groups)))
        else:
            query.reply('You are currently not in any group.')
