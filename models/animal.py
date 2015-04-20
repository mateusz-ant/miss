from abc import abstractmethod
from math import sqrt
import random
import pygame

from parameters import SCREEN_HEIGHT, SCREEN_LENGTH, ANIMAL_START_ENERGY
from models.utils.utils import AnimalUtils


class Animal(AnimalUtils):
    def __init__(self, env, display, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0,
                 max_speed=5, energy=ANIMAL_START_ENERGY):
        self.display = display
        self.x = x
        self.y = y
        self.image = None
        self.displayed = False
        self.env = env
        self.name = name
        self.alive = True
        self.max_speed = max_speed
        self.eating_time = eating_duration
        self.running_time = running_duration
        self.sleeping_time = sleeping_duration
        self.action = env.process(self.run())
        self.energy = energy

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def can_reproduce_with(self, other_animal) -> bool:
        pass

    def show_up(self, x, y):
        clock = pygame.time.Clock()
    @abstractmethod
    def die(self):
        pass

    def show_up(self, display, x, y):
        if not self.displayed:
            self.displayed = True
        self.display.blit(self.image, (x, y))
        pygame.display.update()
        clock.tick(60)

    def move(self):
        def move_coordinate(coordinate, lower_bound, upper_bound):
            max_speed_per_coordinate = self.max_speed / sqrt(2)
            sgn = random.randrange(-10, 10, 3)
            vector = sgn * random.random() * max_speed_per_coordinate
            new_coordinate = coordinate + vector

            return min(max(new_coordinate, lower_bound), upper_bound)

        new_x = move_coordinate(self.x, 0, SCREEN_LENGTH)
        new_y = move_coordinate(self.y, 0, SCREEN_HEIGHT)

        self.report("Moving from:", self.x, self.y, "to", new_x, new_y)

        self.change_energy(-self.distance_from_point(new_x, new_y))

        self.x = new_x
        self.y = new_y
        self.show_up(self.x, self.y)

    def change_energy(self, energy_change):
        self.energy += energy_change
        self.__ensure_alive()

    def __ensure_alive(self):
        if self.energy <= 0:
            self.die()

    def __repr__(self, *args, **kwargs):
        return "[{} {}, x = {}, y = {}, energy = {}]" \
            .format(self.__class__.__name__, self.name, self.x, self.y, self.energy)


def can_reproduce_with(min_distance, sexual_arousal):
    def can_reproduce(self, other_animal):
        myself = self == other_animal
        same_species = other_animal.__class__ == self.__class__
        close_by = self.distance(other_animal) < min_distance
        would_like_to_reproduce = random.random() < sexual_arousal

        return not myself and same_species and close_by and would_like_to_reproduce

    return can_reproduce