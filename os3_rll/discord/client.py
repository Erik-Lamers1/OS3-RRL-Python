import discord
import asyncio
import queue
from discord.ext import commands, tasks
from logging import getLogger

from os3_rll.conf import settings
from os3_rll.actions import stub
from os3_rll.discord.annoucements.challenge import announce_challenge
from os3_rll.operations.challenge import get_challenge

logger = getLogger(__name__)

command_table = {'hi': stub.hello,
            'announce': announce_challenge,
            'get_ranking': stub.test_call_list,
            'get_active_challenges': stub.test_call_int,
            'what': stub.test_call_str,
            'website': stub.get_website,
            'get_challenge': get_challenge,
            'create_challenge': stub.create_challenge,
            'complete_challenge': stub.complete_challenge,
            'reset_challenge': stub.reset_challenge,
            'help': stub.stub_help
            }

message_queue = queue.Queue()

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    logger.info('bot.on_ready: {} is connected to the following guild:\n'.format(bot.user))
    logger.info('bot.on_ready: {}(id: {})'.format(guild.name, guild.id))


@bot.command()
async def hi(ctx, *args):
    logger.debug('bot.command.hi: called with: {} arguments - {}'.format(len(args), ', '.join(args)))
    res = 'Hi {}\n'.format(ctx.author.mention)
    responses = ["How are you doing today? Wait that's retorical, I am a bot I do not care.\n",
                 "I was just looking at your rank. Did you know that you suck at rocket league? I heard some guy SquishyMuffinz is best.\n",
                 "Please leave me alone. I am randomizing the rankings database to mess with Mr.Vin.\n",
                 "Due to COVID-19 I've had to reimplement the transport protocol from QUIC to plain UDP to avoid handshakes.\n",
                 "Please do not bother me. I am looking into this Markov Chain theory. It should be able to give me more human like responses.",
                 "What are you doing here? LOL, your rank is so low you should practice uninstall.\n"]
    res += random.choice(responses)
    await ctx.send(res)


#@bot.event
#async def on_message(message):
#    logger.info('bot.on_message: saw message {} content=<<{}>>'.format(message, message.content))
#    channel = message.channel
#
#    if channel.name == settings.DISCORD_CHANNEL:
#        if message.content.startswith("$"):
#            logger.info('bot.on_message: message.content = {}'.format(message.content))
#            logger.info('bot.on_message: message.author  = {}#{}'.format(message.author.name, message.author.discriminator))
#            full_command = message.content[1:]
#            cmd = full_command.split(' ')[0]
#            params = [message.author, full_command.split(' ')[1:]]
#
#            try:
#                try:
#                    res = commands[cmd](params)
#                except (TypeError, ValueError) as e:
#                    logger.error('bot.on_message: Found a PEBKAC, user provides stupid params: {}\n'.format(params) +
#                                 'This resulted in the following error:\n{}\n'.format(str(e))
#                                )
#                    res = commands['help'](params)
#            except KeyError:
#                logger.error('bot.on_message: unknown command {}'.format(cmd))
#
#            if res is None:
#                res = "Ok..."
#
#            if type(res) is dict:
#                await channel.send(res['content'], embed=res['embed'])
#            else:
#                await channel.send(res)

async def post():
    logger.debug('bot.post: started background task')
    await bot.wait_until_ready()
    while not bot.is_closed():
        if not message_queue.empty():
            msg = message_queue.get()
            logger.debug('bot.post: got a message to post {}'.format(msg))
            channel = discord.utils.get(bot.get_all_channels(), name=settings.DISCORD_CHANNEL)
            await channel.send(msg['content'], embed=msg['embed'])
        await asyncio.sleep(5)


def create_embed(data):
    embed = discord.Embed(title=data['title'],
                          description=data['description'],
                          url=settings.WEBSITE,
                          color=data['colour'])
    embed.set_thumbnail(url=settings.DISCORD_EMBED_THUMBNAIL)
    embed.set_footer(text=data['footer'])
    return embed


def get_player(player):
    # Iterates over all the members the bot can see. (have to be members of guilds that it is connected too)
    members = bot.get_all_members()
    challengee = None

    if player.startswith('<@!'):
        player_id = player[3:-1]
        logger.debug("bot.get_player: got a mention for player_id {}".format(player_id))
        for member in members:
            logger.debug("bot.get_player: check mentions if {} == {}".format(member.id, player_id))
            if str(member.id) == player_id:
                challengee = member
                break
    else:
        for member in members:
            logger.debug("bot.get_player: check name if {} == {}".format(member.name, player))
            if member.name == player:
                challengee = member
                break

    if challengee is None:
        raise TypeError

    return challengee


def discord_client():
    logger.info('Initializing Discord client')
    bot.loop.create_task(post())

    while True:
        bot.run(settings.DISCORD_TOKEN)
