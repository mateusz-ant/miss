import random

from models.animal import Animal
from pygame import image
from parameters import WOLF_EATING_DURATION, WOLF_RUNNING_DURATION, WOLF_MAX_SPEED, WOLF_SLEEPING_DURATION, \
    WOLF_HUNT_PROBABILITY


class Wolf(Animal):
    def __init__(self, env, display, eating_duration=WOLF_EATING_DURATION, running_duration=WOLF_RUNNING_DURATION,
                 sleeping_duration=WOLF_SLEEPING_DURATION, max_speed=WOLF_MAX_SPEED, name="no_name", x=0.0, y=0.0):
        super(Wolf, self).__init__(env, display, eating_duration, running_duration, sleeping_duration, name, x, y, max_speed)
        self.image = image.load('img/wolf.png')
        self.shadow = image.load('img/wolf_b.png')

    def run(self):
        while True:
            self.report("Sleeping")
            yield self.env.timeout(self.sleeping_time)

            self.report("Hunting")
            self.hunt(self.env.hares)
            yield self.env.timeout(self.eating_time)

            self.report("Running")
            self.move()
            yield self.env.timeout(self.running_time)

    def can_reproduce_with(self, other_animal):
        from models.animal import can_reproduce_with
        return can_reproduce_with(.2, .5)(self, other_animal)

    def hunt(self, hares):
        if len(hares) and random.random() < WOLF_HUNT_PROBABILITY:
            hare = random.choice(hares)
            self.report("Running")
            self.report("HARE TO BE KILLED:", hare.name)
            hare.action.interrupt()
            hare.die()
            self.change_energy(hare.energy)
        yield self.env.timeout(2)

    def die(self):
        self.report("Bye bye cruel world")
        try:
            self.env.wolves.remove(self)
        except ValueError:
            self.report("I was dead")
