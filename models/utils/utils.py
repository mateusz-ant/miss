class AnimalUtils(object):
    def report(self, *args):
        print('{} at {}: '.format(self, self.env.now), end='')
        print(*args)

    def distance(self, other_animal):
        return self.distance_from_point(other_animal.x, other_animal.y)

    def distance_from_point(self, x, y):
        from math import sqrt

        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
