import random
from models.animal import Animal


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
        if len(hares):
            print("%s: HARE TO BE KILLED: %s" % (self.name, random.choice(hares).name))
        yield self.env.timeout(2)
