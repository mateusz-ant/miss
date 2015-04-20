from abc import abstractmethod
from math import sqrt
import random
import pygame

from parameters import SCREEN_HEIGHT, SCREEN_LENGTH
from models.utils.utils import AnimalUtils


class Animal(AnimalUtils):
    def __init__(self, env, display, eating_duration=4, running_duration=10, sleeping_duration=10, name="no_name", x=0.0, y=0.0,
                 max_speed=5):
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

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def can_reproduce_with(self, other_animal) -> bool:
        pass

    def show_up(self, x, y):
        clock = pygame.time.Clock()
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

        self.x = new_x
        self.y = new_y
        self.show_up(self.x, self.y)


    def __repr__(self, *args, **kwargs):
        return "[{} {}, x = {}, y = {}]".format(self.__class__.__name__, self.name, self.x, self.y)
