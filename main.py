import discord
from discord.ext import commands
from gamesets import Fair, Crits, EmoteRace, race_loop
from time import sleep
import json

description = '''Have a wacky race with Crim'''
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!crimracing ', description=description, intents=intents)

# key is the player, value[0] is the emoji and value[1] is the position
racers = {}
result = []
config = {
    'distance': 80,
    'token': '',
    'organizer': [],
    'rules': Fair(),
    'offset': 0,
    'channel': 'wacky-races-debug',
    'commercial': False
}

rulebook = {
    'fair': Fair(),
    'crits': Crits(),
    'emote': EmoteRace()
}

with open('token.json') as f:
    configs = json.load(f)
    config['organizer'] = configs['organizer']
    config['token'] = configs['token']
    config['offset'] = configs['offset']
    config['channel'] = configs['channel']


def to_lower(arg):
    return arg.lower()


async def race_result(message):
    winners = 'THE RESULT OF THE RACE:\n'
    for i, r in enumerate(result):
        winners += f'{i + 1}: {racers[r[0]][0]} {r[0]} (tiebreaker distance {r[1]})\n'
    await message.channel.send(winners)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.check
def whitelist(ctx):
    return ctx.message.channel.name == config['channel']


@bot.command(description='Adds an emote to the race with yourself as the participant.')
async def add(ctx, emote: str):
    """Adds an emote to the race with yourself as the participant."""
    if len(result) > 0 and len(result) == len(racers.keys()):
        await ctx.send("Last race hasn't been removed from memory. \n"
                       "Use '!crimracing reset' to clear everything or "
                       "'!crimracing again' to race again")
        return
    if emote in racers.items():
        await ctx.send(f'{emote} is already taken. Try another one')
        return
    player = ctx.message.author.name
    racers[player] = [emote, 0]
    await ctx.send(f'I have added {emote} for participant {player}')


@bot.command(description='Adds an emote to the race with someone else as the participant.')
async def force(ctx, emote: str, player: str):
    """Adds an emote to the race with someone else as the participant."""
    if emote in racers.items():
        await ctx.send(f'{emote} is already taken. Try another one')
        return
    racers[player] = [emote, 0]
    await ctx.send(f'I have added {racers[player][0]} for participant {player}')


@bot.command(description='Describes the rules and players of the next race')
async def describe(ctx):
    """Describes the rules and players of the next race"""
    say = f'current ruleset is: {config["rules"]}\n The racers are: \n'
    if len(racers.keys()) == 0:
        await ctx.send('There are no racers lined up')
    for key, item in racers.items():
        say += f"{item[0]}: {key}\n"
    await ctx.send(say)


@bot.command(description='Resets the racers and the results.')
async def reset(ctx):
    """Resets the racers and the results."""
    racers.clear()
    result.clear()
    await ctx.send('I have cleared the racers and the results')


@bot.command(description='Starts the race!')
async def start(ctx):
    """Starts the race!"""
    if len(result) == len(racers.keys()):
        await ctx.send('Reset the race or run the again command to race again')
        return
    if len(racers.keys()) == 1:
        await ctx.send("A race by yourself isn't that interesting. You should get someone to race with")
        return
    await race_loop(ctx, config, racers, result)
    await race_result(ctx)


@bot.command(description='Runs the race with the same emotes and participants.')
async def again(ctx):
    """Runs the race with the same emotes and participants."""
    result.clear()
    for key, item in racers.items():
        item[1] = 0
    await race_loop(ctx, config, racers, result)
    await race_result(ctx)


@bot.command(description='Gets the different rules you can race with.')
async def list_rules(ctx):
    """Gets the list of rules and what they do"""
    for key, item in rulebook.items():
        await ctx.send(item)
        await ctx.send('------------')


@bot.command(description='Runs the race with the same emotes and participants.')
async def rules(ctx, ruleset: to_lower):
    """Runs the race with the same emotes and participants."""
    if ruleset not in rulebook.keys():
        await ctx.send(f"{ruleset} isn't in my set of rules")
        say = 'Instead, you may use:\n'
        for key, item in rulebook.items():
            say += f'{item}\n'
        await ctx.send(say)
        return

    config['rules'] = rulebook[ruleset]

    if ruleset == 'emote':
        await ctx.send(f'NOTE: emote only supports custom emotes. Not unicode allowed')

    racers.clear()
    result.clear()
    await ctx.send(f'ruleset updated to {ruleset} and memory has been reset')


@bot.command(description='Get the results of the race')
async def raceresult(ctx):
    if len(result) > 0:
        await race_result(ctx)
    else:
        await ctx.send('No race results to report')


@bot.command(description="Run a commercial now")
async def commercial(ctx):
    await ctx.send('Watch Ballers® on HBO - a new season streaming now on HBO Max')
    await ctx.send('https://giphy.com/gifs/hbo-ballers-new-season-2015-year-ender-1iTHRySV2JrO1qeY')


@bot.command(description="Run a commercial during the race")
async def commercial_race(ctx):
    if not config['commercial']:
        config['commercial'] = True
        await ctx.send("Commercials are activated")
    else:
        config['commercial'] = False
        await ctx.send("Commercials are deactivated")


@bot.command()
async def rig_race(ctx):
    await ctx.send("I'm afraid I cannot let you do that")

bot.run(config['token'])
