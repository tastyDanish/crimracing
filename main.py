import discord
import random
import json
from random import shuffle
from time import sleep

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# key is the player, value[0] is the emoji and value[1] is the position
racers = {}
result = []
distance = 80
config = {
    'token': '',
    'organizer': ''
}

with open('token.json') as f:
    configs = json.load(f)
    config['organizer'] = configs['organizer']
    config['token'] = configs['token']


async def race_result(message):
    winners = 'THE RESULT OF THE RACE:\n'
    for i, r in enumerate(result):
        winners += f'{i + 1}: {racers[r[0]][0]} {r[0]} (tiebreaker distance {r[1]})\n'
    await message.channel.send(winners)


async def race_loop(message):
    await message.channel.send('ON YOUR MARKS')
    sleep(.5)
    await message.channel.send('GET SET')
    sleep(.5)
    await message.channel.send('GO')

    # create starting lineup
    start = f'\n╔{"═" * distance}|\n'
    for key, item in racers.items():
        start += f"╟{'─' * item[1]}{item[0]}\n"
    start += f'╚{"═" * distance}|'
    await message.channel.send(start)

    while True:
        out = f'\n╔{"═" * distance}|\n'
        round_winners = {}
        for key, item in racers.items():
            crit_message = ''
            # check if past the line
            if item[1] >= distance:
                if key not in [x[0] for x in result]:
                    round_winners[key] = item[1]
                item[1] = distance
            else:
                # calculate velocity
                crit = random.randint(1, 20)
                if crit == 1:
                    crit_message = '*trips*'
                elif crit == 20:
                    crit_message = '*sudden burst of speed*'
                    item[1] += 8
                else:
                    item[1] += random.randint(1, 5)

            # create racer drawing
            out += f"╟{'─' * item[1]}{item[0]}{crit_message}\n"

        out += f'╚{"═" * distance}|'
        await message.channel.send(out)
        sleep(.5)

        # sort the round winners by final distance. The winner is whoever made the farther distance
        sorted_winners = {k: v for k, v in sorted(round_winners.items(), key=lambda x: x[1], reverse=True)}
        for winner, value in sorted_winners.items():
            result.append([winner, value])
        if len(result) == len(racers.keys()):
            break
    await race_result(message)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # add a racer to the race
    if message.content.startswith('!crimracing add'):
        split = message.content.split(' ')
        if len(split) < 3:
            await message.channel.send('I did not understand that add request')
            return
        emoji = message.content.split(' ')[2]
        if emoji in racers.items():
            await message.channel.send(f'{emoji} is already taken. Try another one')
            return
        racers[message.author] = [emoji, 0]
        await message.channel.send(f'I have added {racers[message.author][0]} for participant {message.author}')

    # show race participants
    if message.content.startswith('!crimracing describe'):
        say = ''
        if len(racers.keys()) == 0:
            await message.channel.send('There are no racers lined up')
        for key, item in racers.items():
            say += f"{item[0]}: {key}\n"
        await message.channel.send(say)

    # reset the race
    if message.content.startswith('!crimracing reset') and str(message.author) == config['organizer']:
        racers.clear()
        result.clear()
        await message.channel.send('I have cleared the racers and the results')

    # race again
    if message.content.startswith('!crimracing again') and str(message.author) == config['organizer']:
        result.clear()
        await race_loop(message)

    # start the race
    if message.content.startswith('!crimracing start') and str(message.author) == config['organizer']:
        if len(result) == len(racers.keys()):
            await message.channel.send('Reset the race or run the again command to race again')
        await race_loop(message)

    # just get the results
    if message.content.startswith('!crimracing result'):
        await race_result(message)


client.run(config['token'])
