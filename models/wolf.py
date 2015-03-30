import random
from models.animal import Animal

HUNT_PROBABILITY = 0.6

class Wolf(Animal):
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
