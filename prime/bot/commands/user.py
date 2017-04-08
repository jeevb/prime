from prime.bot.command import Command
from prime.bot.decorators import arg, reply_with_exception
from prime.bot.exceptions import InvalidEntity
from prime.bot.constants import ADMIN_GROUP

usermod = Command.create(
    'usermod',
    description='Adds/Removes user(s) to/from group.'
)

@usermod.register
@arg('-g', '--group', required=True, type=str.lower,
     help='Group to add user(s) to or remove from.')
@arg('-r', '--remove', action='store_true', default=False,
     help='Remove users from group instead.')
@arg('users', help='Users to add to (or remove from) group.', nargs='+')
@reply_with_exception
def usermod_handler(command, query, args):
    if not command.bot.can_modify_group(query.user, args.group):
        query.reply('Only administrators or group members may do that.')
        return

    handler = (
        command.bot.add_user_to_group
        if not args.remove else
        command.bot.remove_user_from_group
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

usergroups = Command.create(
    'usergroups',
    user_groups=(ADMIN_GROUP,),
    description='Lists user groups.'
)

def get_user_groups(command, user):
    for i in command.bot.list_user_groups(user):
        yield '{0}: {1}'.format(i[0], ','.join(i[1]))

def list_group_users(command, query, group):
    users = list(command.bot.users_in_groups(group))
    if users:
        query.reply_within_block('{0}: {1}'.format(group, ','.join(users)))
    else:
        query.reply('No group users found.')

@usergroups.register
@reply_with_exception
@arg('-g', '--group', help='Only list users in this group.')
@arg('-u', '--user', help='Only list groups for this user.')
def usergroups_handler(command, query, args):
    if args.group is not None:
        return list_group_users(command, query, args.group)

    groups = list(get_user_groups(command, args.user))
    if groups:
        query.reply_within_block('\n'.join(groups))
    else:
        query.reply('No user groups found.')

groups = Command.create(
    'groups',
    description='Lists groups that you are a part of.'
)

@groups.register
def groups_handler(command, query, args):
    try:
        _, groups = next(command.bot.list_user_groups(query.user))
        if groups:
            query.reply('You are in the following groups:\n{0}'.format(
                ', '.join(groups)))
    except StopIteration:
        query.reply('You are currently not in any group.')
