from prime.bot.command import Command
from prime.bot.decorators import arg, description, user_group
from prime.bot.exceptions import InvalidEntity
from prime.bot.constants import ADMIN_GROUP


@user_group(ADMIN_GROUP)
@description('Adds/Removes channel(s) to/from group.')
@arg('-g', '--group', required=True,
     help='Group to add channel(s) to or remove from.')
@arg('-r', '--remove', action='store_true', default=False,
     help='Remove channels from group instead.')
@arg('channels', help='Channels to add to (or remove from) group.', nargs='+')
class Channelmod(Command):
    def handle(self, query, args):
        handler = (
            self.bot.groups.add_channel_to_group
            if not args.remove else
            self.bot.groups.remove_channel_from_group
        )

        added_or_removed = []
        try:
            for channel in args.channels:
                if handler(channel, args.group):
                    added_or_removed.append(channel)
        except InvalidEntity as e:
            query.reply(
                '{0} is not a valid channel identifier.'.format(e.what))
        else:
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
@arg('-c', '--channel', help='List groups for this channel.')
class Channelgroups(Command):
    def get_channel_groups(self, channel):
        for i in self.bot.groups.list_channel_groups(channel):
            yield '{0}: {1}'.format(i[0], ','.join(i[1]))

    def handle(self, query, args):
        groups = list(self.get_channel_groups(args.channel))
        if groups:
            query.reply_within_block('\n'.join(groups))
        else:
            query.reply('No channel groups exist.')
