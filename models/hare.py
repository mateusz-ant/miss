import random

import simpy

from models.animal import Animal
from pygame import image
from math import sqrt
from parameters import HARE_EATING_DURATION, HARE_RUNNING_DURATION, HARE_MAX_SPEED, HARE_SLEEPING_DURATION, \
    HARE_MIN_REPRODUCE_DIST, HARE_SEXUAL_AROUSAL, HARE_FOOD_PORTION, HARE_FOOD_FINDING_PROBABILITY, HARE_VISUAL_ACUITY, \
    ANIMAL_START_ENERGY, SCREEN_HEIGHT, SCREEN_LENGTH, HARE_ENERGY_LOSS_PER_MOVE


class Hare(Animal):
    def __init__(self, env, display, eating_duration=HARE_EATING_DURATION, running_duration=HARE_RUNNING_DURATION,
                 sleeping_duration=HARE_SLEEPING_DURATION, max_speed=HARE_MAX_SPEED, name="no_name", x=0.0, y=0.0,
                 energy=ANIMAL_START_ENERGY, energy_loss_per_move=HARE_ENERGY_LOSS_PER_MOVE):
        super(Hare, self).__init__(env, display, eating_duration, running_duration, sleeping_duration, name, x, y,
                                   max_speed, energy, energy_loss_per_move)
        self.image = image.load('img/hare.png')
        self.shadow = image.load('img/hare_b.png')
        self.max_speed = max_speed * random.random()
        self.eating_time = eating_duration * random.random()
        self.running_time = running_duration * random.random()
        self.sleeping_time = sleeping_duration * random.random()

    def run(self):
        while self.alive:
            try:
                self.report("Sleeping")
                yield self.env.timeout(self.sleeping_time)

                self.report("Eating")
                yield self.env.timeout(self.eating_time)

                self.report("Running")

                self.move()
                self.find_food()

                yield self.env.timeout(self.running_time)
            except simpy.Interrupt:
                self.report("Has been killed!")

    def _move_to_xy(self):
        def bound(coordinate, lower_bound, upper_bound):
            return min(max(coordinate, lower_bound), upper_bound)

        can_see = lambda h: 0 < self.distance(h) < HARE_VISUAL_ACUITY
        hares_nearby = list(filter(can_see, self.env.hares))
        wolves_nearby = list(filter(can_see, self.env.wolves))
        max_speed_per_coordinate = self.max_speed / sqrt(2)

        if not hares_nearby and not wolves_nearby:
            return super(Hare, self)._move_to_xy()

        # approach hares
        hares_vec_x = sum([h.x for h in hares_nearby]) / len(hares_nearby) - self.x if hares_nearby else 0
        hares_vec_y = sum([h.y for h in hares_nearby]) / len(hares_nearby) - self.y if hares_nearby else 0

        # run away from wolves
        wolves_vec_x = self.x - sum([h.x for h in wolves_nearby]) / len(wolves_nearby) if wolves_nearby else 0
        wolves_vec_y = self.y - sum([h.y for h in wolves_nearby]) / len(wolves_nearby) if wolves_nearby else 0

        vec_x = hares_vec_x + wolves_vec_x
        vec_y = hares_vec_y + wolves_vec_y

        if abs(vec_x) > max_speed_per_coordinate:
            vec_x = vec_x / abs(vec_x) * max_speed_per_coordinate

        if abs(vec_y) > max_speed_per_coordinate:
            vec_y = vec_y / abs(vec_y) * max_speed_per_coordinate

        return bound(self.x + vec_x, 20, SCREEN_LENGTH - 50), bound(self.y + vec_y, 20, SCREEN_HEIGHT - 50)

    def can_reproduce_with(self, other_animal):
        from models.animal import can_reproduce_with

        return can_reproduce_with(HARE_MIN_REPRODUCE_DIST, HARE_SEXUAL_AROUSAL)(self, other_animal)

    def die(self):
        self.alive = False
        self.bury()
        self.report("Bye bye cruel world")
        try:
            self.env.hares.remove(self)
        except ValueError:
            self.report("I was dead")

    def __eq__(self, other):
        return self.name == other.name

    def find_food(self):
        if random.random() < HARE_FOOD_FINDING_PROBABILITY:
            self.change_energy(HARE_FOOD_PORTION)
