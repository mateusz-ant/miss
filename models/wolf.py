import random
from models.animal import Animal
from pygame import image

HUNT_PROBABILITY = 0.6


class Wolf(Animal):
    def __init__(self, env, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0):
        super(Wolf, self).__init__(env, eating_duration, running_duration, sleeping_duration, name, x, y)
        self.image = image.load('img/wolf.png')

    def run(self):
        while True:
            print('%s: Sleeping at %d' % (self.name, self.env.now))
            yield self.env.timeout(self.sleeping_time)

            print('%s: Eating at %d' % (self.name, self.env.now))
            yield self.env.timeout(self.eating_time)

            print('%s: Running at %d' % (self.name, self.env.now))
            yield self.env.timeout(self.running_time)

    def hunt(self, hares):
        if len(hares) and random.random() < HUNT_PROBABILITY:
            hare = random.choice(hares)
            print("%s: HARE TO BE KILLED: %s" % (self.name, hare.name))
            hare.action.interrupt()
        yield self.env.timeout(2)
