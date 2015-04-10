import random

import simpy

from models.animal import Animal
from pygame import image


class Hare(Animal):
    def __init__(self, env, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0):
        super(Hare, self).__init__(env, eating_duration, running_duration, sleeping_duration, name, x, y)
        self.image = image.load('img/hare.png')

    def run(self):
        while True:
            try:
                self.report("Sleeping")
                yield self.env.timeout(self.sleeping_time)

                self.report("Eating")
                yield self.env.timeout(self.eating_time)

                self.report("Running")
                self.move()
                yield self.env.timeout(self.running_time)
            except simpy.Interrupt:
                self.report("Has been killed!")

    def can_reproduce_with(self, other_animal):
        myself = self == other_animal
        same_species = other_animal.__class__ == self.__class__
        close_by = self.distance(other_animal) < .001
        would_like_to_reproduce = random.random() > .98

        return not myself and same_species and close_by and would_like_to_reproduce
