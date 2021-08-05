import random
from time import sleep


class Ruleset:
    def run(self, emote, config):
        pass


class Fair(Ruleset):
    def run(self, emote, config):
        return random.randint(1, 5), ''

    def __repr__(self):
        return 'fair: Each Player will move between 1 to 5 spaces forward'


class Crits(Ruleset):
    def run(self, emote, config):
        crit = random.randint(1, 50)
        if crit == 1:
            return 0, '*trips*'
        elif crit == 50:
            return 8, '*sudden burst of speed*'
        else:
            return random.randint(1, 5), ''

    def __repr__(self):
        return 'crits: Each player will move 1 to 5 spaces forward.\n' \
               'There is a 5% chance to trip and move 0 spaces.\n' \
               'There is a 5% chance to move 8 spaces'


class EmoteRace(Ruleset):
    def run(self, emote, config):
        numbers = emote.split(':')[2][:-1]
        return (int(random.choice(numbers)) + config['offset']) % 10, ''

    def __repr__(self):
        return 'emote: Each emote has an ID. The amount of steps taken will be taken randomly ' \
               'from all of the numbers in the ID. This value will be offset by an unknown number.\n' \
               'This will ensure the behavior of an emote stays the same, but you can only figure it ' \
               'out by racing'


async def do_commercial(ctx):
    await ctx.send('WE INTTERUPT THIS BROADCAST FOR A MESSAGE FROM OUR SPONSORS')
    await ctx.send('...')
    sleep(0.5)
    await ctx.send('Dont tell anyone, but Dwayne Johnson is back as Spencer Stasmore ready to ball out with some ballers')
    await ctx.send('https://giphy.com/gifs/hbo-l1CC5T7JDUfU62uTC')
    sleep(0.5)
    await ctx.send('Another season of FOOTBALL and FAMILY')
    await ctx.send('https://giphy.com/gifs/hbo-spencer-ballers-2015-year-ender-d2Zh8bX4ETA2l49a')
    sleep(0.5)
    await ctx.send('Spencer is ready to put his money back to work even more so than ever in this new exciting season')
    await ctx.send('https://giphy.com/gifs/hbo-l1CC67iU5rs0dw2f6')
    sleep(0.5)
    await ctx.send('Watch Ballers® on HBO - a new season streaming now on HBO Max')
    await ctx.send('https://giphy.com/gifs/hbo-ballers-new-season-2015-year-ender-1iTHRySV2JrO1qeY')
    sleep(0.5)
    await ctx.send('And now - back to the race')
    await ctx.send('...')


async def race_loop(ctx, config, racers, result):
    await ctx.send('ON YOUR MARKS')
    sleep(.5)
    await ctx.send('GET SET')
    sleep(.5)
    await ctx.send('GO')

    # create starting lineup
    start = f'\n╔{"═" * config["distance"]}|\n'
    for key, item in racers.items():
        start += f"╟{item[0]}\n"
    start += f'╚{"═" * config["distance"]}|'
    await ctx.send(start)

    i = 0
    while True:
        if config['commercial'] and i == 10:
            await do_commercial(ctx)
        i += 1
        out = f'\n╔{"═" * config["distance"]}|\n'
        round_winners = {}
        for key, item in racers.items():
            crit_message = ''
            # check if past the line
            if item[1] >= config["distance"]:
                if key not in [x[0] for x in result]:
                    round_winners[key] = item[1]
                item[1] = config["distance"]
            else:
                # calculate velocity based on ruleset
                velocity, crit_message = config['rules'].run(item[0], config)
                item[1] += velocity

            # create racer drawing
            out += f"╟{'─' * item[1]}{item[0]}{crit_message}\n"

        out += f'╚{"═" * config["distance"]}|'

        # sort the round winners by final distance. The winner is whoever made the farther distance
        sorted_winners = {k: v for k, v in sorted(round_winners.items(), key=lambda x: x[1], reverse=True)}
        for winner, value in sorted_winners.items():
            result.append([winner, value])
        if len(result) == len(racers.keys()):
            break

        await ctx.send(out)
        sleep(.5)
    return
