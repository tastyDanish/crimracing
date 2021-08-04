import random
from time import sleep


class Ruleset:
    def run(self, emote, config):
        pass


class Fair(Ruleset):
    def run(self, emote, config):
        return random.randint(1, 5), ''

    def __repr__(self):
        return 'Fair: Each Player will move between 1 to 5 spaces forward'


class Crits(Ruleset):
    def run(self, emote, config):
        crit = random.randint(1, 20)
        if crit == 1:
            return 0, '*trips*'
        elif crit == 20:
            return 8, '*sudden burst of speed*'
        else:
            return random.randint(1, 5), ''

    def __repr__(self):
        return 'Crits: Each player will move 1 to 5 spaces forward.\n' \
               'There is a 5% chance to trip and move 0 spaces.\n' \
               'There is a 5% chance to move 8 spaces'


class EmoteRace(Ruleset):
    def run(self, emote, config):
        numbers = emote.split(':')[2][:-1]
        return (int(random.choice(numbers)) + config['offset']) % 10, ''

    def __repr__(self):
        return 'Emote Race: Each emote has an ID. The amount of steps taken will be taken randomly' \
               'from all of the numbers in the ID. This value will be offset by an unknown number.\n' \
               'This will ensure the behavior of an emote stays the same, but you can only figure it ' \
               'out by racing'


async def race_loop(ctx, config, racers, result):
    await ctx.send('ON YOUR MARKS')
    sleep(.5)
    await ctx.send('GET SET')
    sleep(.5)
    await ctx.send('GO')

    # create starting lineup
    start = f'\n╔{"═" * config["distance"]}|\n'
    for key, item in racers.items():
        start += f"╟{'─' * item[1]}{item[0]}\n"
    start += f'╚{"═" * config["distance"]}|'
    await ctx.send(start)

    while True:
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
        await ctx.send(out)
        sleep(.5)

        # sort the round winners by final distance. The winner is whoever made the farther distance
        sorted_winners = {k: v for k, v in sorted(round_winners.items(), key=lambda x: x[1], reverse=True)}
        for winner, value in sorted_winners.items():
            result.append([winner, value])
        if len(result) == len(racers.keys()):
            break
    return
