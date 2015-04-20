import random

import simpy

from models.animal import Animal
from pygame import image


class Hare(Animal):
    def __init__(self, env, display, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0):
        super(Hare, self).__init__(env, display, eating_duration, running_duration, sleeping_duration, name, x, y)
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
        from models.animal import can_reproduce_with
        return can_reproduce_with(.1, .25)(self, other_animal)

    def die(self):
        self.report("Bye bye cruel world")
        try:
            self.env.hares.remove(self)
        except ValueError:
            self.report("I was dead")

    def __eq__(self, other):
        return self.name == other.name
