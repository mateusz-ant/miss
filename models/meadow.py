import random
import itertools

from models.hare import Hare
from models.wolf import Wolf
from parameters import *


SEQUENCE = 0


def seq():
    global SEQUENCE
    SEQUENCE += 1
    return str(SEQUENCE)


class Meadow(object):
    def __init__(self, env, display):
        self.env = env
        self.display = display
        self.action = env.process(self.run())
        self.env.hares = [Hare(env, name="hare_" + seq(), display=self.display, x=rand_x(), y=rand_y()) for _ in range(NUM_OF_HARES)]
        self.env.wolves = [Wolf(env, name="wolf_" + seq(), display=self.display, x=rand_x(), y=rand_y()) for _ in range(NUM_OF_WOLVES)]

    @staticmethod
    def reproduce_species(animals, new_animal_constructor):
        animal_pairs = itertools.product(filter(lambda _: random.randint(0, 9) == 0, animals), repeat=2)
        can_reproduce = lambda h: h[0].can_reproduce_with(h[1]) and h[1].can_reproduce_with(h[0])
        new_animals_count = len(list(filter(can_reproduce, animal_pairs)))
        new_animals = [new_animal_constructor() for _ in range(new_animals_count)]
        animals.extend(new_animals)

    def run(self):
        while True:
            print(
                'MEADOW Report (at %d):\n  Hares: %d\n  Wolves: %d' % (
                self.env.now, len(self.env.hares), len(self.env.wolves)))
            yield self.env.timeout(REPORT_INTERVAL)

            if len(self.env.wolves):
                wolf = random.choice(self.env.wolves)
                yield wolf.env.process(wolf.hunt(hares=self.env.hares))

            self.reproduce_species(self.env.hares, lambda: Hare(self.env, name='hare_' + seq()))
            self.reproduce_species(self.env.wolves, lambda: Wolf(self.env, name='wolf_' + seq()))

