class Hare(object):
    def __init__(self, env, eating_duration=4, running_duration=10, sleeping_duration=10):
        self.env = env

        self.eating_time = eating_duration
        self.running_time = running_duration
        self.sleeping_time = sleeping_duration

        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Sleeping at %d' % self.env.now)
            yield self.env.timeout(self.sleeping_time)

            print('Eating at %d' % self.env.now)
            yield self.env.timeout(self.eating_time)

            print('Running at %d' % self.env.now)
            yield self.env.timeout(self.running_time)