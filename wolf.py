from animal import Animal

class Wolf(Animal):
    def run(self):
        while True:
            print('Sleeping at %d' % self.env.now)
            yield self.env.timeout(self.sleeping_time)

            print('Eating at %d' % self.env.now)
            yield self.env.timeout(self.eating_time)

            print('Running at %d' % self.env.now)
            yield self.env.timeout(self.running_time)