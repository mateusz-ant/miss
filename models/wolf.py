import random

from models.animal import Animal
from pygame import image

HUNT_PROBABILITY = 0.6

class Wolf(Animal):
    def __init__(self, env, display, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0):
        super(Wolf, self).__init__(env, display, eating_duration, running_duration, sleeping_duration, name, x, y)
        self.image = image.load('img/wolf.png')

    def run(self):
        while True:
            self.report("Sleeping")
            yield self.env.timeout(self.sleeping_time)

            self.report("Eating")
            yield self.env.timeout(self.eating_time)

            self.report("Running")
            self.move()
            yield self.env.timeout(self.running_time)

    def can_reproduce_with(self, other_animal):
        return False

    def hunt(self, hares):
        if len(hares) and random.random() < HUNT_PROBABILITY:
            hare = random.choice(hares)
            self.report("Running")
            self.report("HARE TO BE KILLED:", hare.name)
            hare.action.interrupt()
        yield self.env.timeout(2)
