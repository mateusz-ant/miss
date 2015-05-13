import itertools
from random import random, randint

from models.hare import Hare
from models.wolf import Wolf
from parameters import *


SEQUENCE = 0


def seq():
    global SEQUENCE
    SEQUENCE += 1
    return str(SEQUENCE)


def rand_x():
    return random() * SCREEN_LENGTH


def rand_y():
    return random() * SCREEN_HEIGHT


class Meadow(object):
    def __init__(self, env, display):
        self.env = env
        self.display = display
        self.action = env.process(self.run())
        self.env.hares = [Hare(env, name="hare_" + seq(), display=self.display, x=rand_x(), y=rand_y())
                          for _ in range(NUM_OF_HARES)]
        self.env.wolves = [Wolf(env, name="wolf_" + seq(), display=self.display, x=rand_x(), y=rand_y())
                           for _ in range(NUM_OF_WOLVES)]

    @staticmethod
    def reproduce_species(animals, new_animal_constructor):
        can_reproduce = lambda h: h[0].can_reproduce_with(h[1]) and h[1].can_reproduce_with(h[0])
        waste_energy_to_reproduce = lambda h: h.change_energy(-h.energy / 2)

        animal_pairs = itertools.product(filter(lambda _: randint(0, 9) > 3, animals), repeat=2)
        parent_animals = list(filter(can_reproduce, animal_pairs))

        new_animals = [new_animal_constructor(p[0].energy / 3 + p[1].energy / 3) for p in parent_animals]
        animals.extend(new_animals)

        for parents in parent_animals:
            parents[0].change_energy(-parents[0].energy / 3)
            parents[1].change_energy(-parents[1].energy / 3)

    def run(self):
        while True:
            print(
                'MEADOW Report (at %d):\n  Hares: %d\n  Wolves: %d' % (
                    self.env.now, len(self.env.hares), len(self.env.wolves)))
            yield self.env.timeout(REPORT_INTERVAL)

            # if len(self.env.wolves):
            # wolf = random.choice(self.env.wolves)
            # yield wolf.env.process(wolf.hunt(hares=self.env.hares))

            self.reproduce_species(self.env.hares, lambda e: Hare(self.env, name='hare_' + seq(), display=self.display,
                                                                  x=rand_x(), y=rand_y(), energy=e))
            self.reproduce_species(self.env.wolves, lambda e: Wolf(self.env, name='wolf_' + seq(), display=self.display,
                                                                   x=rand_x(), y=rand_y(), energy=e))

