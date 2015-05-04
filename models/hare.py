import random

import simpy

from models.animal import Animal
from pygame import image
from parameters import HARE_EATING_DURATION, HARE_RUNNING_DURATION, HARE_MAX_SPEED, HARE_SLEEPING_DURATION


class Hare(Animal):
    def __init__(self, env, display, eating_duration=HARE_EATING_DURATION, running_duration=HARE_RUNNING_DURATION,
                 sleeping_duration=HARE_SLEEPING_DURATION, max_speed=HARE_MAX_SPEED, name="no_name", x=0.0, y=0.0):
        super(Hare, self).__init__(env, display, eating_duration, running_duration, sleeping_duration, name, x, y, max_speed)
        self.image = image.load('img/hare.png')
        self.shadow = image.load('img/hare_b.png')
        self.max_speed = max_speed * random.random()
        self.eating_time = eating_duration * random.random()
        self.running_time = running_duration * random.random()
        self.sleeping_time = sleeping_duration * random.random()

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
