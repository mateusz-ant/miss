from models.hare import Hare
from models.wolf import Wolf

REPORT_INTERVAL = 5
NUM_OF_HARES = 10
NUM_OF_WOLVES = 3

class Meadow(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
        self.wolves = [Wolf(env, name="wolf_" + str(x)) for x in range(NUM_OF_WOLVES)]
        self.hares = [Hare(env, name="hare_" + str(x)) for x in range(NUM_OF_HARES)]

    def run(self):
        while True:
            print('MEADOW Report (at %d):\n  Hares: %d\n  Wolves: %d' % (self.env.now, len(self.hares), len(self.wolves)))
            yield self.env.timeout(REPORT_INTERVAL)