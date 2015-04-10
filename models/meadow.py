import random
import itertools

from models.hare import Hare
from models.wolf import Wolf
from parameters import NUM_OF_HARES, NUM_OF_WOLVES, REPORT_INTERVAL


SEQUENCE = 0


def seq():
    global SEQUENCE
    SEQUENCE += 1
    return str(SEQUENCE)


class Meadow(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
        self.hares = [Hare(env, name="hare_" + seq()) for _ in range(NUM_OF_HARES)]
        self.wolves = [Wolf(env, name="wolf_" + seq()) for _ in range(NUM_OF_WOLVES)]

    def run(self):
        while True:
            print(
                'MEADOW Report (at %d):\n  Hares: %d\n  Wolves: %d' % (self.env.now, len(self.hares), len(self.wolves)))
            yield self.env.timeout(REPORT_INTERVAL)

            if len(self.wolves):
                wolf = random.choice(self.wolves)
                yield wolf.env.process(wolf.hunt(hares=self.hares))

            hare_pairs = itertools.product(self.hares, repeat=2)
            can_reproduce = lambda h: h[0].can_reproduce_with(h[1]) and h[1].can_reproduce_with(h[0])
            new_hares_count = len(list(filter(can_reproduce, hare_pairs)))
            new_hares = [Hare(self.env, name='hare_' + seq()) for _ in range(new_hares_count)]
            self.hares.extend(new_hares)


