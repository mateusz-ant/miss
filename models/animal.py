class Animal(object):
    def __init__(self, env, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.image = None
        self.displayed = False
        self.env = env
        self.name = name
        self.alive = True
        self.eating_time = eating_duration
        self.running_time = running_duration
        self.sleeping_time = sleeping_duration
        self.action = env.process(self.run())

    def run(self):
        pass

    def show_up(self, display, x, y):
        if not self.displayed:
            display.blit(self.image, (x,y))
            self.displayed = True
