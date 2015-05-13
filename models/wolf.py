import random
from math import sqrt

from pygame import image

from models.animal import Animal
from parameters import WOLF_EATING_DURATION, WOLF_RUNNING_DURATION, WOLF_MAX_SPEED, WOLF_SLEEPING_DURATION, \
    WOLF_HUNT_PROBABILITY, WOLF_HUNT_MIN_DIST, WOLF_SEXUAL_AROUSAL, WOLF_MIN_REPRODUCE_DIST, WOLF_VISUAL_ACUITY, \
    ANIMAL_START_ENERGY, SCREEN_LENGTH, SCREEN_HEIGHT, WOLF_ENERGY_LOSS_PER_MOVE


class Wolf(Animal):
    def __init__(self, env, display, eating_duration=WOLF_EATING_DURATION, running_duration=WOLF_RUNNING_DURATION,
                 sleeping_duration=WOLF_SLEEPING_DURATION, max_speed=WOLF_MAX_SPEED, name="no_name", x=0.0, y=0.0,
                 energy=ANIMAL_START_ENERGY, energy_loss_per_move=WOLF_ENERGY_LOSS_PER_MOVE):
        super(Wolf, self).__init__(env, display, eating_duration, running_duration, sleeping_duration, name, x, y,
                                   max_speed, energy, energy_loss_per_move)
        self.image = image.load('img/wolf.png')
        self.shadow = image.load('img/wolf_b.png')

    def run(self):
        while self.alive:
            self.report("Sleeping")
            yield self.env.timeout(self.sleeping_time)

            self.report("Hunting")
            self.hunt(self.env.hares)
            yield self.env.timeout(self.eating_time)

            self.report("Running")
            self.move()
            yield self.env.timeout(self.running_time)

    def _move_to_xy(self):
        def bound(coordinate, lower_bound, upper_bound):
            return min(max(coordinate, lower_bound), upper_bound)

        can_see = lambda h: 0 < self.distance(h) < WOLF_VISUAL_ACUITY
        hares_nearby = list(filter(can_see, self.env.hares))
        wolves_nearby = list(filter(can_see, self.env.wolves))
        max_speed_per_coordinate = self.max_speed / sqrt(2)

        if not hares_nearby and not wolves_nearby:
            return super(Wolf, self)._move_to_xy()

        # approach hares
        hares_vec_x = sum([h.x for h in hares_nearby]) / len(hares_nearby) - self.x if hares_nearby else 0
        hares_vec_x *= (ANIMAL_START_ENERGY - self.energy) / ANIMAL_START_ENERGY
        hares_vec_y = sum([h.y for h in hares_nearby]) / len(hares_nearby) - self.y if hares_nearby else 0
        hares_vec_y *= (ANIMAL_START_ENERGY - self.energy) / ANIMAL_START_ENERGY

        # approach wolves
        wolves_vec_x = sum([h.x for h in wolves_nearby]) / len(wolves_nearby) - self.x if wolves_nearby else 0
        wolves_vec_x *= self.energy / ANIMAL_START_ENERGY
        wolves_vec_y = sum([h.y for h in wolves_nearby]) / len(wolves_nearby) - self.y if wolves_nearby else 0
        wolves_vec_y *= self.energy / ANIMAL_START_ENERGY

        vec_x = hares_vec_x + wolves_vec_x
        vec_y = hares_vec_y + wolves_vec_y

        if abs(vec_x) > max_speed_per_coordinate:
            vec_x = vec_x / abs(vec_x) * max_speed_per_coordinate

        if abs(vec_y) > max_speed_per_coordinate:
            vec_y = vec_y / abs(vec_y) * max_speed_per_coordinate

        return bound(self.x + vec_x, 20, SCREEN_LENGTH - 50), bound(self.y + vec_y, 20, SCREEN_HEIGHT - 50)

    def can_reproduce_with(self, other_animal):
        from models.animal import can_reproduce_with

        return can_reproduce_with(WOLF_MIN_REPRODUCE_DIST, WOLF_SEXUAL_AROUSAL)(self, other_animal)

    def hunt(self, hares):
        if random.random() < WOLF_HUNT_PROBABILITY * (self.energy / ANIMAL_START_ENERGY):
            nearby_hares = list(filter(lambda h: self.distance(h) < WOLF_HUNT_MIN_DIST, hares))
            if len(nearby_hares):
                hare = nearby_hares[0]
                self.report("HARE TO BE KILLED:", hare.name)
                hare.die()
                hare.action.interrupt()
                self.change_energy(hare.energy)

    def die(self):
        self.alive = False
        self.bury()
        self.report("Bye bye cruel world")
        try:
            self.env.wolves.remove(self)
        except ValueError:
            self.report("I was dead")
