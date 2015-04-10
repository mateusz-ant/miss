class AnimalUtils(object):
    def report(self, *args):
        print('{} at {}: '.format(self, self.env.now), end='')
        print(*args)

    def distance(self, other_animal):
        from math import sqrt

        return sqrt((self.x - other_animal.x) ** 2 + (self.y - other_animal.y) ** 2)
