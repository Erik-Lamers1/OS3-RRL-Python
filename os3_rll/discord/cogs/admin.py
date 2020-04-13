import discord
import re
from discord.ext import commands
from logging import getLogger
from os3_rll.actions.player import add_player

# from os3_rll.discord.announcements.challenge import announce_new_season
from os3_rll.discord.announcements.player import announce_new_player
from os3_rll.discord.client import is_rll_admin
from os3_rll.discord.utils import get_player, not_implemented
from os3_rll.conf import settings

logger = getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ps_regex = re.compile("^(<@[0-9]+>), (.+), (.+)$")

    @commands.command(pass_context=True)
    @is_rll_admin
    async def start_new_season(self, ctx):
        """Resets the player ranking, scrambles a new leader bord, but keeps player statistics."""
        logger.debug("start_new_seasion requested by {}".format(str(ctx.author)))
        # announcement = announce_new_season(res)
        # await ctx.send(announcement["content"], embed=announcement["embed"])
        await ctx.send(not_implemented())

    @commands.command(pass_context=True)
    @is_rll_admin
    async def add_player(self, ctx, player: discord.Member, player_settings: str):
        """Allows RLL Admins to add players to the Rocket League Ladder.
           Players need a gamertag, discord handle and a name
        """
        logger.info("add_player: called by {} for {}".format(ctx.author, str(player)))
        input_match = self.ps_regex.fullmatch(player_settings)
        if not input_match:
            input_err_msg = (
                "Wrong arguments given.\n" + "Expected: <@DiscordMention>, <name>, <gamertag>\n" + "Got: {}\n".format(player_settings)
            )
            raise commands.UserInputError(input_err_msg)
        if get_player(str(player)) is None:
            raise commands.BadArgument("{} is not a member of this guild.".format(str(player)))

        # TODO check if player is alread in the database
        name, gamertag = input_match.group(2, 3)
        player_info, password = add_player(name, gamertag, str(player))
        player_channel = await player.create_dm()
        admin_channel = await ctx.author.create_dm()
        admin_msg = "Created player for {0[0][0]} with gamertag: {0[0][1]} and discord {0[0][2]}".format(player_info)
        player_msg = (
            "{} has created an account for you, "
            + "your login is {}, your password is {}, "
            + "please change this password at {} ASAP.".format(str(ctx.author), player_info.gamertag, password, settings.website)
        )
        await admin_channel.send(admin_msg)
        await player_channel.send(player_msg)
        announcement = announce_new_player(player_info)
        await ctx.send(announcement["content"], embed=announcement["embed"])


def setup(bot):
    bot.add_cog(Admin(bot))
    logger.debug("{} added to bot {}".format(__name__, bot.user))