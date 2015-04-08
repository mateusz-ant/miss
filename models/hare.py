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
                print('%s: Sleeping at %d' % (self.name, self.env.now))
                yield self.env.timeout(self.sleeping_time)

                print('%s: Eating at %d' % (self.name, self.env.now))
                yield self.env.timeout(self.eating_time)

                print('%s: Running at %d' % (self.name, self.env.now))
                yield self.env.timeout(self.running_time)
            except simpy.Interrupt:
                print('%s: Has been killed now!' % self.name)
