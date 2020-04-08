from datetime import datetime
from logging import getLogger

from os3_rll.utils.math import ordinal
from os3_rll.discord.utils import create_embed

logger = getLogger(__name__)


def announce_challenge(p1, p2):
    """Generates an announcement to be posted by the discord bot as an embed

       Params:
           p1: player1 (the challenger) as a discord.Member object.
           p2: player2 (the challengee) as a discord.Member object.

       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    try:
        embed = {'title': "**{0.name} challenges {1.name}.**".format(p1, p2),
                 'description': "This match should be played within one week or {0.mention} loses automatically.".format(
                     p2),
                 'footer': "Good Luck!",
                 'colour': 2234352}

        message = {'content': "New Challenge!",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {} or {}".format(p1, p2))


def announce_winner(p1, p2, winner_id: int, match_results: str):
    """Generates an announcement to be posted by the discord bot as an embed

       Params:
           p1: Player() object.
           p2: Player() object.

       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    p1_games_won = 0
    p2_games_won = 0
    for game in match_results.split(' '):
        if int(game.split('-')[0]) > int(game.split('-')[1]):
            p1_games_won += 1
        else:
            p2_games_won += 1

    title = ""
    if p1.id == winner_id:
        title = "**{0.gamertag} has defeated {1.gamertag} with {2} games to {3}.**".format(p1, p2, p1_games_won,
                                                                                           p2_games_won)
        description = "{0.gamertag} takes {1.gamertag}'s spot on the leaderboard!.".format(p1, p2)
        footer = "No dream is too big. ... "
        colour = 48393
    else:
        title = "**{0.gamertag} successfully defended their spot against {1.gamertag} with a score of {2}-{3}**".format(
            p2, p1, p2_games_won, p1_games_won)
        description = "That means that {0.gamertag} is now on a timeout of 1 week.".format(p1)
        footer = "If you don't struggle, you'll never improve!"
        colour = 11540741

    try:
        embed = {'title': title,
                 'description': description,
                 'footer': footer,
                 'colour': colour}

        message = {'content': "Challenge Completed!",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found {} {} Objects for {} and {}".format(type(p1), type(p2), p1, p2))


def announce_challenge_info(challenge_data: dict):
    """"
    Announces some info about a challenge to Discord
    param dict: The info generated by os3_rll.actions.challenge.get_challenge
    return dist: message which can be send to discord
    """
    try:
        embed = {
            "title": "Awaiting completion of challenge between {} and {}".format(
                challenge_data['p1']['name'], challenge_data['p2']['name']
            ),
            "description": "{p2_gamertag} is defending their {p2_rank} place on the leaderboard against {p1_gamertag}. "
                           "This match should be player before {deadline} or {p1_gamertag} will win automatically".format(
                p1_gamertag=challenge_data['p1']['name'],
                p2_gamertag=challenge_data['p2']['name'],
                p2_rank=ordinal(challenge_data['p2']['rank']),
                deadline=datetime.strftime(challenge_data['deadline'], '%Y/%m/%d %H:%M')
            ),
            "colour": 0,
            "footer": "Let's get it on!"
        }
        message = {
            "content": "You have an outstanding challenge",
            'embed': create_embed(embed)
        }
        return message
    except KeyError as e:
        logger.error(
            'Encountered a non existing key while trying to build challenge_info message, got error: {}'.format(e)
        )


def announce_reset(challenge_data: dict):
    """Generates an announcement that a player has reset a challenge.
       param dict: The info generated by os3_rll.actions.challenge.get_challenge
       return dist: message which can be send to discord
    """
    try:
        embed = {
            'title': "**Challenge between {0} and {1} has been reset!**".format(challenge_data['p1']['name'],
                                                                                challenge_data['p2']['name']),
            "description": "{p2_gamertag} is defending their {p2_rank} place on the leaderboard against {p1_gamertag}. "
                           "This match should be player before {deadline} or "
                           "{p1_gamertag} will win automatically".format(
                p1_gamertag=challenge_data['p1']['name'],
                p2_gamertag=challenge_data['p2']['name'],
                p2_rank=ordinal(challenge_data['p2']['rank']),
                deadline=datetime.strftime(challenge_data['deadline'], '%Y/%m/%d %H:%M')),
            'footer': "Everybody deserves a second chance!",
            'colour': 2234352
        }

        message = {'content': "Resetting Challenge!",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except KeyError as e:
        logger.error(
            'Encountered a non existing key while trying to build challenge reset message, got error: {}'.format(e)
        )
