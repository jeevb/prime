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
     help='Group to add channel(s) to or remove from.')
@arg('-r', '--remove', action='store_true', default=False,
     help='Remove channels from group instead.')
@arg('channels', help='Channels to add to (or remove from) group.', nargs='+')
@description('Adds/Removes channel(s) to/from group.')
class Channelmod(Command):
    @reply_with_exception
    def handle(self, query, args):
        if not self.bot.can_modify_group(query.user, args.group):
            query.reply('Only administrators or group members may do that.')
            return

        handler = (
            self.bot.add_channel_to_group
            if not args.remove else
            self.bot.remove_channel_from_group
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


@user_group(ADMIN_GROUP)
@description('Lists channel groups.')
class Channelgroups(Command):
    def init_parser(self):
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument('-g',
                           '--group',
                           help='Only list channels in this group.')
        group.add_argument('-c',
                           '--channel',
                           help='Only list groups for this channel.')

    def get_channel_groups(self, channel):
        for i in self.bot.list_channel_groups(channel):
            yield '{0}: {1}'.format(i[0], ','.join(i[1]))

    def list_group_channels(self, query, group):
        channels = list(self.bot.channels_in_groups(group))
        if channels:
            query.reply_within_block(
                '{0}: {1}'.format(group, ','.join(channels)))
        else:
            query.reply('No group channels found.')

    @reply_with_exception
    def handle(self, query, args):
        if args.group is not None:
            return self.list_group_channels(query, args.group)

        groups = list(self.get_channel_groups(args.channel))
        if groups:
            query.reply_within_block('\n'.join(groups))
        else:
            query.reply('No channel groups exist.')
