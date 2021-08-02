import discord
import random
from random import shuffle
from time import sleep

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# key is the player, value[0] is the emoji and value[1] is the position
racers = {}
lock = False
result = []
distance = 100


async def race_result(message):
    winners = 'THE RESULT OF THE RACE:\n'
    for i, r in enumerate(result):
        winners += f'{i + 1}: {r}\'s racer {racers[r][0]}\n'
    await message.channel.send(winners)


async def race_loop(message):
    winner = None
    await message.channel.send('ON YOUR MARKS')
    sleep(.5)
    await message.channel.send('GET SET')
    sleep(.5)
    await message.channel.send('GO')

    while True:
        out = f'|{"-" * distance}|\n'
        round_winners = []
        for key, item in racers.items():
            out += f"|{' ' * item[1]}{item[0]}{' ' * (distance - item[1])}"
            if item[1] >= distance:
                if key not in result:
                    round_winners.append(key)
                out += '\n'
            else:
                out += '|\n'
                item[1] += random.randint(1, 10)
        out += f'|{"-" * distance}|'
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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello {author}!'.format(author=message.author))

    if message.content.startswith('!crimracing add'):
        racers[message.author] = [message.content.split(' ')[2], 0]
        await message.channel.send(f'I have added {racers[message.author][0]} for participant {message.author}')

    if message.content.startswith('!crimracing describe'):
        say = ''
        if lock:
            await message.channel.send(f'{message.author} the race has already begun, you cannot be included as a racer')
        if len(racers.keys()) == 0:
            await message.channel.send('There are no racers lined up')
        for key, item in racers.items():
            say += f"{key}'s racer is {item[0]}\n"
        await message.channel.send(say)

    if message.content.startswith('!crimracing reset') and message.author == 'atastydanish#9181':
        racers.clear()
        result.clear()
        await message.channel.send('I have cleared the racers and the results')

    if message.content.startswith('!crimracing start') and message.author == 'atastydanish#9181':
        await race_loop(message)

    if message.content.startswith('!crimracing result'):
        await race_result(message)

client.run('ODIxMTc1NDIyMzU0OTgwODY1.YE_5NQ.-ok53z2KsYBRXTrP5oQT8VzHmfI')