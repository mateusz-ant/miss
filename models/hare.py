import simpy
from models.animal import Animal

class Hare(Animal):
    def run(self):
        while True:
            try:
                print('%s: Sleeping at %d' % (self.name, self.env.now))
                yield self.env.timeout(self.sleeping_time)

                print('%s: Eating at %d' % (self.name, self.env.now))
                yield self.env.timeout(self.eating_time)

                print('%s: Running at %d' % (self.name, self.env.now))
                yield self.env.timeout(self.running_time)
            except simpy.Interrupt:
                print('%s: Has been killed now!' % self.name)
