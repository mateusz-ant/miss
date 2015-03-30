class Animal(object):
    def __init__(self, env, eating_duration=4, running_duration=10, sleeping_duration=10):
        self.env = env
        self.eating_time = eating_duration
        self.running_time = running_duration
        self.sleeping_time = sleeping_duration
        self.action = env.process(self.run())