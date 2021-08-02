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
        winners += f'{i + 1}: {racers[r][0]} {r}\n'
    await message.channel.send(winners)


async def race_loop(message):
    await message.channel.send('ON YOUR MARKS')
    sleep(.5)
    await message.channel.send('GET SET')
    sleep(.5)
    await message.channel.send('GO')

    while True:
        out = f'\n╔{"═" * distance}|\n'
        round_winners = []
        for key, item in racers.items():
            out += f"╟{'─' * item[1]}{item[0]}\n"
            if item[1] >= distance:
                if key not in result:
                    round_winners.append(key)
            else:
                item[1] += random.randint(1, 5)
                if item[1] >= distance:
                    item[1] = distance
        out += f'╚{"═" * distance}|'
        await message.channel.send(out)
        sleep(.5)
        shuffle(round_winners)
        for winner in round_winners:
            result.append(winner)
        if len(result) == len(racers.keys()):
            break
    await race_result(message)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!crimracing add'):
        split = message.content.split(' ')[2]
        if len(split) < 3:
            await message.channel.send('I did not understand that add request')
            return
        emoji = message.content.split(' ')[2]
        if emoji in racers.items():
            await message.channel.send(f'{emoji} is already taken. Try another one')
            return
        racers[message.author] = [emoji, 0]
        await message.channel.send(f'I have added {racers[message.author][0]} for participant {message.author}')

    if message.content.startswith('!crimracing describe'):
        say = ''
        if len(racers.keys()) == 0:
            await message.channel.send('There are no racers lined up')
        for key, item in racers.items():
            say += f"{key}'s racer is {item[0]}\n"
        await message.channel.send(say)

    if message.content.startswith('!crimracing reset') and str(message.author) == config['organizer']:
        racers.clear()
        result.clear()
        await message.channel.send('I have cleared the racers and the results')

    if message.content.startswith('!crimracing again') and str(message.author) == config['organizer']:
        result.clear()
        await race_loop(message)

    if message.content.startswith('!crimracing start') and str(message.author) == config['organizer']:
        if len(result) == len(racers.keys()):
            await message.channel.send('Reset the race or run the again command to race again')
        await race_loop(message)

    if message.content.startswith('!crimracing result'):
        await race_result(message)


client.run(config['token'])
