import random
from models.hare import Hare
from models.wolf import Wolf

REPORT_INTERVAL = 5
NUM_OF_HARES = 400
NUM_OF_WOLVES = 100

class Meadow(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
        self.hares = [Hare(env, name="hare_" + str(x)) for x in range(NUM_OF_HARES)]
        self.wolves = [Wolf(env, name="wolf_" + str(x)) for x in range(NUM_OF_WOLVES)]

    def run(self):
        while True:
            print('MEADOW Report (at %d):\n  Hares: %d\n  Wolves: %d' % (self.env.now, len(self.hares), len(self.wolves)))
            yield self.env.timeout(REPORT_INTERVAL)

            if len(self.wolves):
                wolf = random.choice(self.wolves)
                yield wolf.env.process(wolf.hunt(hares=self.hares))