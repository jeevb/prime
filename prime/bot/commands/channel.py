from prime.bot.command import Command
from prime.bot.decorators import arg, reply_with_exception
from prime.bot.exceptions import InvalidEntity
from prime.bot.constants import ADMIN_GROUP

channelmod = Command.create(
    'channelmod',
    description='Channels to add to (or remove from) group.'
)

@channelmod.register
@arg('-g', '--group', required=True, type=str.lower,
     help='Group to add channel(s) to or remove from.')
@arg('-r', '--remove', action='store_true', default=False,
     help='Remove channels from group instead.')
@arg('channels', help='Channels to add to (or remove from) group.', nargs='+')
@reply_with_exception
def channelmod_handler(command, query, args):
    if not command.bot.can_modify_group(query.user, args.group):
        query.reply('Only administrators or group members may do that.')
        return

    handler = (
        command.bot.add_channel_to_group
        if not args.remove else
        command.bot.remove_channel_from_group
    )

    added_or_removed = [
        channel for channel in args.channels
        if handler(channel, args.group)
    ]
    if added_or_removed:
        query.reply(
            'The following channels have '
            'been successfully {0} group "{1}": {2}'.format(
                'removed from' if args.remove else 'added to',
                args.group.lower(),
                ', '.join(added_or_removed)
            )
        )

channelgroups = Command.create(
    'channelgroups',
    user_groups=(ADMIN_GROUP,),
    description='Lists channel groups.'
)

def get_channel_groups(command, channel):
    for i in command.bot.list_channel_groups(channel):
        yield '{0}: {1}'.format(i[0], ','.join(i[1]))

def list_group_channels(command, query, group):
    channels = list(command.bot.channels_in_groups(group))
    if channels:
        query.reply_within_block(
            '{0}: {1}'.format(group, ','.join(channels)))
    else:
        query.reply('No group channels found.')

@channelgroups.register
@arg('-g', '--group', help='Only list channels in this group.')
@arg('-c', '--channel', help='Only list groups for this channel.')
@reply_with_exception
def channelgroups_handler(command, query, args):
    if args.group is not None:
        return list_group_channels(command, query, args.group)

    groups = list(get_channel_groups(command, args.channel))
    if groups:
        query.reply_within_block('\n'.join(groups))
    else:
        query.reply('No channel groups exist.')
